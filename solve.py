import numpy as np
from PIL import Image, ImageDraw, ImageFont
import time
from mazes import Maze
from solver_factory import SolverFactory
import argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation
Image.MAX_IMAGE_PIXELS = None

def solve(factory, input_file):
    # Load Image
    print ("Loading image...")
    im = Image.open(input_file)

    # Create the maze (and time it) - for many mazes this is more time consuming than solving the maze
    print ("Creating maze...")
    t0 = time.time()
    maze = Maze(im)
    t1 = time.time()
    print ("Node Count:", maze.count)
    total = t1-t0
    print ("Time elapsed:", total, "\n")

    stats_list = []
    animation_frames_list = []

    # Iterate through all solver methods
    for method in factory.Choices:
        [title, solver] = factory.create_solver(method)
        print ("Starting Solve:", title)

        t0 = time.time()
        [result, stats] = solver(maze)
        t1 = time.time()

        total = t1-t0
        stats.append(total)

        # Print solve stats
        print ("Nodes explored: ", stats[0])
        if (stats[2]):
            print ("Path found, length", stats[1])
        else:
            print ("No Path Found")
        print ("Time elapsed: ", total, "\n")

        stats_list.append(stats)

        print("Saving image...")
        im_copy = im.copy()
        im_copy = im_copy.convert('RGB')
        impixels = im_copy.load()

        resultpath = [n.Position for n in result]

        length = len(resultpath)

        # Create a frame for each step of the path
        animation_frames = []
        for i in range(0, length - 1):
            a = resultpath[i]
            b = resultpath[i + 1]

            r = int((i / length) * 255)
            px = (r, 0, 255 - r)

            if a[0] == b[0]:
                for x in range(min(a[1], b[1]), max(a[1], b[1])):
                    impixels[x, a[0]] = px
            elif a[1] == b[1]:
                for y in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
                    impixels[a[1], y] = px

            # Append a copy of the current frame to the animation frames list
            animation_frames.append(np.array(im_copy))

        animation_frames_list.append(animation_frames)

    del animation_frames, im_copy

    # Plot the animations in subplots
    print("Creating animation...")
    num_solvers = len(animation_frames_list)
    max_frames = max(len(frames) for frames in animation_frames_list)

    fig, axs = plt.subplots(2, num_solvers, figsize=(4 * num_solvers, 8))

    # Initialize the images for the upper subplots
    images = [axs[0, i].imshow(np.zeros_like(animation_frames_list[0][0]), animated=True) for i in
              range(num_solvers)]

    # Initialize the text subplots
    text_subplots = [axs[1, i].text(0.2, 0.8, "", transform=axs[1, i].transAxes, fontsize=10,
                                    verticalalignment='top', bbox=dict(boxstyle="round", alpha=0.1))
                     for i in range(num_solvers)]

    def update(frame):
        for i, (img, text_subplot) in enumerate(zip(images, text_subplots)):
            if frame < len(animation_frames_list[i]):
                img.set_array(animation_frames_list[i][frame])
                text_subplot.set_text(f"Nodes explored: {stats_list[i][0]}\n"
                                      f"Path length: {stats_list[i][1]}\n"
                                      f"Time elapsed: {stats_list[i][3]:.3f} seconds")
        return images + text_subplots

    ani = animation.FuncAnimation(fig, update, frames=max_frames, interval=20, blit=True, repeat=False)

    # Set titles and axis properties for the upper image subplots
    for i, ax in enumerate(axs[0]):
        ax.set_title(f"Solver: {factory.Choices[i]}")
        ax.axis('off')

    # Remove axis properties for the text subplots
    for ax in axs[1]:
        ax.axis('off')

    plt.show()


def main():
    sf = SolverFactory()
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()

    solve(sf, args.input_file)

if __name__ == "__main__":
    main()

