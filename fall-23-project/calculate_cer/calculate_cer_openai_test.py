import os
import time
import openai
import nltk
import pandas as pd
from nltk.metrics import edit_distance

openai.api_key = os.environ.get("OPENAI_API_KEY")

def get_edit_distance_from_openai(reference, hypothesis):
    prompt = (
        "Compute the edit distance (Levenshtein distance) for the hypothesis text given the reference text. "
        f"Reference text: '{reference[:5000]}'. Hypothesis text: '{hypothesis[:5000]}'. "
        "Respond with one single number for the edit distance, without any additional text, no matter what."
    )
    response = openai.Completion.create(model="text-davinci-003", prompt=prompt, max_tokens=10, n=1, temperature=0.2)
    try:
        edit_distance_openai = int(response.choices[0].text.strip())
    except ValueError:
        print(f"Unexpected response from GPT-3: {response.choices[0].text.strip()}")
        edit_distance_openai = -1  # Default to an invalid value
    return edit_distance_openai

def calculate_cer(reference, hypothesis):
    distance = edit_distance(reference, hypothesis)
    return distance / len(reference)

def write_to_file(filename, data):
    with open(filename, 'w', encoding="utf-8") as f:
        f.write(data)

def write_to_csv(filename, data):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

def main():
    ocr_dir = "C:\\Users\\larak\\OneDrive\\Documents\\History-Lab\\ocr_data\\preprocessed_ocr"
    truth_dir = "C:\\Users\\larak\\OneDrive\\Documents\\History-Lab\\truth_data\\preprocessed_truth"
    results_file_txt = "C:\\Users\\larak\\OneDrive\\Documents\\GitHub\\HL-Fall-23\\fall-23-project\\calculate_cer\\cer_results_openai.txt"
    results_file_csv = "C:\\Users\\larak\\OneDrive\\Documents\\GitHub\\HL-Fall-23\\fall-23-project\\calculate_cer\\cer_results_openai.csv"
    
    ocr_files = os.listdir(ocr_dir)
    
    total_cer = 0
    total_tokens_ref = 0
    total_tokens_hyp = 0
    total_characters_ocr = 0
    total_characters_truth = 0
    num_files = len(ocr_files)

    results_data = "Document,EditDistance (OpenAI),CER,Tokens (OCR),Length (OCR),Tokens (Truth),Length (Truth),Time\n"

    global_start_time = time.time()

    for ocr_file in ocr_files:
        with open(os.path.join(ocr_dir, ocr_file), 'r', encoding="utf-8") as f_ocr, \
            open(os.path.join(truth_dir, ocr_file), 'r', encoding="utf-8") as f_truth:

            ocr_content = f_ocr.read()
            truth_content = f_truth.read()

            num_tokens_hyp = len(nltk.word_tokenize(ocr_content))
            num_chars_hyp = len(ocr_content)
            num_tokens_ref = len(nltk.word_tokenize(truth_content))
            num_chars_ref = len(truth_content)
            
            start_time = time.time()
            edit_distance_openai = get_edit_distance_from_openai(truth_content, ocr_content)
            cer = calculate_cer(truth_content, ocr_content)
            end_time = time.time()

            elapsed_time = end_time - start_time
            total_cer += cer
            total_tokens_ref += num_tokens_ref
            total_tokens_hyp += num_tokens_hyp
            total_characters_ocr += num_chars_hyp
            total_characters_truth += num_chars_ref

            results_data += f"{ocr_file},{edit_distance_openai},{cer:.4f},{num_tokens_hyp},{num_chars_hyp},{num_tokens_ref},{num_chars_ref},{elapsed_time:.4f}\n"

    global_end_time = time.time()
    total_time = global_end_time - global_start_time
    average_cer = total_cer / num_files

    results_data += "\n"
    results_data += f"Average Character Error Rate for all documents,{average_cer:.4f}\n"
    results_data += f"Total time to process all documents,{total_time:.4f} seconds\n"
    results_data += f"Total tokens (OCR) for all documents,{total_tokens_hyp}\n"
    results_data += f"Total characters (OCR) for all documents,{total_characters_ocr}\n"
    results_data += f"Total tokens (Truth) for all documents,{total_tokens_ref}\n"
    results_data += f"Total characters (Truth) for all documents,{total_characters_truth}\n"

    # Write to both CSV and text file
    write_to_file(results_file_txt, results_data)
    write_to_csv(results_file_csv, results_data)
    print(f"Results written to {results_file_csv}.")
    print(f"Results written to {results_file_txt}.")

if __name__ == "__main__":
    main()
