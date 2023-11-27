# Project Overview: Fall '23, History Lab

The project aims to assess the reliability of using langdetect library as heuristic for differentiating between accurate and garbled OCR outputs. Current OCR evaluation on COVID-19 collection applies langdetect and checks if the detected language is not English or if certainty <= 0.98. If so, the document is marked as an exception. The goal of this project is to determine if CER calculations and langdetect outputs agree on their classifications of accurate vs. inaccurate OCR documents.

## First Level - OCR Evaluation with Character Error Rate (CER):

### Data Preparation:
20 documents were be sampled from the US Declassified Documents Online (DDO) database. Ground truth (hand-transcribed) and OCR versions in plain text are available for each document. History Lab possesses the former, and the latter are available online via Gale Cengage. 

### CER Calculation:
The Character Error Rate (CER) are calculated using the editdistance library in Python. The library provides a fast C-based implementation of the Levenshtein distance, using the following formula:

CER = {Insertions + Deletions + Substitutions}/{Total Characters in Ground Truth}

This measure provides an indication of how accurate the OCR text is compared to the ground truth.

### Determine CER Threshold for 'Garbled':
Manual examination of documents and corresponding CER values will be conducted to establish a threshold. Documents with a CER above this threshold will be considered as having "garbled" OCR text, requiring reprocessing or manual correction.

### Setting CER Threshold:
Summary statistics for CER across sampled documents will be computed. The mean CER may be considered as the threshold for "good," with values below classified as "garbled."

## Second Level - Comparing CER Results to langdetect:

### Categorization Based on CER Threshold:
Using the CER threshold from the first level, OCR outputs will be categorized into "good" (below the threshold and assumed reliable) and "garbled" (above the threshold and unreliable).

### Running langdetect:
langdetect will be applied to the OCR version of the documents.

### Creating Confusion Matrix for langdetect:
A confusion matrix will be constructed using:
- **Ground Truth:** True categories of "good" and "garbled" based on CER.
- **Predicted:** Output from langdetect. Ideally, langdetect correctly identifies the language for "good" documents and may have difficulty or errors for "garbled" ones.

### Computing Accuracy Metrics:
Various accuracy metrics will be derived from the confusion matrix to assess LangDetect's performance in comparison to CER.

## Additional Considerations:
- OpenAI models will be tested for OCR evaluation and text correction.
- Local processing time will be monitored and recorded for performance evaluation.

# Important Files

## calculate_cer

### calculate_cer.py

The calculate_cer.py script is designed to calculate the Character Error Rate (CER) for a set of OCR (Optical Character Recognition) documents. It compares the OCR content with the ground truth (hand-transcribed) content to measure the accuracy of the OCR output. The script uses the editdistance library for distance calculation and nltk for tokenization.

**How it Works:**
The script reads OCR and ground truth documents from specified directories.
It calculates the CER using the formula: CER = (Insertions + Deletions + Substitutions) / Total Characters in Ground Truth.
The results, including CER, tokens, characters, and processing time for each document, are recorded.
Summary statistics and metrics are generated, including average CER, total processing time, and total tokens and characters for OCR and ground truth.

**How to Run:**
Set your OpenAI API key as an environment variable: export OPENAI_API_KEY=your_api_key
```bash
python calculate_cer_openai_test.py
```

**Directories:**
ocr_dir: Directory containing preprocessed OCR documents.
truth_dir: Directory containing preprocessed ground truth documents.
results_file_csv: CSV file to store results.
results_file_txt: Text file to store results.

**Result Files:**
cer_results_manual.csv: CSV file containing detailed results.
cer_results_manual.txt: Text file containing detailed results.

### calculate_cer_openai.py

The calculate_cer_openai.py script utilizes the OpenAI GPT-3 model to calculate the Character Error Rate (CER) for a set of OCR (Optical Character Recognition) documents. It compares the OCR content with the ground truth (hand-transcribed) content to measure the accuracy of the OCR output. The script uses the OpenAI GPT-3 model for CER calculation and nltk for tokenization.

