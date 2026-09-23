import os
from kivy.core.text import LabelBase
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

class FontManager:
    """커스텀 폰트 등록을 위한 클래스."""
    @staticmethod
    def register_fonts():
        """H2GPRM 폰트를 프로젝트의 assets/fonts에서 등록합니다."""
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        fonts_dir = os.path.join(base, 'assets', 'fonts')
        nanum = os.path.join(fonts_dir, 'H2GPRM.ttf')
        if os.path.exists(nanum):
            LabelBase.register(name='H2GPRM', fn_regular=nanum)

# Note: InfoPage에서 GameScreen import 경로는 프로젝트 표준인 'screens'를 사용합니다.

class InfoPage(FloatLayout):
    """사용자 정보와 능력치를 출력하는 UI 페이지를 구성하는 클래스."""
    def __init__(self, screen_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager
        self.userName = "생존자"
        self.userState = "신탄진동 생존구역에 거주 중이다."
        self.userTrait = "처음 선택한 특성에 관한 문구"

        from screens.game.game_screen import GameScreen

        # GameScreen에서 능력치 불러오기
        GameScreen.add_listener(self.on_stat_update)  # 리스너 추가
        self.ability_stat = GameScreen.ability_stat  # 초기 능력치 불러오기

        # UI 구성
        self.setup_ui()

    def on_stat_update(self, stat):
        """GameScreen에서 능력치 업데이트가 발생했을 때 호출되는 메서드."""
        self.update_ability_stat(stat)

    def update_ability_stat(self, stat):
        """전달받은 stat 배열을 사용해 UI 업데이트."""
        self.ability_stat = stat
        print("infoPage에서 Stat 데이터:", self.ability_stat)
        self.update_ui()  # UI 업데이트 로직

    def update_ui(self):
        """UI를 능력치 정보에 맞게 업데이트."""
        # UI 갱신 로직 추가
        self.clear_widgets()
        self.setup_ui()

    def get_info(self):
        """사용자 이름과 특성을 포맷팅된 문자열로 반환합니다."""
        return f"{self.userName}\n{self.userState}\n\n\" {self.userTrait} \""

    def setup_ui(self):
        """UI를 구성하고 초기화합니다."""
        # 텍스트 레이아웃
        text_layout = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height=400,
            pos_hint={'top': 0.9},  # top 위치를 0.9로 변경해 1cm 정도 아래로 이동
            spacing=10  # 위젯 간 간격 추가
        )

        # 정보 제목
        text_layout.add_widget(self.create_label('__정보__', font_size='24sp', height=40, bold=True, padding_y=38))

        # 사용자 정보
        text_layout.add_widget(self.create_label(self.get_info(), font_size='18sp', height=100, padding_y=38))

        # 능력치 제목
        text_layout.add_widget(self.create_label('__능력치__', font_size='24sp', height=40, bold=True, padding_y=38))

        # 능력치 리스트
        for name, level in self.ability_stat.items():
            description = self.get_ability_description(name)
            if description != "설명이 없습니다.":
                formatted_text = f'  {name} : Lv {level} : "{description}"'
                text_layout.add_widget(self.create_label(formatted_text, font_size='18sp', height=30, padding_y=38))

        # 텍스트 레이아웃 추가
        self.add_widget(text_layout)

        # 돌아가기 버튼
        self.add_widget(self.create_back_button())

    def create_label(self, text, font_size, height, bold=False, padding_y=0):
        """공통적으로 사용되는 Label을 생성."""
        return Label(
            text=text,
            font_size=font_size,
            bold=bold,
            size_hint=(None, None),  # 크기를 고정
            width=800, height=height,  # 기존 높이를 유지
            font_name='H2GPRM',
            halign='left',
            valign='middle',  # 텍스트 세로 정렬 유지
            text_size=(800, None),  # 텍스트 너비 고정
            padding=(50, padding_y)  # 패딩 추가: Y축으로 아래로 이동
        )

    def get_ability_description(self, name):
        """각 능력치의 설명을 반환합니다."""
        descriptions = {
            "컴퓨터기술": "컴퓨터를 다루는 능력",
            "체력": "육체적인 힘과 건강",
            "운": "행운과 기회",
            "지능": "논리적 사고 및 문제 해결 능력",
            "타자": "빠르게 정확히 타자치는 능력",
            "속독": "문서를 빠르게 읽는 능력",
            "창의력": "창의적 사고와 발상"
        }
        return descriptions.get(name, "설명이 없습니다.")

    def create_back_button(self):
        """돌아가기 버튼 생성."""
        back_button = Button(
            text='> 돌아간다',
            size_hint=(None, None),  # 고정 크기로 설정
            width=200, height=50,  # 버튼 크기 설정
            font_name='H2GPRM', font_size=24,
            background_color=(0, 0, 0, 1),
            color=(1, 1, 1, 1),
            pos_hint={'x': 0.05, 'y': 0.05}  # 왼쪽 아래에 위치
        )
        back_button.bind(on_press=self.on_button_clicked)
        return back_button

    def on_button_clicked(self, instance):
        """돌아가기 버튼 클릭 시 호출되는 메서드."""
        self.screen_manager.current = 'gamescreen'