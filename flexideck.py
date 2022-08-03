import gi
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
        Gtk.Window.__init__(self, title="Hello World")
        Gtk.Window.set_default_size(self, 640, 480)
        Notify.init("Welcome to Flexideck")

        self.box = Gtk.Box(spacing=6)
        self.add(self.box)
       
        self.button = Gtk.Button(label="Mute")
        self.button.set_halign(Gtk.Align.CENTER)
        self.button.set_valign(Gtk.Align.CENTER)
        self.button.connect("clicked", self.on_button_clicked)
        self.box.pack_start(self.button, True, True, 0)

    def on_button_clicked(self, widget):        
        n = Notify.Notification.new("Simple GTK3 Application", "Hello World !!")
        sio.emit('pyevent', "Mute-Pressed")
        n.show()

sio.connect('http://localhost:3000')
win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()