RespCycles_VisuoSpatialAttention

This repository contains all experiment scripts, analysis code, and documentation for a research project investigating the influence of respiratory cycles on visuo-spatial attention. The core experiments were programmed in PsychoPy and include probe detection and Posner cueing tasks modulated by the breathing phase (inhalation vs. exhalation).

Repository Structure

    RespCycles_VisuoSpatialAttention/
        ├── DataAnalysis/                # R scripts and outputs for analysis
        │   ├── Experiment1/
        │   └── Experiment2/
        ├── EthicalApproval/            # Ethics documents
        ├── ExperimentScripts/          # Main PsychoPy experiment code
        │   ├── Experiment1/
        │   │   ├── List1/
        │   │   └── List2/
        │   └── Experiment2/
        │       ├── HorizontalAxis/
        │       └── VerticalAxis/
        ├── Manuscript/                 # Thesis drafts and related materials

Experiments
Experiment 1 — Target Detection Task

    Design: Participants detect a brief visual target presented in the upper or lower visual field while respiratory phase is recorded.

    Script locations:

        ExperimentScripts/Experiment1/List1/exp1_target_detection.psyexp

        ExperimentScripts/Experiment1/List2/exp1_target_detection.psyexp

    Outputs: Participant data saved in data/ subdirectories, in .csv format.

Experiment 2 — Exogenous Posner Cueing Task

    Design: Involves exogenous cues followed by targets, measuring attentional orienting effects during inhale/exhale phases.

    Script locations:

        ExperimentScripts/Experiment2/HorizontalAxis/posner_exog_new.psyexp

        ExperimentScripts/Experiment2/VerticalAxis/posner_exog_new.psyexp

Running the Experiments

    Install PsychoPy (2023.2+ recommended):
    https://www.psychopy.org/download.html

    Open the desired .psyexp file in PsychoPy Builder or Coder view.

    Ensure necessary hardware is connected, including:

        Breathing belt or respiration monitoring device

        High-refresh-rate monitor (recommended)

    Run experiment — data will be automatically saved in the relevant data/ folder.

Dependencies

    PsychoPy

    Python 3.8+

    CSV-compatible analysis software (e.g., R or Python for downstream processing)

Data Analysis

Analysis scripts and plots for both experiments are in the DataAnalysis/ folder.
See the individual README.md files in DataAnalysis/Experiment1/ and Experiment2/ for more.

Author & Contact

This project was developed as part of a master's thesis in psychology.
For questions or collaboration, please contact:

Timothy E. Roberts

Email: robertstimothy843@gmail.com

Affiliation: University of Hull
