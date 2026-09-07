import pandas as pd
کند:
```python
import pandas as pd
import numpy as np
import matplotlib.pyplotipy.stats import spearmanr
import seaborn as sns
import os

# Create output directory for figures
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load data (long format = one row per stage/strand per participant)
data = pd.read_csv("../data/survey_long_format.csv")
print("Dataset Shape:", data.shape)

# Basic descriptive statistics
cat_vars = ["ParticipantID", "Proficiency", "Stage", "Strand"]
for var in ["Proficiency", "Stage", "Strand"]:
print(f"\n=== Frequency: {var} ===")
print(data[var].value_counts())

# Nested design check
nested_check = data.groupby(["ParticipantID","Stage","Strand"]).size()
if (nested_check > 1).any():
print("⚠️ Warning: Duplicate rows detected!")
else:
print("✓ Nested structure confirmed: each PID has one observation per Stage×Strand.")

# Descriptive stats by group
print("\n=== Descriptive Statistics by Proficiency ===")
desc = data.groupby("Proficiency")["Score"].describe()
print(desc)

print("\n--- Descriptive Stats by (Proficiency, Stage, Strand) ---")
desc_stage_strand = data.groupby(["Proficiency", "Stage", "Strand"])["Score"].agg(['mean', 'std', 'count'])
print(desc_stage_strand.round(2))

# Correlation between composite engagement and final writing scores
corr_df = data.groupby('ParticipantID').agg(
WritingScore=('WritingScore', 'first'),
MeanScore=('Score', 'mean')
).reset_index()

print("\n--- Correlation: Mean Engagement vs Writing Score ---")
corr_val = corr_df[['WritingScore','MeanScore']].corr().iloc[0,1]
print(f"Pearson r = {corr_val:.3f}")

# Accuracy/Cronbach's alpha demonstration
# Compute participant variance
icc_df = data[['ParticipantID','Score']].groupby('ParticipantID').var().mean()[0]
total_var = data['Score'].var()
icc = icc_df / total_var
print(f"\nParticipant-level variance: {icc_df:.3f}")
print(f"Total variance: {total_var:.3f}")
print(f"Estimated ICC: {icc:.3f}")
</｜DSML｜parameter>
</｜DSML｜invoke>
</｜DSML｜tool_calls>
