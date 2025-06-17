# Experiment 2: Exogenous Posner Cueing Task

**Project:** The Influence of Respiratory Cycles on Visuo-Spatial Attention
**Date:** 21-05-2025
**Version:** v1

---

## Overview

Experiment 2 used an exogenous Posner cueing paradigm to test how breathing phase (inhale vs. exhale) affects response times and accuracy across horizontal (left/right) and vertical (up/down) dimensions, including separate analyses by cue validity and difference scores.

---

## Directory Structure

```
TheInfluenceOfRespiratoryCyclesOnVisuoSpatialAttention_v1_21-05-2025/
└── Experiment2/
    ├── data/
    │   ├── raw/
    │   │   ├── horizontal/
    │   │   │   └── P<participantID>_horizontal.csv
    │   │   └── vertical/
    │   │       └── P<participantID>_vertical.csv
    │   ├── processed/
    │   │   ├── horizontal/
    │   │   │   └── P<participantID>_clean_horizontal.csv
    │   │   └── vertical/
    │   │       └── P<participantID>_clean_vertical.csv
    │   └── merged/
    │       ├── horizontal/
    │       │   └── merged_data_horizontal.csv
    │       ├── vertical/
    │       │   └── merged_data_vertical.csv
    │       └── combined/
    │           ├── merged_data.csv
    │           └── cell_desc.csv
    ├── scripts/
    │   ├── exp2_data_clean_horizontal.R    ← batch clean all horizontal raws
    │   ├── exp2_data_clean_vertical.R      ← batch clean all vertical raws
    │   ├── exp2_data_merge_horizontal.R    ← merges processed horizontals
    │   │   └── exp2_data_merge_vertical.R   ← merges processed verticals
    │   ├── exp2_analysis.R                 ← filtering, descriptives, ANOVAs + exports to `results/tables`
    │   └── exp2_plots.py                   ← reads cell_desc.csv & generates figures
    ├── results/
    │   ├── figures/
    │   │   ├── exp2_left_right.png
    │   │   └── exp2_up_down.png
    │   └── tables/                         ← omnibus ANOVAs and post-hoc CSVs
    │       ├── 01_OV_anova.csv
    │       ├── 02_OV_simpleEffect_Orientation_by_Validity.csv
    │       ├── …
    │       └── 36_UD_diff_interaction.csv
    └── README.md                          ← this file
```

---

## Data

### Raw files (`data/raw/`)

* **Horizontal:** `P<participantID>_horizontal.csv`
* **Vertical:**   `P<participantID>_vertical.csv`
* **Contents:** PsychoPy exports with cue location, probe location, breathing-phase markers, timestamps, metadata.

### Cleaned files (`data/processed/`)

Produced by cleaning scripts in batch:

* **exp2\_data\_clean\_horizontal.R**
  Processes all `data/raw/horizontal/P*_horizontal.csv` → outputs `data/processed/horizontal/P<participantID>_clean_horizontal.csv`

* **exp2\_data\_clean\_vertical.R**
  Processes all `data/raw/vertical/P*_vertical.csv` → outputs `data/processed/vertical/P<participantID>_clean_vertical.csv`

Each cleaning script:

1. Drops practice trials & unused columns
2. Truncates at `key_resp.rt`
3. Recodes breathing-phase markers to `inhale`/`exhale`
4. Recodes `target_x`/`target_y` to `left`/`right`/`up`/`down`/`catch`
5. Recodes `key_resp.keys` & cue validity to `response` (`correct`/`incorrect`)
6. Outputs columns:

   ```
   participant_ID │ dimension │ trial │ validity │ phase │ response │ rt
   ```

### Merged data (`data/merged/`)

1. **Horizontal merge:** `merged_data_horizontal.csv` via `exp2_data_merge_horizontal.R`
2. **Vertical merge:**   `merged_data_vertical.csv` via `exp2_data_merge_vertical.R`
3. **Combined dataset:** `merged_data.csv` (manually concatenated into `data/merged/combined/`)
4. **Cell-level descriptives:** `cell_desc.csv` via `exp2_analysis.R` (weighted means, SEs, 95% CIs by dimension × validity × phase)

---

## Scripts

1. **exp2\_data\_clean\_horizontal.R**

   ```bash
   Rscript scripts/exp2_data_clean_horizontal.R data/raw/horizontal/ data/processed/horizontal/
   ```

2. **exp2\_data\_clean\_vertical.R**

   ```bash
   Rscript scripts/exp2_data_clean_vertical.R data/raw/vertical/ data/processed/vertical/
   ```

3. **exp2\_data\_merge\_horizontal.R**

   ```bash
   Rscript scripts/exp2_data_merge_horizontal.R data/processed/horizontal/ data/merged/horizontal/
   ```

4. **exp2\_data\_merge\_vertical.R**

   ```bash
   Rscript scripts/exp2_data_merge_vertical.R data/processed/vertical/ data/merged/vertical/
   ```

5. **exp2\_analysis.R**

   * Trial filtering (remove catch & incorrect)
   * Participant exclusion (≥30% incorrect)
   * Winsorise RTs (±2 SD)
   * Compute descriptives → `cell_desc.csv`
   * 2×2 ANOVAs (Orientation×Validity, L/R×Phase, U/D×Phase) + Bonferroni contrasts
   * **Export** all ANOVA tables & contrasts → `results/tables/`

   ```bash
   Rscript scripts/exp2_analysis.R data/merged/combined/ data/merged/combined/cell_desc.csv
   ```

6. **exp2\_plots.py**

   ```bash
   python scripts/exp2_plots.py data/merged/combined/cell_desc.csv results/figures/
   ```

---

## Usage Workflow

1. **Install dependencies**

   ```bash
   # R packages
   Rscript -e "install.packages(c('dplyr','readr','afex','emmeans'))"
   # Python packages
   pip install pandas matplotlib
   ```

2. **Clean raw data**

   ```bash
   Rscript scripts/exp2_data_clean_horizontal.R data/raw/horizontal/ data/processed/horizontal/
   Rscript scripts/exp2_data_clean_vertical.R   data/raw/vertical/   data/processed/vertical/
   ```

3. **Merge processed data**

   ```bash
   Rscript scripts/exp2_data_merge_horizontal.R data/processed/horizontal/ data/merged/horizontal/
   Rscript scripts/exp2_data_merge_vertical.R   data/processed/vertical/   data/merged/vertical/
   ```

4. **Combine and analyze**

   ```bash
   # Copy merged horizontal & vertical into combined/
   Rscript scripts/exp2_analysis.R data/merged/combined/ data/merged/combined/cell_desc.csv
   ```

5. **Generate figures**

   ```bash
   python scripts/exp2_plots.py data/merged/combined/cell_desc.csv results/figures/
   ```

---

For questions or issues, please contact the project maintainer.
