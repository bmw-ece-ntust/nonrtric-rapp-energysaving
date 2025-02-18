import numpy as np
import matplotlib.pyplot as plt

# Define the x values (time)
time = np.linspace(0, 600, 1000)

# Define the y values (traffic load) as a reversed triangular wave
traffic_load = 100 * (np.abs((time % 200) - 100) / 100)

# Calculate power consumption based on the given formulas
power_consumption1 = [
    150 + 125 * load / 100 if load > 40 else 120 + 200 * load / 100
    for load in traffic_load
]

power_consumption2 = 150 + 125 * traffic_load / 100
power_consumption3 = np.minimum(330, 150 + 200 * traffic_load / 100)

traffic_load

# Plotting
fig, ax1 = plt.subplots(figsize=(12, 6))

# Create a secondary y-axis for traffic load
ax2 = ax1.twinx()
ax2.plot(time, traffic_load, color="red", label="Traffic Load", linestyle="-", linewidth=2)
ax2.set_ylabel("Traffic Load (%)", color="red", fontsize=12)
ax2.tick_params(axis='y', labelcolor="red")
ax2.set_ylim(0, 100)

# Plot power consumption on the primary y-axis
ax1.plot(time, power_consumption1, color="orange", label="With ES rApp", linestyle="--", linewidth=2)
ax1.plot(time, power_consumption2, color="blue", label="Without ES rApp. UE connect with microcell", linestyle=":", linewidth=2)
ax1.plot(time, power_consumption3, color="green", label="Without ES rApp. UE connect with macrocell", linestyle="-.", linewidth=2)
ax1.set_xlabel("Time (seconds)", fontsize=12)
ax1.set_ylabel("Power Consumption (W)", color="blue", fontsize=12)
ax1.tick_params(axis='y', labelcolor="blue")
ax1.set_xlim(0, 600)
ax1.set_ylim(100, 350)
ax1.grid(True)

# # Add scatter plot for thresholds
# if threshold_time and threshold_values:
#     ax1.scatter(
#         threshold_time, threshold_values, color="orange", edgecolor="black", s=100, zorder=5,
#         label="Threshold for cell on/off"
#     )

# Add legends
fig.legend(loc="upper right", bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes, fontsize=10)

plt.title("Power Consumption vs. Time with Traffic Load", fontsize=14)
plt.tight_layout()

# Save to png with 300 dpi
plt.savefig("Winnie_ES_graph_fixed.png", dpi=300)
plt.show()
