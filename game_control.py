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
        calculate_pins.calculate_pin_count('base_image_game_control.jpg')

    def OnStartGame(self,evt):
        print "Start a game"
        game_control_comm.send_cmd_msg(protocol.START_GAME_CMD)

    def OnStopGame(self,evt):
        print "Stop the game"
        game_control_comm.send_cmd_msg(protocol.STOP_GAME_CMD)


class MyApp(wx.App):
    
    game_loop_working = True

    def OnInit(self):
        game_control_comm.init()
        
        frame = MyFrame(None, "Simple wxPython App")
        self.SetTopWindow(frame)

        print "Print statements go to this stdout window by default."

        thread.start_new_thread(self.game_control_loop, ())

        frame.Show(True)
        return True

    def game_control_loop(self):
        while True:
            if game_control_comm.throw_info_is_ready():
                pin_count,speed  = game_control_comm.recv_throw_info()

                print "Pin count is : %d and speed is : %f" % (pin_count,speed)

            if game_control_comm.image_is_ready():
                img = game_control_comm.recv_image()
                img_fd = open('base_image_game_control.jpg','wb')
                img_fd.write(img)
                img_fd.close()
                calib_res = get_pins_position.calib_camera('base_image_game_control.jpg')
                game_control_comm.send_calib_data(str(calib_res))
        
app = MyApp(redirect=True)
app.MainLoop()
