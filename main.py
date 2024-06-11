import matplotlib.pyplot as plt
from math import atan2
from random import randint

# Function to plot points and optionally the convex hull
def plot_graph(points, hull=None):
    xs, ys = [p[0] for p in points], [p[1] for p in points]
    plt.scatter(xs, ys)

    if hull:
        hull.append(hull[0])
        hull_xs, hull_ys = [p[0] for p in hull], [p[1] for p in hull]
        plt.plot(hull_xs, hull_ys, 'r-')

    plt.show()

# Function to calculate the polar angle
def calculate_angle(p0, p1):
    return atan2(p1[1] - p0[1], p1[0] - p0[0])

# Function to calculate the squared Euclidean distance
def calculate_distance_squared(p0, p1):
    return (p1[1] - p0[1]) ** 2 + (p1[0] - p0[0]) ** 2

# Function to check the determinant of a 3x3 matrix
def determinant(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

# Function to sort points by polar angle and distance
def sort_points(points, start):
    return sorted(points, key=lambda p: (calculate_angle(start, p), calculate_distance_squared(start, p)))

# Graham's algorithm to find the convex hull
def graham_scan(points):
    start = min(points, key=lambda p: (p[1], p[0]))
    sorted_points = sort_points([p for p in points if p != start], start)

    hull = [start, sorted_points[0]]
    for p in sorted_points[1:]:
        while len(hull) > 1 and determinant(hull[-2], hull[-1], p) <= 0:
            hull.pop()
        hull.append(p)

    return hull

# Function to generate random points
def generate_points(num=4, min_val=-50, max_val=50):
    return [[randint(min_val, max_val), randint(min_val, max_val)] for _ in range(num)]

# Function to input coordinates from the user
def input_coordinates():
    points = []
    answer = input("Do you want to input your own coordinates? (yes/no): ").strip().lower()
    if answer == 'yes':
        for i in range(4):
            x = float(input(f"Enter {i+1} X coordinate: "))
            y = float(input(f"Enter {i+1} Y coordinate: "))
            points.append([x, y])
    else:
        points = generate_points()
    return points

# Main part of the program
if __name__ == "__main__":
    points = input_coordinates()
    print("Coordinates:", points)
    plot_graph(points)
    hull = graham_scan(points)
    plot_graph(points, hull)
    print("Convex hull coordinates:", hull)
    prefix = "The convex hull is "
    print(len(hull))
    if len(hull) == 2:
        print(prefix + "a point")
    elif len(hull) == 3:
        print(prefix + "a line segment")
    elif len(hull) == 4:
        print(prefix + "a triangle")
    elif len(hull) == 5:
        print(prefix + "a quadrilateral")
    print("End of program")
