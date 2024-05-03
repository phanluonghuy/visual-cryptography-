import random
import string
import cv2
import matplotlib.pyplot as plt
from PIL import Image, ImageFont, ImageDraw, ImageChops

def generate_captcha_text():
    """Hàm tạo chuỗi captcha ngẫu nhiên."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for i in range(5))

def generate_captcha_image(captcha_text):
    """Hàm tạo ảnh captcha gốc."""
    width = 1300
    height = 300
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
def create_share2(original_image : Image, share1 : Image):

    # Kiểm tra kích thước của ảnh gốc và mảnh 1
    if original_image.size != share1.size:
        raise ValueError("Kích thước của ảnh gốc và mảnh 1 không khớp!")

    # Tạo mảnh 2 bằng phép XOR giữa ảnh gốc và mảnh 1
    img_share2 = ImageChops.logical_xor(original_image,share1)

    # Lưu mảnh 2 thành file ảnh
    return img_share2
# Phần chính
captcha_text = generate_captcha_text()
captcha_image = generate_captcha_image(captcha_text)
captcha_image.save('image.png')
patterns = create_noise_patterns()

image_A, image_B = split_and_encode(captcha_image, patterns)
image_A.save('image_A.png')
image_B.save('image_B.png')
bit_image = create_share2(captcha_image,image_A)
bit_image.save('bit_image.png')