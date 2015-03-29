import socket
import config
import protocol

pin_count_socket = None
image_socket = None
config_socket = None

def init():
    global pin_count_socket
    global image_socket
    global config_socket
    pin_count_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    image_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    config_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    config_socket.bind(('',config.COMM_CONFIG_PORT))

    
def send_msg(sock,msg,port):
    sock.sendto(msg,(config.HOST_IP, port))
    
def send_pin_count(pin_count,speed):
    global pin_count_socket
    send_msg(pin_count_socket,protocol.encode_pin_count_msg(pin_count,speed),config.COMM_PIN_COUNT_PORT)
    
def send_jpeg_image(jpeg_image):
    global image_socket
    send_msg(image_socket,protocol.encode_jpeg_image(jpeg_image),config.COMM_IMAGE_PORT)

def main():
    global pin_count_socket
    global image_socket
    global config_socket
    init()
    #pin_count,speed
    send_pin_count(5,10)
    
if __name__ == "__main__":
    main()