import struct


def encode_pin_count_msg(pin_count,speed):
    return struct.pack('BB',pin_count,speed)

def encode_jpeg_image(image):
    return image
    
def decode_pin_count_msg(msg):
    return struct.unpack('BB',msg)

def decode_jpeg_image(msg):
    return msg