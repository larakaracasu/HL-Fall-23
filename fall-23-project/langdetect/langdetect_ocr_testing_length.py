# langdetect_ocr_testing_length.py

import os
from langdetect import detect_langs
import pandas as pd

# Function to detect language and probability for a given text
def detect_language(text):
    try:
        # Check if the text is empty or very short
        if len(text.strip()) < 3:
            raise ValueError("No features in text.")
        
        results = detect_langs(text)
        return {'lang': results[0].lang, 'prob': results[0].prob}
    except Exception as e:
        print(f"Exception: {e}")
        return {'lang': 'NA', 'prob': 0.0}

# Function to read CER results from the manual CSV
def read_cer_results(csv_path):
    cer_data = pd.read_csv(csv_path)
    return cer_data.set_index('Document')['CER'].to_dict()

# Function to test different lengths of the input text
def test_text_lengths(file_path, lengths):
    with open(file_path, 'r', encoding='utf-8') as file:
        input_text = file.read()

    results = {'Document': os.path.basename(file_path), 'CER': cer_results.get(os.path.basename(file_path), None)}

    for length in lengths:
        truncated_text = input_text[:length]
        lang_prob = detect_language(truncated_text)

        # Append results for each length
        results[f'Language ({length} chars)'] = lang_prob['lang']
        results[f'Probability ({length} chars)'] = lang_prob['prob']

    return results

if __name__ == "__main__":
    # Load the CSV with CER results
    cer_results_path = "C:\\Users\\larak\\OneDrive\\Documents\\GitHub\\HL-Fall-23\\fall-23-project\\calculate_cer\\cer_results_manual.csv"
    cer_results = read_cer_results(cer_results_path)

    # Get the OCR data directory from the environment variable
    ocr_data_directory = os.environ.get("OCR_DATA_DIRECTORY")

    # Results dictionary to store data for all documents
    all_results = {'Document': [], 'CER': []}

    # Collect lengths of all documents
    document_lengths = []

    # Iterate through files in the OCR directory
    for filename in os.listdir(ocr_data_directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(ocr_data_directory, filename)

            # Read the entire document content
            with open(file_path, 'r', encoding='utf-8') as file:
                input_text = file.read()

            document_lengths.append(len(input_text))

    # Set the reference length for the last test case
    reference_length = min(document_lengths)

    # Iterate through files again to get language detection results
    for filename in os.listdir(ocr_data_directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(ocr_data_directory, filename)

            # Read the entire document content
            with open(file_path, 'r', encoding='utf-8') as file:
                input_text = file.read()

            # Test different lengths and get language detection results
            lengths_to_test = [10, 100, 500, 1000, 5000, reference_length]

            results = test_text_lengths(file_path, lengths_to_test)

            # Append results to the all_results dictionary
            all_results['Document'].append(results['Document'])
            all_results['CER'].append(results['CER'])
            for length in lengths_to_test[:-1]:
                lang_key = f'Language ({length} chars)'
                prob_key = f'Probability ({length} chars)'

                # Ensure the lengths match before appending
                lang_value = results.get(lang_key, None)
                prob_value = results.get(prob_key, None)

                if lang_value is not None and prob_value is not None:
                    all_results.setdefault(lang_key, []).append(lang_value)
                    all_results.setdefault(prob_key, []).append(prob_value)

            # Dynamically adjust the length for the last test case
            last_length = lengths_to_test[-1]
            lang_key = f'Language ({last_length} chars)'
            prob_key = f'Probability ({last_length} chars)'
            lang_value = results.get(lang_key, None)
            prob_value = results.get(prob_key, None)

            if lang_value is not None and prob_value is not None:
                all_results.setdefault(lang_key, []).append(lang_value)
                all_results.setdefault(prob_key, []).append(prob_value)

    # Create a DataFrame from the results
    all_results_df = pd.DataFrame(all_results)

    # Save the results to a CSV file in the current directory
    output_csv_path = "language_detection_results_all_documents.csv"
    all_results_df.to_csv(output_csv_path, index=False)

    print(f"Results for all documents saved to {output_csv_path}")
