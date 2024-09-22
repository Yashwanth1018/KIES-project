from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics.texture import Texture
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
import cv2
from kivy.uix.label import Label

class CameraLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(CameraLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Add a background color
        with self.canvas.before:
            Color(1.0, 0.992, 0.816, 1)  # RGBA color (cream)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

class CameraScreen(Screen):
    def __init__(self, **kwargs):
        super(CameraScreen, self).__init__(**kwargs)
        layout = CameraLayout()

        # Camera feed
        self.img = Image()
        layout.add_widget(self.img)

        # Capture button
        self.capture_btn = Button(text="Capture", size_hint=(1, 0.1))
        self.capture_btn.bind(on_press=self.capture_image)
        layout.add_widget(self.capture_btn)

        # Next button
        self.next_btn = Button(text="Next", size_hint=(1, 0.1))
        self.next_btn.bind(on_press=self.go_to_next_screen)
        layout.add_widget(self.next_btn)

        # Start the camera feed
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0 / 30.0)

        self.add_widget(layout)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            buffer = cv2.flip(frame, 0).tobytes()  # Flip the frame vertically
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
            self.img.texture = texture

    def capture_image(self, instance):
        ret, frame = self.capture.read()
        if ret:
            captured_image_path = 'captured_image.png'
            cv2.imwrite(captured_image_path, frame)
            print(f"Image captured and saved as '{captured_image_path}'.")
            self.go_to_next_screen(instance, captured_image_path)

    def go_to_next_screen(self, instance, captured_image_path=None):
        student_data = "Rollno:          \nName:             \nDob:      \nClass:      \nReg no:         \nGender:        "  # Replace with actual data
        self.manager.current = 'student_info'
        self.manager.get_screen('student_info').update_info(student_data, captured_image_path)

    def on_stop(self):
        self.capture.release()

class StudentInfoScreen(Screen):
    def __init__(self, **kwargs):
        super(StudentInfoScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # Image for the captured photo
        self.captured_image = Image(size_hint=(1, 0.6))  # Move image to the top
        layout.add_widget(self.captured_image)

        # Display student information
        self.student_label = Label(text="", size_hint=(1, 0.4))
        layout.add_widget(self.student_label)

        # Back button
        back_btn = Button(text="Back to Camera", size_hint=(1, 0.1))
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def update_info(self, student_data, captured_image_path):
        self.student_label.text = f"Student Details:\n\n{student_data}"
        if captured_image_path:  # Ensure the image path is valid
            self.captured_image.source = captured_image_path
            self.captured_image.reload()  # Reload the image to ensure it displays

    def go_back(self, instance):
        self.manager.current = 'camera'

class CameraApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(CameraScreen(name='camera'))
        sm.add_widget(StudentInfoScreen(name='student_info'))
        return sm

if __name__ == '__main__':
    CameraApp().run()
