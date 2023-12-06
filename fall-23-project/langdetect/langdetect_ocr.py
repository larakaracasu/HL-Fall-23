import os
import langdetect
import csv

# langdetect configs
langdetect.DetectorFactory.seed = 0    # ensure consistent results

ocr_data_directory = os.environ["OCR_DATA_DIRECTORY"]

# Specify the CSV file name in the current working directory
csv_file_path = "langdetect_results.csv"

def lang_eval(body):
    try:
        lang = langdetect.detect_langs(body)
        print(f'in lang_eval: {lang}')
        return lang
    except Exception as e:
        print(f'Exception in lang_eval: {e}')
        return e

def write_to_csv(file_path, lang):
    filename = os.path.basename(file_path)

    if lang is not None:
        meets_criteria = lang[0].lang != 'en' or lang[0].prob <= 0.98

        with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([filename, lang[0].lang, lang[0].prob, meets_criteria])
        
        print(f'Writing to CSV: {filename}, Language:, {lang[0].lang}, Probability: {lang[0].prob}, Garbled: {meets_criteria}')
    else:
        print(f'{filename}: lang is None, skipping CSV write')

def process_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        body = file.read()
        try:
            lang = lang_eval(body)
            if lang:
                filename = os.path.basename(file_path)
                print(f'{filename}: {lang}')
                write_to_csv(file_path, lang)
        except Exception as e:
            print(f'{file_path}: {e}')

def main():
    for filename in os.listdir(ocr_data_directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(ocr_data_directory, filename)
            process_text_file(file_path)

if __name__ == "__main__":
    main()