**How it Works:**
The script reads OCR and ground truth documents from specified directories.
It uses the OpenAI GPT-3 model to generate the Character Error Rate (CER) by providing a prompt with reference and hypothesis texts.
The results, including CER, tokens, characters, and processing time for each document, are recorded.
Summary statistics and metrics are generated, including average CER, total processing time, and total tokens and characters for OCR and ground truth.

**How to Run:**
Set your OpenAI API key as an environment variable: export OPENAI_API_KEY=your_api_key
```bash
python calculate_cer_openai_test.py
```

**Directories:**
ocr_dir: Directory containing preprocessed OCR documents.
truth_dir: Directory containing preprocessed ground truth documents.

**Result Files:**
cer_results_openai.csv: CSV file containing results.
cer_results_openai.txt: Text file containing results.

### calculate_cer_openai_test.py

The calculate_cer_openai_test.py script serves as a testing tool to investigate if OpenAI GPT-3 model accuracy improves when calculating only the edit distance instead of the entire Character Error Rate (CER). It compares the edit distances calculated by OpenAI GPT-3 and the NLTK library for a set of OCR (Optical Character Recognition) documents. The script aims to test whether focusing on edit distance alone improves OpenAI GPT-3 model accuracy.
Results indicate that the edit distances calculated by OpenAI GPT-3 are consistently low, suggesting potential limitations or inaccuracies in the edit distance computation.

**How it Works:**
The script reads OCR and ground truth documents from specified directories.
It calculates edit distance using OpenAI GPT-3 model and NLTK library.
It calculates the Character Error Rate (CER) using the OpenAI edit distance as the numerator.
The results, including CER, edit distances, tokens, characters, and processing time for each document, are recorded.
Summary statistics and metrics are generated, including average CER, average NLTK edit distance, total processing time, and total tokens and characters for OCR and ground truth.

**How to Run:**
Set your OpenAI API key as an environment variable: export OPENAI_API_KEY=your_api_key
```bash
python calculate_cer_openai_test.py
```

**Directories:**
ocr_dir: Directory containing preprocessed OCR documents.
truth_dir: Directory containing preprocessed ground truth documents.
results_file_csv: CSV file to store results.
results_file_txt: Text file to store results.

**Results:**
cer_results_openai_test.csv: CSV file containing detailed results.
cer_results_openai_test.txt: Text file containing detailed results.

### correct_text_test.py

Evaluate if the OpenAI model can correct incorrectly transcribed OCR text. Results were mixed: the OpenAI model sometimes decreases the Character Error Rate (CER), improving the text. However, in other cases, it produces nonsensical output that is too short with random punctuation. Some inaccuracies were observed in the correction process, resulting in outputs that are nonsensical or too short.
Corrected texts are written to a new directory, openai_corrected_text.

**How to Run:**
```bash
python correct_text_test.py
```

**Parameters:**
Model: text-davinci-003
Max Tokens: 2000
Temperature: 0.5

**Results:**
cer_results_corrected.csv: CSV file with detailed CER results for original and corrected OCR text.
cer_results_corrected.txt: Text file with the same information as CSV.

## langdetect

### langdetect_ocr.py

The langdetect_ocr.py script is designed to evaluate the language of preprocessed OCR (Optical Character Recognition) documents using the langdetect library. It assesses whether the detected language meets the criteria for garbledness and records the results in a CSV file. The langdetect library is configured to ensure consistent results by seeding the detector factory.
The criteria for garbledness include non-English languages or English with a probability below 0.98.
The script aims to determine the language of OCR documents and evaluate if they meet the criteria for garbledness based on the detected language.
Results are recorded in a CSV file, including the filename, detected language, language probability, and garbled status.

**How it Works:**
The script reads preprocessed OCR text files from a specified directory.
It uses the langdetect library to detect the language and associated probabilities of each document.
The script evaluates whether the detected language meets the criteria for garbledness.
Results, including the filename, detected language, language probability, and a flag indicating garbled status, are written to a CSV file.
Exceptions and errors during the process are logged for debugging.

**How to Run:**
```bash
python langdetect.py
```

**Directories:**
ocr_data_directory: Directory containing preprocessed OCR text files.

**Results:**
langdetect_results.csv: CSV file containing detailed results, including filename, detected language, language probability, and garbled status.
