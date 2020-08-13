from room import Room
from player import Player
from world import World
from util import Stack, Queue

import random
from ast import literal_eval
import time

def opposite_dir(d):
    """
    Returns the oppsite of a given direction
    """
    if d == "n":
        return "s"
    elif d == "e":
        return "w"
    elif d == "s":
        return "n"
    elif d == "w":
        return "e"

def unexplored_directions(room, trav_graph):
    """
    Returns list of unexplored directions for a room
    """
    unexplored = []
    for direction in trav_graph[room]:
        if trav_graph[room][direction] == "?":
            unexplored.append(direction)
    return unexplored

def dft(starting_room, trav_graph, traversal_path, player):
    while len(unexplored_directions(player.current_room.id, trav_graph)) > 0:
        direction = random.choice(unexplored_directions(player.current_room.id, trav_graph))
        move_player(player, trav_graph, traversal_path, [direction])
    return

def move_player(player, trav_graph, traversal_path, path):
    for direction in path:
        starting_room = player.current_room.id
        player.travel(direction)
        traversal_path.append(direction)
        new_room = player.current_room.id
        trav_graph[starting_room][direction] = new_room
        trav_graph[new_room][opposite_dir(direction)] = starting_room
    return

def bfs(starting_room, player, trav_graph, traversal_path):
    q = Queue()
    visited = set()
    for d in trav_graph[starting_room]:
        q.enqueue((trav_graph[starting_room][d], [d]))
    while q.size() > 0:
        room, path = q.dequeue()
        visited.add(room)
        # print(q.queue)
        if room == "?":
            move_player(player, trav_graph, traversal_path, path)
            return
        else:
            for d in trav_graph[room]:
                if trav_graph[room][d] not in visited:
                    new_path = path.copy()
                    new_path.append(d)
                    q.enqueue((trav_graph[room][d], new_path))


# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = r"projects\adventure\maps\test_line.txt"
# map_file = r"projects\adventure\maps\test_cross.txt"
# map_file = r"projects\adventure\maps\test_loop.txt"
# map_file = r"projects\adventure\maps\test_loop_fork.txt"
map_file = r"projects\adventure\maps\main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

fewest_moves = 2000
counter = 0
# Adjust number counter needs to be less than to determine how many times it runs
while counter < 100000:
    player = Player(world.starting_room)

    # Fill this out with directions to walk
    # traversal_path = ['n', 'n']
    traversal_path = []
    # Create a traversal graph
    ## Key = each room in the world, value = what's in each direction
    ### Set value of all available exits/directions to "?"
    all_rooms = world.rooms
    unexplored_rooms = {ID: room.get_exits() for ID, room in all_rooms.items()}
    trav_graph = {}
    for i in range(len(room_graph)):
        trav_graph[i] = {}
        for val in unexplored_rooms[i]:
            trav_graph[i][val] = "?"

    # Check to see if there are still unexplored rooms
    rooms_unexplored = True
    while rooms_unexplored == True:
        dft(player.current_room.id, trav_graph, traversal_path, player)
        if any("?" in direction.values() for direction in trav_graph.values()):
            bfs(player.current_room.id, player, trav_graph, traversal_path)

        # Check if we need to make rooms_unexplored False
        rooms_unexplored = any("?" in direction.values() for direction in trav_graph.values())
    visited_rooms = set()
    player.current_room = world.starting_room
    visited_rooms.add(player.current_room)

    for move in traversal_path:
        player.travel(move)
        visited_rooms.add(player.current_room)
    if len(traversal_path) < fewest_moves:
        fewest_moves = len(traversal_path)
        shortest_path = traversal_path.copy()
    counter += 1

# print(trav_graph)


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")
print(f"Fewest moves: {fewest_moves}")
print(f"Shortest path: {shortest_path}")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
