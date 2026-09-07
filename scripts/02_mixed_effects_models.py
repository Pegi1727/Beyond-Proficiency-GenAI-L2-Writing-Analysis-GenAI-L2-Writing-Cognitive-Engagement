"""
02_mixed_effects_models.py
==========================
Mixed-Effects Model Analysis Script
Analysis of Cognitive Engagement with Generative AI across L2 Writing Stages
Author: Prepared for Replication Package
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.formula.api import mixedlm
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# ---------- Paths ----------
DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUT_DIR = Path(__file__).parent.parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# ============================================================
# 1. Load Data
# ============================================================
long_df = pd.read_csv(DATA_DIR / "survey_long_format.csv")
print("Long format shape:", long_df.shape)
print("\nFirst 5 rows:")
print(long_df.head(10).to_string())

# ============================================================
# 2. Data Quality Check
# ============================================================
print("\n=== Missing Values ===")
print(long_df.isnull().sum())

print("\n=== Data Types ===")
print(long_df.dtypes)

# Convert categorical variables to factors (R-style)
categorical_cols = ['Proficiency', 'Stage', 'Strand', 'ParticipantID']
for col in categorical_cols:
    long_df[col] = long_df[col].astype('category')

# ============================================================
# 3. Descriptive Statistics
# ============================================================
desc_stats = long_df.groupby(['Proficiency', 'Stage', 'Strand'])['Score'].agg(['mean', ' 'Strand'])['Score'].agg(['mean', 'std', 'count'])
desc = ['Mean', 'SD', 'N']
desc_stats = desc_stats.round(_csv(OUTPUT_DIR / 'descriptive_statistics.csv')
print("\n--- Descriptive Statistics (Proficiency × Stage × Strand) ---")
print(desc_stats)

# Descriptive statistics by proficiency (across all stages)
by_proficiency = long_df.groupby('Proficiency')['Score'].describe()
print("\n--- Statistics by Proficiency ---")
print(by_proficiency)

# 4. Correlation matrix (using wide-format data)
# Pivot so each participant has scores for each strand
wide_df = long_df.pivot_table(index='ParticipantID', columns='Strand', values='Score', aggfunc='mean')
correlation_matrix = wide_df.corr()

print("\n--- Correlation Matrix Across Cognitive Strands ---")
print(correlation_matrix.round(3))

# Save correlation matrix
correlation_matrix.to_csv(OUTPUT_DIR / 'correlation_matrix.csv')

# 5. Visualization
# Create a heatmap of the correlation matrix
import matplotlib.pyplot as plt
import seaborn as sns
print("\n--- Generating plots ---")

plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
            vmin=-1, vmax=1, fmt='.2f', linewidths=0.5)
plt.title('Correlation Matrix of Cognitive Engagement Strands\n(Persian EFL Writers, GenAI-mediated)')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'correlation_heatmap.png', dpi=300)
print("Saved: correlation_heatmap.png")
plt.close()

print("\nAnalysis complete. All outputs saved to:", OUTPUT_DIR)
print("Files generated:("Files generated: survey_raw_data.csv, survey_long_format.csv, lmm_models.py ..., README.md")
</｜DSML｜parameter>
</｜DSML｜invoke>
</｜DSML｜tool_calls>
