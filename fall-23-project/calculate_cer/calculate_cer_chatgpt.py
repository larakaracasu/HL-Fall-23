import os
import time
import openai

# Set up the OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

def get_cer_from_chatgpt(reference, hypothesis):
    """
    Get Character Error Rate from ChatGPT.
    """
    prompt = (f"Given the reference text \"{reference}\" and the hypothesis text \"{hypothesis}\", "
              "please compute and provide the Character Error Rate (CER) as a single numerical value. "
              "The Character Error Rate (CER) is calculated as (Substitutions + Insertions + Deletions) / Total number of reference characters. "
              "Ensure the answer is a single number without any additional text.")
    response = openai.Completion.create(model="text-davinci-003", prompt=prompt, max_tokens=1, n=1, temperature=0.1)
    
    try:
        cer = float(response.choices[0].text.strip())
    except ValueError:
        print(f"Unexpected response from ChatGPT: {response.choices[0].text.strip()}")
        cer = 1.0  # you can default to maximum error or any other fallback strategy
    
    return cer


def write_to_file(filename, data):
    """
    Write the given data to a file.
    """
    with open(filename, 'w', encoding="utf-8") as f:
        f.write(data)

def main():
    ocr_dir = "C:\\Users\\larak\\OneDrive\\Documents\\History-Lab\\ocr_data\\preprocessed_ocr"
    truth_dir = "C:\\Users\\larak\\OneDrive\\Documents\\History-Lab\\truth_data\\preprocessed_truth"
    results_file = "C:\\Users\\larak\\OneDrive\\Documents\\GitHub\\HL-Fall-23\\fall-23-project\\calculate_cer\\cer_results_chatgpt.txt"
    
    ocr_files = os.listdir(ocr_dir)
    
    total_cer = 0
    num_files = len(ocr_files)

    results_data = "Document Name\tCharacter Error Rate\tTime (seconds)\n"
    results_data += "-"*70 + "\n"
    
    global_start_time = time.time()

    for ocr_file in ocr_files:
        with open(os.path.join(ocr_dir, ocr_file), 'r', encoding="utf-8") as f_ocr, \
             open(os.path.join(truth_dir, ocr_file), 'r', encoding="utf-8") as f_truth:
            
            ocr_content = f_ocr.read()
            truth_content = f_truth.read()

            start_time = time.time()
            cer = get_cer_from_chatgpt(truth_content, ocr_content)
            end_time = time.time()

            elapsed_time = end_time - start_time
            total_cer += cer
            results_data += f"{ocr_file}\t{cer:.4f}\t{elapsed_time:.4f}\n"

    global_end_time = time.time()
    total_time = global_end_time - global_start_time
    average_cer = total_cer / num_files

    results_data += "\n" + "-"*70 + "\n"
    results_data += f"Average Character Error Rate for all documents: {average_cer:.4f}\n"
    results_data += f"Total time to process all documents: {total_time:.4f} seconds\n"

    # Write the results to a file
    write_to_file(results_file, results_data)
    print(f"Results written to {results_file}")

if __name__ == "__main__":
    main()
