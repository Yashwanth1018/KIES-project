from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import time

Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (640, 480)
        play: False  # Disable video recording
    Button:
        text: 'Capture Photo'
        size_hint_y: None
        height: '48dp'
        background_color: 0.2, 0.6, 0.8, 1 
        on_press: root.capture()
''')

class CameraClick(BoxLayout):
    def capture(self):
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_{}.png".format(timestr))
        print("Photo Captured")

class TestCamera(App):
    def build(self):
        return CameraClick()

TestCamera().run()
