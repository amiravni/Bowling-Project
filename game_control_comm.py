import socket
from select import select
import time

import config
import protocol


throw_info_socket = None
image_socket = None
cmd_socket = None

def init():
    global throw_info_socket
    global image_socket
    global cmd_socket
    
    throw_info_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    throw_info_socket.bind(('', config.COMM_PIN_COUNT_PORT))

    image_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    image_socket.bind(('', config.COMM_IMAGE_PORT))
    
    cmd_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def is_ready(sock):
    return  len(select([sock], [], [],0)[0]) > 0

def throw_info_is_ready():
    return is_ready(throw_info_socket)

def image_is_ready():
    return is_ready(image_socket)
    
def send_msg(sock,msg,port):
    sock.sendto(msg,(config.HOST_IP, port))

def send_cmd_msg(msg):
    cmd_msg = protocol.encode_cmd_msg(msg)
    send_msg(cmd_socket,cmd_msg,config.COMM_COMMANDS_PORT)

def send_calib_data(calib_data):
    msg = 'calib_result,%s'% calib_data    
    send_msg(cmd_socket,msg,config.COMM_COMMANDS_PORT)

def recv_msg(sock_fd):
    msg,addr = sock_fd.recvfrom(64*1024)
    return msg
    
def recv_throw_info():
    throw_info = protocol.decode_throw_info_msg(recv_msg(throw_info_socket))
    return throw_info
    
def recv_image():
    img = protocol.decode_jpeg_image(recv_msg(image_socket))
    return img
    
def main():
    pass

if __name__ == "__main__":
    main()