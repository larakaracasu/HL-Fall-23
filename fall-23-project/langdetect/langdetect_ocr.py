import os
import langdetect
import csv

# langdetect configs
langdetect.DetectorFactory.seed = 0    # ensure consistent results

def lang_eval(body):
    try:
        #print(body[:50])
        lang = langdetect.detect_langs(body)
        print(f'in lang_eval: {lang}')
        return lang
    except Exception as e:
        print(f'Exception in lang_eval: {e}')
        return e

def write_to_csv(file_path, lang):
    filename = os.path.basename(file_path)

    if lang is not None:
        # Determine if it meets the criteria for garbledness
        meets_criteria = lang[0].lang != 'en' or lang[0].prob <= 0.98

        # Write to CSV
        with open("C:\\Users\\larak\\OneDrive\\Documents\\GitHub\\HL-Fall-23\\fall-23-project\\langdetect\\langdetect_results.csv", 'a', newline='', encoding='utf-8') as csvfile:
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
    ocr_data_directory = "C:\\Users\\larak\\OneDrive\\Documents\\History-Lab\\ocr_data\\preprocessed_ocr"
    for filename in os.listdir(ocr_data_directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(ocr_data_directory, filename)
            process_text_file(file_path)

if __name__ == "__main__":
    main()
