import pathlib
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import random
from sklearn.metrics import roc_curve


def get_roc_data(percent_correct=0.9):
    # simulate some data
    random.seed(16)
    y_true = [random.choice([0, 1]) for _ in range(100)]

    y_pred = list()
    for i in range(len(y_true)):
        noise = (random.random() - 0.5) * 0.2
        if random.random() < percent_correct:
            val = y_true[i] + noise
            if val < 0:
                val = 0
            elif val > 1:
                val = 1
            y_pred.append(val)
        else:
            val = 1 - y_true[i] + noise
            if val < 0:
                val = 0
            elif val > 1:
                val = 1
            y_pred.append(val)
    # calculate the ROC curve
    fpr, tpr, _ = roc_curve(y_true, y_pred)
    return fpr, tpr


save_path = "plots/figure1_abstract/roc.svg"
# set scientific style
plt.rcParams["axes.formatter.useoffset"] = False
sns.set_context("talk")
sns.set_style("white")
# set font to helvetica
plt.rcParams["font.family"] = "Helvetica"
plt.rcParams["font.sans-serif"] = "Helvetica"

plt.figure(figsize=(7, 7))
# plot the ROC curve
x, y = get_roc_data(percent_correct=0.8)
plot_col = "#4c2c92"
sns.lineplot(
    x=x,
    y=y,
    ci=None,
    color=plot_col,
    lw=3,
    label="3D protein model",
)
# plot again, but with lower accuracy
x, y = get_roc_data(percent_correct=0.6)
plot_col = "#2e8540"
# convert to hex
sns.lineplot(x=x, y=y, ci=None, color=plot_col, lw=3, label="2D protein model")
# increase font size by 150%
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.legend(fontsize=20)
plt.xlabel("False positive rate", fontsize=20)
plt.ylabel("True positive rate", fontsize=20)
plt.title("Peptide classifier performance", fontsize=30)

# add dashed baseline
plt.plot([0, 1], [0, 1], "k--", alpha=0.5)
# set x and y limits
plt.xlim([0, 1])
plt.ylim([0, 1])

# save the plot
plt.tight_layout()
plt.savefig(save_path)
plt.close()
