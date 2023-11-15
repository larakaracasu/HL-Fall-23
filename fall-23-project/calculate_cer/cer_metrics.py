# CER values from the OpenAI and Manual tables for corresponding documents
cer_openai = [0.4118, 0.7143, 0.5455, 0.7308, 0.3125, 0.7143, 0.8571, 0.7143, 0.7368, 0.7143, 0.7143, 0.7386, 0.7368, 0.7368, 0.7692, 0.8333, 0.7368, 0.7368, 0.7143, 0.7143]

cer_manual = [0.1978, 0.0960, 0.0635, 0.1131, 0.0972, 0.1621, 0.3631, 0.3713, 0.1007, 0.1722, 0.1113, 0.3468, 0.3816, 0.1317, 0.4042, 0.5553, 0.1718, 0.2511, 0.0888, 0.1452]

# Calculate the absolute differences in CER
differences = [abs(cer_openai[i] - cer_manual[i]) for i in range(len(cer_openai))]

# Calculate the average difference
average_difference = sum(differences) / len(differences)

# Print the average difference
print(f"Average Difference in CER: {average_difference:.4f}")

import statistics

# Absolute differences in CER values
absolute_differences = [abs(cer_openai[i] - cer_manual[i]) for i in range(len(cer_openai))]

# Calculate the median of the absolute differences
median_difference = statistics.median(absolute_differences)

# Print the median difference
print(f"Median Difference in CER: {median_difference:.4f}")

# Calculate the standard deviation for CER values in the OpenAI table
std_dev_openai = statistics.stdev(cer_openai)

# Calculate the standard deviation for CER values in the Manual table
std_dev_manual = statistics.stdev(cer_manual)

# Print the standard deviations
print(f"Standard Deviation (OpenAI): {std_dev_openai:.4f}")
print(f"Standard Deviation (Manual): {std_dev_manual:.4f}")

import numpy as np

# Calculate the correlation between CER values
correlation = np.corrcoef(cer_openai, cer_manual)[0, 1]

# Print the correlation
print(f"Correlation between CER values: {correlation:.4f}")
