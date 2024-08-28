import time
import matplotlib.pyplot as plt

class TimeWeightedEMA:
    def __init__(self, half_life):
        self.half_life = half_life
        self.average = None
        self.last_update_time = None

    def update(self, new_value, current_time=None):
        if current_time is None:
            current_time = time.time()

        if self.average is None:
            self.average = new_value
            self.last_update_time = current_time
        else:
            elapsed_time = current_time - self.last_update_time
            alpha = 1 - 0.5 ** (elapsed_time / self.half_life)
            self.average = new_value + (1 - alpha) * self.average
            self.last_update_time = current_time

        return self.average

# Example usage
twema = TimeWeightedEMA(half_life=12*60*60)  # 12 hours half-life

# Initialize arrays to store timestamps and values
timestamps = []
twema_values = []
threshold = 2000000
threshold_claimed = False
value = 59

# Simulate submitting a value of 59 every second for a full day
for timestamp in range(24 * 60 * 60):  # 86400 seconds in a day
    twema_value = twema.update(value, timestamp)
    if twema_value > threshold and not threshold_claimed:
        print("Threshold triggered at timestamp {}, hours after start {:.2f}, total amount claimed {}".format(timestamp, timestamp/60/60, timestamp * 59))
        threshold_claimed = True;
    timestamps.append(timestamp)
    twema_values.append(twema_value)

# Plot the results
plt.plot(timestamps, twema_values, label='TWEMA')
plt.axhline(y=threshold, color='r', linestyle='--', label='Threshold (2M)')  # Add threshold line
plt.xlabel('Timestamp (s)')
plt.ylabel('Value')
plt.title('TWEMA over Time when claiming 59 tokens per second')
plt.legend()
plt.show()
