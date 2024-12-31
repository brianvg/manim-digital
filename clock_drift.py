from manim import *
import numpy as np
import digital_clock as dc  # Ensure this imports your Clock class

class ClockDrift(Scene):
    def construct(self):
        duration = 10  # Total duration of the signal
        nSignals = 2
        clock1 = dc.Clock(time=duration, frequency=1, phase=0, offset=0)
        clock2 = dc.Clock(time=duration, frequency=1, phase=0, offset=1.1)

        # Create the axes
        axes = Axes(
            x_range=[0, duration, 1],
            y_range=[0, 1.5*nSignals, 1.1],
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
        x1, y1 = clock1()
        reference_clock_line = self.create_step_plot(axes, x1, y1, color=RED)

        # Create the companion clock graph
        x2, y2 = clock2(jitter = 0.01)
        companion_clock_line = self.create_step_plot(axes, x2, y2, color=BLUE)

        # Add the elements to the scene
        self.play(FadeIn(axes))
        self.add(axes_labels)
        self.wait(1)
        self.play(FadeIn(reference_clock_line))
        reference_label = axes.get_graph_label(reference_clock_line, label="Ideal Reference Clock", direction=DOWN,x_val=duration-0.1)
        self.play(Write(reference_label))
        self.wait(1)
        self.play(FadeIn(companion_clock_line))
        self.wait(2)
        companion_label = axes.get_graph_label(companion_clock_line, label="Ideal Companion Clock", direction=UP,x_val=duration-0.1)
        self.play(Write(companion_label))
        self.wait(3)
        nonIdeal_reference_label = axes.get_graph_label(reference_clock_line, label="Non-Ideal Reference Clock", direction=DOWN,x_val=duration-0.1)
        nonIdeal_companion_label = axes.get_graph_label(companion_clock_line, label="Non-Ideal Companion Clock", direction=UP,x_val=duration-0.1)
        self.play(Transform(reference_label, nonIdeal_reference_label), Transform(companion_label, nonIdeal_companion_label))
    
        # Animate the scene by updating the step plot values with new ones
        animationSteps = 100
        # animationSteps = 10
        animationStepDuration = 0.1
        totalPhaseShift = 2*np.pi
        for i in range(1, animationSteps):
            # Dynamically adjust jitter and phase
            jitter = 0.01  # Fixed jitter for this example
            
            # up to pi phase shift.
            phase = i * totalPhaseShift/animationSteps  # Phase increment per iteration

            # Update the companion clock signal with jitter and phase
            x2, y2 = clock2(jitter=jitter)
            clock2.phase = phase  # Adjust phase for the next update

            # Clock one does not update phase, but does update jitter
            x1, y1 = clock1(jitter=jitter)
            # Update the companion clock line
            companion_clock_line.become(self.create_step_plot(axes, x2, y2, color=BLUE))
            self.wait(animationStepDuration)
            # Update the reference clock line
            reference_clock_line.become(self.create_step_plot(axes, x1, y1, color=RED))

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
