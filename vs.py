import random
import string
import os
import shutil
from PIL import Image, ImageFont, ImageDraw, ImageChops

def generate_captcha_text():
    """Hàm tạo chuỗi captcha ngẫu nhiên."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(5))  # Sử dụng '_' cho biến không cần dùng

def generate_captcha_image(captcha_text):
    """Hàm tạo ảnh captcha gốc."""
    width = 1300
    height = 400
    background_color = (255, 255, 255)
    text_color = (0, 0, 0)
    font_size = 250
    font = ImageFont.load_default(size=font_size)

    image = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(image)

    x = 10
    y = 10
    for character in captcha_text:
        draw.text((x, y), character, font=font, fill=text_color)
        x += 250

    return image.convert('1')  # Chuyển thành ảnh đen trắng

def create_noise_patterns():
    """Hàm tạo các mẫu nhiễu."""
    return [(1, 1, 0, 0), (1, 0, 1, 0), (1, 0, 0, 1),
            (0, 1, 1, 0), (0, 1, 0, 1), (0, 0, 1, 1)]

def split_and_encode(image, patterns):
    """Chia ảnh và mã hóa thành hai phần."""
    width, height = image.size
    out_image_A = Image.new('1', (width, height))
    out_image_B = Image.new('1', (width, height))
    draw_A = ImageDraw.Draw(out_image_A)
    draw_B = ImageDraw.Draw(out_image_B)

    for x in range(width):
        for y in range(height):
            pixel = image.getpixel((x, y))
            pattern = random.choice(patterns)

            # Vẽ lên ảnh A
            draw_A.point((x*2, y*2), pattern[0])
            draw_A.point((x*2+1, y*2), pattern[1])
            draw_A.point((x*2, y*2+1), pattern[2])
            draw_A.point((x*2+1, y*2+1), pattern[3])

            # Vẽ lên ảnh B (nghịch đảo mẫu nếu điểm ảnh là đen)
            if pixel == 0: 
                draw_B.point((x*2, y*2), 1 - pattern[0])
                draw_B.point((x*2+1, y*2), 1 - pattern[1])
                draw_B.point((x*2, y*2+1), 1 - pattern[2])
                draw_B.point((x*2+1, y*2+1), 1 - pattern[3])
            else:
                draw_B.point((x*2, y*2), pattern[0])
                draw_B.point((x*2+1, y*2), pattern[1])
                draw_B.point((x*2, y*2+1), pattern[2])
                draw_B.point((x*2+1, y*2+1), pattern[3])

    return out_image_A, out_image_B

def create_share2(original_image, hint):
    """Tạo mảnh 2 từ ảnh gốc và mảnh 1 bằng phép toán XOR."""
    share1_image = Image.open('base.png').convert('1')

    if original_image.size != share1_image.size:
        raise ValueError("Kích thước của ảnh gốc và mảnh 1 không khớp!")

    img_share2 = ImageChops.logical_xor(original_image, share1_image)
    width, height = img_share2.size
    draw = ImageDraw.Draw(img_share2)
    # text = "sample watermark"
    font = ImageFont.truetype('arial.ttf', 70)
    # textwidth, textheight = font.getbbox(text)
    # textwidth, textheight = 36, 36
    # textwidth = font.textlength(text)
    # textheight = font.getsize(text)[1]
    _, _, textwidth, textheight = draw.textbbox((0, 0), text=hint, font=font)

    margin = 10
    x = width - textwidth - margin
    y = height - textheight - margin
    draw.text((x, y), hint, font=font)
    # img_share2.show()

    return img_share2

def save_image(image, image_path):
    """Hàm lưu ảnh."""
    image.save(image_path) 

def delete_all_images(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        try:
            shutil.rmtree(filepath)  # Delete directories
        except NotADirectoryError:
            os.remove(filepath)

def getImage():
     # Phần chính
    image_folder = "images"
    # shutil.rmtree(image_folder)
    # shutil.rmtree("/"+image_folder)
    for filename in os.listdir(image_folder):
        filepath = os.path.join(image_folder, filename)
        return filepath

def transparent_img(img):
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    img.putdata(newData)
    return img

def register(hint):
    # Phần chính
    image_folder = "images"
    # shutil.rmtree(image_folder)
    # shutil.rmtree("/"+image_folder)
    for filename in os.listdir(image_folder):
        filepath = os.path.join(image_folder, filename)
        try:
            shutil.rmtree(filepath)  # Delete directories
        except NotADirectoryError:
            os.remove(filepath)  # Delete files
    os.makedirs(image_folder, exist_ok=True)

    # Tạo ảnh base.png
    base_captcha_text = generate_captcha_text()
    base_captcha_image = generate_captcha_image(base_captcha_text)
    patterns = create_noise_patterns()
    base_image_A, _ = split_and_encode(base_captcha_image, patterns)
    transparent_img(base_image_A).save('base.png')

    # Tạo các ảnh captcha khác
    for _ in range(2):  # Lặp lại 2 lần cho ví dụ
        captcha_text = generate_captcha_text()
        captcha_image = generate_captcha_image(captcha_text)
        patterns = create_noise_patterns()
        image_A, _ = split_and_encode(captcha_image, patterns)
        bit_image = create_share2(captcha_image, hint)
        bit_image = transparent_img(bit_image)
        save_image(bit_image, os.path.join(image_folder, captcha_text + '.png')) 