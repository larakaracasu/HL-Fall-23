import os
import random
import shutil
from bs4 import BeautifulSoup
import chardet

source_directory = 'C:/Users/larak/OneDrive/Documents/History/1979'
target_directory = 'C:/Users/larak/OneDrive/Documents/History/truth-data'

# Ensure the target directory exists
if not os.path.exists(target_directory):
    os.makedirs(target_directory)

def detect_file_encoding(file_path):
    with open(file_path, 'rb') as f:
        rawdata = f.read()
    return chardet.detect(rawdata)['encoding']

# Get a list of all .sgm files
all_files = [f for f in os.listdir(source_directory) if f.endswith(".sgm")]

# Randomly select 20 files
selected_files = random.sample(all_files, 20)

# Move the selected files to the target directory
for file in selected_files:
    shutil.move(os.path.join(source_directory, file), os.path.join(target_directory, file))

# Now, proceed with the extraction from files in the target directory
for filename in os.listdir(target_directory):
    filepath = os.path.join(target_directory, filename)
    file_encoding = detect_file_encoding(filepath)

    with open(filepath, 'r', encoding=file_encoding) as file:
        content = file.read()

        # Using BeautifulSoup to extract plain text
        soup = BeautifulSoup(content, "lxml")
        plain_text = soup.get_text()

        # Save plain text to a new .txt file with the same base name
        output_filepath = os.path.join(target_directory, filename.replace('.sgm', '.txt'))
        with open(output_filepath, 'w', encoding='utf-8') as output_file:
            output_file.write(plain_text)

print("Processing completed!")
