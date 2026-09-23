import os
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.core.text import LabelBase
from kivy.graphics import Color, Rectangle, Line
from kivy.core.window import Window

# 폰트 등록 관리 클래스
class FontManager:
    @staticmethod
    def register_fonts():
        # 프로젝트의 assets/fonts 폴더에서 폰트 파일을 등록합니다
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        fonts_dir = os.path.join(base, 'assets', 'fonts')
        nanum = os.path.join(fonts_dir, 'H2GPRM.ttf')
        if os.path.exists(nanum):
            LabelBase.register(name='H2GPRM', fn_regular=nanum)

        malgun = os.path.join(fonts_dir, 'malgunbd.ttf')
        if os.path.exists(malgun):
            LabelBase.register(name='Malgun Gothic', fn_regular=malgun)

class ProgressPageCompo(BoxLayout):
    def __init__(self, screen_manager, layout, **kwargs):
        super().__init__(**kwargs)
        self.layout = layout
        self.progress_value = 50
        self.days_left = {'mid_exam': 5, 'project': 10, 'final_exam': 12}
        self.ability_stat = 0  # 능력치 기본 값으로 정수 설정

        self.progress_bar = []
        self.screen_manager = screen_manager

        # UI 요소 초기화
        self.days_left_labels = []
        self.back_button = None
        # progress_icon.png가 프로젝트의 assets/image_file에 있으므로 그 경로를 가리킴
        self.title_image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'image_file', 'progress_icon.png'))

        # GameScreen 이벤트 리스너 등록
        from screens.game.game_screen import GameScreen
        GameScreen.add_listener(self.on_stat_update)

        # UI 초기화
        self.initialize_components()

        # 창 크기 변경 시 진행 바 위치 업데이트
        self.layout.bind(size=self.update_progress_rect)

    def initialize_components(self):
        """UI 구성 요소를 초기화합니다."""
        self.days_left_labels = [
            self.create_days_left_label('중간고사', 'mid_exam'),
            self.create_days_left_label('팀 프로젝트', 'project'),
            self.create_days_left_label('기말고사', 'final_exam')
        ]
        self.back_button = self.create_back_button()

    def draw_progress_rect(self):
        """진행 바를 생성하고 중앙에 배치합니다."""
        self.rect_width = 600
        self.rect_height = 45

        with self.layout.canvas:
            # 테두리
            Color(1, 1, 1)
            self.progress_bar.append(
                Line(rectangle=(0, 0, self.rect_width, self.rect_height), width=9)
            )
            # 검정 배경
            Color(0, 0, 0)
            self.progress_bar.append(
                Rectangle(pos=(0, 0), size=(self.rect_width, self.rect_height))
            )
            # 진행 바
            Color(1, 1, 1)
            progress_width = (self.progress_value / 100) * self.rect_width
            self.progress_bar.append(
                Rectangle(pos=(0, 0), size=(progress_width, self.rect_height))
            )

        # 초기 위치 업데이트
        self.update_progress_rect()

    def create_back_button(self):
        """다른 UI 요소에 영향을 미치지 않고 독립적으로 위치하는 뒤로가기 버튼을 생성합니다."""
        # FloatLayout을 사용하여 버튼을 독립적으로 배치
        float_layout = FloatLayout(size_hint=(1, None), height=60)

        back_button = Button(
            text='> 돌아간다',
            size_hint=(None, None),  # 크기 고정
            size=(200, 50),  # 버튼의 크기 설정
            font_name='H2GPRM',
            font_size=24,
            background_color=(0, 0, 0, 1),
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.5, 'y': 0}  # 수평 중앙에 배치, y는 FloatLayout의 아래쪽
        )
        back_button.bind(on_press=self.on_button_clicked)

        # 버튼을 FloatLayout에 추가
        float_layout.add_widget(back_button)
        return float_layout

    def on_button_clicked(self, instance):
        """뒤로가기 버튼 클릭 시 호출됩니다."""
        self.screen_manager.current = 'gamescreen'

    def update_progress_rect(self, *args):
        """진행 바를 창 중앙에 위치시킵니다."""
        x_pos = (Window.width - self.rect_width) / 2
        y_pos = (Window.height - self.rect_height) / 2
        self.progress_bar[0].rectangle = (x_pos, y_pos, self.rect_width, self.rect_height)
        self.progress_bar[1].pos = (x_pos, y_pos)
        self.progress_bar[2].pos = (x_pos, y_pos)

    def on_stat_update(self, stat):
        """GameScreen에서 능력치 업데이트 시 호출됩니다."""
        if isinstance(stat, int):  # stat이 정수인지 확인
            self.ability_stat = stat
            self.update_ui()
        else:
            print(f"올바르지 않은 stat 값: {stat}")
            self.ability_stat = stat.get('day')

    def update_day_stat(self, day):
        """외부에서 day 값을 업데이트할 수 있도록 메서드 추가."""
        if isinstance(day, int):  # day가 정수인지 확인
            self.ability_stat = day
            self.update_ui()
        else:
            print(f"올바르지 않은 day 값: {day}")

    def update_ui(self):
        """UI를 업데이트합니다."""
        for i, label in enumerate(self.days_left_labels):
            event_key = list(self.days_left.keys())[i]
            days_left = max(0, self.days_left[event_key] - self.ability_stat)
            label.text = f"{label.text.split('까지')[0]}까지 {days_left}일 남았다."
            print(f"{event_key} 남은 일수: {days_left}")

        # UI 새로고침
        self.layout.canvas.ask_update()

    def create_days_left_label(self, event_name, event_key):
        """남은 일수 라벨을 생성합니다."""
        days_left = max(0, self.days_left[event_key] - self.ability_stat)
        days_left_text = f"{event_name}까지 {days_left}일 남았다."
        return Label(text=days_left_text, size_hint=(1, None), height=30, font_name='H2GPRM')

