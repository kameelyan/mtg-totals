theirName = "Mat Bimonte"

import efl.elementary as elm
from efl.elementary.window import StandardWindow, DialogWindow
from efl.elementary.background import Background
from efl.elementary.entry import Entry
from efl.elementary.box import Box
from efl.elementary.button import Button

from efl.evas import EVAS_HINT_EXPAND, EVAS_HINT_FILL, \
    EVAS_CALLBACK_KEY_UP, EVAS_EVENT_FLAG_ON_HOLD
EXPAND_BOTH = EVAS_HINT_EXPAND, EVAS_HINT_EXPAND
EXPAND_HORIZ = EVAS_HINT_EXPAND, 0.0
FILL_BOTH = EVAS_HINT_FILL, EVAS_HINT_FILL
FILL_HORIZ = EVAS_HINT_FILL, 0.5

class MainWindow(StandardWindow):
    def __init__(self):
        StandardWindow.__init__(self, "lifetracker", "Life Tracker", size=(200, 200))
        self.callback_delete_request_add(lambda o: elm.exit())
        self.elm_event_callback_add(self.eventsCb)

        self.ourLifeTotal = 20
        self.theirLifeTotal = 20
        
        self.buildSubs()
    
    def buildSubs(self):
        self.subWin = DialogWindow(self, "lifetracker", "Life Tracker Assignment", size=(300, 300))
        self.subWin.callback_delete_request_add(lambda o: elm.exit())
        self.ourWin = DialogWindow(self, "lifetracker", "Life Tracker Jeff Hoogland", size=(1200, 300))
        self.ourWin.callback_delete_request_add(lambda o: elm.exit())
        self.ourWin.elm_event_callback_add(self.eventsCb)
        self.theirWin = DialogWindow(self, "lifetracker", "Life Tracker %s"%theirName, size=(1200, 300))
        self.theirWin.callback_delete_request_add(lambda o: elm.exit())
        self.theirWin.elm_event_callback_add(self.eventsCb)
        
        self.ourLife = ourLabel = Entry(self.ourWin, editable=False)
        ourLabel.size_hint_weight = EXPAND_HORIZ
        ourLabel.size_hint_align = FILL_HORIZ
        ourLabel.text_style_user_push("DEFAULT='font_size=100'")
        ourLabel.text = "%s  -  Jeff Hoogland"%self.ourLifeTotal
        ourLabel.show()
        
        self.theirLife = ourLabel2 = Entry(self.theirWin, editable=False)
        ourLabel2.size_hint_weight = EXPAND_HORIZ
        ourLabel2.size_hint_align = FILL_HORIZ
        ourLabel2.text_style_user_push("DEFAULT='font_size=100'")
        ourLabel2.text = "%s  -  %s"%(self.theirLifeTotal, theirName)
        ourLabel2.show()
        
        self.ourEntry = ourEntry = Entry(self.subWin)
        ourEntry.size_hint_weight = EXPAND_HORIZ
        ourEntry.size_hint_align = (-1, 0)
        ourEntry.single_line_set(True)
        ourEntry.text_style_user_push("DEFAULT='font_size=50'")
        ourEntry.callback_activated_add(self.ourLifeUpdate)
        ourEntry.text = "20"
        ourEntry.show()
        
        self.theirEntry = theirEntry = Entry(self.subWin)
        theirEntry.size_hint_weight = EXPAND_HORIZ
        theirEntry.size_hint_align = (-1, 0)
        theirEntry.single_line_set(True)
        theirEntry.text_style_user_push("DEFAULT='font_size=50'")
        theirEntry.callback_activated_add(self.theirLifeUpdate)
        theirEntry.text = "20"
        theirEntry.show()
        
        resetBtn = Button(self.subWin)
        resetBtn.text = "Reset life totals"
        resetBtn.callback_pressed_add(self.resetLifeTotals)
        resetBtn.show()
        
        entryBox = Box(self.subWin)
        entryBox.size_hint_weight = EXPAND_HORIZ
        entryBox.pack_end(ourEntry)
        entryBox.pack_end(theirEntry)
        entryBox.pack_end(resetBtn)
        entryBox.show()
        
        self.ourWin.resize_object_add(ourLabel)
        self.theirWin.resize_object_add(ourLabel2)
        self.subWin.resize_object_add(entryBox)
        
        self.ourWin.show()
        self.theirWin.show()
        self.subWin.show()
        
        self.ourWin.center(True, True)
        self.theirWin.center(True, True)
        self.subWin.center(True, True)
    
    def resetLifeTotals(self, obj):
        self.ourLifeTotal = 20
        self.ourLife.text = "%s  -  Jeff Hoogland"%self.ourLifeTotal
        self.ourEntry.text = str(self.ourLifeTotal)
        self.theirLifeTotal = 20
        self.theirLife.text = "%s  -  %s"%(self.theirLifeTotal, theirName)
        self.theirEntry.text = str(self.theirLifeTotal)
    
    def ourLifeUpdate(self, obj):
        self.ourLifeTotal = int(obj.text)
        self.ourLife.text = "%s  -  Jeff Hoogland"%self.ourLifeTotal
    
    def theirLifeUpdate(self, obj):
        self.theirLifeTotal = int(obj.text)
        self.theirLife.text = "%s  -  %s"%(self.theirLifeTotal, theirName)
    
    def lifeChange(self, who, direction):
        if direction == "up":
            change = 1
        else:
            change = -1
        
        if who == "mine":
            self.ourLifeTotal += change
            self.ourLife.text = "%s  -  Jeff Hoogland"%self.ourLifeTotal
            self.ourEntry.text = str(self.ourLifeTotal)
        else:
            self.theirLifeTotal += change
            self.theirLife.text = "%s  -  %s"%(self.theirLifeTotal, theirName)
            self.theirEntry.text = str(self.theirLifeTotal)
    
    def eventsCb(self, obj, src, event_type, event):
        #print(obj)
        #print(src)
        #print(event.key.lower())
        #print(event_type)
        #print("")

        if not event_type == EVAS_CALLBACK_KEY_UP:
            return False

        if event.keyname == "Up":
            self.lifeChange("mine", "up")
        elif event.keyname == "Down":
            self.lifeChange("mine", "down")
        elif event.keyname == "Right":
            self.lifeChange("thiers", "up")
        elif event.keyname == "Left":
            self.lifeChange("theirs", "down")
            

        event.event_flags = event.event_flags | EVAS_EVENT_FLAG_ON_HOLD
        return True

if __name__ == "__main__":
    elm.init()
    GUI = MainWindow()
    #GUI.show()
    elm.run()
    elm.shutdown()