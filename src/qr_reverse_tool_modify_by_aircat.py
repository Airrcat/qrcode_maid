from pyzbar.pyzbar import decode
import cv2
from PIL import Image
import random


def reverse_color(x):
    return 0 if x == 255 else 255

# 行反转，需要根据对应的图片像素和二维码码元组成修改，即block_size=图片像素/码元。


def reverse_row_colors(pixels, row, width, block_size=10):
    for x_block in range(width // block_size):
        x = x_block * block_size
        y = row * block_size
        for x_small in range(x, x + block_size):
            for y_small in range(y, y + block_size):
                pixel = pixels[x_small, y_small]
                pixels[x_small, y_small] = reverse_color(pixel)

# 列反转


def reverse_col_colors(pixels, col, height, block_size=10):
    for y_block in range(height // block_size):
        x = col * block_size
        y = y_block * block_size
        for x_small in range(x, x + block_size):
            for y_small in range(y, y + block_size):
                pixel = pixels[x_small, y_small]
                pixels[x_small, y_small] = reverse_color(pixel)


def qrcode_scan(file: str):

    # 读取图像
    image = cv2.imread(file)
    Data = []
    # 图像预处理（根据需要进行预处理）
    # 这里只是简单的示例，实际预处理可能需要更多步骤和参数调整

    # 转换为灰度图像
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 使用 Pyzbar 进行二维码解码
    decoded_objects = decode(gray_image)

    # 打印识别的结果
    for obj in decoded_objects:
        Data.append(obj.data.decode('utf-8'))
    return Data


def test1():
    original_img = Image.open("../attachment/new.png")

    new_img = original_img.copy()

    width, height = new_img.size
    pixels = new_img.load()
    # 想要反转哪行哪列就修改数字即可，不够就复制一下。
    reverse_row_colors(pixels, 1, width)  # 从最小的x,y值开始计数，所以数字0为第一行/列。
    reverse_row_colors(pixels, 12, width)

    reverse_col_colors(pixels, 0, height)
    reverse_col_colors(pixels, 2, height)
    reverse_col_colors(pixels, 5, height)
    reverse_col_colors(pixels, 10, height)
    reverse_col_colors(pixels, 11, height)

    new_img.save("../output/flag.png")
    print("test1 success.")


def test2():
    # test2
    prefix = "../output/output_flags/flag"
    suffix = ".png"
    count1 = 0
    count2 = 0
    data_list = qrcode_scan("../output/output_flags/flag.png")
    while (count1 != 25) and (count2 != 25):
        name = prefix + str(count1) + "_"+str(count2) + suffix
        data_list += qrcode_scan(name)
        count2 += 1
        if count2 == 24:
            count1 += 1
            count2 = 0
    with open("../output/output.txt", "w") as f:
        for data in data_list:
            for l in data:
                f.write(l)
    print("test2 success.")


if __name__ == '__main__':

    test1()
    test2()