class ProgressPageBackground:
    def __init__(self, layout):
        self.layout = layout
        self.layout.bind(size=self.update_rect, pos=self.update_rect)
        with self.layout.canvas.before:
            Color(0, 0, 0, 1)
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)

    def update_rect(self, *args):
        self.rect.size = self.layout.size
        self.rect.pos = self.layout.pos

def ProgressPage(screen_manager):
    """진행도 페이지의 위젯을 반환합니다."""
    layout = FloatLayout(size=(400, 600))
    ProgressPageBackground(layout)

    # ProgressPageCompo 생성 및 초기화
    progress_compo = ProgressPageCompo(screen_manager, layout)
    layout.progress_compo = progress_compo

    # 이미지 추가 또는 대체 텍스트
    if os.path.exists(progress_compo.title_image_path):
        title_image = Image(
            source=progress_compo.title_image_path,
            size_hint=(1, None), height=100, pos_hint={'top': 0.68}
        )
        layout.add_widget(title_image)
    else:
        layout.add_widget(Label(
            text="progress_icon.png 파일을 찾을 수 없습니다.",
            font_name='Malgun Gothic', size_hint=(1, None), height=150, pos_hint={'top': 0.85}
        ))

    # 텍스트 레이블을 위한 BoxLayout
    text_layout = BoxLayout(
        orientation='vertical',
        size_hint=(1, None),  # 높이 고정을 위해 size_hint 설정
        height=150,  # 적절한 높이 설정
        pos_hint={'top': 0.45},
        padding=[10, 10, 10, 10], spacing=10
    )

    # 텍스트 레이블 추가
    for label in progress_compo.days_left_labels:
        text_layout.add_widget(label)

    # 텍스트 레이아웃을 추가
    layout.add_widget(text_layout)

    # 뒤로가기 버튼을 독립적으로 추가
    progress_compo.back_button.pos_hint = {'center_x': 0.5, 'y': 0.1}
    layout.add_widget(progress_compo.back_button)

    # 진행 바 그리기 및 중앙 배치
    progress_compo.draw_progress_rect()

    return layout