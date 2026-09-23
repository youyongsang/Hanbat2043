## 대전 2046 — 본편 (원본: story/main_story.txt)
## Stage 1: 오프닝 ~ 박순임 4지선다 메뉴 ~ 완충지대 진입(오정동 이동 이벤트 연결)까지

label main_story:
    n "해가 뉘엿뉘엿 넘어갈 무렵, 배낭을 메고 마을 어귀로 들어섭니다."
    nvl clear
    n "오늘은 좀 늦었네."
    n "마을 입구 평상에 앉아 있던 박순임이 먼저 알은체를 합니다.\n촌장이라기엔 수더분한 옷차림, 그래도 눈빛만은 늘 살피는 눈빛입니다."
    n "경계 쪽 요즘 뒤숭숭하다던데. 별일 없었고?"
    menu:
        "네, 별일 없었어요.":
            pass
        "상자 하나 주웠어요.":
            pass
    nvl clear
    n "그래, 다행이다. 얼른 들어가서 밥부터 먹어. 국 식겠다."
    n "짧은 인사지만, 오늘 하루 무사히 돌아왔다는 사실이\n그 말 한마디로 새삼 실감 납니다."
    nvl clear
    n "마을로 돌아온 당신은 밤이 깊어서야 노트와 장치를 다시 꺼내봅니다.\n장치는 여전히 반응이 없습니다.\n전원이 문제가 아니라, 애초에 뭔가로 잠겨 있는 것 같습니다.\n노트 안쪽 몇 장은 습기에 절어 알아볼 수 없지만,\n그나마 멀쩡한 페이지 한 귀퉁이에 낯선 기호와 숫자가 빼곡히 적혀 있습니다.\n암호 같기도 하고, 통신 기록 같기도 합니다.\n당신 혼자 힘으로는 이게 뭔지 알 도리가 없습니다."
    menu:
        "일단 자자.":
            pass
    nvl clear
    n "다음날, 당신은 배급소에 도착했습니다.\n배급소 보급 담당인 장씨 아저씨가 사람들에게 이것 저것 나눠주고 있습니다.\n장씨 아저씨가 한가할 때 당신은 그에게 가서 말을 걸었습니다."
    menu:
        "아저씨 뭐 좀 물어볼 수 있을까요?":
            pass
    nvl clear
    n "응? 뭐야 너 아직 배급 날짜가 아니잖아. 무슨 일이지?"
    n "수상한 눈빛으로 당신을 바라봅니다.\n당신은 다급하게 목적을 말합니다.\n폐허에서 무엇을 찾았는지, 그게 뭔지 알 수 있는지 물어봅니다."
    n "이런 거라면 오세연한테 가져가봐. 그 여자, 이상한 거 해독하는 데는 도가 텄어.\n대신 공짜는 아닐 거다. 뭐든 대가를 요구하는 사람이니까."
    nvl clear
    n "오세연.\n완충지대 어딘가를 떠돌며 정보와 물자를 거래한다는 소문의 그 사람.\n직접 만나본 적은 없지만, 이름은 몇 번 들어봤습니다."
    n "그럼 이제 가라. 바쁘다."
    n "장씨 아저씨는 손을 휙휙 저으면서 당신을 보냅니다."
    nvl clear
    jump main_story_park_sunim_intro

label main_story_park_sunim_intro:
    n "그날 저녁, 박순임이 조용히 당신을 불러 세웁니다."
    n "오세연 만나러 간다는 얘기, 벌써 들었다. 요 동네가 좁아서."
    n "박순임은 손으로 대충 그린 낡은 종이 지도 한 장을 펼쳐 보입니다."
    n "떠나기 전에, 물어보고 싶은 거 있으면 물어봐."
    nvl clear
    jump ask_park_sunim

label ask_park_sunim:
    menu:
        "완충지대는 어떤 곳이에요?" if not flag_is("asked_buffer_zone"):
            $ flag_set("asked_buffer_zone")
            jump park_answer_buffer_zone
        "완충지대는 어떤 곳이에요?" if flag_is("asked_buffer_zone"):
            jump park_answer_buffer_zone_repeat
        "오염구역은 어떤 곳이에요?" if not flag_is("asked_pollution_zone"):
            $ flag_set("asked_pollution_zone")
            jump park_answer_pollution_zone
        "오염구역은 어떤 곳이에요?" if flag_is("asked_pollution_zone"):
            jump park_answer_pollution_zone_repeat
        "진앙지는 어떤 곳이에요?" if not flag_is("asked_epicenter"):
            $ flag_set("asked_epicenter")
            jump park_answer_epicenter
        "진앙지는 어떤 곳이에요?" if flag_is("asked_epicenter"):
            jump park_answer_epicenter_repeat
        "더 이상 물어볼 게 없어요.":
            jump park_menu_done

