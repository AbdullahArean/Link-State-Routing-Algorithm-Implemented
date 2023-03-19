import sys
import socket as s
import time
import threading
import pickle
from collections import defaultdict
from math import inf
import datetime as dt
from typing import Dict, List, Any, Union
import copy
import random

arg_num = 2
file_name = 1
name_router = 0
parent_port = 1
port_child = 2
distance = 1
update_interval = 1
router_update_interval = 15
server_name = 'localhost'


class NodeRouter:
    def __init__(self, name, port, neighbours_list):
        self.name = name
        self.port = port
        self.neigh = neighbours_list
        self.msg = None
        self.preve_sent_msg_seq = defaultdict(int)
        self.global_time_st = defaultdict(float)
        self.global_routers = defaultdict(list)

    def neighbour_add(self, neighbour):
        self.neigh.append(neighbour)
        self.global_routers[self.name].append(neighbour)

    def mesg_set(self, msg):
        self.msg = msg

    def add_prev_seq(self, msg):
        self.preve_sent_msg_seq[msg.name] = msg.seq_num

    def chk_prev_seq(self, msg):
        return self.preve_sent_msg_seq[msg.name] != msg.seq_num

    def add_timestamp(self, msg):
        self.global_time_st[msg.name] = msg.timestamp

    def chk_timestamp(self, msg):
        return self.global_time_st[msg.name] != msg.timestamp

    def update_global_routers(self, msg):
        if len(self.global_routers[msg.name]) > 0:
            for neighbour in msg.neigh:
                present = False
                for present_neighbour in self.global_routers[msg.name]:
                    if present_neighbour.port == neighbour.port \
                            and present_neighbour.name == neighbour.name \
                            and present_neighbour.distance == neighbour.distance:
                        present = True
                if not present:
                    self.global_routers[msg.name].append(neighbour)
        else:
            for neighbour in msg.neigh:
                self.global_routers[msg.name].append(neighbour)

    def check_neighbour_alive(self, msg):
        for neighbour in msg.neigh:
            if neighbour.name == self.name:
                present = False
                for my_neighbour in self.neigh:
                    if my_neighbour.name == msg.name:
                        present = True
                if not present:
                    to_be_added = Neighbours(msg.name, msg.port, neighbour.distance)
                    self.neigh.append(to_be_added)
                    self.global_routers[self.name].append(to_be_added)


class LinkStatePacket:
    def __init__(self, sender: NodeRouter):
        self.port = sender.port
        self.name = sender.name
        self.neigh = sender.neigh
        self.seq_num = 0
        self.timestamp = dt.datetime.now().timestamp()
        self.last_send = sender.name

    def increment_sequence_number(self):
        self.seq_num += 1


class Neighbours:
    def __init__(self, name, port, distance):
        self.name = name
        self.port = port
        self.distance = distance


class Edge:
    def __init__(self, u, v, weight):
        self.start = u
        self.end = v
        self.weight = weight


class Graph:
    def __init__(self, global_routers):
        self.global_routers = global_routers
        self.graph = defaultdict(list)
        self.parse(self.global_routers)

    def parse(self, global_routers):
        for router, neigh in global_routers.items():
            parent = router
            for child in neigh:
                self.graph[parent].append(Edge(parent, child.name, child.distance))


def calculate_paths_activator():
    while True:
        for key, value in parent_router.global_routers.items():
            if(key==parent_router.name):
                print(f"NodeRouter {key}:")
                for neighbour in value:
                    print(f"  - Name: {neighbour.name}, Port: {neighbour.port}, Distance: {neighbour.distance}")
        time.sleep(router_update_interval)
        dijkstra_calculate_path()
        
        # select a this router name from the global_routers dictionary
        router_name = parent_router.name
        # select a random neighbour of the router
        neighbour_index = random.randint(0, len(parent_router.global_routers[router_name])-1)
        # change the cost of the neighbour's link
        new_cost = random.randint(1, 10)
        parent_router.global_routers[router_name][neighbour_index].distance = new_cost


def dijkstra_calculate_path():
    # Copying the parent router object
    _parent_router = parent_router

    # Indices for accessing calculation_table values
    weight = 0
    visited_status = 1
    parent_ = 2

    # Creating a new graph object from the parent router's global routers
    g = Graph(_parent_router.global_routers)

    # A dictionary to store the current least cost and visited status for each router
    calculation_table: Dict[Any, List[Union[float, bool]]] = {}

    # Initializing the calculation_table with initial values
    total_routers = 0
    for router in _parent_router.global_routers:
        if router != _parent_router.name:
            # filling all the table with name of router
            calculation_table[router] = [inf, False, None]
        else:
            # set the parent router's least cost to itself to 0
            calculation_table[router] = [0.0, True, None]
        total_routers += 1

    # Counter for counting number of routers visited so far
    counter = 0

    # Print the current router's name
    print(f'I am NodeRouter {_parent_router.name}')

    # Set the current router to the parent router
    current_router = _parent_router.name

    # Initialize variables for storing the routers visited and the corresponding hops taken
    printing_routers = _parent_router.name
    printing_list = []

    # While all routers haven't been visited
    while counter != total_routers-1:
        # For all edges from the current router
        for edge in g.graph[current_router]:
            # For each router in the calculation_table
            for node, weight_status in calculation_table.items():
                # If the router is the edge's end and hasn't been visited yet and has a higher cost than the current path
                if node == edge.end and not weight_status[visited_status] and calculation_table[node][weight] > calculation_table[current_router][weight] + float(edge.weight):
                    # Update the least cost for the router
                    calculation_table[node][weight] = calculation_table[current_router][weight] + float(edge.weight)
                    # Set the parent for the router to the current router
                    calculation_table[node][parent_] = edge.start

        # Find the router with the minimum least cost that hasn't been visited yet
        min_weight = inf
        min_node = ''
        for node, weight_status in calculation_table.items():
            if weight_status[weight] < min_weight and weight_status[visited_status] == False:
                min_node = node
                min_weight = weight_status[weight]

        # If a router was found
        if min_node != '':
            # Set the visited status of the router to True
            calculation_table[min_node][visited_status] = True
            # Set the current router to the newly found router
            current_router = min_node
            # Increment the counter
            counter += 1
            # Append the router to the list of visited routers
            printing_list.append(min_node)
            # Append the router to the string of routers visited so far
            printing_routers = printing_routers + min_node

    # Print the hops and the corresponding cost for each visited router
    for node in printing_list:
        hops = node
        current_parent = calculation_table[node][parent_]
        while current_parent is not None:
            hops = hops + current_parent
            current_parent = calculation_table[current_parent][parent_]
        print(f'Least cost path to router {node}:{hops[::-1]} and the cost is {calculation_table[node][weight]:.1f}')


