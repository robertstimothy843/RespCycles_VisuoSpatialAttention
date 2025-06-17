# Experiment 2 analysis script
# Author: Timothy E. Roberts
# Description:
#   * Loads data from the specified absolute path
#   * Removes catch trials and incorrect responses (trial-level cleaning)
#   * Identifies participants with ≥ 30 % incorrect responses (non-catch)
#     • Excludes them from *all* subsequent analyses (descriptives, winsorising, ANOVAs)
#   * Prints clear counts for trials and participant exclusions
#   * **Winsorises RTs (±2 SD within participant)** before descriptive statistics
#   * Computes descriptive statistics (weighted mean, SD, SE, 95 % CI) per Position × Phase
#   * Runs two 2×2 within-participant repeated-measures ANOVAs on the winsorised data
#       1. Left/Right × Inhale/Exhale
#       2. Up/Down   × Inhale/Exhale
#   * Provides Bonferroni-adjusted **simple effects** (Position | Phase; Phase | Position)
#     and **interaction contrasts** (all Position×Phase pairwise) for each omnibus ANOVA
#   * Then, for each of those two analyses:
#       • ANOVAs on Valid cues only (with simple effects + interaction contrasts)
#       • ANOVAs on Invalid cues only (with simple effects + interaction contrasts)
#       • ANOVAs on the difference (Invalid − Valid) (with simple effects + interaction contrasts)

# ──────────────────────────────────────────────────────────────────────────────
# 1. SET-UP --------------------------------------------------------------------
# ──────────────────────────────────────────────────────────────────────────────

# Uncomment to install if first run:
# install.packages(c("tidyverse", "afex", "emmeans"))

library(tidyverse)
library(afex)
library(emmeans)

afex_options(type = 3)

# Path to data ----------------------------------------------------------------
raw_data <- read_csv(
  "C:/Users/amnesia/Desktop/RespCycles_VisuoSpatialAttention/Experiment2/data/merged/combined/merged_data.csv",
  show_col_types = FALSE
)

# ──────────────────────────────────────────────────────────────────────────────
# 2. TRIAL-LEVEL CLEANING ------------------------------------------------------
# ──────────────────────────────────────────────────────────────────────────────

total_trials <- nrow(raw_data)

catch_trials           <- raw_data %>% filter(position == "catch")
incorrect_trials_total <- raw_data %>% filter(response != "correct")
overlap_trials         <- raw_data %>% filter(position == "catch", response != "correct")

n_catch              <- nrow(catch_trials)
n_incorrect_total    <- nrow(incorrect_trials_total)
n_overlap            <- nrow(overlap_trials)
n_incorrect_noncatch <- n_incorrect_total - n_overlap

clean_data <- raw_data %>%
  filter(position != "catch", response == "correct")
remaining_trials <- nrow(clean_data)

cat("\n===== Trial counts =====\n")
cat("Total trials:                  ", total_trials,          "\n")
cat("Removed catch trials:          ", n_catch,               "\n")
cat("Removed incorrect (non-catch): ", n_incorrect_noncatch,  "\n")
cat("  …of which overlap with catch:", n_overlap,             "\n")
cat("Remaining trials after clean:  ", remaining_trials,      "\n\n")

# ──────────────────────────────────────────────────────────────────────────────
# 2a. PARTICIPANT-LEVEL ACCURACY FILTER (≥ 30 % incorrect) --------------------
# ──────────────────────────────────────────────────────────────────────────────

participant_accuracy <- raw_data %>%
  filter(position != "catch") %>%
  group_by(participant_ID) %>%
  summarise(
    total_trials     = n(),
    incorrect_trials = sum(response != "correct"),
    prop_incorrect   = incorrect_trials / total_trials,
    .groups          = "drop"
  )

excluded_participants <- participant_accuracy %>%
  filter(prop_incorrect >= 0.30) %>%
  pull(participant_ID)

cat("===== Participant accuracy filter (≥30% incorrect) =====\n")
cat("Participants excluded from ALL analyses: ", length(excluded_participants), "\n")
if (length(excluded_participants) > 0) {
  print(excluded_participants)
}
cat("\n")

