#!/usr/bin/python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Pango,GObject
from datetime import datetime

import threading
import datetime
import time
import socketio


gi.require_version("Gtk", "3.0")
gi.require_version('Notify', '0.7')

from gi.repository import Gtk
from gi.repository import Notify

# standard Python
sio = socketio.Client()

@sio.event
def connect():
    print("I'm connected!")
    sio.emit('login', {'userKey': 'streaming_api_key'})

@sio.event
def connect_error():
    print("The connection failed!")

@sio.event
def message(data):
    print('I received a message!')

@sio.on('handshake')
def on_message(data):
    print('HandShake', data)


@sio.on('price')
def on_message(data):
    print('Price Data ', data)

class MyWindow(Gtk.Window):
        def __init__(self):
            Gtk.Window.__init__(self, title="app")
            self.timer = None
            self.event = None
            self.clock = '00:00:00'
 
            Gtk.Window.__init__(self, title="Timer")
            self.set_default_size(800, 450)
            self.box = Gtk.Box(spacing=6)
            self.add(self.box)
            self.label = Gtk.Label()
            self.box.pack_start(self.label, True, True, 0)

            self.button_start = Gtk.Button(label="Mute")
            self.button_start.connect("clicked",self.start_timer)
 
            self.button_stop = Gtk.Button(label="Stop")
            self.button_stop.connect("clicked",self.stop_timer)
 
            self.status = Gtk.Label()
            self.status.set_text(self.clock)
            # override_font is deprecated but good enough for a preview.
            font = Pango.FontDescription("Tahoma 48")
            self.status.override_font(font)
 
            self.vbox = Gtk.VBox()
 
            self.vbox.pack_start(self.button_start,False,False,5)
            self.vbox.pack_start(self.button_stop,False,False,5)
            self.vbox.pack_end(self.status,True,True,5)
 
            self.add(self.vbox)
    
        
   	# Displays Timer
        def displayclock(self):
		    #  putting our datetime into a var and setting our label to the result. 
		    #  we need to return "True" to ensure the timer continues to run, otherwise it will only run once.
            datetimenow = str(datetime.datetime.now())
            self.label.set_label(datetimenow)
            return True

	# Initialize Timer
        def startclocktimer(self):
		    #  this takes 2 args: (how often to update in millisec, the method to run)
            GObject.timeout_add(1000, self.displayclock) 

        def get_time(self):
            seconds = 0
            while not self.event.is_set():
                seconds += 1
                self.clock = str(datetime.timedelta(seconds = seconds))
                self.status.set_text(self.clock)
                time.sleep(1)
 
        def start_timer(self,button):
            print('start')
            sio.emit('pyevent', "Mute-Pressed")
            self.timer = threading.Thread(target=self.get_time)
            self.event = threading.Event()
            self.timer.daemon=True
            self.timer.start() 
 
        def stop_timer(self,button):
            print('stop')
            self.event.set()
            self.timer = None
 
win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
win.startclocktimer()
Gtk.main()