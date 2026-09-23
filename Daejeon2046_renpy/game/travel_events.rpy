## 대전 2046 — 동(洞)별 이동 중 랜덤 이벤트
## 원본: story/travel_event/{동}/*.txt — 옛 엔진의 sub_travel_event_story(dong)를 대체

define travel_events = {
    "오정동": ["travel_ojeong_a"],
}

label call_travel_event(dong):
    if dong not in travel_events or not travel_events[dong]:
        return
    $ chosen = renpy.random.choice(travel_events[dong])
    call expression chosen
    return

## --- 오정동 ---

label travel_ojeong_a:
    n "길가에 반쯤 넘어간 채 방치된 승용차 한 대가 눈에 들어옵니다.\n타이어는 다 삭아 내려앉았고, 유리창엔 뽀얗게 먼지가 앉아 있습니다.\n운전석 쪽 문이 살짝 열려 있습니다."
    nvl clear
    menu:
        "안을 살펴본다.":
            n "당신은 조심스레 차 안으로 손을 뻗습니다.\n조수석엔 색이 바랜 아이 옷 몇 벌과 작은 인형이 놓여 있습니다.\n서둘러 떠나느라 미처 챙기지 못한 짐인 듯합니다.\n트렁크를 열어보니, 다행히 녹슬지 않은 공구함 하나가 눈에 띕니다."
            $ adjust_stat("손재주", 1)
            n "쓸만한 공구 몇 개를 챙겨 넣습니다.\n인형은 잠시 손에 쥐었다가, 다시 조수석에 가만히 내려놓습니다.\n누구의 것이었을지, 지금은 알 도리가 없습니다."
            nvl clear
        "그냥 지나친다.":
            pass
    n "당신은 차에서 물러나 다시 걷기 시작합니다."
    return
