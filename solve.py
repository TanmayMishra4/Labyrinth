from PIL import Image
import argparse
import time
from factory import SolverFactory
from mazes import Maze
Image.MAX_PIXELS = None

def solve(factory, method, input_file, output_file):
    # Load Image
    print ("Loading Image")
    im = Image.open(input_file)

    #Creating Maze
    t0 = time.time()
    maze = Maze(im)
    t1 = time.time()
    print("Node count:", maze.count)
    total = t1-t0
    print("total time taken:", total, "\n")

    #Running the algorithm on the maze
    [title, solver] = factory.createSolver(method)
    print ("Starting Solve:", title)
    t0 = time.time()
    [result, stats] = solver(maze)
    t1 = time.time()
    total = t1-t0

    print ("Nodes explored: ", stats[0])
    if (stats[2]):
        print ("Path found, length", stats[1])
    else:
        print ("No Path Found")
    print ("Time elapsed: ", total, "\n")

    """
    Create and save the output image.
    This is simple drawing code that travels between each node in turn, drawing either
    a horizontal or vertical line as required. Line colour is roughly interpolated between
    blue and red depending on how far down the path this section is.
    """

    print ("Saving Image")
    im = im.convert('RGB')
    impixels = im.load()

    resultpath = [n.Position for n in result]

    length = len(resultpath)

    for i in range(0, length - 1):
        a = resultpath[i]
        b = resultpath[i+1]

        # Blue - red
        r = int((i / length) * 255)
        px = (r, 0, 255 - r)

        if a[0] == b[0]:
            # Ys equal - horizontal line
            for x in range(min(a[1],b[1]), max(a[1],b[1])):
                impixels[x,a[0]] = px
        elif a[1] == b[1]:
            # Xs equal - vertical line
            for y in range(min(a[0],b[0]), max(a[0],b[0]) + 1):
                impixels[a[1],y] = px

    im.save(output_file)



# def test(method, input_file, output_file):
#     print(f'your input was method{method}, \n input_file was{input_file}, \noutput file was {output_file}')
#     im = Image.open(input_file)
#     im.show()



def main():
    sf = SolverFactory()
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--method", nargs='?', const=sf.Default, default=sf.Default, choices=sf.Choices)
    parser.add_argument("input_file")
    parser.add_argument("output_file")
    args = parser.parse_args()

    solve(sf, args.method, args.input_file, args.output_file)
    # test(args.method, args.input_file, args.output_file)




if __name__ == "__main__":
    main()
