import sys
import time
import collections
from tkinter import *
from math import pi , acos , sin , cos
from heapq import heappop, heappush

#Each node will have (x, y, connected graphs, Name)

nodes = dict()
name_to_index = dict()

def get_nodes():
    input = list(open("rrNodes.txt"))
    for line in input:
        line = line.replace("\n", "")
        index, y, x = line.split(" ")
        nodes[int(index)] = [float(x), float(y), set(), ""]
    input = list(open("rrNodeCity.txt"))
    for line in input:
        line = line.replace("\n", "")
        split_index = line.find(" ")
        split_index = int(split_index)
        index = int(line[0:split_index])
        city = line[split_index + 1:]
        nodes[index][3] = city
        name_to_index[city] = index

def calcd(y1,x1, y2,x2):
   R   = 3958.76 # miles = 6371 km
   y1 *= pi/180.0
   x1 *= pi/180.0
   y2 *= pi/180.0
   x2 *= pi/180.0
   # approximate great circle distance with law of cosines
   return acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * R

def get_adjacenceis():
    input = list(open("rrEdges.txt"))
    for line in input:
        line = line.replace("\n", "")
        index1, index2 = line.split(" ")
        index1 = int(index1)
        index2 = int(index2)
        distance = calcd(nodes[index1][1], nodes[index1][0], nodes[index2][1], nodes[index2][0])
        nodes[index1][2].add((index2, distance))
        nodes[index2][2].add((index1, distance))

# while len(fringe) > 0:
#     pull node of heap
#     if node in visited:
#         continue
#     visited.add(node)
#     generate children

def diakstra(start, end):
    # each tuple will have (total distance, index, ancestors - list)
    num_visited = 0
    try:
        if start == end:
            print("Error: Start and end locations are the same.")
        else:
            fringe = collections.deque()
            start_state = (0.0, name_to_index[start], set())
            fringe = [start_state]
            visited = set()
            while fringe:
                state = heappop(fringe)
                if nodes[state[1]][3] == end:
                    return state[0]
                if state[1] in visited:
                    continue
                else:
                    visited.add(state[1])
                    weighted_nodes = nodes[state[1]][2]
                    for node in weighted_nodes:
                        child, weight = node
                        set_1 = set()
                        set_1.add(state[1])
                        set_2 = state[2].union(set_1)
                        child_tuple = (weight + state[0], child, set_2)
                        heappush(fringe, child_tuple)
                        num_visited += 1
            return None
    except MemoryError:
        return ("Memory Error.", num_visited)

def distance(start, end):
    return calcd(nodes[start][1], nodes[start][0], nodes[end][1], nodes[end][0])

def AStar(start, end):
    # each tuple will have (total distance + huerestic, index, ancestors - list, total distance)
    num_visited = 0
    try:
        if start == end:
            print("Error: Start and end locations are the same.")
        else:
            fringe = collections.deque()
            start_index = name_to_index[start]
            end_index = name_to_index[end]
            start_state = (distance(start_index, end_index), name_to_index[start], set(), 0.0)
            fringe = [start_state]
            visited = set()
            while fringe:
                state = heappop(fringe)
                if nodes[state[1]][3] == end:
                    return state[0]
                if state[1] in visited:
                    continue
                else:
                    visited.add(state[1])
                    weighted_nodes = nodes[state[1]][2]
                    for node in weighted_nodes:
                        child, weight = node
                        set_1 = set()
                        set_1.add(state[1])
                        set_2 = state[2].union(set_1)
                        child_tuple = ((weight + state[3]) + distance(child, end_index), child, set_2, weight + state[3])
                        heappush(fringe, child_tuple)
                        num_visited += 1
            return None
    except MemoryError:
        return ("Memory Error.", num_visited)

def draw_map():
    root = Tk()
    C = Canvas(root, height = "500", width = "1000")
    for index, location in nodes.items():
        x1 = abs(location[0])
        x1 *= 7
        x1 = 1000 - x1
        y1 = abs(location[1])
        y1 *= 7
        y1 = 500 - y1
        connections = nodes[index][2]
        for connection in connections:
            x2 = abs(nodes[connection[0]][0])
            x2 *= 7
            x2 = 1000 - x2
            y2 = abs(nodes[connection[0]][1])
            y2 *= 7
            y2 = 500 - y2
            C.create_line(x1,y1,x2,y2)
    C.pack()
    root.mainloop()


get_nodes()
get_adjacenceis()

# start = sys.argv[1]
# end = sys.argv[2]
start = "Ciudad Juarez"
end = "Montreal"
start_time = time.process_time()
shortet_path = diakstra(start, end)
end_time = time.process_time()
print("Diakstra:", shortet_path, end_time - start_time)
start_time = time.process_time()
shortet_path = AStar(start, end)
end_time = time.process_time()
print("AStar:", shortet_path, end_time - start_time)

draw_map()