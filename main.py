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
    def get_float(prompt):
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("Invalid input. Please enter a float number.")

    points = []
    answer = input("Do you want to input your own coordinates? (yes/no): ").strip().lower()
    if answer == 'yes':
        for i in range(4):
            x = get_float(f"Enter X {i+1} coordinate: ")
            y = get_float(f"Enter Y {i+1} coordinate: ")
            points.append([x, y])
    else:
        points = generate_points()
    return points


# Main part of the program
points = input_coordinates()
print("Coordinates:", points)
plot_graph(points)
hull = graham_scan(points)
plot_graph(points, hull)
hull.pop()
print("Convex hull coordinates:", hull)
prefix = "The convex hull is "
    
shapes = {1: "a point", 2: "a line segment", 3: "a triangle", 4: "a quadrilateral"}
print(prefix + shapes.get(len(hull), "an unknown shape"))