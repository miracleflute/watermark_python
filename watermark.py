import tkinter as tk
from tkinter import filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageDraw, ImageFont
import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import tkinter.font as tkFont

def resize_image(image, scale_percent):
    width, height = image.size
    new_width = int(width * scale_percent / 100)
    new_height = int(height * scale_percent / 100)
    new_size = (new_width, new_height)
    resized_image = image.resize(new_size, Image.LANCZOS)
    return resized_image

def open_watermark_dialog():
    watermark_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")])
    if watermark_path:
        watermark_entry.delete(0, tk.END)
        watermark_entry.insert(0, watermark_path)

def open_target_dialog():
    target_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")])
    if target_paths:
        target_entry.delete(0, tk.END)
        target_entry.insert(0, "\n".join(target_paths))

def open_folder_dialog():
    folder_path = filedialog.askdirectory()
    if folder_path:
        target_paths = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        target_entry.delete(0, tk.END)
        target_entry.insert(0, "\n".join(target_paths))

def on_drop(event):
    file_paths = event.data
    if isinstance(file_paths, str):
        path_list = file_paths.split()
        path_list = path_list[0]
        print("워터마크 이미지(드롭):", path_list)
        watermark_entry.delete(0, tk.END)
        watermark_entry.insert(0, path_list)
        
def on_drop_img(event):
    file_paths = event.data
    if isinstance(file_paths, str):
        file_paths = file_paths.split()
        
    image_paths = []
    for path in file_paths:
        if os.path.isdir(path):
            for filename in os.listdir(path):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    image_paths.append(os.path.join(path, filename))
        elif path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            image_paths.append(path)
            
    print("선택한 이미지(드롭):")
    for path in image_paths:
        print(path)
        
    target_entry.delete(0, tk.END)
    target_entry.insert(0, "\n".join(image_paths))
    
def open_output_folder_dialog():
    output_folder = filedialog.askdirectory()
    if output_folder:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, output_folder)
        

def apply_watermark():
    watermark_image_path = watermark_entry.get()
    target_paths = target_entry.get().split("\n")
    output_folder = output_entry.get()
    
    os.makedirs(output_folder, exist_ok=True)
    
    # 워터마크 이미지 로드 (apply_watermark 함수 내에서 로드)
    watermark = cv2.imread(watermark_image_path, cv2.IMREAD_UNCHANGED)
    print(watermark)


    # 워터마크 이미지를 40%로 축소
    scale_factor = 0.9  # 크기를 40%로 축소 (조절 가능)
    watermark = cv2.resize(watermark, None, fx=scale_factor, fy=scale_factor)
    
    for target_path in target_paths:
        # 원본 이미지 로드
        image = cv2.imread(target_path)
        
        image_width = image.shape[1]
        image_height = image.shape[0]
        
        # 이미지 중앙과 워터마크 중앙을 맞추기 위한 좌표 계산
        x_offset = (watermark.shape[1] - image_width) // 2
        y_offset = (watermark.shape[0] - image_height) // 2
        
        # 이미지 중앙과 워터마크 중앙을 맞춤
        x = x_offset
        y = y_offset
        
        # 이미지 크기에 맞게 워터마크의 나머지 부분을 자르기
        watermark_cropped = watermark[y:y+image_height, x:x+image_width].copy()
        
        # 워터마크를 이미지 중앙에 덧붙이기
        x = (image.shape[1] - watermark_cropped.shape[1]) // 2
        y = (image.shape[0] - watermark_cropped.shape[0]) // 2
        
        # 워터마크 투명도 조절
        alpha = 0.2  # 투명도 (0.0부터 1.0까지의 값, 0.0은 완전 투명, 1.0은 불투명)
        for c in range(0, 3):
            image[y:y+watermark_cropped.shape[0], x:x+watermark_cropped.shape[1], c] = \
                image[y:y+watermark_cropped.shape[0], x:x+watermark_cropped.shape[1], c] * (1 - alpha) + \
                watermark_cropped[:, :, c] * alpha * (watermark_cropped[:, :, 3] / 255.0)
        
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.axis('off')  # 축 숨기기
        plt.show()
        
        file_name, file_extension = os.path.splitext(os.path.basename(target_path))
        output_file_path = os.path.join(output_folder, file_name + '_watermarked.png')
        output_file_path = output_file_path.replace('\\', '/') 
        
        cv2.imwrite(output_file_path, image)
        
        print(output_file_path)

        
        
        
        
        
        
        
        
