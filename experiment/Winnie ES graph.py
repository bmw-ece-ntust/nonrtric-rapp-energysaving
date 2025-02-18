import numpy as np
import matplotlib.pyplot as plt

# Define the x values (time)
time = np.linspace(0, 600, 1000)

# Define the y values (traffic load) as a reversed triangular wave
traffic_load = 100 * (np.abs((time % 200) - 100) / 100)

# Define the y values (power consumption) as a sine wave
power_consumption = 50 * np.sin(2 * np.pi * time / 400) + 50

# Plotting
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot power consumption on the primary y-axis
ax1.plot(time, power_consumption, color="red", label="Power Consumption", linestyle="--")
ax1.set_xlabel("Time")
ax1.set_ylabel("Power Consumption (W)", color="red")
ax1.tick_params(axis='y', labelcolor="red")
ax1.set_xlim(0, 600)
ax1.set_ylim(0, 100)
ax1.grid(True)

# Create a secondary y-axis for traffic load
ax2 = ax1.twinx()
ax2.plot(time, traffic_load, color="blue", label="Traffic Load", linestyle="-")
ax2.set_ylabel("Traffic Load (%)", color="blue")
ax2.tick_params(axis='y', labelcolor="blue")
ax2.set_ylim(0, 100)

# Add legends
fig.legend(loc="upper right", bbox_to_anchor=(1,1), bbox_transform=ax1.transAxes)

plt.title("Traffic Load and Power Consumption vs Time")
plt.tight_layout()

# Save to png with 300 dpi
plt.savefig("Result - ES Traffic.png", dpi=300)