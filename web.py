# -*- coding: utf-8 -*-
import streamlit as st
from mul import Apriltag_gen
from PIL import Image
from time import sleep
import os

# 检查文件是否存在，如果不存在则创建一个初始计数器值为0的文件
if not os.path.isfile("couter.txt"):
    with open("couter.txt", "w") as f:
        f.write("0")

# 设置网页标题和头部信息
st.set_page_config(page_title="AprilTag生成器", page_icon=":pencil2:")

# 定义应用程序
def main():
    # 在页面中添加标题和副标题
    st.title("AprilTag生成器")
    st.write("这个应用程序能生成多种多样的AprilTag，并输出精确的PDF文件 From ZHENGYU。")

    # 读取当前计数器值
    with open("couter.txt", "r") as f:
        count = int(f.read())

    col1, col2 = st.columns(2)

    with col1:
        # 选择标记类型
        tag_type = ["tag16h5", "tag25h9", "tag36h10", "tag36h11", "tagCircle21h7", "tagCircle49h12", "tagCustom48h12",
                    "tagStandard41h12", "tagStandard52h13"]
        tag_type_choice = st.selectbox("选择AprilTag类型", tag_type, index=3)

    with col2:
        # 选择输出纸张大小
        page_size = ["A3", "A4", "A5"]
        page_size_choice = st.selectbox("选择打印纸张类型", page_size, index=1)

    col3, col4 = st.columns(2)

    with col3:
        # 间隔大小
        pad_size = st.number_input('间隔大小：mm')

    with col4:
        # Tag大小
        marker_size = st.number_input('单Tag大小：mm')

    # Tag序列
    id_list = st.text_input('[[1, 2, 3], [4, 5, 6]]')

    col5, col6 = st.columns(2)

    image = Image.open('result.png')
    im = st.image(image, use_column_width='always')
   
    with open("result.pdf", "rb") as f:
        pdf_contents = f.read()

    with col5:
        if st.button('生成Tag'):
            # print(str(page_size_choice)+str(tag_type_choice)+ str(marker_size)+ str(pad_size)+ str(id_list))
            Apriltag_gen(str(page_size_choice), str(tag_type_choice), int(marker_size), int(pad_size), str(id_list))
            sleep(0.05)
            with open("result.pdf", "rb") as f:
                pdf_contents = f.read()
            image = Image.open('result.png')
            im.image(image)
            count += 1
            with open("couter.txt", "w") as f:
                    f.write(str(count))

    with col6:
        pdf = st.download_button(
                label="Download data as PDF",
                data=pdf_contents,
                file_name='result.pdf',
                mime='application/pdf'
            )

    st.write('已生成过', count, '个Apriltag文件')

# 运行应用程序
if __name__ == '__main__':
    main()
