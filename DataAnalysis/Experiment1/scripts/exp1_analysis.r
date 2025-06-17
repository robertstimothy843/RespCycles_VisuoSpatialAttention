# Experiment 1 analysis script (weighted aggregation + post-hoc tests)
# Author: Timothy E. Roberts
# Description:
#   * Loads data from the specified absolute path
#   * Removes catch trials and incorrect responses (trial-level cleaning)
#   * Identifies participants with ≥ 30% incorrect responses (non-catch)
#     • Excludes them from all subsequent analyses
#   * Winsorises RTs (±2 SD within participant)
#   * Computes descriptive statistics with weighted aggregation
#   * Runs two 2×2 within-participant repeated-measures ANOVAs on the winsorised data:
#       1. Left/Right × Inhale/Exhale
#       2. Up/Down   × Inhale/Exhale
#   * Provides Bonferroni-adjusted pairwise comparisons for:
#       - Interaction contrasts (all position × phase combinations)
#       - Main effects of position and phase
#       - Simple effects of position at each phase and phase at each position

# ──────────────────────────────────────────────────────────────────────────────
# 1. SET-UP --------------------------------------------------------------------
# ──────────────────────────────────────────────────────────────────────────────

library(tidyverse)   # data wrangling
library(afex)        # repeated-measures ANOVA (aov_ez)
library(emmeans)     # post-hoc comparisons & estimated marginal means

# Use Type III sums of squares and report partial eta-squared (pes) instead of generalized (ges)
afex_options(
  type   = 3,    # Type III SS
  es_aov = "pes" # partial eta squared
)

# Path to data ----------------------------------------------------------------
raw_data <- read_csv(
  "C:/Users/amnesia/Desktop/RespCycles_VisuoSpatialAttention/DataAnalysis/Experiment1/data/merged/merged_data.csv",
  show_col_types = FALSE
)

# ──────────────────────────────────────────────────────────────────────────────
# 2. TRIAL-LEVEL CLEANING ------------------------------------------------------
# ──────────────────────────────────────────────────────────────────────────────

total_trials <- nrow(raw_data)

# Identify trial categories ---------------------------------------------------
catch_trials           <- raw_data %>% filter(position == "catch")
incorrect_trials_total <- raw_data %>% filter(response != "correct")
overlap_trials         <- raw_data %>% filter(position == "catch", response != "correct")

n_catch               <- nrow(catch_trials)
n_incorrect_total     <- nrow(incorrect_trials_total)
n_overlap             <- nrow(overlap_trials)
n_incorrect_noncatch  <- n_incorrect_total - n_overlap

# Keep only trials that are NOT catch and ARE correct
clean_data <- raw_data %>% 
  filter(position != "catch", response == "correct")

remaining_trials <- nrow(clean_data)

# Print a clear accounting ----------------------------------------------------
cat("\n===== Trial counts =====\n")
cat("Total trials:                  ", total_trials,          "\n")
cat("Removed catch trials:          ", n_catch,               "\n")
cat("Removed incorrect (non-catch): ", n_incorrect_noncatch,  "\n")
cat("  …of which overlap with catch:", n_overlap,             "\n")
cat("Remaining trials after clean:  ", remaining_trials,      "\n\n")

# ──────────────────────────────────────────────────────────────────────────────
# 2a. PARTICIPANT-LEVEL ACCURACY FILTER (≥ 30% incorrect) ---------------------
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

# Data set for ALL downstream analyses (trials + participant filter) ----------
analysis_data <- clean_data %>% 
  filter(!participant_ID %in% excluded_participants)

n_trials_after_exclusion <- nrow(analysis_data)
cat("Trials after participant exclusion:   ", n_trials_after_exclusion, "\n\n")

n_removed_trials <- total_trials - n_trials_after_exclusion
pct_removed     <- n_removed_trials / total_trials * 100
cat(
  "Total removed trials:                ",
  n_removed_trials,
  sprintf("(%.1f%% of total trials)", pct_removed),
  "\n\n"
)

# ──────────────────────────────────────────────────────────────────────────────
# 3. WINSORISING RTs (±2 SD within participant) -------------------------------
# ──────────────────────────────────────────────────────────────────────────────

