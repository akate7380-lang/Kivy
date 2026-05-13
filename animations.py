from kivy.app import App
from kivy.uix.button import Button
from kivy.animation import Animation
import random

class AnimatedApp(App):
    def build(self):
        button = Button(text="Анімація", size_hint=(None, None), size=(150, 100), pos=(100, 100), 
                        background_color=(0.51, 0.12, 0.98, 1))
        button.bind(on_press=self.start_anim)
        
        return button
    
    def start_anim(self, instance):
        target_x = random.randint(0, 800 - instance.width)
        target_y = random.randint(0, 600 - instance.height)
        
        anim = Animation(pos=(target_x, target_y), duration=1, t="out_bounce")
        
        anim &= Animation(background_color=(random.random(), 0.5, 0.8, 1), duration=0.5)
        
        anim.start(instance)
        
if __name__ == "__main__":
    AnimatedApp().run()
