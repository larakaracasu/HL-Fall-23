import os
import editdistance
import time
import nltk
import pandas as pd

# nltk.download('punkt')

# Environment variables for directories
ocr_dir = 'C:/Users/larak/OneDrive/Documents/History-Lab/ocr_data/preprocessed_ocr_pagewise'
truth_dir = 'C:/Users/larak/OneDrive/Documents/History-Lab/truth_data/preprocessed_truth_pagewise'
manual_results_file_csv = "cer_results_manual_pagewise.csv"
results_file_csv = "cer_results_enhanced.csv"
results_file_txt = "cer_results_enhanced.txt"

def calculate_cer(reference, hypothesis):
    distance = editdistance.eval(reference, hypothesis)
    return distance / len(reference)

def get_tokens_and_characters(text):
    tokens = len(nltk.word_tokenize(text))
    characters = len(text)
    return tokens, characters

def write_to_file(filename, data):
    with open(filename, 'w', encoding="utf-8") as f:
        f.write(data)

def write_to_csv(filename, data):
    with open(filename, 'w', encoding="utf-8") as f:
        f.write(data)

def process_page_files(ocr_path, truth_path, manual_results):
    with open(ocr_path, 'r', encoding="utf-8") as f_ocr, open(truth_path, 'r', encoding="utf-8") as f_truth:

        ocr_content = f_ocr.read()
        truth_content = f_truth.read()

        tokens_ocr, characters_ocr = get_tokens_and_characters(ocr_content)
        tokens_truth, characters_truth = get_tokens_and_characters(truth_content)

        cer = calculate_cer(truth_content, ocr_content)

        # Get manual CER values from the manual CSV
        manual_cer_row = manual_results[manual_results['Document'] == os.path.basename(ocr_path)]
        manual_cer = manual_cer_row.iloc[0]['CER'] if not manual_cer_row.empty else None

        return f"{os.path.basename(ocr_path)},{cer:.4f},{tokens_ocr},{characters_ocr},{tokens_truth},{characters_truth},{manual_cer}\n"

def main():
    ocr_files = os.listdir(ocr_dir)

    total_cer = 0
    total_tokens_ocr = 0
    total_characters_ocr = 0
    total_tokens_truth = 0
    total_characters_truth = 0
    num_files = len(ocr_files)

    # Read the manual pagewise results CSV
    manual_results = pd.read_csv(manual_results_file_csv)

    results_data = "Document,CER,Tokens (OCR),Length (OCR),Tokens (Truth),Length (Truth),Manual CER,CER >= 0.21,Match Garbled (CER >= 0.21),CER >= 0.35,Match Garbled (CER >= 0.35),Time\n"

    global_start_time = time.time()  # Start the timer for all documents

    for ocr_filename in ocr_files:
        if ocr_filename.endswith(".txt"):
            ocr_path = os.path.join(ocr_dir, ocr_filename)
            truth_path = os.path.join(truth_dir, ocr_filename)  # Assumes matching filenames

            result_line = process_page_files(ocr_path, truth_path, manual_results)
            results_data += result_line

            total_cer += float(result_line.split(',')[1])
            total_tokens_ocr += int(result_line.split(',')[2])
            total_characters_ocr += int(result_line.split(',')[3])
            total_tokens_truth += int(result_line.split(',')[4])
            total_characters_truth += int(result_line.split(',')[5])

    global_end_time = time.time()  # End the timer for all documents
    total_time = global_end_time - global_start_time
    average_cer = total_cer / num_files

    results_data += "\n"
    results_data += f"Average Character Error Rate for all documents,{average_cer:.4f}\n"
    results_data += f"Total time to process all documents,{total_time:.4f} seconds\n"
    results_data += f"Total tokens (OCR) for all documents,{total_tokens_ocr}\n"
    results_data += f"Total characters (OCR) for all documents,{total_characters_ocr}\n"
    results_data += f"Total tokens (Truth) for all documents,{total_tokens_truth}\n"
    results_data += f"Total characters (Truth) for all documents,{total_characters_truth}\n"

    # Write to CSV and text files in the current directory
    write_to_file(results_file_txt, results_data)
    write_to_csv(results_file_csv, results_data)
    print(f"Results written to {results_file_csv}.")
    print(f"Results written to {results_file_txt}.")

if __name__ == "__main__":
    main()
