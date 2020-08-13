from room import Room
from player import Player
from world import World
from util import Stack, Queue

import random
from ast import literal_eval
import time


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
# print(trav_graph)
# Traverse through all the rooms, logging everything as we go

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

rooms_to_check = trav_graph.copy()
# Check to see if there are still unexplored rooms
rooms_unexplored = True
while rooms_unexplored == True:
    # Pick an unexplored direction and use dft to traverse
    ## Find unexplored directions in current room
    current_room = player.current_room
    # Check if current room has unexplored exits, if it does traverse and log
    unexplored_dirs = []
    for key in trav_graph[current_room.id]:
        if trav_graph[current_room.id][key] == "?":
            unexplored_dirs.append(key)
    if len(unexplored_dirs) > 0:
        direction = random.choice(unexplored_dirs)

        # Move and log it in traversal path
        player.travel(direction)
        traversal_path.append(direction)

        # Save the old room and update the current room
        old_room = current_room
        current_room = player.current_room

        # Save the edges in trav_graph
        trav_graph[old_room.id][direction] = current_room.id
        trav_graph[current_room.id][opposite_dir(direction)] = old_room.id

        # Check if the old room has unexplored exits, if not then delete it from rooms_to_check
        if "?" not in trav_graph[old_room.id].values():
            rooms_to_check.pop(old_room.id, None)
        # Check if the current room has unexplored exits, if not then delete it from rooms_to_check
        if "?" not in trav_graph[current_room.id].values():
            rooms_to_check.pop(current_room.id, None)

    # If current room didn't have unexplored exits, try to find the closest room w/ exits
    else:
        q = Queue()        
        q.enqueue([opposite_dir(traversal_path[-1])])

        # Move along the path while queue size > 0
        while q.size() > 0:
            path = q.dequeue()
            checked_room = current_room.id

            # If queued room has unexplored exits, move+log, and break loop
            for move in path:
                checked_room = trav_graph[checked_room][move]
            if checked_room in rooms_to_check:
                # Move and log
                for move in path:
                    player.travel(move)
                    traversal_path.append(move)
                break
            # Else enqueue next move
            else:
                for d in trav_graph[checked_room].keys():
                    new_path = path.copy()
                    new_path.append(d)
                    q.enqueue(new_path)

    # Check if we need to make rooms_unexplored False
    rooms_unexplored = any("?" in direction.values() for direction in trav_graph.values())

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
