import socket as s
import pickle
import copy
from LinkStatePacket import LinkStatePacket
from PathCalculation import *


def chk_prev_seq(msg: LinkStatePacket, _parent_router: NodeRouter):
    return _parent_router.preve_sent_msg_seq[msg.name] < msg.seq_num


def check_previous_sent_timestamp(msg: LinkStatePacket, _parent_router: NodeRouter):
    return _parent_router.global_time_st[msg.name] < msg.timestamp


def server_receiver_sender_udp(_parent_router: NodeRouter):
    server_port = int(_parent_router.port)
    server_socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
    server_socket.bind((server_name, server_port))
    client_socket = s.socket(s.AF_INET, s.SOCK_DGRAM)

    while True:
        msg, client_address = server_socket.recvfrom(2048)
        received_message: LinkStatePacket = pickle.loads(msg, fix_imports=True, encoding="utf-8", errors="strict")

        last_sent_message = copy.deepcopy(received_message.last_sent_message)
        for neighbour in _parent_router.neigh:
            # dont send to the previous sender
            if last_sent_message != neighbour.name and check_previous_sent_timestamp(received_message, _parent_router):
                received_message.last_sent_message = copy.deepcopy(_parent_router.name)
                client_socket.sendto(pickle.dumps(received_message), (server_name, int(neighbour.port)))
        _parent_router.add_prev_seq(received_message)
        _parent_router.add_timestamp(received_message)
        _parent_router.check_neighbour_alive(received_message)
        _parent_router.update_global_routers(received_message)