analysis_data <- clean_data %>%
  filter(!participant_ID %in% excluded_participants)

# Count trials after participant exclusion
n_trials_after_exclusion <- nrow(analysis_data)
cat("Trials after participant exclusion:   ", n_trials_after_exclusion, "\n\n")

# Total removed and pct of original
n_removed_trials <- total_trials - n_trials_after_exclusion
pct_removed     <- n_removed_trials / total_trials * 100
cat(
  "Total removed trials:                ",
  n_removed_trials,
  sprintf("(%.1f%% of total trials)", pct_removed),
  "\n\n"
)

# ──────────────────────────────────────────────────────────────────────────────
# 3. WINSORISING RTs (±2 SD within participant) ------------------------------
# ──────────────────────────────────────────────────────────────────────────────

winsor_data <- analysis_data %>%
  group_by(participant_ID) %>%
  mutate(
    mu    = mean(rt, na.rm = TRUE),
    sd_v  = sd(rt,  na.rm = TRUE),
    lower = mu - 2 * sd_v,
    upper = mu + 2 * sd_v,
    rt    = pmin(pmax(rt, lower), upper)
  ) %>%
  ungroup() %>%
  select(-mu, -sd_v, -lower, -upper)

n_winsor <- sum(winsor_data$rt != analysis_data$rt)
cat("Winsorising: ", n_winsor, " RTs were clamped to ±2 SD limits\n\n")

pct_winsor <- n_winsor / nrow(winsor_data) * 100
cat("Percentage of trials winsorised:  ", sprintf("%.1f%%", pct_winsor), "\n\n")

analysis_data <- winsor_data

# ──────────────────────────────────────────────────────────────────────────────
# 4. DESCRIPTIVE STATISTICS (weighted means) ----------------------------------
# ──────────────────────────────────────────────────────────────────────────────

# 4.1 Compute per‐participant cell means and trial counts
pp_cell_stats <- analysis_data %>%
  group_by(participant_ID, position, phase) %>%
  summarise(
    n_trials = n(),
    mean_rt  = mean(rt, na.rm = TRUE),
    .groups   = "drop"
  )

# 4.2 Compute weighted descriptives across participants
cell_desc <- pp_cell_stats %>%
  group_by(position, phase) %>%
  summarise(
    n_ppt   = n(),                       # number of participants in cell
    total_n = sum(n_trials),             # total trials in cell (for weights)
    wmean   = sum(n_trials * mean_rt) / total_n,
    wvar    = sum(n_trials * (mean_rt - wmean)^2) / total_n,
    sd_rt   = sqrt(wvar),
    se_rt   = sd_rt / sqrt(n_ppt),       # SE based on participants
    t_crit  = qt(0.975, df = n_ppt - 1),
    ci_low  = wmean - t_crit * se_rt,
    ci_high = wmean + t_crit * se_rt,
    .groups = "drop"
  ) %>%
  select(
    position,
    phase,
    sd_rt,
    mean_rt = wmean,
    n       = n_ppt,
    se_rt,
    ci_low,
    ci_high
  )

cat("===== Descriptive statistics (Position × Phase | weighted mean, between-ppt CI) =====\n")
print(cell_desc)
cat("\n")

output_dir <- "C:/Users/amnesia/Desktop/RespCycles_VisuoSpatialAttention_v1_21-05-2025/Experiment2/data/merged/combined"
write_csv(cell_desc, file.path(output_dir, "cell_desc.csv"))

# ──────────────────────────────────────────────────────────────────────────────
# 5. REPEATED‐MEASURES ANOVAs WITH COHEN’S dz (no duplicated prints) ----------
# ──────────────────────────────────────────────────────────────────────────────

library(afex)    # for aov_ez
library(emmeans) # for emmeans, pairs

# report partial η² globally
afex_options(type   = 3,
             es_aov = "pes")

