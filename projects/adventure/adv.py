from room import Room
from player import Player
from world import World
from util import Stack, Queue

import random
from ast import literal_eval

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
trav_graph = {}
for i in range(len(room_graph)):
    trav_graph[i] = {}

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

# Check to see if there are still unexplored rooms
rooms_unexplored = True
print(len(room_graph))
while rooms_unexplored == True:
    # Pick an unexplored direction and use dft to traverse
    ## Find unexplored directions in current room
    unexplored = []
    current_room = player.current_room
    for direction in current_room.get_exits():
        if direction not in trav_graph[current_room.id]:
            trav_graph[current_room.id][direction] = "?"
            unexplored.append(direction)
        elif trav_graph[current_room.id][direction] == "?":
            unexplored.append(direction)
    # Check if current room has unexplored exits, if it does traverse and log
    ## If length of unexplored >= 2, save the room ID
    # if len(unexplored) >= 2:
    #     last_unexplored = player.current_room.id
    if len(unexplored) > 0:
        direction = random.choice(unexplored)

        # Move and log it in traversal path
        player.travel(direction)
        traversal_path.append(direction)

        # Save the old room and update the current room
        old_room = current_room
        current_room = player.current_room

        # Save the edges in trav_graph
        trav_graph[old_room.id][direction] = current_room.id
        trav_graph[current_room.id][opposite_dir(direction)] = old_room.id

        # Check all exits
        for direction in current_room.get_exits():
            if direction not in trav_graph[current_room.id]:
                trav_graph[current_room.id][direction] = "?"

    # If current room didn't have unexplored exits, try to find the closest room w/ exits
    else:
        q = Queue()
        # Queue a copy of the traversal path
        trav_path_copy = traversal_path.copy()
        q.enqueue(trav_path_copy)
        # Move in the opposite direction while queue size > 0
        while q.size() > 0:
            path = q.dequeue()
            direction = opposite_dir(path[-1])
            # Move and log
            player.travel(direction)
            traversal_path.append(direction)
            # If current room has unexplored exits, break loop
            if "?" in trav_graph[player.current_room.id].values():
                break
            # Else enqueue next move
            else:
                if len(path) > 0:
                    new_path = path.copy()
                    new_path = new_path[:-1]
                    q.enqueue(new_path)
                else:
                    break
        


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
