import csv
from queue import PriorityQueue
from collections import defaultdict


class CityNotFoundError(Exception):
    def __init__(self, city):
        print("%s does not exist" % city)


class SameCityError(Exception):
    def __init__(self):
        print("Your Current and Destination cities should be different")


# Implement this function to read data into an appropriate data structure.
def build_graph(path):
    # initialize the graph
    graph = Graph()
    all_cities = []
    with open(path, newline='', encoding="utf8") as roadMap:
        reader = csv.DictReader(roadMap)
        for row in reader:
            city1 = row['city1']
            city2 = row['city2']
            distance = row['distance']

            if city1 not in all_cities:
                all_cities.append(city1)
            if city2 not in all_cities:
                all_cities.append(city2)

            graph.edges[city1].append(city2)
            graph.edges[city2].append(city1)
            graph.costs[get_cost_key(city1, city2)] = distance
    return graph, all_cities


# Implement this function to perform uniform cost search on the graph.
def uniform_cost_search(graph, start, end):
    frontier = PriorityQueue()
    explored = set()
    frontier.put((0, start, [start]))

    while frontier.not_empty:
        cost, state, path_to_goal = frontier.get()
        explored.add(state)

        if state == end:
            lowest_cost = cost
            print("The shortest path for you: " + str(path_to_goal))
            print("Distance = " + str(lowest_cost))
            return "Goal found"

        for neighbor in graph.neighbors(state):
            if neighbor not in explored:
                neighbor_cost = cost + int(graph.get_cost(state, neighbor))
                frontier.put((neighbor_cost, neighbor, path_to_goal + [neighbor]))

    return "Failure"


# Implementation of a Bi-directional Graph data structure
class Graph:
    # Edges holds a dictionary of every city associated with a list of its neighbors
    # Costs holds the distance between each 2 connected cities
    def __init__(self):
        self.edges = defaultdict(list)
        self.costs = {}

    # Function to get the neighbor cities of a city
    def neighbors(self, vertex):
        return self.edges[vertex]

    # Function to get the distance between 2 cities
    def get_cost(self, start, end):
        return self.costs[(get_cost_key(start, end))]


# Helper function to name the edge between 2 cities
def get_cost_key(city1, city2):
    words = [city1, city2]
    # get the alphabetical order of the 2 cities
    words.sort()
    key = words[0] + words[1]
    return key


# Implement main to call functions with appropriate try-except blocks
if __name__ == "__main__":
    try:
        path = input('Welcome! \nPlease enter the path of the road map file: ').strip()
        graph, all_cities = build_graph(path)

        start = input('Please give your current city: ').strip()
        if start not in all_cities:
            raise CityNotFoundError(start)
        end = input('Please give your destination city: ').strip()
        if end not in all_cities:
            raise CityNotFoundError(end)

        if start == end:
            raise SameCityError

        uniform_cost_search(graph, start, end)
    except FileNotFoundError:
        print("File not found! Please try again")
    except CityNotFoundError:
        print('Please try with a valid City')
    except SameCityError:
        print('Please try with different cities')

    # Handle other exceptions
    except:
        print('An error occurred, Please try again.')
    finally:
        print('Thank you for using our app!')
