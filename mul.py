import numpy as np
from moms_apriltag import TagGenerator3, TagGenerator2
from fpdf import FPDF
from PIL import Image

page_size_t = "A4"
tag_name_t = "tag36h10"
marker_size_t = 50  # unit:mm
pad_size_t = 5  # unit:mm
# id_list_t = [[1, 3, 3], [6, 5, 6]]
id_list_t = "[[1, 2,4, 3], [4, 5, 3,6]]"


def Apriltag_gen(page_size, tag_name, marker_size, pad_size, id_list):

    # 首先将字符串按照 '], [' 进行拆分，得到每一行的字符串
    rows_str = id_list.strip('[]').split('], [')

    # 对每一行的字符串进行处理，得到该行的二维数组
    arr = []
    for row_str in rows_str:
        # 将该行的字符串按照逗号拆分，得到该行的元素列表
        elements_str = row_str.split(',')
        # 将每个元素从字符串类型转换为整型，并添加到该行的二维数组中
        row = []
        for elem_str in elements_str:
            row.append(int(elem_str))
        # 将该行的二维数组添加到最终的二维数组中
        arr.append(row)

    id_list = arr

    tag_sizes = {
        "tag16h5": 6,
        "tag25h9": 7,
        "tag36h10": 8,
        "tag36h11": 8,
        "tagCircle21h7": 9,
        "tagCircle49h12": 11,
        "tagCustom48h12": 10,
        "tagStandard41h12": 9,
        "tagStandard52h13": 10,
    }
    if tag_sizes[tag_name] <= 8:
        tg = TagGenerator2(tag_name)
    else:
        tg = TagGenerator3(tag_name)

    dpi_set = 1000

    px = int(marker_size * dpi_set / (24.5*int(tag_sizes[tag_name])))
    pad = int(pad_size * dpi_set / 24.5)
    imgs = []

    for row in id_list:
        for tag_id in row:
            im = tg.generate(tag_id, px)
            im = np.pad(im, pad, mode="constant", constant_values=255)

            imgs.append(im)

    img = np.concatenate(imgs, axis=1)
    
    #pad_height = int(188 * dpi_set / 24.5)
    #img = np.pad(img, ((pad_height, 0), (0, 0)), mode="constant", constant_values=255)

    # 将数组横向切成id_list块
    img = np.split(img, len(id_list), axis=1)

    # 竖向拼接所有子数组
    result = np.concatenate(img, axis=0)

    # result = result[pad_height:, :]

    # # # # # # # # result = np.pad(result, pad, mode="constant", constant_values=255)

    result = np.pad(result, 1, mode="constant", constant_values=0)

    image = Image.fromarray(result.astype('uint8'))

    image.save('result.png', dpi=(dpi_set, dpi_set))

    # print("Gen Apriltag")

    # ***************  Output PDF ***************

    # 获取图像的尺寸和 DPI
    width, height = image.size
    dpi = image.info.get('dpi', dpi_set)

    # 将像素转换为毫米
    width_mm = width*24.5/dpi
    height_mm = height*24.5/dpi

    pdf = FPDF('P', 'mm', page_size)  # p/l  A3/A4/A5
    pdf.add_page()

    img_width = width *24.5/dpi
    img_height = height *24.5/dpi

    pdf.image('result.png', x=210 / 2 - width_mm / 2, y=297 / 2 - height_mm / 2, w=img_width ,h=img_height)

    pdf.output("result.pdf", "F")

    # print("Gen pdf")


if __name__ == '__main__':
    Apriltag_gen(page_size_t, tag_name_t, marker_size_t, pad_size_t, id_list_t)

