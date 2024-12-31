import numpy as np

class DigitalSignal:
    def __init__(self, clock, riseFallTime = 0.1, offset=0, rise = 1, duration=1):
        """
        Initialize the clock with the total time duration, frequency, and phase.
        :param time: Total duration of the data signal.
        :param frequency: Frequency of the clock in Hz (default is 1 Hz).
        :param phase: Initial phase shift in radians (default is 0).
        :param offset: Offset to apply to the signal values (default is 0).
        """
        self.time = clock.time
        self.clock = clock
        self.frequency = clock.frequency
        self.riseTime = riseFallTime
        self.fallTime = riseFallTime
        self.offset = offset
        self.rise = rise
        self.duration = duration
        # These are characteristics of an imaginary capture flip-flop
        self.setupTime = clock.frequency/10
        self.holdTime = clock.frequency/10
    
    def __call__(self, synchronized=False):
        """
        Generate the clock signal with additional points before and after change points.
        :param risetime: time it takes for the signal to transition from low to high.
        :param falltime: time it takes for the signal to transition from high to low.
        :param synchronized: Whether the signal is synchronized with it's companion clock or not.
        :return: Two numpy arrays: time points where the clock signal changes and the corresponding signal values.
        """
        change_points = [self.rise,self.duration + self.rise]  # Points of signal change

        # Generate the signal transitions with additional points
        expanded_times = []
        signal_values = []
        
        risetime = self.riseTime
        falltime = self.fallTime
        
        if(not synchronized):
            
            for i, t in enumerate(change_points):
                # Add a point slightly before the change point
                if t - risetime/2 > 0:
                    expanded_times.append(t - risetime/2)
                    signal_values.append(0 if i % 2 == 1 else 1)  # Retain previous signal value
                
                # Add the actual change point
                expanded_times.append(t+risetime/2)
                signal_values.append(1 if i % 2 == 0 else 0)  # Transition to the new signal value
                
                # Add a point slightly after the change point
                if i < len(change_points) - 1:
                    expanded_times.append(t + falltime/2)
                    signal_values.append(1 if i % 2 == 0 else 0)  # Retain new signal value
        else:
            # Use the companion clock's transition times and setup/hold constraints
            clock_transition_times, clock_values = self.clock.last  # Companion clock signal data
            
            setup_time = self.setupTime  # Define setup time

            for i, t in enumerate(change_points):
                # Find the next valid clock edge after setup time
                valid_rise_time = next(
                    (ct for ct in clock_transition_times if ct >= t - setup_time), None
                )
                # If within setup/hold time, skip to the next clock edge
                if valid_rise_time:
                    t = valid_rise_time

                # Add synchronized rise time point
                if t - risetime / 2 > 0:
                    expanded_times.append(t - risetime / 2)
                    signal_values.append(0 if i % 2 == 1 else 1)

                # Add synchronized change point
                expanded_times.append(t + risetime / 2)
                signal_values.append(1 if i % 2 == 0 else 0)

                # Add synchronized fall time point
                if i < len(change_points) - 1:
                    expanded_times.append(t + falltime / 2)
                    signal_values.append(1 if i % 2 == 0 else 0)

        # add time zero and time end points
        expanded_times = np.insert(expanded_times, 0, 0)
        signal_values = np.insert(signal_values, 0, 0)
        expanded_times = np.append(expanded_times, self.time)
        signal_values = np.append(signal_values, 0)
        return np.array(expanded_times), np.array(signal_values) + self.offset
                