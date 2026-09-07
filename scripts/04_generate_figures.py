#!/usr/bin/env python3
"""
04_generate_figures.py
======================
Generates and exports all publication-ready empirical figures (Figures 2-5):
- Figure 2: Stage x Proficiency Interaction Plot
- Figure 3: Correlation between Editing Engagement & Writing Score
- Figure 4: Cognitive Engagement Strand by Writing Stage Distribution
- Figure 5: Writing Score Distribution & Ceiling Effect Analysis

Author: Pegah Merrikhi
DOI: 10.5281/zenodo.22635467
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


def set_style():
    sns.set_theme(style="ticks")
    plt.rcParams.update({
        'font.sans-serif': 'DejaVu Sans',
        'font.family': 'sans-serif',
        'figure.dpi': 300,
        'savefig.dpi': 300,
        'axes.labelsize': 11,
        'axes.titlesize': 12,
        'xtick.labelsize': ick.labelsize': 10,
        ' 10,
        'legend.fontsize': 10,
        'figure.titlesize': 13
    })


def generate_all_figures():
    set_style()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    data_dir = os.path.join(project_root, "data")
    fig_dir = os.path.join(project_root, "figures")
    os.makedirs(fig_dir, exist_ok=True)

    raw_path = os.path.join(data_dir, "survey_raw_data.csv")
    long_path = os.path.join(data_dir, "survey_long_format.csv")

    if not os.path.exists(raw_path):
        raw_path = "/mnt/data/survey_raw_data.csv"
    if not os.path.exists(long_path):
        long_path = "/mnt/data/survey_long_format.csv"

    df_raw = pd.read_csv(raw_path)
    df_long = pd.read_csv(long_path)

    navy = "#1B365D"
    rose = "#D9534F"
    teal = "#2E8B57"
    gold = "#E6A100"

    # ----------------------------------------------------
    # Figure 2: Interaction Plot (Stage x Proficiency)
    # ----------------------------------------------------
    fig, ax = plt.subplots(figsize=(7, 5))
    stage_order = ['Pre-writing', 'Drafting', 'Editing']

    stage_means = df_long.groupby(['Stage', 'Proficiency'])['Score'].agg(['mean', 'sem']).reset_index()
    stage_means['Stage'] = pd.Categorical(stage_means['Stage'], categories=stage_order, ordered=True)
    stage_means = stage_means.sort_values('Stage')

    colors = {'Low': rose, 'Intermediate': teal, 'High': navy}
    markers = {'Low': 's', 'Intermediate': '^', 'High': 'o'}

    for prof in ['Low', 'Intermediate', 'High']:
        sub = stage_means[stage_means['Proficiency'] == prof]
        if len(sub) > 0:
            ax.errorbar(sub['Stage'], sub['mean'], yerr=sub['sem'], label=f'{prof} Proficiency',
                        color=colors.get(prof, '#333333'), marker=markers.get(prof, 'o'),
                        linewidth=2, markersize=8, capsize=4, capthick=1.5)

    ax.set_title("Stage \u00d7 Proficiency Interaction on Cognitive Engagement", weight='bold', pad=12)
    ax.set_xlabel("L2 Writing Stage", weight='bold')
    ax.set_ylabel("Mean Engagement Score (1\u20135)", weight='bold')
    ax.set_ylim(2.5, 4.8)
    ax.legend(frameon=True, loc='lower right')
    ax.annotate(r"Interaction $\beta = -0.358, p = .043^*$", xy=(0.05, 0.90), xycoords='axes fraction',
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", lw=1))
    sns.despine()
    plt.tight_layout()
    f2_path = os.path.join(fig_dir, "Figure_2_Interaction_Stage_Proficiency.png")
    plt.savefig(f2_path)
    plt.close()
    print(f"Generated Figure 2: {f2_path}")

    # ----------------------------------------------------
    # Figure 3: Correlation (Editing Engagement vs Writing Score)
    # ----------------------------------------------------
    fig, ax = plt.subplots(figsize=(6.5, 5))
    if 'Edit_Composite' not in df_raw.columns:
        df_raw['Edit_Composite'] = df_raw[['Edit_Ling', 'Edit_Strat', 'Edit_Crit']].mean(axis=1)

    r, p = stats.pearsonr(df_raw['Edit_Composite'], df_raw['WritingScore'])
    sns.regplot(x='Edit_Composite', y='WritingScore', data=df_raw, ax=ax,
                color=navy, scatter_kws={'alpha': 0.7, 's': 45},
                line_kws={'color': rose, 'linewidth': 2})

    ax.set_title("Correlation: Editing Engagement vs. Writing Score", weight='bold', pad=12)
    ax.set_xlabel("Editing Cognitive Engagement", weight='bold')
    ax.set_ylabel("L2 Writing Score (Max: 20)", weight='bold')
    ax.annotate(f"r = {r:.3f}\np = {p:.4f}**", xy=(0.06, 0.85), xycoords='axes fraction',
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", lw=1), fontsize=10)
    sns.despine()
    plt.tight_layout()
    f3_path = os.path.join(fig_dir, "Figure_3_Correlation_Editing_WritingScore.png")
    plt.savefig(f3_path)
    plt.close()
    print(f"Generated Figure 3: {f3_path}")

    # ----------------------------------------------------
    # Figure 4: Strand by Stage Distribution (Box Plot)
    # ----------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 5))
    df_long['Stage'] = pd.Categorical(df_long['Stage'], categories=stage_order, ordered=True)
    sns.boxplot(x='Stage', y='Score', hue='Strand', data=df_long, ax=ax,
                palette=[navy, teal, gold], width=0.6, fliersize=2)
    ax.set_title("Distribution of Cognitive Strands Across Writing Stages", weight='bold', pad=12)
    ax.set_xlabel("Writing Stage", weight='bold')
    ax.set_ylabel("Cognitive Engagement Score", weight='bold')
    ax.legend(title="Strand", frameon=True, loc='upper right')
    sns.despine()
    plt.tight_layout()
    f4_path = os.path.join(fig_dir, "Figure_4_Strand_by_Stage_Distribution.png")
    plt.savefig(f4_path)
    plt.close()
    print(f"Generated Figure 4: {f4_path}")

    # ----------------------------------------------------
    # Figure 5: Writing Score Distribution & Ceiling Effect
    # ----------------------------------------------------
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.histplot(df_raw['WritingScore'], bins=12, kde=True, color=teal, ax=ax, edgecolor='white')
    ceiling_count = (df_raw['WritingScore'] >= 20).sum()
    ceiling_pct = (ceiling_count / len(df_raw)) * 100

    ax.axvline(20, color=rose, linestyle='--', linewidth=2, label=f'Ceiling at 20 ({ceiling_pct:.0f}%)')
    ax.set_title("Distribution of L2 Writing Scores & Ceiling Effect", weight='bold', pad=12)
    ax.set_xlabel("L2 Writing Score (Scale 0\u201320)", weight='bold')
    ax.set_ylabel("Participant Count", weight='bold')
    ax.legend(frameon=True, loc='upper left')
    sns.despine()
    plt.tight_layout()
    f5_path = os.path.join(fig_dir, "Figure_5_WritingScore_Ceiling_Proficiency.png")
    plt.savefig(f5_path)
    plt.close()
    print(f"Generated Figure 5: {f5_path}")

    print("All figures successfully generated and saved.\n")


if __name__ == "__main__":
    generate_all_figures()
