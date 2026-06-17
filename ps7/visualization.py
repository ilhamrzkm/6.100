import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D
# import imageio
# import os


class DiseaseSimVisualizer:

    def __init__(self, sim, num_steps):
        self._sim = sim
        self._num_steps = num_steps

        self.fig = plt.figure(figsize=(14, 6))
        self.fig.subplots_adjust(left=0.05, right=0.97, top=0.92, bottom=0.1, wspace=0.5)

        # Left axes: spatial simulation
        self.ax_sim = self.fig.add_subplot(1, 2, 1)
        # Right axes: time series chart
        self.ax_chart = self.fig.add_subplot(1, 2, 2)

        # History for the live chart
        self._time_steps = []
        self._infected_history = []
        self._dead_history = []

        self._started = False

    def start(self):
        """Open the visualization window."""
        if not self._started:
            plt.ion()
            plt.show(block=False)
            self._started = True

    def _draw_simulation(self, t):
        """Draw the spatial simulation on self.ax_sim."""

        all_stats, num_infected, _ = self._sim.get_stats()
        width, height = self._sim.width, self._sim.height

        # group agents for better plotting
        groups = {
            ("healthy", "Person"): ([], []),
            ("healthy", "MenacingPerson"): ([], []),
            ("healthy", "CarefulPerson"): ([], []),
            ("healthy", "MoreMenacingPerson"): ([], []),

            ("infected", "Person"): ([], []),
            ("infected", "MenacingPerson"): ([], []),
            ("infected", "CarefulPerson"): ([], []),
            ("infected", "MoreMenacingPerson"): ([], []),

            ("dead", "Person"): ([], []),
            ("dead", "MenacingPerson"): ([], []),
            ("dead", "CarefulPerson"): ([], []),
            ("dead", "MoreMenacingPerson"): ([], []),
        }

        # get all agent info
        for agent, stats in all_stats.items():
            x, y = stats["location"]
            infected = stats["infected"]
            alive = stats["alive"]

            # determine type
            agent_type = type(agent).__name__

            # determine health state
            if not alive:
                state = "dead"
            elif infected:
                state = "infected"
            else:
                state = "healthy"

            # update grouping
            groups[(state, agent_type)][0].append(x)
            groups[(state, agent_type)][1].append(y)

        self.ax_sim.clear()

        # different markers and colors for different agent types and healths
        marker_map = {
            "Person": "s",         # square
            "MenacingPerson": "^",       # triangle
            "CarefulPerson": "o",        # circle
            "MoreMenacingPerson": "*",  # star
        }

        color_map = {
            "healthy": "green",
            "infected": "red",
            "dead": "gray",
        }

        # plot
        for (state, agent_type), (xs, ys) in groups.items():
            if xs:  # only plot if non-empty
                # plot agents
                self.ax_sim.scatter(
                    xs, ys,
                    c=color_map[state],
                    marker=marker_map[agent_type],
                    s=20,
                    label=f"{state.capitalize()} ({agent_type})"
                )
                # plot infection radius around infected agents
                if state == "infected":
                    for x, y in zip(xs, ys):
                        circle = patches.Circle(
                            (x, y),
                            self._sim.infection_radius,
                            color='red',
                            alpha=0.1,
                            fill=True
                        )
                        self.ax_sim.add_patch(circle)

        self.ax_sim.set_xlim(-0.5, width + 0.5)
        self.ax_sim.set_ylim(-0.5, height + 0.5)
        self.ax_sim.set_title("Disease Simulation")

        # color legend
        color_handles = [
            Line2D([0], [0], marker='s', color='w', label='Healthy',
                markerfacecolor='green', markersize=8),
            Line2D([0], [0], marker='s', color='w', label='Infected',
                markerfacecolor='red', markersize=8),
            Line2D([0], [0], marker='s', color='w', label='Dead',
                markerfacecolor='gray', markersize=8),
        ]

        # add color legend
        legend1 = self.ax_sim.legend(
            handles=color_handles,
            title="Health Status",
            loc="upper left",
            bbox_to_anchor=(1.02, 1)
        )

        # shape legend, only include if there are different types
        if not all(type(agent).__name__ == "Person" for agent in all_stats):
            shape_handles = [
                Line2D([0], [0], marker='s', color='black', label='Person',
                    linestyle='None', markersize=8),
                Line2D([0], [0], marker='^', color='black', label='Menacing',
                    linestyle='None', markersize=8),
                Line2D([0], [0], marker='o', color='black', label='Careful',
                    linestyle='None', markersize=8),
                Line2D([0], [0], marker='*', color='black', label='More Menacing',
                    linestyle='None', markersize=8),
            ]

            # add shape legend
            legend2 = self.ax_sim.legend(
                handles=shape_handles,
                title="Agent Type",
                loc="upper left",
                bbox_to_anchor=(1.02, 0.7)
            )

            # add the first legend back (important!)
            self.ax_sim.add_artist(legend1)

        self.ax_sim.text(
            0.02, 0.98,
            f"t = {t}",
            transform=self.ax_sim.transAxes,
            fontsize=12,
            verticalalignment='top',
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.7)
        )

    def _draw_chart(self, t):
        """Draw the live infection/death chart on self.ax_chart."""
        self.ax_chart.clear()

        # get sim info
        all_stats, num_infected, num_alive = self._sim.get_stats()
        total = len(all_stats)
        num_dead = total - num_alive

        self._time_steps.append(t)
        self._infected_history.append(num_infected)
        self._dead_history.append(num_dead)

        # draw chart
        self.ax_chart.plot(self._time_steps, self._infected_history,
                           color='red',  linewidth=2, label='Infected')
        self.ax_chart.plot(self._time_steps, self._dead_history,
                           color='gray', linewidth=2, label='Dead')

        self.ax_chart.set_xlim(0, self._num_steps + 1)
        self.ax_chart.set_ylim(0, total + 1)
        self.ax_chart.set_xlabel("Time step", fontsize=10)
        self.ax_chart.set_ylabel("Number of people", fontsize=10)
        self.ax_chart.set_title("Population Status Over Time", fontsize=11)
        self.ax_chart.legend(fontsize=9)

    def draw(self, t):
        """
        Draw and display current frame.
        """
        if not self._started:
            self.start()

        self._draw_simulation(t)
        self._draw_chart(t)

        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()
        plt.pause(0.1)

    def stop(self):
        """Close the visualization window."""
        if self._started:
            plt.close(self.fig)
            self._started = False

    def _draw_on_axis(self, t=0):
        """
        Internal helper used by save_frame / save_gif:
        draws both panels onto the figure without displaying.
        """
        all_stats, num_infected, num_alive = self._sim.get_stats()
        total = len(all_stats)
        num_dead = total - num_alive

        self._time_steps.append(t)
        self._infected_history.append(num_infected)
        self._dead_history.append(num_dead)

        self._draw_simulation(t)
        self._draw_chart()

    def save_frame(self, filepath, t=0):
        """
        Save the current frame as an image.

        Parameters:
            filepath (str): path to save image (e.g. "frame.png")
            t (int): current time step label
        """
        self._draw_on_axis(t)
        self.fig.savefig(filepath)

    def save_gif(self, filepath, steps, fps=5):
        """
        Run simulation and save as a GIF (both panels per frame).

        Parameters:
            filepath (str): output gif path (e.g. "sim.gif")
            steps (int): number of steps
            fps (int): frames per second
        """
        frames = []
        temp_dir = "_temp_frames"
        os.makedirs(temp_dir, exist_ok=True)

        self._sim.reset()
        self._num_steps = steps  # fix 1: set so _draw_chart uses the correct x-axis range
        self._time_steps.clear()
        self._infected_history.clear()
        self._dead_history.clear()

        for t in range(steps):
            # fix 2: capture state before stepping, so t=0 shows initial state
            # and the final state is included
            all_stats, num_infected, num_alive = self._sim.get_stats()
            total = len(all_stats)
            self._time_steps.append(t)
            self._infected_history.append(num_infected)
            self._dead_history.append(total - num_alive)

            # fix 3: draw directly without going through _draw_on_axis,
            # which would double-append to history
            self._draw_simulation(t)
            self._draw_chart(t)

            frame_path = os.path.join(temp_dir, f"frame_{t}.png")
            self.fig.savefig(frame_path)
            frames.append(imageio.imread(frame_path))

            if num_alive == 0:
                break
            self._sim.step()

        imageio.mimsave(filepath, frames, fps=fps, loop=0)

        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))
        os.rmdir(temp_dir)


