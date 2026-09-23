import kivy
import random
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.anchorlayout import AnchorLayout
from kivy.clock import Clock  # Kivy의 Clock을 이용해 딜레이 처리
from typing import Tuple, Any
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.image import Image
from screens.info.infoPage import InfoPage, FontManager
from screens.progress.progressPage import ProgressPage
import os
STORY_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'story'))
import re
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

IMAGE_BASE_PATH = "assets/image_file/"
SOUND_BASE_PATH = "assets/sound_file/"
# 아이콘 폴더 경로 (절대 경로로 변환)
ICON_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'image_file', 'icon'))


# 기본 16:9 비율 설정 (예: 720x1280)
target_aspect_ratio = 16 / 9

from kivy.properties import ListProperty


class ColoredBox(Widget):
    """사각형 배경 위젯. KV에서 `color: r, g, b, a`로 설정 가능하도록 구현했습니다."""
    color = ListProperty([1, 0, 0, 1])  # 기본 빨강

    def __init__(self, **kwargs):
        super(ColoredBox, self).__init__(**kwargs)
        with self.canvas:
            # Color 인스트럭션을 멤버로 보관해 나중에 변경하도록 함
            self._color_instr = Color(*self.color)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        # 크기/위치/색상 변경 시 업데이트
        self.bind(size=self.update_rect, pos=self.update_rect, color=self.update_color)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def update_color(self, instance, value):
        # ListProperty로부터 색상값이 바뀌면 캔버스 Color 인스트럭션을 갱신
        if hasattr(self, '_color_instr'):
            self._color_instr.rgba = value
class ClickableLabel(ButtonBehavior, Label):
    pass