label park_answer_buffer_zone:
    player "완충지대는 어떤 곳이에요?"
    n "오정동부터 중리동, 대화동 쪽까지가 완충지대야. 사람이 살긴 하는데, 절반은 떠돌이 스캐빈저지.\n국가에서 나온 감시 인력도 가끔 돈다더라. 위험하긴 해도, 다닐 수는 있는 곳이야."
    n "박순임이 지도에서 눈을 떼고 당신을 바라봅니다."
    n "또 물어볼 거 있어?"
    nvl clear
    jump ask_park_sunim

label park_answer_buffer_zone_repeat:
    player "완충지대는 어떤 곳이에요?"
    n "완충지대는 아까 말했잖아. 오정동부터 중리동, 대화동 쪽까지라고.\n몇 번을 물어봐, 그거."
    nvl clear
    jump ask_park_sunim

label park_answer_pollution_zone:
    player "오염구역은 어떤 곳이에요?"
    n "그 위는 오염구역, 유성구 쪽이야. 사람이 살 수 없는 곳이지. 건물은 멀쩡한데 사람만 없어.\n방사능 때문이야. 오래 있으면 몸이 축나. 절대 혼자 들어갈 생각 하지 마라."
    n "박순임이 지도에서 눈을 떼고 당신을 바라봅니다."
    n "또 물어볼 거 있어?"
    nvl clear
    jump ask_park_sunim

label park_answer_pollution_zone_repeat:
    player "오염구역은 어떤 곳이에요?"
    n "오염구역도 아까 말했잖아. 유성구 쪽, 사람 못 사는 데라고.\n같은 얘기 자꾸 물어보면 나만 피곤해."
    nvl clear
    jump ask_park_sunim

label park_answer_epicenter:
    player "진앙지는 어떤 곳이에요?"
    n "그보다 더 안쪽은 진앙지. 그 사건이 진짜로 터진 자리야.\n거긴 나도 자세힌 몰라. 알고 싶지도 않고."
    n "박순임이 지도에서 눈을 떼고 당신을 바라봅니다."
    n "또 물어볼 거 있어?"
    nvl clear
    jump ask_park_sunim

label park_answer_epicenter_repeat:
    player "진앙지는 어떤 곳이에요?"
    n "진앙지 얘기도 했잖아. 나도 자세힌 모른다고 했고.\n왜 자꾸 물어, 뭐 걸리는 거라도 있어?"
    nvl clear
    jump ask_park_sunim

label park_menu_done:
    player "더 이상 물어볼 게 없어요."
    n "완충지대까지는 그럭저럭 다녀도 돼. 근데 그 이상은 절대 혼자 넘어가지 말아라.\n…아무튼, 그 이상은 생각하지 마. 조심해서 다녀와."
    n "그녀는 더 말을 잇지 않고 자리를 뜹니다."
    nvl clear
    jump after_park_menu

label after_park_menu:
    n "완충지대 너머는 만만한 곳이 아닙니다.\n당장 떠나기보다, 먼저 신탄진 인근 안전지대부터 돌아보기로 합니다."
    nvl clear
    n "덕암동 쪽에는 물자를 조금씩 거래하는 노인이 있다고 들었습니다.\n목상동 쪽엔 예전에 완충지대를 드나들었다는 사람이 산다고도 하고요."
    menu:
        "덕암동으로 향한다.":
            pass
        "목상동으로 향한다.":
            pass
    nvl clear
    n "아직 신탄진 생존구역 안쪽이라 그런지, 길 자체는 낯익습니다.\n무너진 건물도 드문드문 있지만, 사람이 다니는 흔적이 훨씬 또렷합니다."
    nvl clear
    n "한참을 돌아본 끝에, 마스크 하나와 낡은 지도 한 장을 구했습니다.\n지도 귀퉁이에 완충지대의 대략적인 길목이 손글씨로 표시돼 있습니다."
    n "오정동 지나서 대화동 쪽으로, 거기서부터는 알아서 조심해."
    nvl clear
    n "준비는 이 정도면 충분할 것 같습니다.\n더 미루다간 오히려 마음만 무거워질 뿐이겠죠."
    nvl clear
    n "당신은 노트와 장치를 챙겨 다시 배낭을 꾸립니다.\n이제 진짜, 완충지대 너머로 떠날 차례입니다."
    nvl clear
    n "신탄진을 벗어나 남쪽으로, 완충지대가 시작됩니다.\n오정동과 대화동을 지나는 길, 버려진 건물들 사이로 검문소였던 흔적이 남아 있습니다.\n사람은 없지만, 누군가 최근까지 머문 흔적들이 곳곳에 보입니다."
    nvl clear
    call call_travel_event("오정동")

    ## Stage 2에서 계속: 노을 조우 ~ 마지막폭파까지
    n "(Stage 1 끝 — 다음 내용은 Stage 2에서 이어집니다.)"
    return
