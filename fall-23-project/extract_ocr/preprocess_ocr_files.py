import os

source_directory = 'C:/Users/larak/OneDrive/Documents/History-Lab/ocr_data/original_ocr'
target_directory = 'C:/Users/larak/OneDrive/Documents/History-Lab/ocr_data/preprocessed_ocr'

# Ensure the target directory exists
if not os.path.exists(target_directory):
    os.makedirs(target_directory)

selected_files = [f for f in os.listdir(source_directory) if f.endswith(".txt")]

for filename in selected_files:
    source_filepath = os.path.join(source_directory, filename)
    
    with open(source_filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Skip the first two lines
    modified_content = "".join(lines[2:])
    
    target_filepath = os.path.join(target_directory, filename)
    with open(target_filepath, 'w', encoding='utf-8') as output_file:
        output_file.write(modified_content)

print("Processing completed!")
