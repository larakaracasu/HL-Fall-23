import os
from bs4 import BeautifulSoup
import chardet

source_directory = 'C:/Users/larak/OneDrive/Documents/History-Lab/truth_data/original_truth'
target_directory = 'C:/Users/larak/OneDrive/Documents/History-Lab/truth_data/preprocessed_truth'

# Ensure the target directory exists
if not os.path.exists(target_directory):
    os.makedirs(target_directory)

def detect_file_encoding(file_path):
    with open(file_path, 'rb') as f:
        rawdata = f.read()
    return chardet.detect(rawdata)['encoding']

# Randomly select 20 files -- the first time (in further script revisions, we use the initially sampled files)
#source_directory = 'C:/Users/larak/OneDrive/Documents/History-Lab/1979'
#all_files = [f for f in os.listdir(source_directory) if f.endswith(".sgm")]
#selected_files = random.sample(all_files, 20)
#for file in selected_files:
#    shutil.move(os.path.join(source_directory, file), os.path.join(target_directory, file))

# Use this once sampled files are already in target directory
selected_files = [f for f in os.listdir(target_directory) if f.endswith(".sgm")]

# Now, proceed with the extraction from files in the target directory
for filename in selected_files:
    filepath = os.path.join(target_directory, filename)
    file_encoding = detect_file_encoding(filepath)

    with open(filepath, 'r', encoding=file_encoding) as file:
        content = file.read()

        # Using BeautifulSoup to extract plain text
        soup = BeautifulSoup(content, "lxml")

        # Extracting text only from the doc.body
        body_content = soup.find("doc.body")
        
        if body_content:
            # Extract text with spaces added after each paragraph
            plain_text = ' '.join([para.get_text() for para in body_content.find_all("para")])
                    
            # Replace /PRE> tag occurrences
            plain_text = plain_text.replace("/PRE>", "").strip()
                    
            # Replace multiple newlines with a single newline
            plain_text = '\n'.join([line.strip() for line in plain_text.splitlines() if line.strip()])
            
            # Save plain text to a new .txt file with the same base name
            output_filepath = os.path.join(target_directory, filename.replace('.sgm', '.txt'))
            with open(output_filepath, 'w', encoding='utf-8') as output_file:
                output_file.write(plain_text)

print("Processing completed!")
