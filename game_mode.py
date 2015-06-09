import wx
import thread
import game_control_comm
import get_pins_position
import facebook_api
import zmq
import config
import time
import struct

port = config.GAME_CONTROL_PORT
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect("tcp://localhost:%s" % port)

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
    main_box = None
    score_box = None
    frame_count_box = None
    shots_box = None
    total_box = None
    total_list = None
    first_ball_count_list = None
    
    def add_score(self,panel,frame,shot_count,score,total,prev_total=None,prev2_total=None):
        if shot_count == 1:        
            if frame == 1:
                self.frame_count_box.AddSpacer(10)            
            elif frame == 11 or frame == 12:
                pass
            else:
                self.frame_count_box.AddSpacer(20)
                self.shots_box.AddSpacer(5)
            if not (frame == 11 or frame == 12):
                self.frame_count_box.Add(wx.StaticText(panel, label="  " + str(frame)),0,wx.TOP ,0)
            if score == 10:
                if not (frame == 11 or frame == 12):
                    self.shots_box.AddSpacer(14)                
                self.shots_box.Add(wx.StaticText(panel, label="  " + str('X')),0,wx.TOP,5)
            else:
                self.shots_box.Add(wx.StaticText(panel, label="  " + str(score)),0,wx.TOP,5)
            total_box = wx.TextCtrl(panel,value='',size=(33,20))            
            self.total_list.append(total_box)
            if frame == 11:
                self.total_list[frame - 2].AppendText(str(total)) 
            elif frame == 12:
                self.total_list[frame - 3].AppendText(str(total))
            else:
                self.total_list[frame - 1].AppendText(str(total))
            self.total_box.AddSpacer(2)            
            self.total_box.Add(total_box,0,wx.TOP,5)
            if (frame == 11 or frame == 12):
                total_box.Hide()
            self.first_ball_count_list.append(score)
            if prev_total is not None:
                self.total_list[frame - 2].Clear()
                self.total_list[frame - 2].AppendText(str(prev_total))
            if prev2_total is not None:
                self.total_list[frame - 3].Clear()
                self.total_list[frame - 3].AppendText(str(prev2_total))
        if shot_count == 2:
            if self.first_ball_count_list[frame - 1] + score == 10:
                self.shots_box.Add(wx.StaticText(panel, label="  " + str('/')),0,wx.TOP,5)
            else:
                self.shots_box.Add(wx.StaticText(panel, label="  " + str(score)),0,wx.TOP,5)
            if  frame == 11:
                self.total_list[frame - 2].Clear()
                self.total_list[frame - 2].AppendText(str(total))
            else:
                self.total_list[frame - 1].Clear()
                self.total_list[frame - 1].AppendText(str(total))
            if prev_total is not None:
                self.total_list[frame - 2].Clear()
                self.total_list[frame - 2].AppendText(str(prev_total))
            if prev2_total is not None:
                self.total_list[frame - 3].Clear()
                self.total_list[frame - 3].AppendText(str(prev2_total))
        panel.Layout()
            
class game_mode_frame(wx.Frame):
    """
    This is MyFrame.  It just shows a few controls on a wxPanel,
    and has a simple menu.
    """
    def __init__(self, parent, title,players_list):
        wx.Frame.__init__(self, parent, -1, title,
                          pos=(150, 150), size=(640, 480))

        self.CreateStatusBar()
        # Now create the Panel to put the other controls on.
        self.panel = wx.Panel(self)

        self.players_gui = []
        users = [] 
        for p in players_list:
            users.append(p.name)
        for username in users:
            p = player(facebook_api.get_user_data(username))
            
            pg = player_gui()
            pg.player = p
            pg.lbl_username = wx.StaticText(self.panel, label=p.name)
            img = wx.Image(facebook_api.get_user_picture_path(p.username), wx.BITMAP_TYPE_ANY)
            img = img.Scale(100,100)
            pg.pic_profile = wx.StaticBitmap(self.panel, -1, wx.BitmapFromImage(img))     

            self.players_gui.append(pg)

        # Use a sizer to layout the controls, stacked vertically and with
        # a 10 pixel border around each
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        for pg in self.players_gui:
            pg.main_box = wx.BoxSizer()
            pg.score_box = wx.BoxSizer(wx.VERTICAL)
            pg.frame_count_box = wx.BoxSizer()
            pg.shots_box = wx.BoxSizer()
            pg.total_box = wx.BoxSizer()
            pg.total_list = []
            pg.first_ball_count_list = []            
            profile_box = wx.BoxSizer(wx.VERTICAL)
            profile_box.Add(pg.lbl_username, 0, wx.ALL)
            profile_box.Add(pg.pic_profile, 0, wx.ALL)
            
            pg.main_box.Add(profile_box, 0, wx.ALL)
            pg.main_box.Add(pg.score_box, 0, wx.ALL)
            pg.score_box.Add(pg.frame_count_box, 0, wx.ALL)
            pg.score_box.Add(pg.shots_box, 0, wx.ALL)
            pg.score_box.Add(pg.total_box, 0, wx.ALL)
            
            self.sizer.Add(pg.main_box)
        
        self.panel.SetSizer(self.sizer)
        #panel.Layout()
        
    def addScoreToGui(self,player_id,
                      frame,shot_count,
                      pin_count,total,
                      prev_total,prev2_total):
        #print 'add',player_id,frame,shot_count,pin_count,total
        wx.MutexGuiEnter()
        if frame == 1:        
            self.players_gui[player_id].add_score(self.panel,
                                                  frame,
                                                  shot_count,
                                                  pin_count,
                                                  total)
        elif frame == 2:        
            self.players_gui[player_id].add_score(self.panel,
                                                  frame,
                                                  shot_count,
                                                  pin_count,
                                                  total,
                                                  prev_total)
        else:        
            self.players_gui[player_id].add_score(self.panel,
                                                  frame,
                                                  shot_count,
                                                  pin_count,
                                                  total,
                                                  prev_total,
                                                  prev2_total)
        wx.MutexGuiLeave()
class game_mode_app(wx.App):
    
    game_loop_working = True

    def __init__(self,players_list): 
        
        wx.App.__init__(self) 
        
        #game_control_comm.init()
        
        self.frame = game_mode_frame(None, "Game window",players_list)
        self.SetTopWindow(self.frame)
        
        msg = 'new game '+str(len(players_list))
        socket.send(msg)

        thread.start_new_thread(self.game_control_loop, ())

        self.frame.Show(True)
        
        return None

    def game_control_loop(self):
        while True:
            msg = socket.recv()
            data = struct.unpack('=BB?BHhh',msg)            

            player_id = int(data[0])
            frame = int(data[1])
            shot_count = 1 if data[2] else 2
            pin_count = int(data[3])
            total = int(data[4])          
            prev_total = int(data[5])
            prev2_total = int(data[6]) 
            #print data
            self.frame.addScoreToGui(player_id,
                                     frame,
                                     shot_count,
                                     pin_count,
                                     total,
                                     prev_total,
                                     prev2_total)
            #socket.send("Got the PinCount")
            time.sleep(1)            
            '''            
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
            '''
#app = game_mode_app(redirect=True)
#app.MainLoop()