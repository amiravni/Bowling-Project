import socket
from select import select
import time

import config
import protocol


pin_count_socket = None
image_socket = None

def init():
    global pin_count_socket
    global image_socket

    pin_count_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    pin_count_socket.bind(('', config.COMM_PIN_COUNT_PORT))
    print pin_count_socket
    image_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    image_socket.bind(('', config.COMM_IMAGE_PORT))
    print image_socket

def pin_count_is_ready():
    return  select([pin_count_socket], [], [])
def image_is_ready():
    return  select([image_socket], [], [])

def send_msg(sock,msg,port):
    sock.sendto(msg,(config.HOST_IP, port))

def recv_msg(sock_fd):
    msg,addr = sock_fd.recvfrom(64*1024)
    return msg

def send_pin_count(pin_count):
    send_msg(pin_count_socket,protocol.encode_pin_count_msg(pin_count),config.COMM_PIN_COUNT_PORT)
    
def send_jpeg_image(jpeg_image):
    sock.sendto(image_socket,protocol.encode_jpeg_image(jpeg_image),config.COMM_IMAGE_PORT)

def main():
    global pin_count_socket
    global image_socket
    init()
    while True:
        #if pin_count_is_ready():
        pin_msg  = recv_msg(pin_count_socket)
        
        pin_count,speed = protocol.decode_pin_count_msg(pin_msg)
        print "Pin count is : %d and speed is : %d" % (pin_count,speed)
        
        time.sleep(0.01)
    
if __name__ == "__main__":
    main()