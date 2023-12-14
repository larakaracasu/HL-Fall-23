import os

source_directory = 'C:/Users/larak/OneDrive/Documents/History-Lab/ocr_data/original_ocr'
target_directory = 'C:/Users/larak/OneDrive/Documents/History-Lab/ocr_data/preprocessed_ocr_pagewise'

# Ensure the target directory exists
if not os.path.exists(target_directory):
    os.makedirs(target_directory)

selected_files = [f for f in os.listdir(source_directory) if f.endswith(".txt")]

for filename in selected_files:
    source_filepath = os.path.join(source_directory, filename)

    with open(source_filepath, 'r', encoding='utf-8') as file:
        content = file.read()
 
    pages = content.split('\n')[2:]
    for i, page in enumerate(pages):
        target_filepath = os.path.join(target_directory, f"{filename[:-4]}_page_{i + 1}.txt")
        with open(target_filepath, 'w', encoding='utf-8') as output_file:
            output_file.write(page)

print("Processing completed!")
