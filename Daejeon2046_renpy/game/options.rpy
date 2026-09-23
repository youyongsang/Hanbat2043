## 대전 2046 — 프로젝트 설정 (렌파이 기본 템플릿의 options.rpy를 기반으로 수정)
## 해상도(1080x1920, 세로)와 한글 폰트는 gui.rpy에서 gui.init()으로 설정함.

define config.name = _("대전 2046")
define gui.show_name = True
define config.version = "0.1"
define gui.about = _p("""
포스트 아포칼립스 대전을 배경으로 한 텍스트 어드벤처. Ren'Py 포팅 Stage 1.
""")
define build.name = "daejeon2046"

define config.has_sound = True
define config.has_music = True
define config.has_voice = True

define config.enter_transition = dissolve
define config.exit_transition = dissolve
define config.intra_transition = dissolve
define config.after_load_transition = None
define config.end_game_transition = None

define config.window = "auto"
define config.window_show_transition = Dissolve(.2)
define config.window_hide_transition = Dissolve(.2)

default preferences.text_cps = 0
default preferences.afm_time = 15

define config.save_directory = "Daejeon2046-renpy"

define config.window_icon = "gui/window_icon.png"

init python:
    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)
    build.documentation('*.html')
    build.documentation('*.txt')
