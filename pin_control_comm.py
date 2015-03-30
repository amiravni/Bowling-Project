import socket
import protocol
from select import select

import config

pin_count_socket = None
image_socket = None
config_socket = None
cmd_socket = None

def init():
    global pin_count_socket
    global image_socket
    global config_socket
    global cmd_socket
    
    pin_count_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    image_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    config_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    config_socket.bind(('',config.COMM_CONFIG_PORT))
    
    cmd_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cmd_socket.bind(('',config.COMM_COMMANDS_PORT))
    
def send_msg(sock,msg,port):
    sock.sendto(msg,(config.HOST_IP, port))

def recv_msg(sock_fd):
    msg,addr = sock_fd.recvfrom(64*1024)
    return msg
    
def send_pin_count(pin_count,speed):
    global pin_count_socket
    send_msg(pin_count_socket,protocol.encode_pin_count_msg(pin_count,speed),config.COMM_PIN_COUNT_PORT)
    
def send_jpeg_image(jpeg_image):
    global image_socket
    send_msg(image_socket,protocol.encode_jpeg_image(jpeg_image),config.COMM_IMAGE_PORT)

def is_ready(sock):
    return  len(select([sock], [], [],0)[0]) > 0    

def cmd_sock_is_ready():
    return is_ready(cmd_socket)
    
def recv_cmd_sock():
    cmd = recv_msg(cmd_socket)
    return protocol.decode_cmd_msg(cmd)   
    
def main():
    global pin_count_socket
    global image_socket
    global config_socket
    init()
    #pin_count,speed
    send_pin_count(5,10)
    
if __name__ == "__main__":
    main()