# helper to append dz and print a single table
print_with_dz <- function(emobj, desc) {
  df <- as.data.frame(emobj)
  df$dz <- df$t.ratio / sqrt(df$df + 1)
  cat(desc, "\n")
  print(df)
  cat("\n")
}

# ──────────────────────────────────────────────────────────────────────────────
# 4. REPEATED‐MEASURES ANOVAs WITH COHEN’S dz (no duplicated prints) ----------
# ──────────────────────────────────────────────────────────────────────────────

library(afex)    # for aov_ez
library(emmeans) # for emmeans, pairs

# report partial η² globally
afex_options(type   = 3,
             es_aov = "pes")

# helper to append dz and print a single table
print_with_dz <- function(emobj, desc) {
  df <- as.data.frame(emobj)
  df$dz <- df$t.ratio / sqrt(df$df + 1)
  cat(desc, "\n")
  print(df)
  cat("\n")
}

## 4.0 Orientation (Horizontal vs Vertical) × Validity ------------------------

ov_data <- analysis_data %>%
  filter(position %in% c("left", "right", "up", "down")) %>%
  mutate(
    orientation = factor(
      ifelse(position %in% c("left", "right"), "horizontal", "vertical"),
      levels = c("horizontal", "vertical")
    ),
    validity = factor(validity, levels = c("valid", "invalid"))
  )

anova_ov <- aov_ez(
  id            = "participant_ID",
  dv            = "rt",
  within        = c("orientation", "validity"),
  data          = ov_data,
  include_aov   = TRUE,
  fun_aggregate = mean,
  anova_table   = list(es = "pes")
)
cat("===== ANOVA: Orientation (Horizontal vs Vertical) × Validity (pes) =====\n")
print(anova_ov); cat("\n")

print_with_dz(
  pairs(emmeans(anova_ov, ~ orientation | validity), adjust = "bonferroni"),
  "=== Orientation | Validity (w/ dz) ==="
)
print_with_dz(
  pairs(emmeans(anova_ov, ~ validity | orientation), adjust = "bonferroni"),
  "=== Validity | Orientation (w/ dz) ==="
)
print_with_dz(
  pairs(emmeans(anova_ov, ~ orientation * validity), adjust = "bonferroni"),
  "=== Interaction (Orientation × Validity) w/ dz ==="
)


## 4.1 Left/Right × Inhale/Exhale ---------------------------------------------

lr_data <- analysis_data %>%
  filter(position %in% c("left", "right")) %>%
  mutate(
    position = factor(position, levels = c("left", "right")),
    phase    = factor(phase,    levels = c("inhale", "exhale"))
  )

anova_lr <- aov_ez(
  id            = "participant_ID",
  dv            = "rt",
  within        = c("position", "phase"),
  data          = lr_data,
  include_aov   = TRUE,
  fun_aggregate = mean,
  anova_table   = list(es = "pes")
)
cat("===== ANOVA: Left/Right × Inhale/Exhale (pes) =====\n")
print(anova_lr); cat("\n")

print_with_dz(
  pairs(emmeans(anova_lr, ~ position | phase), adjust = "bonferroni"),
  "=== LR: Position | Phase (w/ dz) ==="
)
print_with_dz(
  pairs(emmeans(anova_lr, ~ phase | position), adjust = "bonferroni"),
  "=== LR: Phase | Position (w/ dz) ==="
)
print_with_dz(
  pairs(emmeans(anova_lr, ~ position * phase), adjust = "bonferroni"),
  "=== LR: Interaction (w/ dz) ==="
)


### 4.1a Left/Right × Phase — Valid cues only --------------------------------

lr_valid <- lr_data %>% filter(validity == "valid")

anova_lr_valid <- aov_ez(
  id            = "participant_ID",
  dv            = "rt",
  within        = c("position", "phase"),
  data          = lr_valid,
  include_aov   = TRUE,
  fun_aggregate = mean,
  anova_table   = list(es = "pes")
)
cat("===== ANOVA (LR × Phase) — Valid (pes) =====\n")
print(anova_lr_valid); cat("\n")

