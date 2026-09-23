## 대전 2046 — 진입점
## config.name / gui.about 등 프로젝트 설정은 options.rpy에서 관리

## NVL 모드 화면에도 스탯 표시가 겹쳐 보이도록 오버레이로 등록
init python:
    config.overlay_screens.append("stat_hud")

label start:
    jump start_story
