library(dplyr)
library(readr)

# Set the directories
data_dir        <- "C:/Users/amnesia/Desktop/RespCycles_VisuoSpatialAttention_v1_21-05-2025/Experiment1/data/processed"
merged_dir      <- "C:/Users/amnesia/Desktop/RespCycles_VisuoSpatialAttention_v1_21-05-2025/Experiment1/data/merged"

# Create the merged output directory if needed
if (!dir.exists(merged_dir)) {
  dir.create(merged_dir, recursive = TRUE)
}

# List all clean CSV files matching P##_experiment_1_clean.csv
file_list <- list.files(
  path       = data_dir,
  pattern    = "^P[0-9]+_experiment_1_clean\\.csv$",
  full.names = TRUE
)

# Function to read each CSV without adding a Participant ID
read_file <- function(file_path) {
  read_csv(file_path, show_col_types = FALSE)
}

# Read and merge all files into one data frame
data_combined <- lapply(file_list, read_file) %>% bind_rows()

# Save the merged dataset unmodified into the new merged folder
output_file <- file.path(merged_dir, "merged_data.csv")
write_csv(data_combined, output_file)

cat("Merged", nrow(data_combined), "rows into", output_file, "\n")
