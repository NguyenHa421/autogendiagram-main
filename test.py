import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib.patches as patches
import numpy as np
import textwrap  # Thư viện để chia văn bản thành nhiều dòng
import math

# Hàm vẽ người que
def draw_person(ax, x, y, scale = 3):

    # Đầu người
    head_radius = 10 * scale  # Bán kính đầu tăng lên gấp 4 lần
    head = patches.Circle((x, y + 15 * scale), radius=head_radius, edgecolor='black', facecolor='white', lw=2, zorder=5)
    ax.add_patch(head)

    # Thân người
    ax.plot([x, x], [y - 10 * scale, y + 5 * scale], color='black', lw=2, zorder=5)

    # Tay
    ax.plot([x - 15 * scale, x + 15 * scale], [y + 5 * scale, y + 5 * scale], color='black', lw=2, zorder=5)

    # Chân
    ax.plot([x, x - 10 * scale], [y - 10 * scale, y - 25 * scale], color='black', lw=2, zorder=5)
    ax.plot([x, x + 10 * scale], [y - 10 * scale, y - 25 * scale], color='black', lw=2, zorder=5)

    return head_radius

# Hàm vẽ hình chữ nhật xung quanh người que
def draw_rectangle(ax, x, y, center_radius=20, scale = 3):

    # Vẽ một hình chữ nhật bao quanh người que với màu nền trắng
    rect_width = center_radius * 2 * scale  # Kích thước chiều rộng của hình chữ nhật
    rect_height = center_radius * 3 * scale   # Kích thước chiều cao của hình chữ nhật
    rectangle = patches.Rectangle((x - rect_width / 2, y - rect_height / 2), rect_width, rect_height, 
                                  linewidth=2, facecolor='white', zorder=4)  # Màu nền trắng
    ax.add_patch(rectangle)

# Hàm vẽ các vòng tròn chứa nội dung
def draw_ovals(ax, x, y, branches, center_radius=20, scale=3):
    branch_distance = 80 * scale  # Tăng khoảng cách giữa các vòng tròn
    
    # Vẽ người que ở chính giữa
    head_radius = draw_person(ax, x, y, scale)

    # Vẽ hình chữ nhật xung quanh người que
    draw_rectangle(ax, x, y, center_radius, scale)

    # Thêm chữ "QTHT" xuống dưới chân người
    ax.text(x, y - head_radius - 30 * scale, 'QTHT', ha='center', va='center', fontsize=12 , color='black', zorder=10)

    # Vẽ các ovals xung quanh
    for i, branch in enumerate(branches):
       
        angle = (i / len(branches)) * 360  # Để phân phối các vòng tròn xung quanh người theo hình tròn
        dis = 0
        if len(branches) <= 5:
            dis = center_radius + 130 * scale
        elif len(branches) == 6:
            dis = center_radius + 160 * scale
        elif len(branches) <= 10:
            if i % 2 == 0 and i == len(branches) - 1:
                dis = center_radius + 180 * scale
            elif i % 2 == 0:
                dis = center_radius + 130 * scale
            else:
                dis = center_radius + 240 * scale
        else:
            if i % 2 == 0 and i == len(branches) - 1:
                dis = center_radius + 200 * scale
            elif i % 2 == 0:
                dis = center_radius + 170 * scale
            else:
                dis = center_radius + 300 * scale
        branch_x = x + dis * np.cos(np.radians(angle))  # Tăng khoảng cách giữa người que và vòng tròn
        branch_y = y + dis * np.sin(np.radians(angle))  # Tăng khoảng cách giữa người que và vòng tròn
        
        # Chia văn bản thành nhiều dòng nếu quá dài
        wrapped_text = textwrap.fill(branch, width=25)  # Cập nhật độ dài của văn bản xuống dòng

        # Tính toán chiều cao và chiều rộng của vòng tròn tùy theo số dòng
        lines = wrapped_text.split("\n")  # Tạo danh sách các dòng
        oval_width = 160 * scale  # Giữ kích thước chiều rộng vòng tròn cố định
        oval_height = 48 * scale + (len(lines) - 1) * 12 * scale  # Tăng chiều cao vòng tròn để chứa toàn bộ văn bản

        oval = patches.Ellipse((branch_x, branch_y), width=oval_width, height=oval_height, edgecolor='black', facecolor='white', lw=2, zorder=3)
        ax.add_patch(oval)

        # Vẽ từng dòng của văn bản vào trong vòng tròn từ trên xuống dưới
        offset_y = 9 * scale  # Điều chỉnh để văn bản hạ xuống thêm một chút
        for j, line in enumerate(lines):
            # Điều chỉnh vị trí y sao cho dòng đầu tiên nằm ở trên cùng và dãn cách nhau
            ax.text(branch_x, branch_y + (len(lines) / 2 - j) * 12 * scale - offset_y, line, ha='center', va='center', fontsize=5, color='black', zorder=3)

        # Tính toán vị trí bắt đầu của đường nối từ tâm người que
        center_x = x
        center_y = y + 15 * scale  # Vị trí trung tâm người que (trên đầu)

        # Tính toán vị trí trên viền của ellipse (hình tròn) 
        oval_edge_x = branch_x + (oval_width / 2) * np.cos(np.radians(angle))  # Viền ngoài của hình ellipse
        oval_edge_y = branch_y + (oval_height / 2) * np.sin(np.radians(angle))  # Viền ngoài của hình ellipse

        # Vẽ đường nối từ tâm người que đến viền của oval, zorder=2 để nó nằm dưới các hình vẽ khác
        ax.plot([center_x, oval_edge_x], [center_y, oval_edge_y], color='black', lw=1, zorder=2)
        
def create_ovals_from_excel(file_path, output_folder='output_images'):
    df = pd.read_excel(file_path, header=None)  

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    grouped = []
    current_person = None
    branches = []

    for index, row in df.iterrows():
        person = row[0]
        branch = row[1]

        if pd.notna(person):  
            if current_person is not None:
                grouped.append((current_person, branches))
            current_person = person
            branches = [branch]  
        elif pd.notna(branch):  
            branches.append(branch)  

    if current_person is not None:
        grouped.append((current_person, branches))

    for i, (name, branches) in enumerate(grouped):
        fig, ax = plt.subplots(figsize=(8, 8))

        # Điều chỉnh giới hạn khu vực vẽ 
        ax.set_xlim(-1000, 1350)  # Mở rộng trục x 
        ax.set_ylim(-1100, 1300)  # Mở rộng trục y
        #ax.set_aspect('equal', adjustable='box')
        x = 180  
        y = 130  # Vị trí trung tâm cho "người"

        # Vẽ nền màu trắng cho ảnh
        ax.set_facecolor('white')

        # Vẽ tất cả các đối tượng
        draw_ovals(ax, x, y, branches)

        ax.axis('off')

        # Lưu ảnh
        output_file = os.path.join(output_folder, f"{name}.png")
        fig.savefig(output_file, bbox_inches='tight', transparent=True, dpi=300)  
        plt.close(fig)

# Đọc file đường dẫn từ config.txt
with open('config.txt', 'r') as file:
    file_path = file.read().replace('\n', '')
    print(file_path)

create_ovals_from_excel(file_path)
