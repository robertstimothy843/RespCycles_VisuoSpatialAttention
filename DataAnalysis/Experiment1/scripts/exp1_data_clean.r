# Load necessary libraries
library(dplyr)

# Define the directories
data_dir   <- "C:/Users/amnesia/Desktop/RespCycles_VisuoSpatialAttention_v1_21-05-2025/Experiment1/data/raw"
output_dir <- "C:/Users/amnesia/Desktop/RespCycles_VisuoSpatialAttention_v1_21-05-2025/Experiment1/data/processed"

# Create the output directory if it doesn't exist
if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

# List of participant IDs (P101 to P140), rename all the raw files to P101.csv, P102.csv, etc. then run the script
participant_ids <- paste0("P", 101:140)

# Columns to remove
columns_to_remove <- c(
  "key_resp.duration", "practice.thisRepN", "practice.thisTrialN", "practice.thisN",
  "practice.thisIndex", "session_1.thisRepN", "session_1.thisTrialN", "session_1.thisN",
  "session_1.thisIndex", "session_2.thisRepN", "session_2.thisTrialN", "session_2.thisN",
  "session_2.thisIndex", "thisRow.t", "notes", "instructions.started", "instructions_txt.started",
  "key_control.started", "instructions.stopped", "key_control.keys", "key_control.rt",
  "key_control.duration", "ready.started", "ready_txt.started", "ready.stopped",
  "fix.started", "fixation_cross.started", "key_control2.started", "fix.stopped",
  "practice.key_control2.keys", "practice.key_control2.rt", "practice.key_control2.duration",
  "target.started", "star.started", "fixation_cross_target.started", "key_resp.started",
  "star.stopped", "target.stopped", "practice.key_resp.keys", "practice.key_resp.rt",
  "practice.key_resp.duration", "session_1.key_control2.keys", "session_1.key_control2.rt",
  "session_1.key_control2.duration", "session_1.key_resp.keys", "session_1.key_resp.rt",
  "session_1.key_resp.duration", "break_2.started", "text.started", "key_control3.started",
  "break_2.stopped", "key_control3.keys", "session_2.key_control2.keys", "session_2.key_control2.rt",
  "session_2.key_control2.duration", "session_2.key_resp.keys", "session_2.key_resp.rt",
  "session_2.key_resp.duration", "participant", "session", "date", "expName", "psychopyVersion",
  "frameRate", "expStart", "key_control2.rt"
)

# Direction labels
directions <- c("up", "down", "left", "right", "catch")

# Process each participant file
for (participant_id in participant_ids) {
  # Construct file paths
  input_file  <- file.path(data_dir, paste0(participant_id, ".csv"))
  output_file <- file.path(output_dir, paste0(participant_id, "_experiment_1_clean.csv"))
  
  # Check existence and read
  if (!file.exists(input_file)) {
    warning("Input file not found: ", input_file)
    next
  }
  df <- read.csv(input_file, stringsAsFactors = FALSE)
  
  # 1) Remove unwanted columns
  df_cleaned <- df %>% select(-one_of(intersect(names(df), columns_to_remove)))
  
  # 2) Strip practice rows (first 13)
  df_cleaned <- df_cleaned[-(1:13), ]
  
  # 3) Keep columns up to key_resp.rt
  if ("key_resp.rt" %in% names(df_cleaned)) {
    last_rt <- which(names(df_cleaned) == "key_resp.rt")
    df_cleaned <- df_cleaned %>% select(1:last_rt)
  }
  
  # 4) Drop final unwanted columns (cue_img, cue_soa)
  df_cleaned <- df_cleaned %>%
    select(-one_of(intersect(names(df_cleaned), c("cue_img", "cue_soa"))))
  
  # 5) Add participant_ID as first column
  df_cleaned <- df_cleaned %>%
    mutate(participant_ID = participant_id) %>%
    select(participant_ID, everything())
  
  # 6) Rename and recode phase
  df_cleaned <- df_cleaned %>%
    rename(phase = key_control2.keys) %>%
    mutate(phase = recode(phase, down = "exhale", up = "inhale"))
  
  # 7) Use global trial index and drop block-local indices
  df_cleaned <- df_cleaned %>%
    rename(trial = thisN) %>%
    select(-thisTrialN, -thisRepN)
  
  # 8) Remove blank separator rows (where trial is NA)
  df_cleaned <- df_cleaned %>% filter(!is.na(trial))
  
  # 9) Recode target_x / target_y into direction labels, merge into 'position'
  df_cleaned <- df_cleaned %>% mutate(
    target_x = case_when(
      target_x == 10    ~ "catch",
      target_x == -0.31 ~ "left",
      target_x == 0.31  ~ "right",
      TRUE               ~ as.character(target_x)
    ),
    target_y = case_when(
      target_y == 10    ~ "catch",
      target_y == -0.31 ~ "down",
      target_y == 0.31  ~ "up",
      TRUE               ~ as.character(target_y)
    ),
    position = if_else(target_x %in% directions, target_x, target_y)
  ) %>%
    select(-target_x, -target_y)
  
  # 10) Recode responses to 'correct'/'incorrect'
  if ("key_resp.keys" %in% names(df_cleaned)) {
    df_cleaned <- df_cleaned %>%
      mutate(response = case_when(
        position == "catch" & key_resp.keys == "None"       ~ "correct",
        position == "catch" & key_resp.keys == "space"      ~ "incorrect",
        position %in% directions & key_resp.keys == "space" ~ "correct",
        position %in% directions & key_resp.keys != "space" ~ "incorrect",
        TRUE                                                 ~ as.character(key_resp.keys)
      )) %>%
      select(-key_resp.keys)
  }
  
  # 11) Rename RT column
  df_cleaned <- df_cleaned %>% rename(rt = key_resp.rt)
  
  # 12) Final column ordering
  df_cleaned <- df_cleaned %>%
    select(participant_ID, position, trial, phase, response, rt)
  
  # Save cleaned data
  write.csv(df_cleaned, output_file, row.names = FALSE)
  message("Saved cleaned data for ", participant_id)
}

cat("Batch processing complete.\n")
