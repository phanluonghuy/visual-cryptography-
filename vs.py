import random
import string
from PIL import Image, ImageFont, ImageDraw

def generate_captcha_image():
    """
    Hàm tạo ảnh captcha với các thông số được truyền vào.
    Returns:
        Image: Ảnh captcha được tạo.
    """

    # Kích thước ảnh
    width = 1300
    height = 300

    # Màu nền
    background_color = (255, 255, 255)

    # Màu chữ
    text_color = (0, 0, 0)

    # Kích thước font chữ
    font_size = 250
    font = ImageFont.load_default(size=font_size)

    # Tạo ảnh nền
    image = Image.new('RGB', (width, height), background_color)

    # Tạo text và vẽ nó lên ảnh
    draw = ImageDraw.Draw(image)

    # Tạo chuỗi mã captcha
    characters = string.ascii_uppercase + string.digits
    captcha_text = ''.join(random.choice(characters) for i in range(5))

    # Vị trí chữ
    x = 10
    y = 10

    # Vẽ từng ký tự
    for character in captcha_text:
        draw.text((x, y), character, font=font, fill=text_color)
        x += 250

    # Thêm nhiễu (có thể bỏ qua)
    # for i in range(10000):
        # x = random.randint(0, width - 1)
        # y = random.randint(0, height - 1)
        # image.putpixel((x, y), random.choice((0, 0, 0, 255)))

    return image



# Tạo ảnh captcha
captcha_image = generate_captcha_image()

# Hiển thị ảnh
captcha_image.show()
