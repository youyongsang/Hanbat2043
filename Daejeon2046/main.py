import kivy
from kivy.config import Config
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
import os
base_dir = os.path.dirname(__file__)
from kivy.core.text import LabelBase

# Register fonts used throughout the app (map logical font names or filenames to actual files present in the repo)
fonts_dir = os.path.join(base_dir, 'assets', 'fonts')
LabelBase.register(name='NanumGothic.ttf', fn_regular=os.path.join(fonts_dir, 'NanumGothic.ttf'))
LabelBase.register(name='GowunBatang-Bold.ttf', fn_regular=os.path.join(fonts_dir, 'GowunBatang-Bold.ttf'))
LabelBase.register(name='GowunBatang-Regular.ttf', fn_regular=os.path.join(fonts_dir, 'GowunBatang-Regular.ttf'))
LabelBase.register(name='Malgun Gothic', fn_regular=os.path.join(fonts_dir, 'malgunbd.ttf'))
# Some code expects 'H2GPRM' font name; map it to an available font
LabelBase.register(name='H2GPRM', fn_regular=os.path.join(fonts_dir, 'NanumGothic.ttf'))

from screens.main_menu.main_menu import MainMenu
from screens.game.game_screen import GameScreen
from screens.ending.ending_screen import EndingScreen
from screens.info.infoPage import InfoPage, FontManager
from screens.progress.progressPage import ProgressPage


class MyGameApp(App):
    def build(self):
        sm = ScreenManager()

        Builder.load_file(os.path.join(base_dir, 'Screens', 'main_menu', 'main_menu.kv'))
        Builder.load_file(os.path.join(base_dir, 'Screens', 'ending', 'ending_screen.kv'))
        Builder.load_file(os.path.join(base_dir, 'Screens', 'game', 'game_screen.kv'))

        sm.add_widget(MainMenu(name='mainmenu'))  # 스크린에 추가 스크린을 상속받은 클래스만 바로 추가 가능

        game_screen = GameScreen(screen_manager=sm, name='gamescreen')  # 해당 스크린에 스크린 매니저 전달
        sm.add_widget(game_screen)  # 스크린에 추가

        sm.add_widget(EndingScreen(name='endingscreen'))

        # 정보 페이지 화면 추가
        info_screen = Screen(name='info')  # info란 이름의 스크린 래핑
        # 박스 레이아웃인 InfoPage의 스크린 역할을 함
        info_page = InfoPage(screen_manager=sm)
        # InfoPage 클래스에 스크린 매니저 전달
        info_screen.add_widget(info_page)
        # 임시 래핑한 info스크린에 InfoPage위젯 부여(InfoPage는 박스레이아웃이다)
        sm.add_widget(info_screen)
        # 해당 스크린을 스크린 매니저에 추가

        # 진행도 페이지 화면 추가
        progress_screen = Screen(name='progress')
        progress_page = ProgressPage(screen_manager=sm)
        progress_screen.add_widget(progress_page)
        sm.add_widget(progress_screen)

        return sm

    def start_game(self):
        self.root.current = 'gamescreen'

    def game_ending(self, game_result):
        ending_screen = self.root.get_screen('endingscreen')
        ending_screen.show_screen(game_result)
        self.root.current = 'endingscreen'

    def quit_game(self):
        self.stop()


if __name__ == '__main__':
    MyGameApp().run()