winsor_data <- analysis_data %>% 
  group_by(participant_ID) %>% 
  mutate(
    mu    = mean(rt, na.rm = TRUE),
    sd_v  = sd(rt,   na.rm = TRUE),
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

# Replace analysis_data with the Winsorised version for all downstream steps
analysis_data <- winsor_data

# ──────────────────────────────────────────────────────────────────────────────
# 4. DESCRIPTIVE STATISTICS (WEIGHTED AGGREGATION) -----------------------------
# ──────────────────────────────────────────────────────────────────────────────

pp_cell_stats <- analysis_data %>% 
  group_by(participant_ID, position, phase) %>% 
  summarise(
    mean_rt  = mean(rt, na.rm = TRUE),
    n_trials = n(),
    .groups  = "drop"
  )

cell_desc <- pp_cell_stats %>% 
  group_by(position, phase) %>% 
  summarise(
    weighted_mean = weighted.mean(mean_rt, w = n_trials),
    w_total       = sum(n_trials),
    weighted_var  = sum(n_trials * (mean_rt - weighted_mean)^2) / w_total,
    sd_rt         = sqrt(weighted_var),
    n             = n(),
    se_rt         = sd_rt / sqrt(n),
    t_crit        = qt(0.975, df = n - 1),
    ci_low        = weighted_mean - t_crit * se_rt,
    ci_high       = weighted_mean + t_crit * se_rt,
    .groups       = "drop"
  ) %>% 
  select(position, phase, sd_rt, mean_rt = weighted_mean, n, se_rt, ci_low, ci_high)

cat("===== Descriptive statistics (weighted Position × Phase) =====\n")
print(cell_desc)
cat("\n")

readr::write_csv(
  cell_desc,
  file.path("C:/Users/amnesia/Desktop/RespCycles_VisuoSpatialAttention_v1_21-05-2025/DataAnalysis/Experiment1/data/merged", "cell_desc.csv")
)

# ──────────────────────────────────────────────────────────────────────────────
# Before running any analyses, define and create the results directory
# ──────────────────────────────────────────────────────────────────────────────

results_dir <- "C:/Users/amnesia/Desktop/RespCycles_VisuoSpatialAttention_v1_21-05-2025/DataAnalysis/Experiment1/results/tables"
if (!dir.exists(results_dir)) {
  dir.create(results_dir, recursive = TRUE)
}

# ──────────────────────────────────────────────────────────────────────────────
# 5. REPEATED-MEASURES ANOVAs WITH COHEN’S dz (no duplicated prints) ----------
# ──────────────────────────────────────────────────────────────────────────────

library(afex)    # for aov_ez
library(emmeans) # for emmeans, pairs

## 5.1 Left/Right × Inhale/Exhale ---------------------------------------------

lr_data <- analysis_data %>%
  filter(position %in% c("left", "right")) %>%
  mutate(
    position = factor(position, levels = c("left", "right")),
    phase    = factor(phase,    levels = c("inhale", "exhale"))
  )

# 1. Omnibus ANOVA (include aov for σ & df)
anova_lr <- aov_ez(
  id            = "participant_ID",
  dv            = "rt",
  within        = c("position", "phase"),
  data          = lr_data,
  include_aov   = TRUE,
  fun_aggregate = mean
)
cat("===== ANOVA: Left/Right × Inhale/Exhale =====\n")
print(anova_lr); cat("\n")

# Helper to append dz and print a single table
print_with_dz <- function(emobj, desc) {
  df <- as.data.frame(emobj)
  df$dz <- df$t.ratio / sqrt(df$df + 1)
  cat(desc, "\n")
  print(df)
  cat("\n")
}

# 2. Simple effects: Position | Phase
ps_lr_pos <- pairs(emmeans(anova_lr, ~ position | phase),
                   adjust = "bonferroni")
print_with_dz(ps_lr_pos, "=== Simple effects (Position | Phase) w/ dz ===")

# 3. Simple effects: Phase | Position
ps_lr_phase <- pairs(emmeans(anova_lr, ~ phase | position),
                     adjust = "bonferroni")
print_with_dz(ps_lr_phase, "=== Simple effects (Phase | Position) w/ dz ===")

# 4. Interaction contrasts
ps_lr_int <- pairs(emmeans(anova_lr, ~ position * phase),
                   adjust = "bonferroni")
print_with_dz(ps_lr_int, "=== Interaction contrasts (Position × Phase) w/ dz ===")


## 5.2 Up/Down × Inhale/Exhale ------------------------------------------------

ud_data <- analysis_data %>%
  filter(position %in% c("up", "down")) %>%
  mutate(
    position = factor(position, levels = c("up", "down")),
    phase    = factor(phase,    levels = c("inhale", "exhale"))
  )

# 1. Omnibus ANOVA
anova_ud <- aov_ez(
  id            = "participant_ID",
  dv            = "rt",
  within        = c("position", "phase"),
  data          = ud_data,
  include_aov   = TRUE,
  fun_aggregate = mean
)
cat("===== ANOVA: Up/Down × Inhale/Exhale =====\n")
print(anova_ud); cat("\n")

# 2. Simple effects: Position | Phase
ps_ud_pos <- pairs(emmeans(anova_ud, ~ position | phase),
                   adjust = "bonferroni")
print_with_dz(ps_ud_pos, "=== Simple effects (Position | Phase) w/ dz ===")

# 3. Simple effects: Phase | Position
ps_ud_phase <- pairs(emmeans(anova_ud, ~ phase | position),
                     adjust = "bonferroni")
print_with_dz(ps_ud_phase, "=== Simple effects (Phase | Position) w/ dz ===")

# 4. Interaction contrasts
ps_ud_int <- pairs(emmeans(anova_ud, ~ position * phase),
                   adjust = "bonferroni")
print_with_dz(ps_ud_int, "=== Interaction contrasts (Position × Phase) w/ dz ===")

# ──────────────────────────────────────────────────────────────────────────────
# 5.1 Left/Right × Inhale/Exhale ---------------------------------------------
# ──────────────────────────────────────────────────────────────────────────────

# … your existing anova_lr and print(anova_lr) calls …

# 1. Export Omnibus ANOVA table
lr_anova_tbl <- as.data.frame(anova_lr$anova_table)
readr::write_csv(
  lr_anova_tbl,
  file.path(results_dir, "01_LR_anova.csv")
)

# 2. Simple effects: Position | Phase
ps_lr_pos_df <- as.data.frame(ps_lr_pos)
readr::write_csv(
  ps_lr_pos_df,
  file.path(results_dir, "02_LR_simpleEffect_Position_by_Phase.csv")
)

# 3. Simple effects: Phase | Position
ps_lr_phase_df <- as.data.frame(ps_lr_phase)
readr::write_csv(
  ps_lr_phase_df,
  file.path(results_dir, "03_LR_simpleEffect_Phase_by_Position.csv")
)

# 4. Interaction contrasts
ps_lr_int_df <- as.data.frame(ps_lr_int)
readr::write_csv(
  ps_lr_int_df,
  file.path(results_dir, "04_LR_interactionContrasts.csv")
)


# ──────────────────────────────────────────────────────────────────────────────
# 5.2 Up/Down × Inhale/Exhale ------------------------------------------------
# ──────────────────────────────────────────────────────────────────────────────

# … your existing anova_ud and print(anova_ud) calls …

# 1. Export Omnibus ANOVA table
ud_anova_tbl <- as.data.frame(anova_ud$anova_table)
readr::write_csv(
  ud_anova_tbl,
  file.path(results_dir, "05_UD_anova.csv")
)

# 2. Simple effects: Position | Phase
ps_ud_pos_df <- as.data.frame(ps_ud_pos)
readr::write_csv(
  ps_ud_pos_df,
  file.path(results_dir, "06_UD_simpleEffect_Position_by_Phase.csv")
)

# 3. Simple effects: Phase | Position
ps_ud_phase_df <- as.data.frame(ps_ud_phase)
readr::write_csv(
  ps_ud_phase_df,
  file.path(results_dir, "07_UD_simpleEffect_Phase_by_Position.csv")
)

# 4. Interaction contrasts
ps_ud_int_df <- as.data.frame(ps_ud_int)
readr::write_csv(
  ps_ud_int_df,
  file.path(results_dir, "08_UD_interactionContrasts.csv")
)

# ──────────────────────────────────────────────────────────────────────────────
# End of script ---------------------------------------------------------------
# ──────────────────────────────────────────────────────────────────────────────
