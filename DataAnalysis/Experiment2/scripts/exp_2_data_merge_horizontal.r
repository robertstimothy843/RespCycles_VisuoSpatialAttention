# Load necessary libraries
library(dplyr)
library(readr)

# Directories
input_dir  <- "C:/Users/amnesia/Desktop/RespCycles_VisuoSpatialAttention_v1_21-05-2025/Experiment2/data/processed/horizontal"
output_dir <- "C:/Users/amnesia/Desktop/RespCycles_VisuoSpatialAttention_v1_21-05-2025/Experiment2/data/merged/horizontal"

# Ensure output directory exists
if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

# Get list of all “Pxxx_horizontal.csv” files in the input directory
file_list <- list.files(
  path        = input_dir,
  pattern     = "^P\\d+_horizontal\\.csv$",
  full.names  = TRUE
)

# Function to read each CSV and tag it with its participant ID
read_and_label <- function(file_path) {
  df <- read_csv(file_path, show_col_types = FALSE)
  participant_id <- gsub(".*(P\\d+)_horizontal\\.csv", "\\1", basename(file_path))
  df %>% mutate(Participant = participant_id)
}

# Read & merge
data_combined <- bind_rows(lapply(file_list, read_and_label))

# Write merged file
output_file <- file.path(output_dir, "merged_horizontal.csv")
write_csv(data_combined, output_file)

cat("Merged", length(file_list), "files into", output_file, "\n")