def udp_client(_parent_router: NodeRouter):
    client_socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
    while True:
        for child in _parent_router.neigh:
            _parent_router.msg.timestamp = dt.datetime.now().timestamp()
            message_to_send = pickle.dumps(_parent_router.msg)
            server_port = int(child.port)
            client_socket.sendto(message_to_send, (server_name, server_port))
        time.sleep(update_interval)
        _parent_router.msg.increment_sequence_number()


def chk_prev_seq(msg: LinkStatePacket, _parent_router: NodeRouter):
    return _parent_router.preve_sent_msg_seq[msg.name] < msg.seq_num


def check_previous_sent_timestamp(msg: LinkStatePacket, _parent_router: NodeRouter):
    return _parent_router.global_time_st[msg.name] < msg.timestamp


def udp_server(_parent_router: NodeRouter):
    server_port = int(_parent_router.port)
    server_socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
    server_socket.bind((server_name, server_port))
    client_socket = s.socket(s.AF_INET, s.SOCK_DGRAM)

    while True:
        msg, client_address = server_socket.recvfrom(2048)
        received_message: LinkStatePacket = pickle.loads(msg, fix_imports=True, encoding="utf-8", errors="strict")

        last_send = copy.deepcopy(received_message.last_send)
        for neighbour in _parent_router.neigh:
            # dont send to the previous sender
            if last_send != neighbour.name and check_previous_sent_timestamp(received_message, _parent_router):
                received_message.last_send = copy.deepcopy(_parent_router.name)
                client_socket.sendto(pickle.dumps(received_message), (server_name, int(neighbour.port)))
        _parent_router.add_prev_seq(received_message)
        _parent_router.add_timestamp(received_message)
        _parent_router.check_neighbour_alive(received_message)
        _parent_router.update_global_routers(received_message)


def check_if_neighbours_alive(_parent_router: NodeRouter):
    neighbours_to_remove = None
    for neighbour in _parent_router.neigh:
        if dt.datetime.now().timestamp() - _parent_router.global_time_st[neighbour.name] > 3:
            # remove from LSA
            neighbours_to_remove = neighbour.name

            # remove from global key
            # remove from global values
    if neighbours_to_remove is not None:
        _parent_router.global_routers.pop(neighbours_to_remove, None)
        for neighbour in _parent_router.neigh:
            if neighbours_to_remove == neighbour.name:
                _parent_router.neigh.remove(neighbour)
                break


def not_my_neighbour(router, _parent_router):
    for neighbour in _parent_router.neigh:
        if router == neighbour.name:
            return False
    return True


def check_if_non_neighbours_alive(_parent_router: NodeRouter):
    router_to_remove = None
    for router, all_neighbours in _parent_router.global_routers.items():
        if not_my_neighbour(router, _parent_router) and router != _parent_router.name:
            if dt.datetime.now().timestamp() - _parent_router.global_time_st[router] > 12:
                router_to_remove = router
    if router_to_remove is not None:
        _parent_router.global_routers.pop(router_to_remove, None)


def check_alive(_parent_router: NodeRouter):
    while True:
        time.sleep(3)
        check_if_neighbours_alive(_parent_router)
        check_if_non_neighbours_alive(_parent_router)


if len(sys.argv) == arg_num:
    f = open(sys.argv[file_name], "r")
    line_counter = 0
    number_of_neighbour = 0
    parent_router: NodeRouter
    list_file = []
    for line in f:
        list_file.append(line.split())
    for i in range(len(list_file)):
        # First line will always be Parent router
        if i == 0:
            parent_router = NodeRouter(list_file[i][name_router], list_file[i][parent_port], [])

        # Second line will always be the number of neigh
        elif i == 1:
            number_of_neighbour = list_file[i]  # TODO not using right now

        # From 3 onwards it will be the child routers
        elif i > 1:
            child_router = Neighbours(list_file[i][name_router], list_file[i][port_child], list_file[i][distance])
            parent_router.neighbour_add(child_router)
        line_counter += 1

    parent_router.mesg_set(LinkStatePacket(parent_router))
    client_thread = threading.Thread(target=udp_client, args=(parent_router,))
    server_thread = threading.Thread(target=udp_server, args=(parent_router,))
    calculation_thread = threading.Thread(target=calculate_paths_activator)
    check_alive_thread = threading.Thread(target=check_alive, args=(parent_router,))
    client_thread.start()
    server_thread.start()
    calculation_thread.start()
    check_alive_thread.start()
