import matplotlib.pyplot as plt
import numpy as np

# Define load values
load_x = [i for i in range(0, 101, 10)]  # Load values: 10, 20, ..., 100

# Calculate power consumption for each formula (10 iterations)
green_y = []
orange_y = []
blue_y = []

for i in range(11):
    green_y.append(130 + 125 * load_x[i]/100)
    orange_y.append(100 + 200 * load_x[i]/100)
    blue_y.append(30 + 125 * load_x[i]/100)

# Create the plot
plt.plot(load_x, green_y, color="red", linestyle='-', label="Macrocell and Microcell power consumption")
plt.plot(load_x, orange_y, color="green", linestyle='--', label="Macrocell power consumption")
plt.plot(load_x, blue_y, color="blue", linestyle='-.', label="Microcell power consumption")

plt.scatter(40, 100 + 200 * 40/100, color="brown", marker='o', label="ES threshold", s=100, zorder=5)

# plt.scatter(load_x, green_y, color="red")
# plt.scatter(load_x, orange_y, color="green")
# plt.scatter(load_x, blue_y, color="blue")

# Labels and title
plt.xlabel('Traffic Load (%)', fontsize=12)
plt.ylabel('Power Consumption (W)', fontsize=12)
# plt.title('Power Consumption vs Load')

# Set axis limits
plt.xlim(0, 100)
plt.ylim(0, 300)

# Set y-axis ticks to exclude 0
plt.yticks(np.arange(50, 301, 50))

# Display legend
plt.legend(fontsize=12)

# Show the plot
plt.grid(True)

# Adjust margins
plt.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.1)

# Save the figure as a .png file with 300 dpi
plt.savefig('./Result - Threshold_cell loadings.png', dpi=300)