print_with_dz(
  pairs(emmeans(anova_lr_valid, ~ position | phase), adjust = "bonferroni"),
  "=== LR Valid: Position | Phase (w/ dz) ==="
)
print_with_dz(
  pairs(emmeans(anova_lr_valid, ~ phase | position), adjust = "bonferroni"),
  "=== LR Valid: Phase | Position (w/ dz) ==="
)
print_with_dz(
  pairs(emmeans(anova_lr_valid, ~ position * phase), adjust = "bonferroni"),
  "=== LR Valid: Interaction (w/ dz) ==="
)


### 4.1b Left/Right × Phase — Invalid cues only ------------------------------

lr_invalid <- lr_data %>% filter(validity == "invalid")

anova_lr_invalid <- aov_ez(
  id            = "participant_ID",
  dv            = "rt",
  within        = c("position", "phase"),
  data          = lr_invalid,
  include_aov   = TRUE,
  fun_aggregate = mean,
  anova_table   = list(es = "pes")
)
cat("===== ANOVA (LR × Phase) — Invalid (pes) =====\n")
print(anova_lr_invalid); cat("\n")

print_with_dz(
  pairs(emmeans(anova_lr_invalid, ~ position | phase), adjust = "bonferroni"),
  "=== LR Invalid: Position | Phase (w/ dz) ==="
)
print_with_dz(
  pairs(emmeans(anova_lr_invalid, ~ phase | position), adjust = "bonferroni"),
  "=== LR Invalid: Phase | Position (w/ dz) ==="
)
print_with_dz(
  pairs(emmeans(anova_lr_invalid, ~ position * phase), adjust = "bonferroni"),
  "=== LR Invalid: Interaction (w/ dz) ==="
)


### 4.1c Left/Right × Phase — Difference (Invalid − Valid) --------------------

lr_diff <- analysis_data %>%
  filter(position %in% c("left", "right")) %>%
  group_by(participant_ID, position, phase, validity) %>%
  summarise(mean_rt = mean(rt, na.rm = TRUE), .groups = "drop") %>%
  pivot_wider(names_from = validity, values_from = mean_rt) %>%
  mutate(diff = invalid - valid)

anova_lr_diff <- aov_ez(
  id            = "participant_ID",
  dv            = "diff",
  within        = c("position", "phase"),
  data          = lr_diff,
  include_aov   = TRUE,
  fun_aggregate = mean,
  anova_table   = list(es = "pes")
)
cat("===== ANOVA (LR diff) — Invalid minus Valid (pes) =====\n")
print(anova_lr_diff); cat("\n")

print_with_dz(
  pairs(emmeans(anova_lr_diff, ~ position | phase), adjust = "bonferroni"),
  "=== LR Diff: Position | Phase (w/ dz) ==="
)
print_with_dz(
  pairs(emmeans(anova_lr_diff, ~ phase | position), adjust = "bonferroni"),
  "=== LR Diff: Phase | Position (w/ dz) ==="
)
print_with_dz(
  pairs(emmeans(anova_lr_diff, ~ position * phase), adjust = "bonferroni"),
  "=== LR Diff: Interaction (w/ dz) ==="
)


## 4.2 Up/Down × Inhale/Exhale -----------------------------------------------

ud_data <- analysis_data %>%
  filter(position %in% c("up", "down")) %>%
  mutate(
    position = factor(position, levels = c("up", "down")),
    phase    = factor(phase,    levels = c("inhale", "exhale"))
  )

anova_ud <- aov_ez(
  id            = "participant_ID",
  dv            = "rt",
  within        = c("position", "phase"),
  data          = ud_data,
  include_aov   = TRUE,
  fun_aggregate = mean,
  anova_table   = list(es = "pes")
)
cat("===== ANOVA: Up/Down × Inhale/Exhale (pes) =====\n")
print(anova_ud); cat("\n")

