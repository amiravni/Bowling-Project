import wx
import game_control_comm
import game_mode
import protocol

class player():

    username = ''
    name = ''
    raw_data = []
    name_gui = None
    remove_gui_btn = None
    
    def __init__(self,raw_data):
        if 'name' in raw_data.keys():        
            self.name = raw_data['name']
        
        if 'username' in raw_data.keys():
            self.username = raw_data['username']
   
class game_setup_frame(wx.Frame):
    """
    This is MyFrame.  It just shows a few controls on a wxPanel,
    and has a simple menu.
    """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title,
                          pos=(150, 150), size=(640, 480))
        
        print "Game Setup"
        self.CreateStatusBar()
        # Now create the Panel to put the other controls on.
        self.panel = wx.Panel(self)
        self.players_list = []
        
        btn_add_player = wx.Button(self.panel, -1, "Add Player",
                                   pos=(315,400),size=(160,30))
        btn_start_game = wx.Button(self.panel, -1, "Start Game",
                                   pos=(480,400),size=(160,30))
                
        
        # bind the button events to handlers
        self.Bind(wx.EVT_BUTTON, self.OnAddPlayer, btn_add_player)
        self.Bind(wx.EVT_BUTTON, self.OnStartGame, btn_start_game)
        # Use a sizer to layout the controls, stacked vertically and with
        # a 10 pixel border around each
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.panel.SetSizer(self.sizer)
        self.panel.Layout()

    def OnAddPlayer(self,evt):
        self.UpdateData()        
        new_player_number = len(self.players_list) + 1
        new_player = player({'name': 'player'+str(new_player_number),
                             'username': ''})
        self.players_list.append(new_player)
        self.UpdatePlayersGrid()
    
    def OnRemovePlayer(self,event):
        self.UpdateData()
        for i,player in enumerate(self.players_list):
            if player.remove_gui_btn.GetId() == event.GetId():
                del self.players_list[i]    
        self.UpdatePlayersGrid()
        
    def UpdateData(self):
        for player in self.players_list:
            player.name = player.name_gui.GetLineText(0).encode('UTF8')
        
    def UpdatePlayersGrid(self):
        while self.sizer.GetChildren():
            self.sizer.Hide(0)
            self.sizer.Remove(0)
            
        i = 10        
        for player in self.players_list:
            name_entry = wx.TextCtrl(self.panel,
                                     value=player.name,
                                     size=(200,30),
                                     pos=(20,i))        
            remove_btn = wx.Button(self.panel, -1, "Remove",
                                   pos=(230,i),size=(70,30))
            self.Bind(wx.EVT_BUTTON, self.OnRemovePlayer, remove_btn)
            
            player.name_gui = name_entry
            player.remove_gui_btn = remove_btn
            
            self.sizer.Add(name_entry, 0 , wx.ALL)
            self.sizer.Add(remove_btn, 0 , wx.ALL)
            i += 35

    def OnStartGame(self,event):
        print "Start a game"
        self.Close()        
        self.UpdateData()        
        #game_control_comm.send_cmd_msg(protocol.START_GAME_CMD)
        
        self.game_mode_app = game_mode.game_mode_app(self.players_list)
        self.game_mode_app.MainLoop()
        
        
class game_setup_app(wx.App):

    def OnInit(self):
        #game_control_comm.init()
        
        frame = game_setup_frame(None, "Game Setup")
        self.SetTopWindow(frame)
        
        frame.Show(True)
        
        return True
        
#app = game_setup_app(redirect = True)
#app.MainLoop()