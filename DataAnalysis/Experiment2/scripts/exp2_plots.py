import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------------- File paths ------------------------
input_path = "C:/Users/amnesia/Desktop/RespCycles_VisuoSpatialAttention_v1_21-05-2025/Experiment2/data/merged/combined/cell_desc.csv"
output_dir  = "C:/Users/amnesia/Desktop/RespCycles_VisuoSpatialAttention_v1_21-05-2025/Experiment2/results/figures"
os.makedirs(output_dir, exist_ok=True)

# ---------------- Read descriptive stats ---------------------
df = pd.read_csv(input_path)
# Convert seconds → milliseconds
df["mean_ms"] = df["mean_rt"] * 1000
df["se_ms"]   = df["se_rt"] * 1000

# ---------------- Generic plotting function ---------------------
def make_plot(df_sub, positions, fname):
    # Match matplotlib defaults
    LABEL_FS        = 12
    TICK_FS         = 12
    LEGEND_FS       = 10
    LEGEND_TITLE_FS = 10

    bar_width = 0.35
    colors    = ["#666666", "#BBBBBB"]
    x         = np.arange(len(positions))

    fig, ax = plt.subplots(figsize=(7,5))
    for i, phase in enumerate(["exhale", "inhale"]):
        subset = (
            df_sub[df_sub["phase"] == phase]
            .set_index("position")
            .loc[positions]
            .reset_index()
        )
        ci_hw = subset["se_ms"] * 1.96

        ax.bar(
            x + (i - 0.5) * bar_width,
            subset["mean_ms"],
            bar_width,
            yerr=ci_hw,
            capsize=5,
            color=colors[i],
            edgecolor="black",
            error_kw={"elinewidth":1, "linestyle":"dashed", "capthick":1},
            label=phase.capitalize(),
            alpha=0.9,
        )

    # ---------------- Styling ------------------------
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.set_xlabel("Target Position", fontsize=LABEL_FS)
    ax.set_ylabel("Reaction Time (ms)", fontsize=LABEL_FS)

    ax.set_xticks(x)
    ax.set_xticklabels([p.capitalize() for p in positions], fontsize=TICK_FS)
    ax.set_ylim(310, 470)
    ax.set_yticks(np.arange(310, 471, 20))
    ax.set_yticklabels(np.arange(310, 471, 20).astype(int), fontsize=TICK_FS)

    ax.legend(
        title="Phase",
        title_fontsize=LEGEND_TITLE_FS,
        fontsize=LEGEND_FS,
        loc="upper right",
        bbox_to_anchor=(1.15,1),
        frameon=True
    )

    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")
    plt.grid(False)
    plt.tight_layout()

    # ---------------- Save and return path ------------------------
    out_path = os.path.join(output_dir, fname)
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.show()
    plt.close(fig)
    return out_path

# ---------------- Plot 1: Left / Right -----------------------
file_lr = make_plot(
    df[df["position"].isin(["left", "right"])],
    ["left", "right"],
    "exp2_left_right.png"
)

# ---------------- Plot 2: Up / Down -------------------------
file_ud = make_plot(
    df[df["position"].isin(["up", "down"])],
    ["up", "down"],
    "exp2_up_down.png"
)

print("Saved plots to:")
print(file_lr)
print(file_ud)
