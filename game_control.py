#----------------------------------------------------------------------
# A very simple wxPython example.  Just a wx.Frame, wx.Panel,
# wx.StaticText, wx.Button, and a wx.BoxSizer, but it shows the basic
# structure of any wxPython application.
#----------------------------------------------------------------------
 
import wx
import thread
import game_control_comm
import protocol
import get_pins_position
import calculate_pins
import game_setup
import zmq
import config
import time
from calc_score import NewGame
import struct
import numpy as np

port = config.GAME_CONTROL_PORT
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind("tcp://*:%s" % port)

class MyFrame(wx.Frame):
    """
    This is MyFrame.  It just shows a few controls on a wxPanel,
    and has a simple menu.
    """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title,
                          pos=(150, 150), size=(640, 480))

        self.CreateStatusBar()
        # Now create the Panel to put the other controls on.
        panel = wx.Panel(self)

        btn_start_calib = wx.Button(panel, -1, "Start calib")
        btn_check_calib = wx.Button(panel, -1, "check calib")

        btn_start_game = wx.Button(panel, -1, "Start game")
        btn_stop_game = wx.Button(panel, -1, "Stop game")
                
        # bind the button events to handlers
        self.Bind(wx.EVT_BUTTON, self.OnStartCalib, btn_start_calib)
        self.Bind(wx.EVT_BUTTON, self.OnCheckCalib, btn_check_calib)
        self.Bind(wx.EVT_BUTTON, self.OnStartGame, btn_start_game)
        self.Bind(wx.EVT_BUTTON, self.OnStopGame, btn_stop_game)

        # Use a sizer to layout the controls, stacked vertically and with
        # a 10 pixel border around each
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(btn_start_calib, 0, wx.ALL, 10)
        sizer.Add(btn_check_calib, 0, wx.ALL, 10)
        sizer.Add(btn_start_game, 0, wx.ALL, 10)
        sizer.Add(btn_stop_game, 0, wx.ALL, 10)

        panel.SetSizer(sizer)
        panel.Layout()


    def OnStartCalib(self, evt):
        print "Start calib"
        game_control_comm.send_cmd_msg(protocol.START_CALIB_CMD)

    def OnCheckCalib(self,evt):
        calculate_pins.init()
        calculate_pins.check_calibration('base_image_game_control.jpg')

    def OnStartGame(self,evt):
        print "Start a game"
        game_control_comm.send_cmd_msg(protocol.START_GAME_CMD)
        
        self.game_setup_app = game_setup.game_setup_app()
        self.game_setup_app.MainLoop()
        
    def OnStopGame(self,evt):
        print "Stop the game"
        game_control_comm.send_cmd_msg(protocol.STOP_GAME_CMD)

    def SendScore(self,score):
        self.game_setup_app.game_mode_app.add_score(score)
        
class MyApp(wx.App):
    
    game_loop_working = True

    def OnInit(self):
        game_control_comm.init()
        
        frame = MyFrame(None, "Control panel")
        self.SetTopWindow(frame)

        print "Print statements go to this stdout window by default."

        thread.start_new_thread(self.game_control_loop, ())
        self.game_data = None
        
        frame.Show(True)
        return True

    def game_control_loop(self):
        while True:
            try:
                msg = socket.recv(zmq.NOBLOCK)
            except zmq.Again:
                if game_control_comm.throw_info_is_ready():
                    pin_count,speed  = game_control_comm.recv_throw_info()
                    print "Pin count is : %d and speed is : %f" % (pin_count,speed)
                    #socket.send("pin count "+str(pin_count))
                    if self.game_data is not None and \
                       not self.game_data.gameEnded:
                        data = self.game_data.runGame(pin_count)
                        msg = struct.pack('=BB?BHhh',
                                    np.ubyte(data[0]), #playerID
                                    np.ubyte(data[1]), #currFrame
                                    np.bool(data[2]), #first/second Shot Count
                                    np.ubyte(pin_count), #pinCount
                                    np.ushort(data[3]), # currFrame Total
                                    np.short(data[4]), #prevFrame Total
                                    np.short(data[5])) #twoFrames back Total       
                        socket.send(msg)
                        
                if game_control_comm.image_is_ready():
                    img = game_control_comm.recv_image()
                    img_fd = open('base_image_game_control.jpg','wb')
                    img_fd.write(img)
                    img_fd.close()
                    calib_res = get_pins_position.calib_camera('base_image_game_control.jpg')
                    game_control_comm.send_calib_data(str(calib_res))
                
                #print 'sending msg to client'
                #socket.send("Server message to client3")
                
                time.sleep(0.1)
            else:
                print("received ", msg)
                if msg.startswith('new game'):
                    num_of_players = int(msg.split()[2])
                    self.game_data = NewGame(num_of_players)
app = MyApp(redirect=True)
app.MainLoop()
