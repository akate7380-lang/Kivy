from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock


TARGETS = {
'obj1': {'source': 'assets/images/beach-ball.png', 'hp': 5},
'obj2': {'source': 'assets/images/fish.png', 'hp': 10},
'obj3': {'source': 'assets/images/crystal.png', 'hp': 20}
}

LEVELS = [
['obj1', 'obj1', 'obj2'], # рівень 1
['obj2', 'obj2', 'obj1'], # рівень 2
['obj3', 'obj3', 'obj2'] # рівень 3
]

class Target(Image):
    def __init__(self, game_screen, **kwargs):
        super().__init__(**kwargs)
        self.game_screen = game_screen
        self.current_hp = 0

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and self.opacity == 1:
            self.game_screen.add_click()
            self.current_hp -= 1

            if self.current_hp <= 0:
                self.destroy()
            return True
        return super().on_touch_down(touch)

    def spawn(self, obj_key):
        data = TARGETS[obj_key]
        self.source = data["source"]
        self.current_hp = data["hp"]
        self.opacity = 1

    def destroy(self):
        self.opacity = 0
        Clock.schedule_once(lambda dt: self.game_screen.load_next_target(), 0.3)

class Menu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", padding="20dp", spacing="20dp")

        lbl_title = Label(
            text="Menu",
            font_size="40sp",
            size_hint=(1, 0.2),
            color=(1, 0, 0, 1)
        )

        btn_play = Button(
            text="Go to Game",
            size_hint=(1, 0.15),
            font_size="20sp"
        )
        btn_play.bind(on_press=self.go_game)

        btn_settings = Button(
            text="Go to Settings",
            size_hint=(1, 0.15),
            font_size="20sp"
        )
        btn_settings.bind(on_press=self.go_settings)

        layout.add_widget(lbl_title)
        layout.add_widget(btn_play)
        layout.add_widget(btn_settings)

        self.add_widget(layout)

    def go_game(self, *args):
        self.manager.current = "game"

    def go_settings(self, *args):
        self.manager.current = "settings"


class Game(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.score = 0
        self.current_level_idx = 0
        self.current_target_idx = 0

        # Основний лейаут екрану гри
        layout = BoxLayout(orientation="vertical", padding="20dp", spacing="20dp")
        # Верхня панель
        top_panel = BoxLayout(size_hint=(1, 0.1), padding="10dp")
        self.lbl_level = Label(text="Level: 1", font_size="20sp")
        self.lbl_score = Label(text="Clicks: 0", font_size="20sp")
        btn_back = Button(text="Back", size_hint=(1, 0.15), font_size="20sp")
        btn_back.bind(on_press=self.go_menu)

        top_panel.add_widget(self.lbl_level)
        top_panel.add_widget(self.lbl_score)
        top_panel.add_widget(btn_back)

        # Ігрова зона
        game_area = FloatLayout(size_hint=(1, 0.8))
        self.target = Target(game_screen=self, size_hint=(0.5, 0.5), pos_hint={"center_x": 0.5, "center_y": 0.5})
        game_area.add_widget(self.target)

        lbl_title = Label(
            text="Game",
            font_size="40sp",
            size_hint=(1, 0.2),
            color=(1, 0, 0, 1)
        )
        
        layout.add_widget(lbl_title)
        
        self.lbl_message = Label(text="", font_size='35sp', color=(0, 1, 0, 1), size_hint=(1, 0.1))
        
        layout.add_widget(top_panel)
        layout.add_widget(game_area)
        layout.add_widget(self.lbl_message)
        self.add_widget(layout)

    def go_menu(self, *args):
        self.manager.current = "menu"

    def on_enter(self, *args):
        self.score = 0
        self.current_level_idx = 0
        self.lbl_score.text = f"Clicks: {self.score}"
        self.start_level()
        
    def start_level(self):
        self.current_target_idx = 0
        self.lbl_level.text = f"Level: {self.current_level_idx + 1}"
        self.lbl_message.text = ""
        self.spawn_target()
        
    def spawn_target(self):
        level_data = LEVELS[self.current_level_idx]
        obj_key = level_data[self.current_target_idx]
        self.target.spawn(obj_key)
        
    def load_next_target(self):
        level_data = LEVELS[self.current_level_idx]
        self.current_target_idx += 1
        
        if self.current_target_idx < len(level_data):
            self.spawn_target()
        else:
            self.current_level_idx += 1
            
            if self.current_level_idx < len(LEVELS):
                Clock.schedule_once(lambda dt: self.start_level(), 0.5)
            
            else:
                self.lbl_message.text = "YOU WIN!"
                Clock.schedule_once(lambda dt: self.go_menu(), 2.5)
            
    def add_click(self):
        self.score += 1
        self.lbl_score.text = f"Clicks: {self.score}"

class Settings(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", padding="20dp", spacing="20dp")

        lbl_title = Label(
            text="Settings",
            font_size="40sp",
            size_hint=(1, 0.2),
            color=(1, 0, 0, 1)
        )

        btn_back = Button(text="Back to menu", size_hint=(1, 0.15), font_size="20sp")
        btn_back.bind(on_press=self.go_menu)

        layout.add_widget(lbl_title)
        layout.add_widget(btn_back)

        self.add_widget(layout)

    def go_menu(self, *args):
        self.manager.current = "menu"


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Menu(name="menu"))
        sm.add_widget(Game(name="game"))
        sm.add_widget(Settings(name="settings"))
        return sm


if __name__ == "__main__":
    MyApp().run()
