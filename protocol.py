import struct

START_CALIB_CMD = 'start_calib'
START_GAME_CMD = 'start_game'
STOP_GAME_CMD = 'stop_game'
CALIB_RESULT_CMD = 'calib_result'

def encode_pin_count_msg(pin_count,speed):
    return struct.pack('Bd',pin_count,speed)

def encode_jpeg_image(image):
    return image

def encode_cmd_msg(msg):
    return msg
    
def decode_throw_info_msg(msg):
    return struct.unpack('Bd',msg)

def decode_jpeg_image(msg):
    return msg
    
def decode_cmd_msg(msg):
    return msg