def plot_population_status(sim, num_steps, filename=None):
    """
    Run the simulation for num_steps and plot infected and dead counts over time.

    Parameters:
        sim (DiseaseSimulation): the simulation to run
        num_steps (int): number of steps to simulate
        filename (str, optional): if provided, save the plot as an SVG with this name
            (e.g. "my_plot" saves "my_plot.svg"). Defaults to None (no file saved).
    """
    sim.reset()

    time_steps = []
    infected_history = []
    dead_history = []
    total = len(sim.people_locs)

    title = filename.split('.')[0]

    for t in range(num_steps):
        _, num_infected, num_alive = sim.get_stats()
        time_steps.append(t)
        infected_history.append(num_infected)
        dead_history.append(total - num_alive)

        if num_alive == 0:
            break
        sim.step()

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(time_steps, infected_history, color='red',  linewidth=2, label='Infected')
    ax.plot(time_steps, dead_history,     color='gray', linewidth=2, label='Dead')
    ax.set_xlim(0, num_steps)
    ax.set_ylim(0, total + 1)
    ax.set_xlabel("Time step", fontsize=11)
    ax.set_ylabel("Number of people", fontsize=11)
    ax.set_title(f"Infected & Dead Over Time for {title}", fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    if filename is not None:
        svg_path = filename if filename.endswith(".svg") else filename + ".svg"
        fig.savefig(svg_path, format="svg")
        print(f"Plot saved to {svg_path}")

    plt.show()
