import pandas as pd
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Read the enhanced results CSV
results_df = pd.read_csv("cer_results_enhanced.csv")

# Create a binary column for truth (CER >= 0.35)
results_df['Truth'] = results_df['CER >= 0.35'].apply(lambda x: 'TRUE' if x else 'FALSE')

# Generate confusion matrix
conf_matrix = confusion_matrix(results_df['Truth'], results_df['Garbled?'])

# Plot confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", xticklabels=['FALSE', 'TRUE'], yticklabels=['FALSE', 'TRUE'])
plt.title("Confusion Matrix")
plt.xlabel("Test (Garbled?)")
plt.ylabel("Truth (CER >= 0.35)")
plt.show()
