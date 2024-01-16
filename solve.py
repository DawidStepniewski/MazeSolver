from mazes import Maze
from solver_factory import SolverFactory

import numpy as np
from PIL import Image
import time
import argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def create_animation(factory, algorithm, num_solvers, animation_frames_list):
    figure_width = 2 if num_solvers > 1 else 1
    fig, axs = plt.subplots(figure_width, num_solvers, figsize=(4 * num_solvers, 8))

    # Initialize the images and text subplots
    if algorithm == "all_methods":
        images = [axs[0, i].imshow(np.zeros_like(animation_frames_list[0][0]), animated=True) for i in
                  range(num_solvers)]
        text_subplots = [axs[1, i].text(0.2, 0.8, "", transform=axs[1, i].transAxes, fontsize=10,
                                        verticalalignment='top', bbox=dict(boxstyle="round", alpha=0.1))
                         for i in range(num_solvers)]
        axis_off = [axs[1, i].axis('off') for i in range(num_solvers)]
    else:
        images = [axs.imshow(np.zeros_like(animation_frames_list[0][0]), animated=True)]
        text_subplots = [axs.text(0.2, -0.1, "", transform=axs.transAxes, fontsize=10,
                                  verticalalignment='top', bbox=dict(boxstyle="round", alpha=0.1))]
        axs.axis('off')

    # Set titles and axis properties subplots
    if algorithm == "all_methods":
        for i, ax in enumerate(axs[0]):
            ax.set_title(f"Solver: {factory.Choices[i]}")
            ax.axis('off')
    else:
        axs.set_title(f"Solver: {algorithm}")
        axs.axis('off')

    return fig, axs, images, text_subplots


def solve(factory, algorithm, input_file):
    # Load Image
    print("Loading image...")
    im = Image.open(input_file)

    # Create the maze
    print("Creating maze...")
    maze = Maze(im)
    print("Node Count:", maze.count)

    stats_list = []
    animation_frames_list = []
    method_solver = factory.create_solver(algorithm)

    # Iterate through all solver methods
    for title, solver in method_solver:
        print("Starting Solve:", title)

        t0 = time.time()
        [result, stats] = solver(maze)
        t1 = time.time()

        total = t1 - t0
        stats.append(total)

        # Print solve stats
        print("Nodes explored: ", stats[0])
        if stats[2]:
            print("Path found, length", stats[1])
        else:
            print("No Path Found")
        print("Time elapsed: ", total, "\n")

        stats_list.append(stats)

        print("Saving image...")
        im_copy = im.copy()
        im_copy = im_copy.convert('RGB')
        im_pixels = im_copy.load()

        result_path = [n.Position for n in result]

        length = len(result_path)

        # Create a frame for each step of the path
        animation_frames = []
        for i in range(0, length - 1):
            a = result_path[i]
            b = result_path[i + 1]

            line_color_red = (255, 0, 0)

            if a[0] == b[0]:
                # Ys equal - horizontal line
                for x in range(min(a[1], b[1]), max(a[1], b[1])):
                    im_pixels[x, a[0]] = line_color_red
            elif a[1] == b[1]:
                # Xs equal - vertical line
                for y in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
                    im_pixels[a[1], y] = line_color_red

            # Append a copy of the current frame to the animation frames list
            animation_frames.append(np.array(im_copy))

        animation_frames_list.append(animation_frames)

    # Plot the animations in subplots
    print("Creating animation...")
    num_solvers = len(animation_frames_list)
    max_frames = max(len(frames) for frames in animation_frames_list)

    fig, axs, images, text_subplots = create_animation(factory, algorithm, num_solvers, animation_frames_list)

    def update(frame):
        for i, (img, text_subplot) in enumerate(zip(images, text_subplots)):
            if frame < len(animation_frames_list[i]):
                img.set_array(animation_frames_list[i][frame])
                text_subplot.set_text(f"Nodes explored: {stats_list[i][0]}\n"
                                      f"Path length: {stats_list[i][1]}\n"
                                      f"Time elapsed: {stats_list[i][3]:.3f} seconds")
        return images + text_subplots

    ani = animation.FuncAnimation(fig, update, frames=max_frames, interval=20, blit=False, repeat=False)

    plt.show()


def main():
    sf = SolverFactory()
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--method", nargs='?', const=sf.Default, default=sf.Default, choices=sf.Choices)
    parser.add_argument("input_file")
    args = parser.parse_args()
    solve(sf, args.method, args.input_file)


if __name__ == "__main__":
    main()
