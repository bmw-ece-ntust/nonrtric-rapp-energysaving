import numpy as np
import matplotlib.pyplot as plt

# Define the x values (time)
time = np.linspace(0, 400, 1000)

# Define the y values (traffic load) as a reversed triangular wave
traffic_load = 100 * (np.abs((time % 200) - 100) / 100)

# Plotting
fig, ax1 = plt.subplots(figsize=(10, 6))

# Create a secondary y-axis for traffic load
# ax2 = ax1.twinx()
ax1.plot(time, traffic_load, color="blue", label="Traffic Load", linestyle="-")
ax1.set_ylabel("Traffic Load (%)", fontsize=12)
ax1.set_xlabel("Time", fontsize=12)
# ax2.tick_params(axis='y', labelcolor="blue")
ax1.set_ylim(0, 100)
ax1.set_xlim(0, 400)
ax1.grid(True)

# Set y-axis ticks to start from 20 and go up to 100
ax1.set_yticks(np.arange(20, 101, 20))

# Add legends
fig.legend(loc="upper right", bbox_to_anchor=(1,1), bbox_transform=ax1.transAxes, fontsize=12)

# plt.title("Traffic Load and Power Consumption vs Time")
plt.tight_layout()

# Save to png with 300 dpi
plt.savefig("Result - ES Traffic.png", dpi=300)