print_with_dz(
  pairs(emmeans(anova_ud, ~ position | phase), adjust = "bonferroni"),
  "=== UD: Position | Phase (w/ dz) ==="
)
print_with_dz(
  pairs(emmeans(anova_ud, ~ phase | position), adjust = "bonferroni"),
  "=== UD: Phase | Position (w/ dz) ==="
)
print_with_dz(
  pairs(emmeans(anova_ud, ~ position * phase), adjust = "bonferroni"),
  "=== UD: Interaction (w/ dz) ==="
)


### 4.2a Up/Down × Phase — Valid cues only -----------------------------------

ud_valid <- ud_data %>% filter(validity == "valid")

anova_ud_valid <- aov_ez(
  id            = "participant_ID",
  dv            = "rt",
  within        = c("position", "phase"),
  data          = ud_valid,
  include_aov   = TRUE,
  fun_aggregate = mean,
  anova_table   = list(es = "pes")
)
cat("===== ANOVA (UD × Phase) — Valid (pes) =====\n")
print(anova_ud_valid); cat("\n")

print_with_dz(
  pairs(emmeans(anova_ud_valid, ~ position | phase), adjust = "bonferroni"),
  "=== UD Valid: Position | Phase (w/ dz) ==="
)
print_with_dz(
  pairs(emmeans(anova_ud_valid, ~ phase | position), adjust = "bonferroni"),
  "=== UD Valid: Phase | Position (w/ dz) ==="
)
print_with_dz(
  pairs(emmeans(anova_ud_valid, ~ position * phase), adjust = "bonferroni"),
  "=== UD Valid: Interaction (w/ dz) ==="
)


### 4.2b Up/Down × Phase — Invalid cues only ---------------------------------

ud_invalid <- ud_data %>% filter(validity == "invalid")

anova_ud_invalid <- aov_ez(
  id            = "participant_ID",
  dv            = "rt",
  within        = c("position", "phase"),
  data          = ud_invalid,
  include_aov   = TRUE,
  fun_aggregate = mean,
  anova_table   = list(es = "pes")
)
cat("===== ANOVA (UD × Phase) — Invalid (pes) =====\n")
print(anova_ud_invalid); cat("\n")

print_with_dz(
  pairs(emmeans(anova_ud_invalid, ~ position | phase), adjust = "bonferroni"),
  "=== UD Invalid: Position | Phase (w/ dz) ==="
)
print_with_dz(
  pairs(emmeans(anova_ud_invalid, ~ phase | position), adjust = "bonferroni"),
  "=== UD Invalid: Phase | Position (w/ dz) ==="
)
print_with_dz(
  pairs(emmeans(anova_ud_invalid, ~ position * phase), adjust = "bonferroni"),
  "=== UD Invalid: Interaction (w/ dz) ==="
)


### 4.2c Up/Down × Phase — Difference (Invalid − Valid) ----------------------

ud_diff <- analysis_data %>%
  filter(position %in% c("up", "down")) %>%
  group_by(participant_ID, position, phase, validity) %>%
  summarise(mean_rt = mean(rt, na.rm = TRUE), .groups = "drop") %>%
  pivot_wider(names_from = validity, values_from = mean_rt) %>%
  mutate(diff = invalid - valid)

anova_ud_diff <- aov_ez(
  id            = "participant_ID",
  dv            = "diff",
  within        = c("position", "phase"),
  data          = ud_diff,
  include_aov   = TRUE,
  fun_aggregate = mean,
  anova_table   = list(es = "pes")
)
cat("===== ANOVA (UD diff) — Invalid minus Valid (pes) =====\n")
print(anova_ud_diff); cat("\n")

print_with_dz(
  pairs(emmeans(anova_ud_diff, ~ position | phase), adjust = "bonferroni"),
  "=== UD Diff: Position | Phase (w/ dz) ==="
)
print_with_dz(
  pairs(emmeans(anova_ud_diff, ~ phase | position), adjust = "bonferroni"),
  "=== UD Diff: Phase | Position (w/ dz) ==="
)
print_with_dz(
  pairs(emmeans(anova_ud_diff, ~ position * phase), adjust = "bonferroni"),
  "=== UD Diff: Interaction (w/ dz) ==="
)