# Create the main Tkinter window
root = TkinterDnD.Tk()
root.title("워터마크 삽입 및 이미지 처리 프로그램")
root.geometry("500x650")
root.configure(bg='white')











frame1 = tk.Frame(root, width=420, height=100, relief="solid", bd=2, bg='white')
button_frame1 = tk.Frame(frame1, width=20, height=20)

watermark_label = tk.Label(frame1, text="워터마크 이미지를 선택하세요", bg='white')
watermark_label.place(x=10, y=0)

watermark_button = tk.Button(button_frame1,  text="+", width=10, height=1, bg='white',  command=open_watermark_dialog)
button_frame1.place(x=330, y=5)
watermark_button.pack()

watermark_entry = tk.Entry(frame1, font=("Arial", 16, "bold"), width=29, relief="solid", bd=1, bg='white')

watermark_entry.place(x=207, y=65, anchor="center")
watermark_entry.drop_target_register(DND_FILES)
watermark_entry.dnd_bind('<<Drop>>', on_drop)

font = tkFont.Font(watermark_label, watermark_label.cget("font"))
font.configure(size=14)  # 원하는 크기로 설정 (예: 16)
watermark_label.configure(font=font)










frame2 = tk.Frame(root, width=420, height=100, relief="solid", bd=2, bg='white')
button_frame2 = tk.Frame(frame2, width=200, height=20, bg='white')  # 너비 조정


target_label = tk.Label(frame2, text="대상 이미지 또는 폴더를 선택하세요." ,bg='white')
target_label.place(x=10, y=5)


target_button = tk.Button(button_frame2, text="파일+", width=7, height=1, bg='white',  command=open_target_dialog)

folder_button = tk.Button(button_frame2, text="폴더+", width=7, height=1, bg='white',  command=open_folder_dialog)

button_frame2.place(x=275, y=5 )

target_button.grid(row=0, column=0, padx=5)  # 파일+ 버튼을 그리드의 첫 번째 열에 배치
folder_button.grid(row=0, column=1, padx=5)  # 폴더+ 버튼을 그리드의 두 번째 열에 배치

target_entry = tk.Entry(frame2, font=("Arial", 16, "bold"), width=29, relief="solid", bd=1, bg='white')
target_entry.place(x=207, y=65, anchor="center")
target_entry.drop_target_register(DND_FILES)
target_entry.dnd_bind('<<Drop>>', on_drop_img)

font = tkFont.Font(target_label, target_label.cget("font"))
font.configure(size=11)  # 원하는 크기로 설정 (예: 16)
target_label.configure(font=font)


















frame3 = tk.Frame(root, width=420, height=100, relief="solid", bd=2, bg='white')
button_frame3 = tk.Frame(frame3, width=400, height=20)

output_folder_button = tk.Button(button_frame3, text="저장 폴더 선택", command=open_output_folder_dialog, width=53, height=2, bg='white')

output_entry = tk.Entry(frame3, font=("Arial", 16, "bold"), width=29, relief="solid", bd=1, bg='white')
output_entry.place(x=207, y=75, anchor="center")

button_frame3.place(x=20, y=10)
output_folder_button.pack()




















frame4 = tk.Frame(root, width=420, height=100, bd=2, bg='white')
button_frame4 = tk.Frame(frame4, width=400, height=20)

apply_button = tk.Button(button_frame4,  relief="solid", bd=2, text="워터마크 적용 및 저장", command=apply_watermark,width=53, height=2, bg='white')

button_frame4.place(x=20, y=30)
apply_button.pack()





















frame1.place(x=40, y=30)
frame2.place(x=40, y=180)
frame3.place(x=40, y=330)
frame4.place(x=40, y=480)


# Start the Tkinter main loop
root.mainloop()

