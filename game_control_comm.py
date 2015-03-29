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

def is_ready(sock):
    return  len(select([sock], [], [],0)[0]) > 0


def send_msg(sock,msg,port):
    sock.sendto(msg,(config.HOST_IP, port))

def recv_msg(sock_fd):
    msg,addr = sock_fd.recvfrom(64*1024)
    return msg

def main():
    global pin_count_socket
    global image_socket
    
    init()
    
    while True:

        if is_ready(pin_count_socket):
            pin_msg  = recv_msg(pin_count_socket)
        
            pin_count,speed = protocol.decode_pin_count_msg(pin_msg)
            print "Pin count is : %d and speed is : %f" % (pin_count,speed)

        if is_ready(image_socket):
            img_msg = recv_msg(image_socket)
            img = protocol.decode_jpeg_image(img_msg)
            img_fd = open('base_image_game_control.jpg','wb')
            img_fd.write(img)
            img_fd.close()
        time.sleep(0.01)

if __name__ == "__main__":
    main()