# ──────────────────────────────────────────────────────────────────────────────
# CREATE RESULTS DIRECTORY ----------------------------------------------------
# ──────────────────────────────────────────────────────────────────────────────

results_dir <- "C:/Users/amnesia/Desktop/RespCycles_VisuoSpatialAttention_v1_21-05-2025/Experiment2/results/tables"
if (!dir.exists(results_dir)) {
  dir.create(results_dir, recursive = TRUE)
}


# ──────────────────────────────────────────────────────────────────────────────
# 4.0 Orientation × Validity --------------------------------------------------
# ──────────────────────────────────────────────────────────────────────────────

# (re-compute the pairs so we can save them)
ov_ps_orient_by_valid <- pairs(emmeans(anova_ov, ~ orientation | validity), adjust = "bonferroni")
ov_ps_valid_by_orient <- pairs(emmeans(anova_ov, ~ validity | orientation), adjust = "bonferroni")
ov_ps_interaction    <- pairs(emmeans(anova_ov, ~ orientation * validity), adjust = "bonferroni")

# write omnibus ANOVA
readr::write_csv(
  as.data.frame(anova_ov$anova_table),
  file.path(results_dir, "01_OV_anova.csv")
)

# write pairwise tables
readr::write_csv(
  as.data.frame(ov_ps_orient_by_valid),
  file.path(results_dir, "02_OV_simpleEffect_Orientation_by_Validity.csv")
)
readr::write_csv(
  as.data.frame(ov_ps_valid_by_orient),
  file.path(results_dir, "03_OV_simpleEffect_Validity_by_Orientation.csv")
)
readr::write_csv(
  as.data.frame(ov_ps_interaction),
  file.path(results_dir, "04_OV_interaction.csv")
)


# ──────────────────────────────────────────────────────────────────────────────
# 4.1 Left/Right × Inhale/Exhale ----------------------------------------------
# ──────────────────────────────────────────────────────────────────────────────

lr_ps_position_by_phase  <- pairs(emmeans(anova_lr, ~ position | phase), adjust = "bonferroni")
lr_ps_phase_by_position  <- pairs(emmeans(anova_lr, ~ phase | position), adjust = "bonferroni")
lr_ps_interaction        <- pairs(emmeans(anova_lr, ~ position * phase), adjust = "bonferroni")

readr::write_csv(
  as.data.frame(anova_lr$anova_table),
  file.path(results_dir, "05_LR_anova.csv")
)
readr::write_csv(
  as.data.frame(lr_ps_position_by_phase),
  file.path(results_dir, "06_LR_simpleEffect_Position_by_Phase.csv")
)
readr::write_csv(
  as.data.frame(lr_ps_phase_by_position),
  file.path(results_dir, "07_LR_simpleEffect_Phase_by_Position.csv")
)
readr::write_csv(
  as.data.frame(lr_ps_interaction),
  file.path(results_dir, "08_LR_interaction.csv")
)


# ──────────────────────────────────────────────────────────────────────────────
# 4.1a Left/Right × Phase — Valid only ----------------------------------------
# ──────────────────────────────────────────────────────────────────────────────

lr_valid_ps_position_by_phase <- pairs(emmeans(anova_lr_valid, ~ position | phase), adjust = "bonferroni")
lr_valid_ps_phase_by_position <- pairs(emmeans(anova_lr_valid, ~ phase | position), adjust = "bonferroni")
lr_valid_ps_interaction       <- pairs(emmeans(anova_lr_valid, ~ position * phase), adjust = "bonferroni")

readr::write_csv(
  as.data.frame(anova_lr_valid$anova_table),
  file.path(results_dir, "09_LR_valid_anova.csv")
)
readr::write_csv(
  as.data.frame(lr_valid_ps_position_by_phase),
  file.path(results_dir, "10_LR_valid_simpleEffect_Position_by_Phase.csv")
)
readr::write_csv(
  as.data.frame(lr_valid_ps_phase_by_position),
  file.path(results_dir, "11_LR_valid_simpleEffect_Phase_by_Position.csv")
)
readr::write_csv(
  as.data.frame(lr_valid_ps_interaction),
  file.path(results_dir, "12_LR_valid_interaction.csv")
)


