import cv2
import numpy as np
import matplotlib.pyplot as plt

def create_share2(original_image, share1):
    # Đọc ảnh gốc và mảnh 1
    img_original = cv2.imread(original_image, cv2.IMREAD_GRAYSCALE)
    plt.imshow(img_original, cmap='gray')
    plt.axis('off') # Tắt trục tọa độ
    plt.show()
    print(img_original.shape)
    img_share1 = cv2.imread(share1, cv2.IMREAD_GRAYSCALE)
    print(img_share1.shape)
    plt.imshow(img_share1, cmap='gray')
    plt.axis('off') # Tắt trục tọa độ
    plt.show()

    # Kiểm tra kích thước của ảnh gốc và mảnh 1
    if img_original.shape != img_share1.shape:
        raise ValueError("Kích thước của ảnh gốc và mảnh 1 không khớp!")

    # Tạo mảnh 2 bằng phép XOR giữa ảnh gốc và mảnh 1
    img_share2 = cv2.bitwise_xor(img_original, img_share1)

    # Lưu mảnh 2 thành file ảnh
    cv2.imwrite("share2.png", img_share2)

    print("Mảnh 2 đã được tạo và lưu thành công!")

# Gọi hàm để tạo mảnh 2
create_share2("image.png", "image_A.png")
