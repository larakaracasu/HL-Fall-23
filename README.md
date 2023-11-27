# Project Overview: Fall '23, History Lab

## Goal:
The project aims to assess the reliability of using langdetect library as heuristic for differentiating between accurate and garbled OCR outputs. Current OCR evaluation on COVID-19 collection applies langdetect and checks if the detected language is not English or if certainty <= 0.98. If so, the document is marked as an exception. The goal of this project is to determine if CER calculations and langdetect outputs agree on their classifications of accurate vs. inaccurate OCR documents.

## First Level - OCR Evaluation with Character Error Rate (CER):

### Data Preparation:
20 documents were be sampled from the US Declassified Documents Online (DDO) database. Ground truth (hand-transcribed) and OCR versions in plain text are available for each document. The History Lab possesses the former, and the latter are available online via Gale Cengage. 

### CER Calculation:
The Character Error Rate (CER) are calculated for each document using the formula:
\[CER = \frac{Insertions + Deletions + Substitutions}{Total Characters in Ground Truth}\]
This measure provides an indication of how accurate the OCR text is compared to the ground truth.

### Determine CER Threshold for 'Garbled':
Manual examination of documents and corresponding CER values will be conducted to establish a threshold. Documents with a CER above this threshold will be considered as having "Garbled" OCR text, requiring reprocessing or manual correction.

### Setting CER Threshold:
Summary statistics for CER across sampled documents will be computed. The mean CER may be considered as the threshold for "Good," with values below classified as "Garbled."

## Second Level - Comparing CER Results to langdetect:

### Categorization Based on CER Threshold:
Using the CER threshold from the first level, OCR outputs will be categorized into "Good" (below the threshold and assumed reliable) and "Garbled" (above the threshold and unreliable).

### Running langdetect:
langdetect will be applied to the OCR version of the documents.

### Creating Confusion Matrix for langdetect:
A confusion matrix will be constructed using:
- **Ground Truth:** True categories of "Good" and "Garbled" based on CER.
- **Predicted:** Output from LangDetect. Ideally, LangDetect correctly identifies the language for "Good" documents and may have difficulty or errors for "Garbled" ones.

### Computing Accuracy Metrics:
Various accuracy metrics will be derived from the confusion matrix to assess LangDetect's performance in comparison to CER.

## Additional Considerations:
- ChatGPT will also be employed in the project for OCR evaluation.
- The project will involve experimentation with different approaches, including character-by-character processing and ChatGPT's embedding-based methods.
- Local processing time will be monitored and recorded for performance evaluation.

The project will provide insights into the alignment between langdetect heuristic and Character Error Rate in identifying "Good" and "Garbled" OCR outputs.

# Folder Summaries

## calculate_cer
- **calculate_cer.py:** Python script for calculating Character Error Rate (CER) using the openai library.
- **calculate_cer_chatgpt.py:** Python script for calculating CER using ChatGPT for edit distance.
- **calculate_cer_openai_test.py:** Python script for CER calculation using the openai library.
- **cer_metrics.py:** Python script containing metrics functions for CER evaluation.
- **cer_results_corrected.csv:** CSV file containing corrected CER results.
- **cer_results_corrected.txt:** Text file containing corrected CER results.
- **cer_results_manual.csv:** CSV file containing manually entered CER results.
- **cer_results_manual.txt:** Text file containing manually entered CER results.
- **cer_results_openai.csv:** CSV file containing CER results using openai.
- **cer_results_openai.txt:** Text file containing CER results using openai.
- **cer_results_openai_test.csv:** CSV file containing CER results using openai for testing.
- **cer_results_openai_test.txt:** Text file containing CER results using openai for testing.
- **correct_text_test.py:** Python script for testing text correction.
- **determine_garbled_threshold.ipynb:** Jupyter notebook for determining the CER threshold.
- **test_metrics.py:** Python script for testing metrics.

## langdetect
- **langdetect_ocr.py:** Python script for language detection on OCR outputs.