# ──────────────────────────────────────────────────────────────────────────────
# 4.1b Left/Right × Phase — Invalid only --------------------------------------
# ──────────────────────────────────────────────────────────────────────────────

lr_invalid_ps_position_by_phase <- pairs(emmeans(anova_lr_invalid, ~ position | phase), adjust = "bonferroni")
lr_invalid_ps_phase_by_position <- pairs(emmeans(anova_lr_invalid, ~ phase | position), adjust = "bonferroni")
lr_invalid_ps_interaction       <- pairs(emmeans(anova_lr_invalid, ~ position * phase), adjust = "bonferroni")

readr::write_csv(
  as.data.frame(anova_lr_invalid$anova_table),
  file.path(results_dir, "13_LR_invalid_anova.csv")
)
readr::write_csv(
  as.data.frame(lr_invalid_ps_position_by_phase),
  file.path(results_dir, "14_LR_invalid_simpleEffect_Position_by_Phase.csv")
)
readr::write_csv(
  as.data.frame(lr_invalid_ps_phase_by_position),
  file.path(results_dir, "15_LR_invalid_simpleEffect_Phase_by_Position.csv")
)
readr::write_csv(
  as.data.frame(lr_invalid_ps_interaction),
  file.path(results_dir, "16_LR_invalid_interaction.csv")
)


# ──────────────────────────────────────────────────────────────────────────────
# 4.1c Left/Right × Phase — Difference (Invalid − Valid) ----------------------
# ──────────────────────────────────────────────────────────────────────────────

lr_diff_ps_position_by_phase <- pairs(emmeans(anova_lr_diff, ~ position | phase), adjust = "bonferroni")
lr_diff_ps_phase_by_position <- pairs(emmeans(anova_lr_diff, ~ phase | position), adjust = "bonferroni")
lr_diff_ps_interaction       <- pairs(emmeans(anova_lr_diff, ~ position * phase), adjust = "bonferroni")

readr::write_csv(
  as.data.frame(anova_lr_diff$anova_table),
  file.path(results_dir, "17_LR_diff_anova.csv")
)
readr::write_csv(
  as.data.frame(lr_diff_ps_position_by_phase),
  file.path(results_dir, "18_LR_diff_simpleEffect_Position_by_Phase.csv")
)
readr::write_csv(
  as.data.frame(lr_diff_ps_phase_by_position),
  file.path(results_dir, "19_LR_diff_simpleEffect_Phase_by_Position.csv")
)
readr::write_csv(
  as.data.frame(lr_diff_ps_interaction),
  file.path(results_dir, "20_LR_diff_interaction.csv")
)


# ──────────────────────────────────────────────────────────────────────────────
# 4.2 Up/Down × Inhale/Exhale -------------------------------------------------
# ──────────────────────────────────────────────────────────────────────────────

ud_ps_position_by_phase  <- pairs(emmeans(anova_ud, ~ position | phase), adjust = "bonferroni")
ud_ps_phase_by_position  <- pairs(emmeans(anova_ud, ~ phase | position), adjust = "bonferroni")
ud_ps_interaction        <- pairs(emmeans(anova_ud, ~ position * phase), adjust = "bonferroni")

readr::write_csv(
  as.data.frame(anova_ud$anova_table),
  file.path(results_dir, "21_UD_anova.csv")
)
readr::write_csv(
  as.data.frame(ud_ps_position_by_phase),
  file.path(results_dir, "22_UD_simpleEffect_Position_by_Phase.csv")
)
readr::write_csv(
  as.data.frame(ud_ps_phase_by_position),
  file.path(results_dir, "23_UD_simpleEffect_Phase_by_Position.csv")
)
readr::write_csv(
  as.data.frame(ud_ps_interaction),
  file.path(results_dir, "24_UD_interaction.csv")
)


