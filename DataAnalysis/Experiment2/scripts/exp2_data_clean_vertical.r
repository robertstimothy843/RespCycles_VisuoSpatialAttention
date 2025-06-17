# Load necessary library
library(dplyr)

# Directories
input_dir  <- "C:/Users/amnesia/Desktop/RespCycles_VisuoSpatialAttention_v1_21-05-2025/Experiment2/data/raw/vertical"
output_dir <- "C:/Users/amnesia/Desktop/RespCycles_VisuoSpatialAttention_v1_21-05-2025/Experiment2/data/processed/vertical"

# Make sure output directory exists
if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

# List of participant IDs to process
participant_ids <- paste0("P", 101:160)

# Columns to remove in bulk
columns_to_remove <- c("key_resp.duration", "practice.thisRepN", "practice.thisTrialN", "practice.thisN", 
                       "practice.thisIndex", "block1.thisRepN", "block1.thisTrialN", "block1.thisN", 
                       "block1.thisIndex", "block2.thisRepN", "block2.thisTrialN", "block2.thisN", 
                       "block2.thisIndex", "thisRow.t", "notes", "instructions.started", "instructions_txt.started", 
                       "key_control.started", "instructions.stopped", "key_control.keys", "key_control.rt", 
                       "key_control.duration", "ready.started", "ready_txt.started", "ready_txt.stopped", 
                       "ready.stopped", "fix.started", "fixation.started", "key_control2.started", 
                       "fixation_cross.started", "fix.stopped", "practice.key_control2.keys", 
                       "practice.key_control2.rt", "practice.key_control2.duration", "cue.started", 
                       "cube.started", "fixation_cross_cue.started", "cue.stopped", "target.started", 
                       "fixation_target.started", "fixation_cross_target.started", "key_resp.started", 
                       "star.started", "target.stopped", "practice.key_resp.keys", "practice.key_resp.rt", 
                       "practice.key_resp.duration", "star.stopped", "fixation_target.stopped", 
                       "fixation_cross_target.stopped", "key_resp.stopped", "block1.key_control2.keys", 
                       "block1.key_control2.rt", "block1.key_control2.duration", "block1.key_resp.keys", 
                       "block1.key_resp.rt", "block1.key_resp.duration", "break_2.started", "text.started", 
                       "key_control3.started", "text.stopped", "break_2.stopped", "key_control3.keys", 
                       "key_control3.rt", "key_control3.duration", "block2.key_control2.keys", 
                       "block2.key_control2.rt", "block2.key_control2.duration", "block2.key_resp.keys", 
                       "block2.key_resp.rt", "block2.key_resp.duration", "participant", "session", 
                       "date", "expName", "psychopyVersion", "frameRate", "expStart", "key_control2.rt")

columns_to_remove_final <- c("cue_img", "cue_soa")

for (participant_id in participant_ids) {
  
  # Build file paths
  input_file  <- file.path(input_dir,  paste0(participant_id, "_vertical.csv"))
  output_file <- file.path(output_dir, paste0(participant_id, "_vertical.csv"))
  
  # Read data (skip if missing)
  if (!file.exists(input_file)) {
    warning("Skipping missing file: ", input_file)
    next
  }
  df <- read.csv(input_file, stringsAsFactors = FALSE)
  
  # 1) Drop unwanted columns
  df <- df %>% select(-one_of(columns_to_remove))
  
  # 2) Drop the first 13 rows
  df <- df[-(1:13), ]
  
  # 3) Drop rows 1, 62, 63 of the newly indexed data
  df <- df[-c(1, 62, 63), ]
  
  # 4) Keep only columns up to "key_resp.rt"
  if ("key_resp.rt" %in% names(df)) {
    df <- df %>% select(1:which(names(df) == "key_resp.rt"))
  }
  
  # 5) Drop final unwanted columns if present
  df <- df %>% select(-one_of(columns_to_remove_final))
  
  # 6) Add participant_ID as first column
  df <- df %>%
    mutate(participant_ID = participant_id) %>%
    select(participant_ID, everything())
  
  # 7) Rename and drop various columns
  if ("trial" %in% names(df))      df <- df %>% rename(validity = trial)
  if ("thisN" %in% names(df))       df <- df %>% select(-thisN)
  if ("key_control2.duration" %in% names(df)) 
                                    df <- df %>% select(-key_control2.duration)
  if ("key_control2.keys" %in% names(df)) {
    df <- df %>%
      rename(phase = key_control2.keys) %>%
      mutate(phase = recode(phase, down = "exhale", up = "inhale"))
  }
  
  # 8) Map target coordinates to labels
  if (all(c("target_x","target_y") %in% names(df))) {
    df <- df %>%
      mutate(
        target_x = case_when(
          target_x == 10    ~ "catch",
          target_x == -0.31 ~ "left",
          target_x == 0.31  ~ "right",
          TRUE              ~ as.character(target_x)
        ),
        target_y = case_when(
          target_y == 10    ~ "catch",
          target_y == -0.31 ~ "down",
          target_y == 0.31  ~ "up",
          TRUE              ~ as.character(target_y)
        )
      )
  }
  
  # 9) Trial and response transformations
  if ("thisRepN" %in% names(df))     df <- df %>% select(-thisRepN)
  if ("thisTrialN" %in% names(df))   df <- df %>% rename(trial = thisTrialN)
  
  if ("key_resp.keys" %in% names(df) && "validity" %in% names(df)) {
    df <- df %>%
      mutate(
        key_resp.keys = case_when(
          validity == "catch" & key_resp.keys == "None"       ~ "correct",
          validity == "catch" & key_resp.keys == "space"      ~ "incorrect",
          validity %in% c("valid", "invalid") & key_resp.keys == "space" ~ "correct",
          validity %in% c("valid", "invalid") & key_resp.keys != "space" ~ "incorrect",
          TRUE ~ key_resp.keys
        )
      ) %>%
      rename(response = key_resp.keys)
  }
  
  # 10) Rename rt
  if ("key_resp.rt" %in% names(df)) 
    df <- df %>% rename(rt = key_resp.rt)
  
  # Write out cleaned file
  write.csv(df, output_file, row.names = FALSE)
  message("Processed ", participant_id, " → ", output_file)
}
