#!/usr/bin/env python3
"""
00_data_preprocessing.py
========================
Preprocesses raw survey data for:
1. Long-format data transformation (Stage x Strand per participant, N=900 rows)
2. Participant-level summary metrics
3. LMM-ready formatted dataset

Author: Pegah Merrikhi
DOI: 10.5281/zenodo.22635467
"""

import os
import pandas as pd
import numpy as np


def run_preprocessing():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    data_dir = os.path.join(project_root, "data")
    os.makedirs(data_dir, exist_ok=True)

    raw_path = os.path.join(data_dir, "survey_raw_data.csv")
    if not os.path.exists(raw_path):
        raw_path = os.path.join(project_root, "survey_raw_data.csv")
        if not os.path.exists(raw_path):
            raw_path = "/mnt/data/survey_raw_data.csv"

    print(f"Loading raw survey data from: {raw_path}")
    df = pd.read_csv(raw_path)
    print(f"Raw data shape: {df.shape}")

    id_col = 'ID' if 'ID' in df.columns else df.columns[0]

    subscales = [
        ('Pre-writing', 'Linguistic', 'Pre_Ling'),
        ('Pre-writing', 'Strategic', 'Pre_Strat'),
        ('Pre-writing', 'Critical', 'Pre_Crit'),
        ('Drafting', 'Linguistic', 'Draft_Ling'),
        ('Drafting', 'Strategic', 'Draft_Strat'),
        ('Drafting', 'Critical', 'Draft_Crit'),
        ('Editing', 'Linguistic', 'Edit_Ling'),
        ('Editing', 'Strategic', 'Edit_Strat'),
        ('Editing', 'Critical', 'Edit_Crit')
    ]

    long_rows = []
    for _, row in df.iterrows():
        p_id = row[id_col]
        prof = row['Proficiency']
        ws = row['WritingScore'] if 'WritingScore' in df.columns else np.nan
        gender = row['Gender'] if 'Gender' in df.columns else np.nan
        for stage, strand, col_name in subscales:
            long_rows.append({
                'ID': p_id, 'Proficiency': prof, 'WritingScore': ws,
                'Gender': gender, 'Stage': stage, 'Strand': strand,
                'Score': row[col_name]
            })

    df_long = pd.DataFrame(long_rows)

    long_out = os.path.join(data_dir, "survey_long_format.csv")
    df_long.to_csv(long_out, index=False)
    print(f"Saved long-format dataset to: {long_out} ({len(df_long)} rows)")

    lmm_out = os.path.join(data_dir, "lmm_ready_data.csv")
    df_long.to_csv(lmm_out, index=False)
    print(f"Saved LMM-ready dataset to: {lmm_out}")

    df_summary = df.copy()
    if 'Pre_Composite' not in df_summary.columns:
        df_summary['Pre_Composite'] = df[['Pre_Ling', 'Pre_Strat', 'Pre_Crit']].mean(axis=1)
    if 'Draft_Composite' not in df_summary.columns:
        df_summary['Draft_Composite'] = df[['Draft_Ling', 'Draft_Strat', 'Draft_Crit']].mean(axis=1)
    if 'Edit_Composite' not in df_summary.columns:
        df_summary['Edit_Composite'] = df[['Edit_Ling', 'Edit_Strat', 'Edit_Crit']].mean(axis=1)
    if 'Total_Engagement' not in df_summary.columns:
        df_summary['Total_Engagement'] = df_summary[['Pre_Composite', 'Draft_Composite', 'Edit_Composite']].mean(axis=1)

    summary_out = os.path.join(data_dir, "participant_summary_metrics.csv")
    df_summary.to_csv(summary_out, index=False)
    print(f"Saved summary metrics to: {summary_out}")

    print("Preprocessing completed successfully.\n")


if __name__ == "__main__":
    run_preprocessing()