# ──────────────────────────────────────────────────────────────────────────────
# 4.2a Up/Down × Phase — Valid only -------------------------------------------
# ──────────────────────────────────────────────────────────────────────────────

ud_valid_ps_position_by_phase <- pairs(emmeans(anova_ud_valid, ~ position | phase), adjust = "bonferroni")
ud_valid_ps_phase_by_position <- pairs(emmeans(anova_ud_valid, ~ phase | position), adjust = "bonferroni")
ud_valid_ps_interaction       <- pairs(emmeans(anova_ud_valid, ~ position * phase), adjust = "bonferroni")

readr::write_csv(
  as.data.frame(anova_ud_valid$anova_table),
  file.path(results_dir, "25_UD_valid_anova.csv")
)
readr::write_csv(
  as.data.frame(ud_valid_ps_position_by_phase),
  file.path(results_dir, "26_UD_valid_simpleEffect_Position_by_Phase.csv")
)
readr::write_csv(
  as.data.frame(ud_valid_ps_phase_by_position),
  file.path(results_dir, "27_UD_valid_simpleEffect_Phase_by_Position.csv")
)
readr::write_csv(
  as.data.frame(ud_valid_ps_interaction),
  file.path(results_dir, "28_UD_valid_interaction.csv")
)


# ──────────────────────────────────────────────────────────────────────────────
# 4.2b Up/Down × Phase — Invalid only -----------------------------------------
# ──────────────────────────────────────────────────────────────────────────────

ud_invalid_ps_position_by_phase <- pairs(emmeans(anova_ud_invalid, ~ position | phase), adjust = "bonferroni")
ud_invalid_ps_phase_by_position <- pairs(emmeans(anova_ud_invalid, ~ phase | position), adjust = "bonferroni")
ud_invalid_ps_interaction       <- pairs(emmeans(anova_ud_invalid, ~ position * phase), adjust = "bonferroni")

readr::write_csv(
  as.data.frame(anova_ud_invalid$anova_table),
  file.path(results_dir, "29_UD_invalid_anova.csv")
)
readr::write_csv(
  as.data.frame(ud_invalid_ps_position_by_phase),
  file.path(results_dir, "30_UD_invalid_simpleEffect_Position_by_Phase.csv")
)
readr::write_csv(
  as.data.frame(ud_invalid_ps_phase_by_position),
  file.path(results_dir, "31_UD_invalid_simpleEffect_Phase_by_Position.csv")
)
readr::write_csv(
  as.data.frame(ud_invalid_ps_interaction),
  file.path(results_dir, "32_UD_invalid_interaction.csv")
)


# ──────────────────────────────────────────────────────────────────────────────
# 4.2c Up/Down × Phase — Difference (Invalid − Valid) -------------------------
# ──────────────────────────────────────────────────────────────────────────────

ud_diff_ps_position_by_phase <- pairs(emmeans(anova_ud_diff, ~ position | phase), adjust = "bonferroni")
ud_diff_ps_phase_by_position <- pairs(emmeans(anova_ud_diff, ~ phase | position), adjust = "bonferroni")
ud_diff_ps_interaction       <- pairs(emmeans(anova_ud_diff, ~ position * phase), adjust = "bonferroni")

readr::write_csv(
  as.data.frame(anova_ud_diff$anova_table),
  file.path(results_dir, "33_UD_diff_anova.csv")
)
readr::write_csv(
  as.data.frame(ud_diff_ps_position_by_phase),
  file.path(results_dir, "34_UD_diff_simpleEffect_Position_by_Phase.csv")
)
readr::write_csv(
  as.data.frame(ud_diff_ps_phase_by_position),
  file.path(results_dir, "35_UD_diff_simpleEffect_Phase_by_Position.csv")
)
readr::write_csv(
  as.data.frame(ud_diff_ps_interaction),
  file.path(results_dir, "36_UD_diff_interaction.csv")
)

# ──────────────────────────────────────────────────────────────────────────────
# End of script ---------------------------------------------------------------
# ──────────────────────────────────────────────────────────────────────────────
