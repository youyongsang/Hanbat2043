## 대전 2046 — 스탯/변수/헬퍼 정의
## 대전2046 스토리에서 실제 쓰는 스탯만 포팅함 (한밭2043의 동아리/조별과제/성적 등은 대상 아님)

## 렌파이 기본 폰트는 한글이 없어서(□□□로 깨짐) 한글 폰트로 교체.
## 세로 1080x1920 기준이라 기본 텍스트 크기도 휴대폰 화면에 맞게 키움.
style default:
    font "fonts/NanumGothic.ttf"
    size 44

## plain menu:는 기본적으로 ADV 모드(빈 화면에 선택지만 표시)로 뜬다 —
## 이 게임은 전부 NVL(텍스트 누적) 방식이므로, menu 자체를 nvl_menu로 재정의해서
## 모든 선택지가 위 텍스트 로그에 이어서 표시되도록 함.
define menu = nvl_menu

## 선택지 버튼 글씨가 gui.rpy 쪽 계산값 때문에 대사보다 작게 나와서,
## 대사와 같은 크기(44)로 직접 맞춤.
style nvl_dialogue:
    size 44

style nvl_button_text:
    size 44

default 기술태도 = 0
default 생명력 = 10
default 공학 = 0
default 체력 = 0
default 손재주 = 0
default 돈 = 0
default 운 = 1
default 강민재신뢰 = 0
default 서지원신뢰 = 0
default 신중한재건 = 0
default 설비반파 = 0

## "이 질문을 이미 물어봤는가" 같은 반복 메뉴용 범용 플래그 저장소.
## 이름 붙은 변수(statA/B/C/D)를 매번 새로 만들지 않고, 어느 반복 메뉴에서든 재사용 가능.
default flags = {}

## 서울 2033 식 — 이름표 없이 전부 지문/대사가 그냥 텍스트로 흐르는 방식.
## 인물 이름은 따옴표 대사와 지문으로만 드러남 (Character 이름 라벨 사용 안 함).
define n = Character(None, kind=nvl)
define player = Character(None, kind=nvl, what_color="#8a8a8a")

init python:
    def flag_set(name):
        flags[name] = True

    def flag_is(name):
        return flags.get(name, False)

    def adjust_stat(name, delta):
        """원본 엔진의 감소 가드를 그대로 포팅: 현재값이 1 이상일 때만 감소 적용.
        (delta 크기와 무관 — 원본 동작 그대로 보존, 현재값 1에서 5 빼도 -4가 됨)"""
        cur = getattr(store, name)
        if delta < 0 and cur < 1:
            return
        setattr(store, name, cur + delta)

    def luck_check(factor):
        """원본 parse_luck_adjustment 공식 그대로: (운*factor)/(운*factor+100)*100을 성공 확률로 사용.
        원본은 메뉴가 뜨는 시점에 미리 굴렸지만, 이 포팅에서는 선택한 시점에 굴림(의도적 변경)."""
        chance = (운 * factor) / (운 * factor + 100) * 100
        return renpy.random.uniform(0, 100) <= chance

screen stat_hud():
    ## NVL 창(전체화면 배경)보다 위에 그려지도록 zorder를 높게 고정
    zorder 100
    vbox:
        xalign 1.0
        yalign 0.0
        xoffset -12
        yoffset 8
        text "생명력 [생명력] | 돈 [돈] | 기술태도 [기술태도]" size 28 color "#cccccc"
