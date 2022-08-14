from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.slider import Slider
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from datetime import datetime
from functools import partial
import socketio
import pytz


timeZ_IN = pytz.timezone('Asia/Kolkata')
timeZ_CA = pytz.timezone('Canada/Eastern')
timeString = ""

# standard Python
sio = socketio.Client()

@sio.event
def connect():
    print("Raspberry-PI Coneected with socketio server")
    #sio.emit('login', {'userKey': 'streaming_api_key'})

@sio.event
def connect_error():
    print("connection to server failed")

@sio.event
def message(data):
    print(data)

# @sio.on('handshake')
# def on_message(data):
#     print('HandShake', data)


# @sio.on('price')
# def on_message(data):
#     print('Price Data ', data)

class frm(FloatLayout):

    def __init__(self,**kwargs):
        
        super(frm,self).__init__(**kwargs)

        
        self.flexideckString = Label(text = "flexideck version 0.2", size_hint=(0, 0),pos_hint={'x':0.09, 'y':0.02})
        self.main_label = Label(text = "welcome", size_hint=(0, 0),pos_hint={'x':0.08, 'y':0.10})

        self.brightnessControl = Slider(min = 0, max = 100)
        self.brightnessControl.size_hint_x = .38
        self.brightnessControl.pos_hint = {'x': .60, 'center_y': .15}
        self.add_widget(Label(text ='Brightness :- ', size_hint=(0, 0),pos_hint={'x':.80, 'y':.05}))
        self.add_widget(self.brightnessControl)

        #self.add_widget(Label(text ='Slider Value', ))
        self.brightnessValue = Label(text ='0',size_hint=(0, 0),pos_hint={'x':.87, 'y':.05})
        self.add_widget(self.brightnessValue)
        self.brightnessControl.bind(value = self.on_value)

        self.clockOneLable = Label(text ='00:00:00',size_hint=(0, 0.5),pos_hint={'x':.3, 'y':.5})
        self.clockOneLable.font_size = '50dp'
        self.add_widget(self.clockOneLable)

        self.dateOneLable = Label(text ='10/AUG/2022',size_hint=(0, 0.5),pos_hint={'x':.3, 'y':.4})
        #self.dateOneLable.font_size = '20dp'
        self.add_widget(self.dateOneLable)

        self.clockTwoLable = Label(text ='00:00:00',size_hint=(0, 0.5),pos_hint={'x':.3, 'y':.16})
        self.clockTwoLable.font_size = '50dp'
        self.add_widget(self.clockTwoLable)

        self.dateTwoLable = Label(text ='10/AUG/2022',size_hint=(0, 0.5),pos_hint={'x':.3, 'y':.06})
        #self.dateOneLable.font_size = '20dp'
        self.add_widget(self.dateTwoLable)

    #Main Buttons
        self.camera_button = Button(text = "Camera", size_hint=(.2, .2),pos_hint={'x':.80, 'y':.75}, on_press = self.cameraPressed)
        self.bluetooth_button = Button(text = "Bluetooth", size_hint=(.2, .2),pos_hint={'x':.60, 'y':.75},on_press = self.bluetoothPressed)
        self.mic_button = Button(text = "Mic", size_hint=(.2, .2),pos_hint={'x':.80, 'y':.55})
        self.speaker_button = Button(text = "Speaker", size_hint=(.2, .2),pos_hint={'x':.60, 'y':.55})
        self.browser_button = Button(text = "Browser", size_hint=(.2, .2),pos_hint={'x':.80, 'y':.35})
        self.lock_button = Button(text = "Lock Screen", size_hint=(.2, .2),pos_hint={'x':.60, 'y':.35})
        self.previousTrack_button = Button(text = "<<", size_hint=(.1, .15),pos_hint={'x':.60, 'y':.20})
        self.playPaus_button = Button(text = "Play", size_hint=(.2, .15),pos_hint={'x':.70, 'y':.20})
        self.nextTrack_button = Button(text = ">>", size_hint=(.1, .15),pos_hint={'x':.90, 'y':.20})

        self.add_widget(self.flexideckString)
        self.add_widget(self.main_label)
        self.add_widget(self.camera_button)
        self.add_widget(self.bluetooth_button)
        self.add_widget(self.mic_button)
        self.add_widget(self.speaker_button)
        self.add_widget(self.browser_button)
        self.add_widget(self.lock_button)
        self.add_widget(self.previousTrack_button)
        self.add_widget(self.playPaus_button)
        self.add_widget(self.nextTrack_button)

      

        self.current_text = "Default"


    def on_value(self, instance, brightness):
        self.brightnessValue.text = "% d"% brightness

    def cameraPressed(self,event):
       # sio.emit('pyevent', "toggleCamera")
        self.main_label.text = "Status : Toggling Camera!"

    def bluetoothPressed(self,event):
       # sio.emit('pyevent', "toggleBluetooth")
        self.main_label.text = "Status : Toggling Bluetooth!"
    
def clockUpdateCallback(value, key, *largs):
    timeZ_IN = pytz.timezone('Asia/Kolkata')
    timeZ_CA = pytz.timezone('Canada/Eastern')
    timeString = datetime.now(timeZ_IN).strftime('%I:%M:%S %Z')
    dateString =datetime.now(timeZ_IN).strftime('%A %d %Y')
    timeCAString = datetime.now(timeZ_CA).strftime('%I:%M:%S %Z')
    dateCAString = datetime.now(timeZ_CA).strftime('%A %d %Y')
    value.clockOneLable.text = str(timeString);
    value.dateOneLable.text = str(dateString);
    value.clockTwoLable.text = str(timeCAString);
    value.dateTwoLable.text = str(dateCAString);
    value.main_label.text = "Status: Ready!"
    pass

class Flexideck(App):

    def build(self):  
        self.root = frm()      
        Clock.schedule_interval(partial(clockUpdateCallback,self.root), 0.5)
        
if __name__=="__main__":
     sio.connect('http://localhost:3000')
     Flexideck().run()