from manim import *
import numpy as np
import digital_clock as dc  # Ensure this imports your Clock class
import digital_signal as ds

class ClockDrift(Scene):
    def construct(self):
        duration = 10  # Total duration of the signal
        nSignals = 3
        
        clock = dc.Clock(time=duration, frequency=1, phase=0, offset=0)
        data_signal = ds.DigitalSignal(clock, offset=1.1, rise = 1.4, duration = 2.3)

        # Create the axes
        axes = Axes(
            x_range=[0, duration+1, 1],
            y_range=[0, 1.1*nSignals, 1.1],
            x_length=duration+1,
            y_length=nSignals *1.5,
            axis_config={"color": GREEN},
            tips=True,
        )
        axes_labels = axes.get_axis_labels()
         # Customize the labels
        axes_labels[0] = MathTex("Ticks").next_to(axes.x_axis, DOWN)
        axes_labels[1] = MathTex("").next_to(axes.x_axis, DOWN)

        # Create the reference clock graph
        x1, y1 = clock()
        reference_clock_line = self.create_step_plot(axes, x1, y1, color=RED)
        
        x2, y2 = data_signal()
        data_signal_async = self.create_step_plot(axes, x2, y2, color=ORANGE)
        data_signal.offset = 2.1
        x3, y3 = data_signal(synchronized=True)
        data_signal_sync = self.create_step_plot(axes, x3, y3, color=BLUE)
        
        # Add the elements to the scene
        self.play(FadeIn(axes))
        self.add(axes_labels)
        self.wait(1)
        self.play(FadeIn(reference_clock_line))
        reference_label = axes.get_graph_label(reference_clock_line, label="Clock", direction=DOWN,x_val=duration-0.1)
        self.play(Write(reference_label))
        self.wait(1)
        self.play(FadeIn(data_signal_async))
        self.wait(2)
        self.play(FadeIn(data_signal_sync))
        self.wait(2)
    
        # Animate the pulse signal transitioning across the screen
        # animationSteps = 100
        animationSteps = 30
        animationStepDuration = 0.2
        totalPulseShift = 3
        for i in range(1, animationSteps):
            # Update the companion clock signal with jitter and phase
            data_signal.rise = data_signal.rise + totalPulseShift/animationSteps
            data_signal.offset = 1.1
            x2, y2 = data_signal()
            data_signal.offset = 2.1
            x3, y3 = data_signal(synchronized=True)

            data_signal_async.become(self.create_step_plot(axes, x2, y2,color=ORANGE))
            data_signal_sync.become(self.create_step_plot(axes, x3, y3,color=BLUE))
            self.wait(animationStepDuration)

    def create_step_plot(self, axes, x_values, y_values, color):
        """
        Create a step plot for square waves.
        :param axes: Manim Axes object to transform points into scene coordinates.
        :param x_values: Time points of the signal.
        :param y_values: Signal values at those points (0 or 1).
        :param color: Line color.
        :return: A VMobject representing the step plot.
        """
        points = []
        for i in range(len(x_values) - 1):
            # Add the horizontal line at the current level
            points.append(axes.c2p(x_values[i], y_values[i]))
            points.append(axes.c2p(x_values[i + 1], y_values[i]))
            # Add the vertical transition (only if not at the end)
            if i < len(x_values) - 2:
                points.append(axes.c2p(x_values[i + 1], y_values[i + 1]))

        # Create a VMobject to represent the step plot
        step_plot = VMobject()
        step_plot.set_points_as_corners(points)
        step_plot.set_color(color)
        return step_plot
