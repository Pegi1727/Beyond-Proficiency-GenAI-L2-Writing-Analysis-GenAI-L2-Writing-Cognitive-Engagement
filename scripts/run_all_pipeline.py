#!/usr/bin/env python3
"""
run_all_pipeline.py
===================
Master Pipeline Runner: Executes the entire analytical and figure generation
pipeline for the research project in sequence.

Pipeline Steps:
1. 00_data_preprocessing.py           -> Prepares long-format and summary datasets
2. 01_descriptive_and_correlations.py -> Generates descriptive stats & correlation tables
3. 02_mixed_effects_models.py         -> Computes Linear Mixed-Effects Models (LMM)
4. 04_generate_figures.py             -> Generates Figures 2-5 at 300 DPI

Author: Pegah Merrikhi
DOI: 10.5281/zenodo.22635467
"""

import sys
import subprocess
import time


def run_step(step_name, script_name):
    print("\n" + "=" * 70)
    print(f"STEP: {step_name} ({script_name})")
    print("=" * 70)
    start_time = time.time()
    result = subprocess.run([sys.executable, script_name])
    elapsed = time.time() - start_time
    if result.returncode != 0:
        print(f"Error executing {script_name} (Exit code: {result.returncode})")
        sys.exit(result.returncode)
    else:
        print(f"Completed {script_name} in {elapsed:.2f} seconds.")


def main():
    print("=" * 70)
    print("REPRODUCIBILITY PIPELINE: Beyond Proficiency GenAI L2 Writing Analysis")
    print("Author: Pegah Merrikhi | DOI: 10.5281/zenodo.22635467")
    print("=" * 70)

    steps = [
        ("Data Preprocessing", "scripts/00_data_preprocessing.py"),
        ("Descriptives & Correlations", "scripts/01_descriptive_and_correlations.py"),
        ("Linear Mixed-Effects Models", "scripts/02_mixed_effects_models.py"),
        ("Figure Reproduction", "scripts/04_generate_figures.py")
    ]

    for title, script in steps:
        run_step(title, script)

    print("\n" + "=" * 70)
    print("FULL REPRODUCIBILITY PIPELINE EXECUTED SUCCESSFULLY!")
    print("All outputs, tables, and figures have been generated and validated.")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
