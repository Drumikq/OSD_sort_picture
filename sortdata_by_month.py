import os
import re
from PIL import Image
import pytesseract

def extract_date_from_image_v2(image_path):
    # Open the image
    img = Image.open(image_path)
    
    # Crop the top-left corner of the image to focus on the date
    cropped_img = img.crop((0, 0, 900, 400))
    
    # Use Tesseract to recognize the date
    date_text = pytesseract.image_to_string(cropped_img, config='--psm 10')
    
    # Replace any occurrence of 6 with 8
    corrected_text = date_text.replace('6', '8').strip()
    
    return corrected_text

def sort_image_by_month_updated(image_path, recognized_date, destination_folder):
    # Extract month and year from the recognized date
    month_year = re.search(r"\d{2}.\d{4}", recognized_date)
    
    # Если не удалось обнаружить дату, отправить в папку unsorted
    if not month_year:
        print(f"Date not recognized properly for {image_path}")
        folder_path = os.path.join(destination_folder, "unsorted")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    else:
        print(f"Recognized month_year for {image_path}: {month_year.group(0)}")
        month, year = re.split(r'[.-]', month_year.group(0))


        
        # Установка года 2023
        year = "2023"
        
        # Check if month is within the allowed range (08, 09, 10)
        if month not in ["08", "09", "10"]:
            folder_path = os.path.join(destination_folder, "unsorted")
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
        else:
            folder_path = os.path.join(destination_folder, month + "." + year)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                
    # Move the image to the created/specified folder
    destination_path = os.path.join(folder_path, os.path.basename(image_path))
    os.rename(image_path, destination_path)

source_directory = "/home/drumik/Desktop/ten/unsorted"
destination_directory = "/home/drumik/Desktop/data/sorted_images"

# Получим список всех .jpg файлов в каталоге
all_files = [f for f in os.listdir(source_directory) if f.endswith(".jpg")]

total_files = len(all_files)
processed_files = 0

for filename in all_files:
    full_path = os.path.join(source_directory, filename)
    recognized_date = extract_date_from_image_v2(full_path)
    
    try:
        sort_image_by_month_updated(full_path, recognized_date, destination_directory)
    except Exception as e:
        print(f"Error processing {filename}: {e}")
        continue  # продолжаем обработку следующего файла
    
    processed_files += 1
    print(f"Processed {processed_files}/{total_files}")

print("All files processed!")
