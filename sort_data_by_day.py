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

def sort_image_by_day(image_path, recognized_date, destination_folder):
    # Extract day, month, and year from the recognized date
    date_match = re.search(r"\d{2}.\d{2}.\d{4}", recognized_date)
    
    # If the date is not recognized properly, move to unsorted
    if not date_match:
        print(f"Date not recognized properly for {image_path}")
        folder_path = os.path.join(destination_folder, "unsorted")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    else:
        day, month, year = re.split(r'[.-]', date_match.group(0))
        year = "2023"  # Set year to 2023
        
        # Formulate the folder name in YYYY-MM-DD format
        folder_name = f"{year}-{month}-{day}"
        folder_path = os.path.join(destination_folder, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
                
    # Formulate the destination file name with the date and an optional index
    base_name = os.path.basename(image_path)
    file_name_without_ext, file_extension = os.path.splitext(base_name)
    new_file_name = f"{file_name_without_ext}_{day}-{month}-{year}{file_extension}"
    destination_path = os.path.join(folder_path, new_file_name)
    
    # If a file with the same name exists, append an index to the name
    index = 1
    while os.path.exists(destination_path):
        new_file_name = f"{file_name_without_ext}_{day}-{month}-{year}_{index}{file_extension}"
        destination_path = os.path.join(folder_path, new_file_name)
        index += 1
        
    # Move the image to the created/specified folder
    os.rename(image_path, destination_path)


source_directory = "/home/drumik/Desktop/data/sorted_images/09.2023/"
destination_directory = "/home/drumik/Desktop/data/sorted_images/09.2023/days/"

# Получим список всех .jpg файлов в каталоге
all_files = [f for f in os.listdir(source_directory) if f.endswith(".jpg")]

total_files = len(all_files)
processed_files = 0

for filename in all_files:
    full_path = os.path.join(source_directory, filename)
    recognized_date = extract_date_from_image_v2(full_path)
    
    try:
        sort_image_by_day(full_path, recognized_date, destination_directory)  # Используем функцию sort_image_by_day
    except Exception as e:
        print(f"Error processing {filename}: {e}")
        continue  # продолжаем обработку следующего файла
    
    processed_files += 1
    print(f"Processed {processed_files}/{total_files}")

print("All files processed!")
