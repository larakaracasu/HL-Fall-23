import os
import editdistance
import time
import nltk
import pandas as pd

# nltk.download('punkt')

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

def main():
    ocr_dir = "C:\\Users\\larak\\OneDrive\\Documents\\History-Lab\\ocr_data\\preprocessed_ocr"
    truth_dir = "C:\\Users\\larak\\OneDrive\\Documents\\History-Lab\\truth_data\\preprocessed_truth"
    results_file_csv = "C:\\Users\\larak\\OneDrive\\Documents\\GitHub\\HL-Fall-23\\fall-23-project\\calculate_cer\\cer_results_manual.csv"
    results_file_txt = "C:\\Users\\larak\\OneDrive\\Documents\\GitHub\\HL-Fall-23\\fall-23-project\\calculate_cer\\cer_results_manual.txt"
    
    ocr_files = os.listdir(ocr_dir)
    
    total_cer = 0
    total_tokens_ocr = 0
    total_characters_ocr = 0
    total_tokens_truth = 0
    total_characters_truth = 0
    num_files = len(ocr_files)

    results_data = "Document,CER,Tokens (OCR),Length (OCR),Tokens (Truth),Length (Truth),Time\n"

    global_start_time = time.time()  # Start the timer for all documents

    for ocr_file in ocr_files:
        with open(os.path.join(ocr_dir, ocr_file), 'r', encoding="utf-8") as f_ocr, \
            open(os.path.join(truth_dir, ocr_file), 'r', encoding="utf-8") as f_truth:

            ocr_content = f_ocr.read()
            truth_content = f_truth.read()

            tokens_ocr, characters_ocr = get_tokens_and_characters(ocr_content)
            tokens_truth, characters_truth = get_tokens_and_characters(truth_content)

            total_tokens_ocr += tokens_ocr
            total_characters_ocr += characters_ocr
            total_tokens_truth += tokens_truth
            total_characters_truth += characters_truth

            start_time = time.time()
            cer = calculate_cer(truth_content, ocr_content)
            end_time = time.time()

            elapsed_time = end_time - start_time
            total_cer += cer

            # Using string formatting to ensure consistent spacing
            results_data += f"{ocr_file},{cer:.4f},{tokens_ocr},{characters_ocr},{tokens_truth},{characters_truth},{elapsed_time:.4f}\n"

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

    # Write to both CSV and text file
    write_to_file(results_file_txt, results_data)
    write_to_csv(results_file_csv, results_data)
    print(f"Results written to {results_file_csv}.")
    print(f"Results written to {results_file_txt}.")

if __name__ == "__main__":
    main()
