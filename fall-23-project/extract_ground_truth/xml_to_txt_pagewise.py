import os
import chardet
from bs4 import BeautifulSoup

source_directory = 'C:/Users/larak/OneDrive/Documents/History-Lab/truth_data/original_truth'
target_directory = 'C:/Users/larak/OneDrive/Documents/History-Lab/truth_data/preprocessed_truth_pagewise'

# Ensure the target directory exists
if not os.path.exists(target_directory):
    os.makedirs(target_directory)

def detect_file_encoding(file_path):
    with open(file_path, 'rb') as f:
        rawdata = f.read()
    return chardet.detect(rawdata)['encoding']

selected_files = [f for f in os.listdir(source_directory) if f.endswith(".sgm")]

for filename in selected_files:
    filepath = os.path.join(source_directory, filename)
    file_encoding = detect_file_encoding(filepath)

    with open(filepath, 'r', encoding=file_encoding) as file:
        content = file.read()

        # Using BeautifulSoup to extract plain text
        soup = BeautifulSoup(content, "lxml")

        # Extracting text only from the doc.body
        body_content = soup.find("doc.body")

        if body_content:
            # Split content using <?PRE>
            pre_content = content.split("<?PRE>")

            for i, page_content in enumerate(pre_content[1:]):  # Start from index 1 to skip the content before the first <?PRE>
                # Extract paragraphs within each page
                page_soup = BeautifulSoup("<?xml version='1.0' encoding='UTF-8'?><?PRE>" + page_content, "lxml")
                paragraphs = page_soup.find_all("para")

                # Get the text within <para> tags and join them into a single line
                para_text = ' '.join(para.get_text(separator=" ").strip() for para in paragraphs)

                # Save paragraph to a new .txt file with the same base name
                output_filepath = os.path.join(target_directory, f"{filename.replace('.sgm', '')}_page_{i + 1}.txt")
                with open(output_filepath, 'w', encoding='utf-8') as output_file:
                    output_file.write(para_text)

print("Processing completed!")
