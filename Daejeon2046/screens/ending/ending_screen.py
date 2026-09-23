from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.animation import Animation
from functools import partial
import os
ASSETS_ENDING_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'image_file', 'ending_screen'))
STORY_ENDING_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'story', 'ending_credit'))
from kivy.uix.image import Image


class EndingScreen(Screen):
    image_source = StringProperty(os.path.join(ASSETS_ENDING_DIR, 'background.jpg'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.full_text_lines = []
        self.displayed_text = ""
        self.current_index = 0
        self.button_added = False
        self.game_type = ''

    def show_screen(self, game_result):
        if game_result in ['MENTAL_ZERO', 'CONCENTRATION_ZERO']:
            print('게임 오버 화면 전환')
            self.game_type = 'over'
            self.game_over_screen(game_result)
        else:
            print('게임 엔딩 화면 전환')
            self.game_type = 'ending'
            self.ending_screen(game_result)

    def game_over_screen(self, game_result):
        self.displayed_text = ""
        self.current_index = 0
        self.button_added = False
        self.game_type = 'over'
        # 엔딩/크레딧 텍스트 파일은 story/ending_credit에 위치합니다
        game_over_text = os.path.join(STORY_ENDING_DIR, 'mental-over.txt' if game_result == 'MENTAL_ZERO' else 'concentration-over.txt')

        # 기존 엔딩스크린의 레이아웃을 동적으로 변경하여 게임 오버 화면 구성
        game_over_title = self.ids.ending_background
        game_over_title.size_hint = (1, 0.4)
        game_over_title.opacity = 0
        game_over_title.clear_widgets()
        game_over_title.add_widget(Label(
            text='나약한 멘탈' if game_result == 'MENTAL_ZERO' else '집중력 바닥',
            font_name='NanumGothic.ttf',
            font_size=60,
            halign='center',
            valign='middle',
        ))

        opacity_animation = Animation(opacity=1, duration=3)
        opacity_animation.start(game_over_title)

        game_over_content = self.ids.ending_content
        game_over_content.size_hint = (1, 0.6)
        game_over_content.orientation = 'vertical'

        game_over_content_box = self.ids.ending_content_box
        game_over_button_box = self.ids.ending_button_box
        game_over_button_box.clear_widgets()
        game_over_content_text = self.ids.ending_label
        game_over_button_box.orientation = 'vertical'
        game_over_content_box.size_hint = (1, 0.6)
        game_over_button_box.size_hint = (1, 0.4)

        game_over_content_text.font_size = 25
        game_over_content_text.halign = 'center'
        game_over_content_text.valign = 'middle'
        game_over_content_text.line_height = 2.0

        with open(game_over_text, "r", encoding='utf-8') as file:
            self.full_text_lines = file.readlines()

        Clock.schedule_interval(self.update_text, 1)

    def ending_screen(self, game_result):
        self.displayed_text = ""
        self.current_index = 0
        self.button_added = False
        self.game_type = 'ending'

        # 엔딩 텍스트 파일은 story/ending_credit 폴더에 보관됩니다
        ending_text_file = os.path.join(STORY_ENDING_DIR, f"{game_result.lower()}-ending.txt")
        assets_dir = ASSETS_ENDING_DIR
        if game_result == 'BAD':
            self.image_source = os.path.join(assets_dir, 'bad-ending.jpg')
        elif game_result == 'NORMAL':
            self.image_source = os.path.join(assets_dir, 'normal-ending.jpg')
        elif game_result == 'GOOD':
            self.image_source = os.path.join(assets_dir, 'good-ending.jpg')
        elif game_result == 'HIDDEN':
            self.image_source = os.path.join(assets_dir, 'hidden-ending.jpeg')

        ending_background = self.ids.ending_background
        ending_background.clear_widgets()
        ending_background.orientation = 'horizontal'
        ending_background.size_hint = (1, 0.65)
        ending_background.opacity = 1
        ending_background.padding = 20
        image_widget = Image(
            source=self.image_source,
            size_hint_y=1,
            allow_stretch=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        ending_background.add_widget(image_widget)

        ending_content = self.ids.ending_content
        ending_content.orientation = 'horizontal'
        ending_content.size_hint = (1, 0.35)

        ending_content_box = self.ids.ending_content_box
        ending_content_box.size_hint = (0.8, 1)

        ending_button_box = self.ids.ending_button_box
        ending_button_box.clear_widgets()
        ending_button_box.orientation = 'horizontal'
        ending_button_box.size_hint = (0.2, 1)

        ending_label = self.ids.ending_label
        ending_label.font_size = 24
        ending_label.halign = 'left'
        ending_label.valign = 'bottom'
        ending_label.line_height = 1.0

        with open(ending_text_file, "r", encoding='utf-8') as file:
            self.full_text_lines = file.readlines()

        Clock.schedule_interval(self.update_text, 1)

    def update_text(self, dt):
        """텍스트를 한 줄씩 업데이트. 완료되면 on_complete 콜백을 호출."""
        if self.current_index < len(self.full_text_lines):
            self.displayed_text += self.full_text_lines[self.current_index]
            self.ids.ending_label.text = self.displayed_text
            self.current_index += 1
        else:
            Clock.unschedule(self.update_text)
            if not self.button_added:
                self.add_go_to_main_button()
                self.button_added = True

    def add_go_to_main_button(self):
        self.ids.ending_button_box.clear_widgets()
        print(f'=========================={self.game_type}')
        if self.game_type == 'ending':
            self.ids.ending_button_box.add_widget(Button(
                on_press=self.go_back_to_main_menu,
                size_hint=(None, None),
                size=(100, 100),
                background_normal=os.path.join(ASSETS_ENDING_DIR, 'graduation_cap.png'),
                background_down=os.path.join(ASSETS_ENDING_DIR, 'graduation_cap.png'),
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            ))
        elif self.game_type == 'over':
            go_to_main_button = Button(
                text='> 다시 시작하기',
                font_name='NanumGothic.ttf',
                font_size=30,
                background_normal='',
                background_color=(0, 0, 0, 0),
                color=(1, 1, 1, 1),
                size_hint=(1, None),
                height=50,
                on_press=self.go_back_to_main_menu
            )
            exit_button = Button(
                text='> 졸업 포기하기',
                font_name='NanumGothic.ttf',
                font_size=30,
                background_normal='',
                background_color=(0, 0, 0, 0),
                color=(1, 1, 1, 1),
                size_hint=(1, None),
                height=50,
                on_press=self.quit_game
            )
            self.ids.ending_button_box.add_widget(go_to_main_button)
            self.ids.ending_button_box.add_widget(exit_button)

    def go_back_to_main_menu(self, instance):
        self.button_added = False
        self.ids.ending_button_box.clear_widgets()
        self.ids.ending_label.text = ''
        self.game_type = ''
        self.manager.current = 'mainmenu'

    def quit_game(self):
        self.stop()