class GameScreen(Screen):
    # KV에서 정의한 위젯들을 매핑하기 위한 프로퍼티
    main_layout = ObjectProperty(None)
    text_area = ObjectProperty(None)
    right_layout = ObjectProperty(None)
    stat_image_layout = ObjectProperty(None)
    choice1 = ObjectProperty(None)
    choice2 = ObjectProperty(None)
    choice3 = ObjectProperty(None)
    choice4 = ObjectProperty(None)
    image_overlay = ObjectProperty(None)
    image_rect = ObjectProperty(None)

    ability_stat = {"컴퓨터기술": 0, "체력": 0, "운": 1, "허기": 0, "지능": 0, "타자": 0,
                    "속독": 0, "창의력":0, "속도" : 0, "돈": 3, "집중도": 3, "멘탈": 3,"성적": 100,  "sw" : 0, "zoom" : 0, "day" : 0, "팀인원":0, "dinner" : 0, "저녁약속" : 0, "동아리" : 0
                    ,"running" : 0, "service" : 0}
    on_choice_able = False
    start = False
    reaction_part = False
    event = False
    flag = True
    end = False
    day = 0
    choice = 0
    group_count = 0
    reaction_line = ""
    file_name = ""
    save_file_name = ""
    saved_re_position = ""
    previous_name = "mainmenu"

    listeners = []  # 변수 연결용

    def __init__(self, screen_manager=None, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.screen_manager = screen_manager  # ScreenManager 인스턴스 저장
        # 레이아웃/위젯은 KV에서 정의되므로 여기서는 초기화만 수행합니다.
        self.reaction_index = {}          # ✅ 현재 로드된 리액션 파일의 #태그 인덱스
        self.reaction_index_file = None   # ✅ 인덱스가 어떤 파일 기준인지

    @classmethod
    def add_listener(cls, listener):
        """변경 사항을 알리기 위한 리스너를 추가합니다."""
        cls.listeners.append(listener)

    @classmethod
    def update_stat(cls, stat_name='day', value='0'):
        """능력치를 업데이트하고 리스너에게 변경 사항을 알립니다."""
        if stat_name in cls.ability_stat:
            cls.ability_stat[stat_name] = value
            cls.notify_listeners()  # 모든 리스너에게 변경 사항 알림
            print("리스너 변경사항 전달")

    @classmethod
    def notify_listeners(cls):
        """모든 리스너에게 능력치 변경을 알립니다."""
        for listener in cls.listeners:
            listener(cls.ability_stat)

    def on_kv_post(self, base_widget):
        """KV가 로드된 직후 실행되어 위젯 참조를 초기화합니다."""
        # image_rect가 KV에서 id로 설정되어 있으면 직접 가져오고, 없으면 canvas에서 검색
        rect_instr = self.ids.get('image_rect')
        if rect_instr:
            self.image_rect = rect_instr
        else:
            for instr in self.image_overlay.canvas.children:
                if isinstance(instr, Rectangle):
                    self.image_rect = instr
                    break


        # 텍스트 위젯 이벤트/바인딩 설정
        if self.text_area:
            # 텍스트 클릭 및 이미지 overlay 바인딩 설정
            self.text_area.bind(on_touch_down=self.on_click_next_text)
            self.text_area.bind(pos=self.update_image_overlay, size=self.update_image_overlay)

        # 이미지 오버레이 초기 상태
        if self.image_overlay:
            self.image_overlay.opacity = 0

        # 윈도우 리사이즈 바인딩 및 스탯 초기화
        Window.bind(on_resize=self.adjust_layout)
        self.update_stat_images()
    def update_text_background(self, *args):
        """텍스트 영역 배경 업데이트 (KV에서 처리하는 경우 안전하게 무시)."""
        if hasattr(self, 'text_bg_rect') and self.text_bg_rect:
            self.text_bg_rect.size = self.text_area.size
            self.text_bg_rect.pos = self.text_area.pos

    def update_image_overlay(self, *args):
        """이미지 레이아웃 업데이트."""
        self.image_rect.pos = (self.text_area.pos[0], self.text_area.pos[1] + self.text_area.size[1] / 2)
        self.image_rect.size = (self.text_area.size[0], self.text_area.size[1] / 2)

    def reset_game(self):
        """ 게임 상태를 초기화하는 메서드 """
        self.start = True
        self.reaction_part = False
        self.flag = True
        self.is_waiting_for_click = False
        self.event = False
        self.end = False
        self.choice = 0
        self.current_line = 0
        self.day = 0
        self.group_count = 0
        self.reaction_line = ""
        self.file_name = os.path.join(STORY_DIR, 'start_story.txt')
        self.save_file_name = ""
        self.saved_re_position = ""
        self.text_area.text = ""
        self.ability_stat = {"컴퓨터기술": 0, "체력": 0, "운": 1, "허기": 0, "지능": 0, "타자": 0,
                             "속독": 0, "창의력":0, "속도" : 0, "돈": 3, "집중도": 3, "멘탈": 3,"성적": 100, "sw" : 0,  "zoom" : 0, "day" : 0, "팀인원":0, "dinner" : 0, "저녁약속" : 0,"동아리" : 0
                             ,"running" : 0, "service" : 0}
        self.update_stat_images()
        self.story_lines = self.read_story_text(os.path.join(STORY_DIR, 'start_story.txt')).splitlines()
        self.start_automatic_text()

        self.listeners = [] # 변수 연결용


    def on_enter(self):
        # GameScreen에 들어왔을 때 텍스트 출력을 시작합니다.
        print("on enter 실행")
        if self.previous_name == "mainmenu":
            self.reset_game()
        else:
            print(self.previous_name)

    def open_info_page(self, instance):
        info_screen = self.screen_manager.get_screen('info')  # 'a' 화면 가져오기
        info_layout = info_screen.children[0]  # ABoxLayout 인스턴스 (Screen의 첫 번째 자식)
        info_layout.update_ability_stat(self.ability_stat)  # 점수 전달

        # a 화면으로 전환
        self.screen_manager.current = 'info'
        self.previous_name = "other"

    def open_progress_page(self, instance):
        # 'progress' 화면 가져오기
        progress_screen = self.screen_manager.get_screen('progress')
        progress_layout = progress_screen.children[0]  # ProgressPage 인스턴스

        progress_compo = progress_layout.progress_compo

        progress_compo.update_day_stat(self.day)  # update_day 메서드를 추가해 self.day 값을 반영하도록 함
        # progress 화면으로 전환
        self.screen_manager.current = 'progress'
        self.previous_name = "other"
    # 윈도우 크기가 변경될 때 비율 조정
    def adjust_layout(self, instance, width, height):
        # 현재 창의 비율 계산
        self.text_area.text_size = (width * 7 / 8-30, None)
        if width >800:
            self.text_area.font_size = 32
            self.choice1.font_size = 28
            self.choice2.font_size = 28
            self.choice3.font_size = 28
            self.choice4.font_size = 28
        else :
            self.text_area.font_size = 24
            self.choice1.font_size = 22
            self.choice2.font_size = 22
            self.choice3.font_size = 22
            self.choice4.font_size = 22

    def update_stat_images(self):
        """ 스탯 값에 따라 이미지를 갱신하는 함수 """
        # 기존 이미지 제거
        self.stat_image_layout.clear_widgets()

        # '돈'에 해당하는 돈 이미지
        money_stat = self.ability_stat.get('돈', 0)
        money_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50)
        for _ in range(money_stat):
            money_layout.add_widget(Image(source=os.path.join(ICON_DIR, 'money.png')))  # 돈 이미지 경로 설정
        self.stat_image_layout.add_widget(money_layout)

        # '집중도'에 해당하는 세모 이미지
        focus_stat = self.ability_stat.get('집중도', 0)
        focus_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50)
        for _ in range(focus_stat):
            focus_layout.add_widget(Image(source=os.path.join(ICON_DIR, 'pen.png')))  # 연필 이미지 경로 설정
        self.stat_image_layout.add_widget(focus_layout)

        # '멘탈'에 해당하는 하트 이미지
        mental_stat = self.ability_stat.get('멘탈', 0)
        mental_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50)
        for _ in range(mental_stat):
            mental_layout.add_widget(Image(source=os.path.join(ICON_DIR, 'heart.png')))  # 하트 이미지 경로 설정
        self.stat_image_layout.add_widget(mental_layout)

    # 텍스트 파일에서 내용을 읽어오는 함수
    def read_story_text(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.file_name = file.name
                return file.read()
        except FileNotFoundError:
            return "스토리 파일을 찾을 수 없습니다."

    # 자동으로 텍스트를 출력하는 함수 이벤트 분기 확인
    def start_automatic_text(self, dt=None):
        self.update_day_flag()

        while self.current_line < len(self.story_lines):
            line = self.story_lines[self.current_line].strip()
    
            if self.handle_reaction_search(line):
                return
    
            if self.handle_script_command(line):
                return
    
            if self.handle_choice_block(line):
                return
    
            if self.handle_reaction_entry(line):
                return
    
            if self.handle_reaction_exit(line):
                return
    
            self.handle_normal_text(line)
            return

        self.handle_story_end()

    #--- 짝수별로 돈 추가 ---#
    def update_day_flag(self):
        self.ability_stat["day"] = 1 if self.day % 2 == 0 else 0

    #--- 이미지 or 오디오 커맨드 판별 ---#
    def handle_script_command(self, line):
        if line.startswith("f:I"):
            filename = line[3:].strip()
            self.update_image_source(filename)
            self.image_overlay.opacity = 1
            self.text_area.text = "\n\n\n\n\n"
            self.current_line += 1
            Clock.schedule_once(self.start_automatic_text, 0.5)
            return True
    
        if line.startswith("f:A"):
            filename = line[3:].strip()
            if filename:
                self.play_audio(filename)
            else:
                self.fade_out_audio()
            self.current_line += 1
            return True
    
        return False
    
    #--- 선택지 텍스트 판별, 선택지 버튼 생성 ---#
    def handle_choice_block(self, line):
        if line.startswith("-"):
            self.is_waiting_for_click = False
            self.on_choice_able = True
            self.set_choices_from_story(self.current_line)
            return True
        return False

    #--- 리액션 파일 진입 전, 조건문 파싱 ---#
    def handle_reaction_entry(self, line):
        if line.startswith("#") and not self.reaction_part:
            self.reaction_line = line
    
            while ":" in self.reaction_line and "?" in self.reaction_line:
                self.reaction_line = "#" + self.parse_conditional_reaction(
                    self.reaction_line[1:]
                )
    
            self.load_alternate_story(self.current_line + 1, self.reaction_line)
            return True
    
        return False

    #--- 리액션 파트 진입, 정확한 리액션 파일 위치 탐색 ---#
    def handle_reaction_search(self, line):
        if not self.reaction_part:
            return False
    
        if self.reaction_line == "# lecture": #일상 루트, 강의 전용 리액션 파일 진입
            num = random.randint(1, 3)
            self.reaction_line = f"# lecture_{num + 3*self.ability_stat['dinner']}"
    
        if line.startswith("#") and line == self.reaction_line:
            self.flag = True
            self.current_line += 1
            return False
    
        if not self.flag:
            self.current_line += 1
            Clock.schedule_once(self.start_automatic_text, 0) 
            return True
    
        return False
        
    #--- 리액션 파일 탈출 로직---#
    def handle_reaction_exit(self, line):
        # 또 다른 리액션 파트에 도달하거나 pass를 확인하면 탈출
        is_pass = line == "pass" or line.startswith("pass ")
        if (line.startswith("#") and line != self.reaction_line) or is_pass:
            self.reaction_part = False
            # 저장된 파일, 텍스트로 이동동
            self.story_lines = self.read_story_text(self.save_file_name).splitlines()
            # "pass N" 형태면 원본 파일의 N번째 줄(0-index)로, 그냥 "pass"면 진입 전 위치로 복귀
            jump_target = line[5:].strip() if line.startswith("pass ") else ""
            if jump_target.isdigit():
                self.current_line = int(jump_target)
            else:
                self.current_line = self.saved_re_position + 1
            Clock.schedule_once(self.start_automatic_text, 0.5)
            return True
        return False

    #--- 다음 텍스트 출력 로직 ---#
    def handle_normal_text(self, line):
        if line == "":
            self.is_waiting_for_click = True
            return
    
        self.text_area.text += line + "\n"
        self.current_line += 1
        Clock.schedule_once(self.start_automatic_text, 0.5)

    
    #--- 스토리 진행 로직 ---#
    def handle_story_end(self):
        # 1) reaction 종료 복귀
        if self.reaction_part:
            print("리액션 파트 종료")
            self.story_lines = self.read_story_text(self.save_file_name).splitlines()
            self.current_line = self.saved_re_position + 1
            self.reaction_part = False
            Clock.schedule_once(self.start_automatic_text, 0.5)
            return
    
        # 2) 엔딩
        if self.end:
            self.previous_name = "mainmenu"
            self.end_game()
            return
    
        # 3) ✅ start_story 종료 후 1회성 메인 진입
        if self.start:
            self._enter_main_story_first_time()
            return
    
        # 4) 이벤트 스토리 종료 처리
        if self.event:
            self._return_from_event_story()
            return
    
        # 5) 이후 day 루틴/분기들
        self._advance_day_routine()

    #--- 첫 날 전용 로직 ---#
    def _enter_main_story_first_time(self):
        self.story_lines = self.read_story_text(os.path.join(STORY_DIR, 'main_story.txt')).splitlines()
        self.current_line = 0
        self.start = False
        self.day += 1
        self.text_area.text += f"{self.day}일차입니다.\n"
        Clock.schedule_once(self.start_automatic_text, 0.5)

    #--- 이벤트 스토리 종료 로직 ---#
    def _return_from_event_story(self):
        print("이벤트 스토리 종료 메인 스토리 위치로 돌아갑니다.")
    
        # i.txt는 특수 복귀 지점(하드코딩) 유지
        if self.file_name == os.path.join(STORY_DIR, 'event_story', 'i.txt'):
            self.current_line = 79
        else:
            # 이벤트 진입 전에 저장해둔 메인 스토리 위치로 복귀
            self.current_line = self.saved_position + 1
    
        self.story_lines = self.read_story_text(os.path.join(STORY_DIR, 'main_story.txt')).splitlines()
        self.event = False
        Clock.schedule_once(self.start_automatic_text, 0.5)

    #--- 메인 스토리 처리 로직 ---#
    def _advance_day_routine(self):
        # 메인 스토리 루트가 5주차 진입 시 중간고사 이벤트
        if self.day == 4:
            self.day += 1
            self.story_lines = self.read_story_text(os.path.join(STORY_DIR, 'middle_story.txt')).splitlines()
            self.current_line = 0
            Clock.schedule_once(self.start_automatic_text, 0.5)
            return
    
        # 메인 스토리 루틴 11주차까지 진행 (단, 10주차인 day==9는 조별과제로 분기)
        if self.day <= 10 and self.day != 9:
            print("메인스토리 루트 진행")
            self.story_lines = self.read_story_text(os.path.join(STORY_DIR, 'main_story.txt')).splitlines()
            self.current_line = 0
            self.day += 1
            self.text_area.text += f"{self.day}일차입니다.\n"
            Clock.schedule_once(self.start_automatic_text, 0.5)
            return
    
        # 조별과제 엔딩 루트 진행 (10주차)
        if self.day == 9:
            print("조별과제 엔딩 루트 진행")
            path = os.path.join(
                STORY_DIR, 'group_task', 'result', f"{self.ability_stat['팀인원']}.txt"
            )
            self.story_lines = self.read_story_text(path).splitlines()
            self.current_line = 0
            self.day += 1
            self.text_area.text += f"{self.day}일차입니다.\n"
            Clock.schedule_once(self.start_automatic_text, 0.5)
            return
    
        # 12주차: 기말고사 and end스토리 진입
        if self.day == 11:
            self.story_lines = self.read_story_text(os.path.join(STORY_DIR, 'end_story.txt')).splitlines()
            self.current_line = 0
            self.day += 1
            Clock.schedule_once(self.start_automatic_text, 0.5)
            return
    
        # 13주차: 엔딩 분기
        if self.day == 12:
            self.load_ending_branch()
            return

    def update_image_source(self, image_path):
        """이미지 오버레이에 새로운 이미지를 설정."""
        if self.image_rect:
            self.image_rect.source = image_path  # 이미지 경로 업데이트
            self.image_overlay.canvas.ask_update()  # 캔버스 업데이트 요청

    def play_audio(self, audio_path):
        """지정된 경로의 사운드를 재생."""
        if hasattr(self, 'sound') and self.sound:
            self.sound.stop()  # 기존에 재생 중인 사운드 정지

        self.sound = SoundLoader.load(audio_path)  # 새로운 사운드 로드
        if self.sound:
            print(f"사운드 재생 중: {audio_path}")
            self.sound.volume = 0  # 초기 볼륨 0
            self.sound.play()  # 사운드 재생

            # 사운드 길이 확인
            if self.sound.length and self.sound.length >= 5:  # 사운드 길이가 5초 이상인 경우
                print(f"사운드 길이: {self.sound.length}초, 점진적 볼륨 증가 시작")
                self.fade_in_event = Clock.schedule_interval(self.increase_volume, 0.1)  # 0.1초마다 볼륨 증가
            else:
                print(f"사운드 길이: {self.sound.length}초, 볼륨 즉시 최대")
                self.sound.volume = 1.0  # 볼륨을 즉시 최대치로 설정
        else:
            print(f"사운드 파일을 찾을 수 없습니다: {audio_path}")

    def increase_volume(self, dt):
        """볼륨을 점차적으로 증가."""
        if hasattr(self, 'sound') and self.sound:
            if self.sound.volume < 1.0:
                self.sound.volume = min(1.0, self.sound.volume + 0.05)  # 0.05씩 증가
            else:
                print("볼륨 최대치 도달")
                Clock.unschedule(self.fade_in_event)  # 볼륨 증가 중지

    def fade_out_audio(self):
        """사운드의 볼륨을 점진적으로 줄인 후 정지."""
        if hasattr(self, 'sound') and self.sound:
            self.fade_out_event = Clock.schedule_interval(self.reduce_volume, 0.1)  # 0.1초 간격으로 볼륨 감소

    def reduce_volume(self, dt):
        """사운드 볼륨을 감소시키는 함수."""
        if hasattr(self, 'sound') and self.sound:
            if self.sound.volume > 0:
                self.sound.volume = max(0, self.sound.volume - 0.05)  # 0.05씩 감소
            else:
                print("사운드 정지")
                self.sound.stop()
                self.sound = None
                Clock.unschedule(self.fade_out_event)  # 볼륨 감소 스케줄 취소

    def set_choices_from_story(self, start_index):
        choices = []
        adjustments = []

        # 선택지 라인들 (`-`로 시작하는 줄)을 추출
        while start_index < len(self.story_lines):
            line = self.story_lines[start_index].strip()

            # `-`로 시작하는 줄은 선택지로 처리
            if line.startswith("-"):
                choice_text = line[1:].strip()  # `-` 기호를 제거한 선택지 텍스트
                reaction_number = -1  # 기본값은 -1로 설정

                # `_`로 끝나는지 여부를 확인하고 필요 시 마지막 `_` 제거
                choice_has_underscore = choice_text.endswith("_")
                if choice_has_underscore:
                    choice_text = choice_text[:-1]

                # 조건문이 포함된 경우 처리
                while(True):
                    if ":" in choice_text and "?" in choice_text:
                        choice_text = self.parse_conditional_choice(choice_text)
                    else:
                        break

                # 확률값이 있는 경우 처리
                if "*" in choice_text:
                    choice_text = self.parse_luck_adjustment(choice_text)

                # 가중치 정보가 있는 경우 처리
                if "%" in choice_text or "&" in choice_text:
                    choice, adjustment = self.parse_choice_adjustment(choice_text)
                else:
                    choice, adjustment = choice_text, None

                # `[숫자]` 형태의 리액션 구분 숫자 추출
                match = re.search(r'\[(\d+)\]', choice)
                if match:
                    reaction_number = int(match.group(1))  # 숫자를 reaction_number로 설정
                    choice = re.sub(r'\[\d+\]', '', choice).strip()  # `[]` 구문 제거하여 선택지 텍스트만 남김

                # 빈 선택지는 choices에 추가하지 않음
                if choice:  # 선택지 텍스트가 빈 문자열이 아닌 경우에만 추가
                    choices.append((choice, choice_has_underscore, reaction_number))
                    adjustments.append(adjustment)
            else:
                break  # `-`로 시작하지 않으면 선택지 추출 종료

            start_index += 1

        # 최종 선택지 리스트 역순으로 저장
        choices.reverse()
        adjustments.reverse()

        # 선택지 버튼 텍스트 설정 (선택지 텍스트와 `_` 여부, reaction_number를 분리하여 사용)
        if len(choices) >= 1:
            self.choice1.text = choices[0][0]
            self.choice1.has_underscore = choices[0][1]  # `_` 여부 저장
            self.choice1.reaction_number = choices[0][2]
        if len(choices) >= 2:
            self.choice2.text = choices[1][0]
            self.choice2.has_underscore = choices[1][1]
            self.choice2.reaction_number = choices[1][2]
        if len(choices) >= 3:
            self.choice3.text = choices[2][0]
            self.choice3.has_underscore = choices[2][1]
            self.choice3.reaction_number = choices[2][2]
        if len(choices) >= 4:
            self.choice4.text = choices[3][0]
            self.choice4.has_underscore = choices[3][1]
            self.choice4.reaction_number = choices[3][2]

        # 선택지에 대응하는 능력치 조정 리스트 저장
        self.adjustments = adjustments

        # 선택지 이후의 줄을 스토리 출력 시작 위치로 설정
        self.current_line = start_index  # 선택지 이후의 첫 번째 줄로 이동

    def parse_conditional_choice(self, choice_text):
        # ':'와 '?'로 조건문을 나누기
        main_part, conditional_part = choice_text.split(":", 1)  # 분할 횟수 1 참일 때 실행 문장과 나머지로 이루어짐
        condition, else_part = conditional_part.split("?", 1)  # 분할 횟수 1 조건문과 거짓일 때 실행 문장으로 이루어짐

        # 조건문 해석
        stat_name = ''.join([char for char in condition if char.isalpha()])  # 영어 또는 한글만 출력 (변경 스탯)
        stat_value = int(''.join([char for char in condition if char.isdigit()]))  # 숫자만 출력 (변경값)
        operator = ''.join([char for char in condition if not char.isalnum()])  # 영어 또는 한글이 아닌 특수문자인 경우만 출력 (조건문부등호)

        # stat 딕셔너리에서 현재 능력치를 확인
        current_stat_value = self.ability_stat.get(stat_name, 0)  # 키가 존재하지 않을 경우 0을 반환 (0대신 None넣어도 될듯)

        # 조건 비교
        if self.evaluate_condition(current_stat_value, stat_value, operator):
            # 조건이 참이면 main_part를 선택지 텍스트로 사용하고 조정값 추출
            return main_part
        else:
            # 조건이 거짓이면 else_part를 선택지 텍스트로 사용하고 조정값 추출
            return else_part

    def parse_conditional_reaction(self, line_text):
        main_part, conditional_part = line_text.split(":", 1)  # 참일 때 실행 문장과 나머지로 분리
        condition, else_part = conditional_part.split("?", 1)  # 조건문과 거짓일 때 실행 문장으로 분리

        # 조건문 해석
        stat_name = ''.join([char for char in condition if char.isalpha()])  # 영어 또는 한글만 출력 (변경 스탯)
        stat_value = int(''.join([char for char in condition if char.isdigit()]))  # 숫자만 출력 (변경값)
        operator = ''.join([char for char in condition if not char.isalnum()])  # 특수문자만 출력 (조건문 부등호)

        # stat 딕셔너리에서 현재 능력치를 확인
        current_stat_value = self.ability_stat.get(stat_name, 0)  # 키가 존재하지 않을 경우 0 반환

        # 조건 비교
        if self.evaluate_condition(current_stat_value, stat_value, operator):
            # 조건이 참이면 main_part 반환
            return main_part
        else:
            # 조건이 거짓이면 else_part 반환
            return else_part

    # 텍스트 파일의 조건문에 대한 판별 함수
    def evaluate_condition(self, current_value, target_value, operator):
        if operator == ">=":
            return current_value >= target_value
        elif operator == "<=":
            return current_value <= target_value
        elif operator == "==":
            return current_value == target_value
        elif operator == ">":
            return current_value > target_value
        elif operator == "<":
            return current_value < target_value
        return False  # 정의되지 않은 연산자일 경우 False 반환

    # 선택지 텍스트 내용과 능력치 조정 내용을 구분하는 함수
    def extract_choice_and_adjustment(self, text):
        if "%" in text or "&" in text:  # 수행 문장에 능력치 조정이 있는 지 판단
            choice, adjustment = self.parse_choice_adjustment(text)  # 있을 경우 능력치 조정
            return choice, adjustment
        else:
            return text, None  # 능력치 조정이 없는 경우 텍스트만 반환

    def parse_choice_adjustment(self, choice_text):
        """
        텍스트에서 여러 능력치 조정을 처리하는 함수
        예: %지능1&체력1 또는 &지능1%체력1 혼합 형태도 처리 가능
        """
        adjustments = []  # 여러 능력치 조정을 담을 리스트

        # 능력치 조정 전의 선택지 텍스트
        choice_part = re.split("[%&]", choice_text)[0].strip()

        # 조정치 부분만 추출하기 (%, & 기준으로 split)
        adjustment_parts = re.findall(r'[%&][가-힣A-Za-z0-9]+', choice_text)
        # %나 &로 시작하는 단어들 구분 추출 ex &지능1%속독1인경우 &나 %을 기준으로 나눠져서 ['&지능1','%속독1']이 된다.

        for part in adjustment_parts:
            sign = '+' if part[0] == '%' else '-'  # %면 +, &면 - (상황에 맞게 변경 가능)
            adjustments.append(self.extract_stat_adjustment(part[1:], sign))  # part[1:]조정 속성(&%)을 제외한 나머지 문장

        return choice_part, adjustments

    def extract_stat_adjustment(self, adjustment_text: str, operation: str) -> Tuple[str, int, str]:
        """
        주어진 능력치 조정 텍스트에서 능력치 이름과 값을 추출하고 조정 정보 반환
        """
        # 능력치 이름만 추출 (한글 또는 영어 알파벳만 사용)
        stat_name = ''.join([char for char in adjustment_text if char.isalpha()])

        # 능력치 값만 추출
        stat_value = ''.join([char for char in adjustment_text if char.isdigit()])

        # 값이 없을 경우 기본값 0 설정
        stat_value = int(stat_value) if stat_value else 0  # 문자형으로 받았으니 int형 변경

        return (stat_name, stat_value, operation)

    def parse_luck_adjustment(self, choice_text):
        # *숫자* 형식을 찾고 파싱
        if '*' in choice_text:
            print("운 확인 요소 진입 성공")
            parts = choice_text.split('*')
            print("parts=", parts)
            luck_factor = int(parts[1])  # *숫자* 사이의 숫자
            player_luck = self.ability_stat["운"]

            # 성공 확률 계산 - 확률이 100%를 초과하지 않도록 보정
            # 예: (운 * 조정 값) / (운 * 조정 값 + 일정 보정값)
            max_luck_effect = 100  # 최대 보정값을 설정하여 확률의 상한을 제한
            success_chance = (player_luck * luck_factor) / (player_luck * luck_factor + max_luck_effect) * 100
            print("보정된 성공 확률:", success_chance)

            # 성공 여부 결정
            if random.uniform(0, 100) <= success_chance:
                return parts[0]  # 성공 시 앞쪽 텍스트 반환
            else:
                return parts[2]  # 실패 시 뒤쪽 텍스트 반환
        return choice_text  # *숫자*가 없으면 그대로 반환
    # 텍스트 영역을 클릭하면 다음 텍스트 출력 시작
    def on_click_next_text(self, *args):
        print("is_waiting_for_click : ", self.is_waiting_for_click)
        if self.is_waiting_for_click:
            self.is_waiting_for_click = False  # 클릭을 기다리는 상태를 해제
            self.text_area.text = ""  # 텍스트 영역 초기화
            if self.image_rect.source != "":
                self.image_rect.source = ""
                self.image_overlay.opacity = 0  # 이미지 레이아웃을 숨김
            self.current_line += 1
            self.start_automatic_text()

    # 선택지 버튼을 눌렀을 때의 동작 정의
    def on_choice(self, instance):
        stat_text = ""
        if self.on_choice_able and instance.text != "":
            # 선택된 버튼에 맞는 인덱스를 찾고 해당 조정값을 가져옴
            self.select_text = instance.text
            if instance == self.choice1:
                adjustments = self.adjustments[0]  # (stat_name, stat_value, operation) 각 형태를 가진 배열
                self.choice = 0
                has_underscore = self.choice1.has_underscore  # `_` 여부 저장
            elif instance == self.choice2:
                adjustments = self.adjustments[1]
                self.choice = 1
                has_underscore = self.choice2.has_underscore
            elif instance == self.choice3:
                adjustments = self.adjustments[2]
                self.choice = 2
                has_underscore = self.choice3.has_underscore
            elif instance == self.choice4:
                adjustments = self.adjustments[3]
                self.choice = 3
                has_underscore = self.choice4.has_underscore
            else:
                adjustments = []  # 빈 리스트로 초기화
                has_underscore = False  # 기본값 False

            # None일 경우 빈 리스트로 처리
            if adjustments is None:
                adjustments = []
            # 여러 능력치 조정 처리
            for adjustment in adjustments:
                if adjustment:
                    stat_name, stat_value, operation = adjustment
                    if stat_name in self.ability_stat:  # stat 딕셔너리에서 해당 능력치 확인
                        if operation == "+":
                            self.ability_stat[stat_name] += stat_value
                            if stat_name in ["돈", "집중도", "멘탈"] and self.ability_stat[stat_name] > 3:
                                # ["돈", "집중도", "멘탈"] 스탯이 최대 스탯인 3을 넘을 경우
                                self.ability_stat[stat_name] = 3  # 더해져도 최대치 3으로 설정
                            elif stat_name in list(self.ability_stat.keys())[0:12]:  # 능력치 부분은 능력치 조정 수치가 텍스트에 보임
                                stat_text += "[color=808080]|[/color] "
                                stat_text += f"[color=A5FFC9]{stat_name} {operation}{stat_value}[/color]  "
                        elif operation == "-" and self.ability_stat[stat_name] >= 1:
                            self.ability_stat[stat_name] -= stat_value
                            if stat_name in list(self.ability_stat.keys())[0:12]:
                                stat_text += "[color=808080]|[/color] "
                                stat_text += f"[color=FFA5A5]{stat_name} {operation}{stat_value}[/color]  "
                        print(f"{stat_name} 능력치가 {operation}{stat_value}만큼 조정되었습니다.")
                    else:
                        self.ability_stat[stat_name] = stat_value #주어진 능력치를 추가

            # 선택지 버튼 텍스트 초기화 (선택 후)
            self.clear_choices()
            if self.ability_stat['멘탈'] == 0 or self.ability_stat['집중도'] == 0:
                self.load_ending_branch()


            # 선택한 내용을 출력 후 이어서 출력
            self.text_area.text = ""
            self.text_area.text += f"[color=808080]{self.select_text}[/color] {stat_text}\n"

            # 선택 후 처리
            if has_underscore:
                # 선택한 텍스트가 `_`로 끝난 경우
                print("강제종료 시점", self.file_name, self.current_line)
                if self.file_name == os.path.join(STORY_DIR, 'reaction', 'reaction_a.txt') and self.current_line == 303:
                    self.current_line = 69
                else :
                    self.current_line = self.saved_position + 1  # 저장된 위치로 돌아감
                self.story_lines = self.read_story_text(os.path.join(STORY_DIR, 'main_story.txt')).splitlines()  # 메인 스토리 호출
                self.on_choice_able = False
                self.reaction_part = False
                self.event = False  # 이벤트 스토리 판정 false
                self.start_automatic_text()
                self.update_stat_images()
            else:
                self.current_line += 1
                self.on_choice_able = False
                self.start_automatic_text()
                self.update_stat_images()
            print(self.ability_stat)
            if self.image_rect.source != "":
                self.image_rect.source = ""
                self.image_overlay.opacity = 0  # 이미지 레이아웃을 숨김

    def clear_choices(self):
        self.choice1.text = ""
        self.choice2.text = ""
        self.choice3.text = ""
        self.choice4.text = ""

    def load_alternate_story(self, saved_position, line):
        if line == "# lecture":
            # 1~3 사이의 랜덤 정수를 생성하여 파일 이름 결정
            lecture_num = random.randint(1, 3)
            lecture_file_name = os.path.join(STORY_DIR, 'reaction', 'lecture.txt')

            print(f"강의 파트 파일 로드: {lecture_file_name}")

            # 강의 파트 파일 읽어들이기
            self.save_file_name = self.file_name  # 리액션 텍스트에 돌입하기 전 기존 텍스트 파일의 이름을 저장
            self.story_lines = self.read_story_text(lecture_file_name).splitlines()
            self.current_line = 0  # 강의 파트의 첫 번째 줄부터 시작
            self.saved_re_position = saved_position
            self.reaction_part = True  # 리액션 파일 진입 확인 변수
            self.flag = False  # 리액션 파일에 내가 원하는 부분이 나오기 전까지 자동 텍스트 출력 패스
            Clock.schedule_once(self.start_automatic_text, 0.5)
        elif line == "# group_task":
            if self.group_count >= 4: #5번째 부터는 조원 찾기 이벤트를 스킵한다.
                group_task_file_name = os.path.join(STORY_DIR, 'group_task', 'group_task_e.txt')
            else:
                group_task_file_name = os.path.join(STORY_DIR, 'group_task', f"group_task_{chr(ord('a')+self.group_count)}.txt")
            #group_task는 실행 될 때 마다 다음 파일을 읽음
            print(f"강의 파트 파일 로드: {group_task_file_name}")
            self.group_count += 1
            # 강의 파트 파일 읽어들이기
            self.save_file_name = self.file_name  # 리액션 텍스트에 돌입하기 전 기존 텍스트 파일의 이름을 저장
            self.story_lines = self.read_story_text(group_task_file_name).splitlines()
            self.current_line = 0  # 강의 파트의 첫 번째 줄부터 시작
            self.saved_position = saved_position
            self.event = True  # 이벤트와 유사한 별도의 강의 파트 => 종료 시 메인 파트로 돌아가고 리액션 기능을 사용가능함.
            Clock.schedule_once(self.start_automatic_text, 0.5)
        elif line == "#":
            # 랜덤 이벤트용 파일을 불러오기
            self.event = True
            file_name = self.sub_event_story()
            self.story_lines = self.read_story_text(file_name).splitlines()
            if file_name == os.path.join(STORY_DIR, 'event_story', 'i.txt') and self.ability_stat["저녁약속"] == 1 and self.ability_stat["dinner"] == 1:#저녁 약속이 존재하고 지금이 저녁인 경우
                self.current_line = 15
            elif file_name == os.path.join(STORY_DIR, 'event_story', 'j-1.txt'):
                self.current_line = 60 * self.ability_stat["running"]
            elif file_name == os.path.join(STORY_DIR, 'event_story', 'j-2.txt'):
                self.current_line = 60 * self.ability_stat["service"]
            else:
                self.current_line = 0
            self.saved_position = saved_position
            Clock.schedule_once(self.start_automatic_text, 0.5)
        elif line.startswith("#이동:"):
            # 대전2046: 특정 동에 진입할 때 그 동 전용 랜덤 이벤트 폴더에서 하나 골라 재생
            dong = line[len("#이동:"):].strip()
            file_name = self.sub_travel_event_story(dong)
            if file_name is None:
                # 그 동에 등록된 이벤트가 아직 없으면 그냥 건너뛰고 원래 위치로
                self.current_line = saved_position
                Clock.schedule_once(self.start_automatic_text, 0.5)
                return
            self.event = True
            self.story_lines = self.read_story_text(file_name).splitlines()
            self.current_line = 0
            self.saved_position = saved_position
            Clock.schedule_once(self.start_automatic_text, 0.5)
        else:
            self.save_file_name = self.file_name  # 리액션 텍스트에 돌입하기 전 기존 텍스트 파일의 이름을 저장
            print("저장된 파일 이름", self.save_file_name)
            self.story_lines = self.read_story_text(self.reaction_text()).splitlines()
            self.current_line = 0  # 새로운 파일의 첫 번째 줄부터 시작
            # 스토리가 끝났을 때 이전 파일로 돌아감
            self.saved_re_position = saved_position
            self.reaction_part = True  # 리액션 파일 진입 확인 변수
            # ✅ 인덱스 생성
            self.reaction_index = self.build_reaction_index(self.story_lines)
            self.reaction_index_file = reaction_path
        
            # ✅ 이제 flag 탐색이 아니라, 바로 점프할 거라서 flag 필요 없음(일단은 유지해도 됨)
            self.flag = True  # 혹은 아예 안 쓰게 만들 예정
            Clock.schedule_once(self.start_automatic_text, 0.5)

    def build_reaction_index(self, lines):
        index = {}
        for i, raw in enumerate(lines):
            s = raw.strip()
            if s.startswith("#"):
                # 같은 태그가 여러 번 나오면 첫 번째만 쓰거나, 마지막으로 덮어쓰거나 정책 선택
                # 여기서는 "첫 번째만" 채택
                index.setdefault(s, i)
        return index

    def sub_event_story(self):
        sub_event_list = ["a.txt", "b.txt", "c.txt", "d.txt", "e.txt", "f.txt", "g.txt", "h.txt", "i.txt", "j.txt"]
        if self.ability_stat["동아리"] < 0 : #동아리 이벤트 진입 후 동아리에 들어가는 것을 거부했을 때. 동아리 이벤트를 삭제함
            sub_event_list = ["a.txt", "b.txt", "c.txt", "d.txt", "e.txt", "f.txt", "g.txt", "h.txt", "i.txt"]
        num = random.randint(0, len(sub_event_list)-1)
        print("진입확인", num)
        if self.ability_stat["dinner"] == 1 and self.ability_stat["저녁약속"] == 1:
            #현재 저녁약속이 존재하고 실제로 저녁 시간대일 때
            return os.path.join(STORY_DIR, 'event_story', 'i.txt')
        elif num == 9 and self.ability_stat["동아리"] > 0: #동아리 이벤트에 진입하고 난 뒤, 동아리 참가했을 때 내가 참가한 동아리 이벤트를 들어감
            #동아리가 1인것은 홍보부스 - 하트비트 동아리 이벤트 2인 경우 체험부스 - 봉사활동 동아리 이벤트로 넘어감
            return os.path.join(STORY_DIR, 'event_story', f'j-{self.ability_stat["동아리"]}.txt')
        else:
            return os.path.join(STORY_DIR, 'event_story', f"{sub_event_list[num]}")

    #--- 대전2046: 동(洞)별 이동 중 랜덤 이벤트 ---#
    def sub_travel_event_story(self, dong):
        dong_dir = os.path.join(STORY_DIR, 'travel_event', dong)
        try:
            files = sorted(f for f in os.listdir(dong_dir) if f.endswith('.txt'))
        except FileNotFoundError:
            files = []
        if not files:
            print(f"'{dong}' 이동 이벤트 폴더가 없거나 비어 있음, 건너뜀")
            return None
        chosen = random.choice(files)
        print("이동 이벤트 진입", dong, chosen)
        return os.path.join(dong_dir, chosen)

    def reaction_text(self):
        # 선택된 버튼의 reaction_number를 기준으로 텍스트 파일을 선택
        reaction_number = -1
        if self.choice == 0:
            reaction_number = self.choice1.reaction_number
        elif self.choice == 1:
            reaction_number = self.choice2.reaction_number
        elif self.choice == 2:
            reaction_number = self.choice3.reaction_number
        elif self.choice == 3:
            reaction_number = self.choice4.reaction_number

        # reaction_number에 따라 리액션 텍스트 파일 선택
        if reaction_number == -1:
            # 기본 동작 (reaction_number가 없을 때 기존 로직 실행)
            print("리액션 진입", self.choice)
            reaction_list = ["reaction_a.txt", "reaction_b.txt", "reaction_c.txt", "reaction_d.txt",
                              "reaction_e.txt", "reaction_f.txt", "reaction_g.txt", "reaction_h.txt"]
            return os.path.join(STORY_DIR, 'reaction', reaction_list[self.choice])
        else:
            # reaction_number로 텍스트 파일 선택
            reaction_list = ["reaction_a.txt", "reaction_b.txt", "reaction_c.txt", "reaction_d.txt",
                              "reaction_e.txt", "reaction_f.txt", "reaction_g.txt", "reaction_h.txt"]
            print("내가 정한 특수 리액션 진입", reaction_list[reaction_number])
            if 0 <= reaction_number < len(reaction_list):
                return os.path.join(STORY_DIR, 'reaction', reaction_list[reaction_number])
            else:
                print("경고: 유효하지 않은 reaction_number", reaction_number)
                return os.path.join(STORY_DIR, 'reaction', 'reaction_default.txt')

    def load_ending_branch(self):
        print("엔딩 이벤트 실행")
        self.story_lines = self.read_story_text(self.ending_branch_story()).splitlines()
        self.current_line = 0  # 새로운 파일의 첫 번째 줄부터 시작
        self.end = True
        Clock.schedule_once(self.start_automatic_text, 0.5)

    def ending_branch_story(self):
        if self.ability_stat['멘탈'] == 0:
            return os.path.join(STORY_DIR, 'ending_part', 'game_over_m.txt')
        elif self.ability_stat['집중도'] == 0:
            return os.path.join(STORY_DIR, 'ending_part', 'game_over_c.txt')
        elif self.ability_stat["성적"] > 90:
            return os.path.join(STORY_DIR, 'ending_part', 'hidden_end.txt')
        elif self.ability_stat["성적"] > 80:
            return os.path.join(STORY_DIR, 'ending_part', 'good_end.txt')
        elif self.ability_stat["성적"] > 70:
            return os.path.join(STORY_DIR, 'ending_part', 'normal_end.txt')
        else:
            return os.path.join(STORY_DIR, 'ending_part', 'bad_end.txt')

    def end_game(self):
        self.privious_name = "mainmenu"
        app = App.get_running_app()
        if self.ability_stat['멘탈'] == 0:
            app.game_ending('MENTAL_ZERO')
        elif self.ability_stat['집중도'] == 0:
            app.game_ending('CONCENTRATION_ZERO')
        elif self.ability_stat["성적"] > 90:
            app.game_ending('HIDDEN')
        elif self.ability_stat["성적"] > 80:
            app.game_ending('GOOD')
        elif self.ability_stat["성적"] > 70:
            app.game_ending('NORMAL')
        else:
            app.game_ending('BAD')
