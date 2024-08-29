import time
import matplotlib.pyplot as plt

class TimeWeightedEMA:
    def __init__(self, half_life):
        self.half_life = half_life
        self.average = None
        self.last_update_time = None
        self.SCALING_FACTOR = 262144

    def update(self, new_value, current_time=None):
        if current_time is None:
            current_time = time.time()

        if self.average is None:
            self.average = new_value
            self.last_update_time = current_time
        else:
            elapsed_time = current_time - self.last_update_time
            # alpha = 1 - 0.5 ** (elapsed_time / self.half_life)
            alpha = self.SCALING_FACTOR - (self.SCALING_FACTOR * self.SCALING_FACTOR) / (self.SCALING_FACTOR + (elapsed_time * self.SCALING_FACTOR / self.half_life))
            # self.average = new_value + (1 - alpha) * self.average
            self.average = ((self.SCALING_FACTOR - alpha) * self.average / self.SCALING_FACTOR) + new_value;
            self.last_update_time = current_time

        return self.average

    def estimate(self, new_value, current_time=None):
        if current_time is None:
            current_time = time.time()

        if self.average is None:
            return new_value
        else:
            elapsed_time = current_time - self.last_update_time
            alpha = self.SCALING_FACTOR - (self.SCALING_FACTOR * self.SCALING_FACTOR) / (self.SCALING_FACTOR + (elapsed_time * self.SCALING_FACTOR / self.half_life))
            estimated_average = ((self.SCALING_FACTOR - alpha) * self.average / self.SCALING_FACTOR) + new_value
            return estimated_average

# Example usage
twema = TimeWeightedEMA(half_life=12*60*60)  # 12 hours half-life

# Initialize arrays to store timestamps and values
timestamps = []
twema_values = []
threshold = 2000000
threshold_claimed = False
value = 53
total_claimed = 0

# Simulate submitting a value of every second
for timestamp in range(10 * 24 * 60 * 60):
    twema_estimate = twema.estimate(value, timestamp)
    if twema_estimate > threshold:
        if not threshold_claimed:
            print("Threshold triggered at timestamp {}, hours after start {:.2f}, total amount claimed {}".format(timestamp, timestamp/60/60, timestamp * 59))
        threshold_claimed = True;
        continue
    twema_value = twema.update(value, timestamp)
    timestamps.append(timestamp)
    twema_values.append(twema_value)
    total_claimed += value

print("total amount claimed {}".format(total_claimed))
# Plot the results
plt.plot(timestamps, twema_values, label='TWEMA')
plt.axhline(y=threshold, color='r', linestyle='--', label='Threshold (2M)')  # Add threshold line
plt.xlabel('Timestamp (s)')
plt.ylabel('Value')
plt.title('TWEMA over Time when claiming {} tokens per second'.format(value))
plt.legend()
plt.show()
