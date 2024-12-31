import numpy as np

class Clock:
    def __init__(self, time, frequency=1, phase=0, offset=0):
        """
        Initialize the clock with the total time duration, frequency, and phase.
        :param time: Total duration of the clock signal.
        :param frequency: Frequency of the clock in Hz (default is 1 Hz).
        :param phase: Initial phase shift in radians (default is 0).
        :param offset: Offset to apply to the signal values (default is 0).
        """
        self.time = time
        self.frequency = frequency
        self.phase = phase
        self.offset = offset
    
    def __call__(self, jitter=0, dt=1e-6):
        """
        Generate the clock signal with additional points before and after change points.
        :param jitter: Standard deviation of normally distributed jitter to add to the time steps.
        :param dt: Small time offset to add points before and after each change point.
        :return: Two numpy arrays: time points where the clock signal changes and the corresponding signal values.
        """
        # Calculate the time steps where the clock changes
        period = 1 / self.frequency  # Time for one cycle
        num_cycles = int(self.time / period)  # Total number of cycles
        change_points = np.linspace(0, self.time, num_cycles + 1)  # Points of signal change

        # Apply jitter if specified
        if jitter > 0:
            change_points += np.random.normal(0, jitter, size=change_points.shape)
            change_points = np.clip(change_points, 0, self.time)  # Ensure values stay in bounds

        # Generate the signal transitions with additional points
        expanded_times = []
        signal_values = []
        
        for i, t in enumerate(change_points):
            # Add a point slightly before the change point
            if t - dt > 0:
                expanded_times.append(t - dt)
                signal_values.append(0 if i % 2 == 1 else 1)  # Retain previous signal value
            
            # Add the actual change point
            expanded_times.append(t)
            signal_values.append(1 if i % 2 == 0 else 0)  # Transition to the new signal value
            
            # Add a point slightly after the change point
            if t + dt < self.time:
                expanded_times.append(t + dt)
                signal_values.append(1 if i % 2 == 0 else 0)  # Retain new signal value

        # Apply the phase shift
        expanded_times = np.array(expanded_times) + (self.phase / (2 * np.pi * self.frequency))
        # Create new points at the beginning or end of the signal depending on the phase shift sign
        if self.phase > 0:
            expanded_times = np.insert(expanded_times, 0, expanded_times[0] - period)
        elif self.phase < 0:
            expanded_times = np.append(expanded_times, expanded_times[-1] + period)
        # Ensure values stay in bounds
        expanded_times = np.clip(expanded_times, 0, self.time)

        self.last = [np.array(expanded_times), np.array(signal_values) + self.offset]
        return self.last[0], self.last[1]

# Example usage
if __name__ == "__main__":
    total_time = 10  # Total duration of the signal
    clock1 = Clock(time=total_time, frequency=1, phase=0)  # Reference clock
    clock2 = Clock(time=total_time, frequency=1.01, phase=np.pi/4)  # Slightly faster clock with phase shift

    # Generate signals
    t1, s1 = clock1(dt=1e-3)
    t2, s2 = clock2(dt=1e-3)

    # Plot the signals
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 5))
    plt.step(t1, s1, label="Reference Clock (1 Hz)", where="post")
    plt.step(t2, s2 + 1.5, label="Comparison Clock (1.01 Hz with Phase Shift)", where="post")  # Offset for clarity
    plt.xlabel("Time (s)")
    plt.ylabel("Signal")
    plt.title("Clock Signals with Phase and Frequency Drift")
    plt.legend()
    plt.grid()
    plt.show()
