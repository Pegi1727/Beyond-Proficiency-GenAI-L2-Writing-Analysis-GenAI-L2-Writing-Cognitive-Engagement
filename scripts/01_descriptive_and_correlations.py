"""
01_descriptive_and_correlations.py
Purpose: Compute descriptive statistics and correlation matrix for the study.
Outputs: descriptive_stats.csv, correlation_matrix.csv, plots
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ---------- Paths ----------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# ---------- 1. Load data ----------
df = pd.read_csv(DATA_DIR / "survey_raw_data.csv")

print("Dataset shape:", df.shape)
print("Columns:", df.columns.tolist())

# ---------- 2. Demographic Summary ----------
print("\n--- Proficiency Distribution ---")
print(df["Proficiency"].value_counts())

print("\n--- Strand Distribution ---")
print(df["Strand"].value_counts())

print("\n--- Stage Distribution ---")
print(df["Stage"].value_counts())

# ---------- 3. Cronbach's Alpha (Reliability) ----------
# We compute reliability for the 3 cognitive strands within each stage
def cronbach_alpha(items_df):
    """Compute Cronbach's alpha for a set of items."""
    items = items_df.values
    k = items.shape[1]
    if k < 2:
        return np.nan
    item_variances = items.var(axis=0, ddof=1)
    total_variance = items.sum(axis=1).var(ddof=1)
    alpha = (k / (k - 1)) * (1 - (item_variances.sum() / total_variance))
    return alpha

# Pivot the data: each participant has 9 scores (3 stages × 3 strands)
pivot = survey_long.pivot_table(index='ParticipantID', columns=['Stage','Strand'], values='Score')
alpha_values = pivot.dropna(how='all').values
alpha = cronbach_alpha(pivot.T) if pivot.shape[1] > 1 else np.nan
print(f"\nCronbach's Alpha: {alpha:.3f}")

# ===== ... (The rest of your descriptive analysis code) =====

# 4. Export files
df.groupby(['Proficiency','Stage','Strand'])['Score'].agg(['mean','std','count']).to_csv(OUTPUT_DIR / "stage_strand_means.csv")
</｜DSML｜parameter>
</｜DSML｜invoke>
</｜DSML｜tool_calls>
