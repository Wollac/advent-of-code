"""
--- Day 25: Cryostasis ---
https://adventofcode.com/2019/day/25
"""
from collections import deque
from enum import Enum
from itertools import chain, combinations

import aocd
import networkx as nx
import regex as re

from .intcode import IntComputer

PROGRAM = [int(n) for n in aocd.data.split(",")]

NAME = re.compile(r"^== (.*) ==", re.MULTILINE)
DESCRIPTION = re.compile(r"==\n(.*)\n", re.MULTILINE)
DOORS = re.compile(r"^Doors here lead:\n(?:- (.+)\n)*", re.MULTILINE)
ITEMS = re.compile(r"^Items here:\n(?:- (.+)\n)*", re.MULTILINE)
TAKE = re.compile(r"^You take the (.+).", re.MULTILINE)
DROP = re.compile(r"^You drop the (.+).", re.MULTILINE)
PASSWORD = re.compile(r"You should be able to get in by typing (\d+)", re.MULTILINE)

DIRECTIONS = {"north": (0, -1), "south": (0, 1), "west": (-1, 0), "east": (1, 0)}
INVERSE = {"north": "south", "south": "north", "east": "west", "west": "east"}

# do not pick up these items
BLACKLIST = [
    "photons",
    "infinite loop",
    "molten lava",
    "giant electromagnet",
    "escape pod",
]


def powerset(s: set) -> iter:
    s = s.copy()
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


class State(Enum):
    EXPLORE = 1
    CHECKPOINT = 2
    COMBINE = 3
    TRY = 4


class Room:
    def __init__(self, output):
        self.name = NAME.search(output)[1]
        self.description = DESCRIPTION.search(output)[1]
        self.doors = list(m.captures(1)) if (m := DOORS.search(output)) else []
        self.items = list(m.captures(1)) if (m := ITEMS.search(output)) else []


class Game:
    def __init__(self):
        self.comp = IntComputer(PROGRAM)
        self.comp.input = self
        self.command = deque()
        self.graph = nx.DiGraph()
        self.prev_direction = None
        self.room = None
        self.state = State.EXPLORE
        self.inventory = set()
        self.combinations = None

    def step(self):
        output = "".join([chr(c) for c in self.comp.output])
        self.comp.output.clear()
        # print(output)

        if TAKE.search(output):
            for m in TAKE.finditer(output):
                item = m[1]
                self.inventory.add(item)
                self.room.items.remove(item)

        if DROP.search(output):
            for m in DROP.finditer(output):
                item = m[1]
                self.inventory.remove(item)
                self.room.items.append(item)

        if NAME.search(output):
            room = Room(output)
            if not self.graph.has_node(room.name):
                # add a node to the graph, if it is a new room
                self.graph.add_node(room.name, room=room)
                if self.room:
                    self.graph.remove_node((self.room.name, self.prev_direction))
                    self.graph.add_edge(self.room.name, room.name, dir=self.prev_direction)
                    self.graph.add_edge(room.name, self.room.name, dir=INVERSE[self.prev_direction])

                adj = {data["dir"]: n for n, data in self.graph.adj[room.name].items()}
                for door in room.doors:
                    if door not in adj:
                        tmp = (room.name, door)
                        self.graph.add_edge(room.name, tmp, dir=door)
                        self.graph.add_edge(tmp, "UNVISITED", dir="")

            # we go ejected from the floor, so we are at the checkpoint again
            if room.name == "Pressure-Sensitive Floor" and "ejected" in output:
                self.room = self.graph.nodes["Security Checkpoint"]["room"]
            else:
                self.room = self.graph.nodes[room.name]["room"]

        if self.state == State.EXPLORE and self.graph.degree("UNVISITED") == 0:
            self.state = State.CHECKPOINT  # everything explored, go to the checkpoint
        if self.state == State.CHECKPOINT and self.room.name == "Security Checkpoint":
            self.state = State.COMBINE  # reached the checkpoint, try combinations

        if self.state == State.EXPLORE:
            # pick any remaining item
            if item := next((item for item in self.room.items if item not in BLACKLIST), None):
                return f"take {item}"
            # walk towards the closest not yet visited room
            path = nx.shortest_path(self.graph, self.room.name, "UNVISITED")
            return self.graph.get_edge_data(path[0], path[1])["dir"]

        elif self.state == State.CHECKPOINT:
            path = nx.shortest_path(self.graph, self.room.name, "Security Checkpoint")
            return self.graph.get_edge_data(path[0], path[1])["dir"]

        elif self.state == State.COMBINE:
            if not self.combinations:
                self.combinations = powerset(self.inventory)
            # try the next combination
            combination = set(next(self.combinations))
            self.state = State.TRY
            return "\n".join(chain(
                (f"drop {item}" for item in self.inventory - combination),
                (f"take {item}" for item in combination - self.inventory))
            )

        elif self.state == State.TRY:
            path = nx.shortest_path(self.graph, self.room.name, "Pressure-Sensitive Floor")
            self.state = State.COMBINE
            return self.graph.get_edge_data(path[0], path[1])["dir"]

    def popleft(self):
        if not self.command:
            input_str = self.step()
            # print(input_str)

            if input_str in DIRECTIONS:
                self.prev_direction = input_str

            self.command = deque(ord(c) for c in input_str + "\n")

        return self.command.popleft()

    def play(self):
        output = self.comp.run()
        return "".join([chr(c) for c in output])


game = Game()
result = game.play()
print(result)

password = PASSWORD.search(result)[1]
print("Part One:", password)
