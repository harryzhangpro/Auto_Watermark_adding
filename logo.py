from PIL import Image, ExifTags
import os

def add_watermark_to_images(logo_path, folder_path="."):
    # 创建 watermarked 文件夹（如果不存在）
    output_folder = os.path.join(folder_path, "watermarked")
    os.makedirs(output_folder, exist_ok=True)
    
    # 检查 logo 文件是否存在
    if not os.path.exists(logo_path):
        print(f"Error: Logo file '{logo_path}' not found.")
        return
    
    # 打开 logo 图片
    logo = Image.open(logo_path)
    
    # 标记是否找到符合条件的图片
    found_images = False
    
    # 遍历当前目录中的所有 .jpg 和 .JPG 文件
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".jpg"):
            found_images = True
            image_path = os.path.join(folder_path, filename)
            image = Image.open(image_path)

            # 检查并调整图像方向
            try:
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                exif = image._getexif()
                if exif and orientation in exif:
                    if exif[orientation] == 3:
                        image = image.rotate(180, expand=True)
                    elif exif[orientation] == 6:
                        image = image.rotate(270, expand=True)
                    elif exif[orientation] == 8:
                        image = image.rotate(90, expand=True)
            except (AttributeError, KeyError, IndexError):
                # 无法读取 EXIF 数据，跳过方向调整
                pass

            # 计算 logo 的新尺寸，占用图片大小的 1/64，保持比例
            logo_ratio = logo.width / logo.height
            new_logo_width = image.width // 8
            new_logo_height = int(new_logo_width / logo_ratio)
            resized_logo = logo.resize((new_logo_width, new_logo_height), Image.LANCZOS)
            
            # 计算水印位置，右上角
            position = (image.width - resized_logo.width, 0)
            
            # 将 logo 粘贴到图片上，保持透明度
            image.paste(resized_logo, position, resized_logo.convert("RGBA"))
            
            # 保存带水印的图片到 watermarked 文件夹
            watermarked_image_path = os.path.join(output_folder, f"watermarked_{filename}")
            image.save(watermarked_image_path)

            print(f"Watermark added to {filename}")
    
    if not found_images:
        print("No .jpg or .JPG files found in the specified folder.")

# 调用函数
logo_path = "logo.png"  # logo 图片路径
add_watermark_to_images(logo_path)