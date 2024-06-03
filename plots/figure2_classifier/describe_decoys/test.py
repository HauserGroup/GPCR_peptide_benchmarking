import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Assuming sim_df is your data
# Replace this with your actual data
np.random.seed(42)
sim_df = np.random.randn(1000)

# Create the KDE plot and get the x and y values
kde = sns.kdeplot(
    sim_df,
    color="blue",
    lw=4,
    shade=True,
    bw_method=0.1,
)

# Extract the x and y data from the plot
x_data = np.linspace(min(sim_df), max(sim_df), 1000)
y_data = kde.get_lines()[0].get_data()[1]

# Calculate the cumulative density function (CDF)
cdf_values = np.cumsum(y_data)
cdf_values /= cdf_values[-1]  # Normalize to range from 0 to 1

# Find the threshold for the top 50%
threshold_index = np.searchsorted(cdf_values, 0.5)
threshold_value = x_data[threshold_index]

# Clear the plot to replot with highlighted area
plt.clf()

# Recreate the KDE plot
sns.kdeplot(
    sim_df,
    color="blue",
    lw=4,
    shade=True,
    bw_method=0.1,
)

# Highlight the top 50% area
plt.fill_between(
    x_data, y_data, where=(x_data >= threshold_value), color="red", alpha=0.5
)

# Add plot labels and title
plt.title("KDE Plot with Top 50% Highlighted in Red")
plt.xlabel("Value")
plt.ylabel("Density")

# Display the plot
plt.show()
