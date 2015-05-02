import wx
import thread
import game_control_comm
import protocol
import get_pins_position
import calculate_pins
import facebook_api

class player():

    username = ''
    name = ''
    raw_data = []

    def __init__(self,raw_data):
        self.name = raw_data['name']
        self.username = raw_data['username']


class player_gui():
    player = None    
    lbl_username = None
    pic_profile = None
    box = None
    
    def add_score(self,panel,score):
        self.box.Add(wx.StaticText(panel, label="  " + str(score)),0,wx.TOP,50)
    
class game_mode_frame(wx.Frame):
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


        users = ['danny.wainshtein','avni314','mark']
        players_gui = []
        for username in users:
            p = player(facebook_api.get_user_data(username))
            
            pg = player_gui()
            pg.player = p
            pg.lbl_username = wx.StaticText(panel, label=p.name)
            img = wx.Image(facebook_api.get_user_picture_path(p.username), wx.BITMAP_TYPE_ANY)
            img = img.Scale(100,100)
            pg.pic_profile = wx.StaticBitmap(panel, -1, wx.BitmapFromImage(img))     

            players_gui.append(pg)

        # Use a sizer to layout the controls, stacked vertically and with
        # a 10 pixel border around each
        sizer = wx.BoxSizer(wx.VERTICAL)

        for pg in players_gui:
            pg.box = wx.BoxSizer()
            profile_box = wx.BoxSizer(wx.VERTICAL)
            profile_box.Add(pg.lbl_username, 0, wx.ALL)
            profile_box.Add(pg.pic_profile, 0, wx.ALL)
            pg.box.Add(profile_box, 0, wx.ALL)
            
            sizer.Add(pg.box)
            
        players_gui[0].add_score(panel,1)

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

    def OnStopGame(self,evt):
        print "Stop the game"
        game_control_comm.send_cmd_msg(protocol.STOP_GAME_CMD)


class game_mode_app(wx.App):
    
    game_loop_working = True

    def OnInit(self):
        game_control_comm.init()
        
        frame = game_mode_frame(None, "Game window")
        self.SetTopWindow(frame)

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
        
#app = game_mode_app(redirect=True)
#app.MainLoop()