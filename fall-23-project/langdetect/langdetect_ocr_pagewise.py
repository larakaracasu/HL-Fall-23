import os
import langdetect
import csv

# langdetect configs
langdetect.DetectorFactory.seed = 0  # ensure consistent results

truth_data_directory = 'C:/Users/larak/OneDrive/Documents/History-Lab/truth_data/preprocessed_truth_pagewise'
ocr_data_directory = 'C:/Users/larak/OneDrive/Documents/History-Lab/ocr_data/preprocessed_ocr_pagewise'

# Specify the CSV file name in the current working directory
csv_file_path = "langdetect_results_pagewise.csv"

def lang_eval(body):
    try:
        lang = langdetect.detect_langs(body)
        print(f'in lang_eval: {lang}')
        return lang
    except Exception as e:
        print(f'Exception in lang_eval: {e}')
        return e

def write_to_csv(file_path, lang, meets_criteria):
    filename = os.path.basename(file_path)

    with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([filename, lang[0].lang, lang[0].prob, meets_criteria])

    print(f'Writing to CSV: {filename}, Language:, {lang[0].lang}, Probability: {lang[0].prob}, Garbled: {meets_criteria}')

def process_page_file(ocr_path):
    with open(ocr_path, 'r', encoding='utf-8') as ocr_file:
        ocr_body = ocr_file.read()

        try:
            ocr_lang = lang_eval(ocr_body)

            meets_criteria = False
            if ocr_lang:
                meets_criteria = ocr_lang[0].lang != 'en' or ocr_lang[0].prob <= 0.98

            filename = os.path.basename(ocr_path)
            print(f'{filename}: OCR Language: {ocr_lang}')

            write_to_csv(ocr_path, ocr_lang, meets_criteria)

        except Exception as e:
            print(f'{ocr_path}: {e}')

def main():
    for ocr_filename in os.listdir(ocr_data_directory):
        if ocr_filename.endswith(".txt"):
            ocr_path = os.path.join(ocr_data_directory, ocr_filename)

            process_page_file(ocr_path)

if __name__ == "__main__":
    main()
