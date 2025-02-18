import matplotlib.pyplot as plt

# Sample data (replace these with your actual data)
time = [0, 100, 200, 300]
power_with_es = [300, 200, 300, 200]
power_without_es_micro = [300, 250, 300, 250]
power_without_es_macro = [350, 300, 350, 300]
threshold = [200, 200, 200, 200]

# Plot the data
plt.plot(time, power_with_es, label="With ES rApp", color="red", linestyle="-")
plt.plot(time, power_without_es_micro, label="Without ES rApp. UE connect with microcell", color="orange", linestyle="--")
plt.plot(time, power_without_es_macro, label="Without ES rApp. UE connect with macrocell", color="green", linestyle="-.")

# Add threshold markers
for t, th in zip(time, threshold):
    plt.scatter(t, th, color="orange", edgecolor="black", s=100, label="Threshold for cell on/off" if t == 0 else "")

# Add labels and legend
plt.xlabel("Time")
plt.ylabel("Power Consumption (W)")
plt.legend()
plt.grid(True)
plt.show()
