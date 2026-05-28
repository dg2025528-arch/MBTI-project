
import streamlit as st
import streamlit.components.v1 as components
import random

# 페이지 설정
st.set_page_config(
    page_title="포켓몬 MBTI 도감 🎮",
    page_icon="⚡",
    layout="wide"
)

# 포켓몬 게임 스타일 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Jua&display=swap');
    
    html, body, [class*="css"] { font-family: 'Jua', sans-serif; }
    
    .stApp {
        background: linear-gradient(180deg, #87CEEB 0%, #98D8E8 50%, #B0E0E6 100%);
        background-attachment: fixed;
    }
    
    .pokemon-title {
        text-align: center;
        font-family: 'Press Start 2P', cursive;
        font-size: 2.5em;
        color: #FFCB05;
        text-shadow: 4px 4px 0 #3B4CCA, -2px -2px 0 #3B4CCA, 2px -2px 0 #3B4CCA,
            -2px 2px 0 #3B4CCA, 2px 2px 0 #3B4CCA, 6px 6px 0 #000;
        letter-spacing: 3px;
        margin: 20px 0;
        animation: titleBounce 2s ease-in-out infinite;
    }
    
    @keyframes titleBounce {
        0%, 100% { transform: translateY(0) rotate(-1deg); }
        50% { transform: translateY(-8px) rotate(1deg); }
    }
    
    .sub-text {
        text-align: center;
        font-size: 1.3em;
        color: #2a2a2a;
        background: rgba(255,255,255,0.8);
        padding: 10px 20px;
        border-radius: 30px;
        display: inline-block;
        border: 3px solid #FFCB05;
    }
    
    .pokemon-box {
        background: white;
        border: 4px solid #2a2a2a;
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: inset 0 0 0 3px white, inset 0 0 0 6px #3B4CCA, 6px 6px 0 #2a2a2a;
        position: relative;
    }
    
    .pokemon-box::before {
        content: '▼';
        position: absolute;
        bottom: 10px;
        right: 20px;
        color: #3B4CCA;
        animation: arrowBlink 0.8s infinite;
    }
    
    @keyframes arrowBlink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0; }
    }
    
    .stButton>button {
        background: linear-gradient(180deg, #FFFFFF 0%, #E8E8E8 100%);
        color: #2a2a2a;
        border: 4px solid #2a2a2a;
        border-radius: 15px;
        padding: 15px 30px;
        font-size: 1.2em;
        font-weight: bold;
        font-family: 'Jua', sans-serif;
        box-shadow: inset 0 0 0 2px white, 4px 4px 0 #2a2a2a;
        transition: all 0.1s ease;
    }
    
    .stButton>button:hover {
        background: linear-gradient(180deg, #FFCB05 0%, #FFA500 100%);
        transform: translate(2px, 2px);
        box-shadow: inset 0 0 0 2px white, 2px 2px 0 #2a2a2a;
    }
    
    .progress-box {
        background: white;
        border: 4px solid #2a2a2a;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        font-weight: bold;
        font-size: 1.1em;
        box-shadow: 4px 4px 0 #2a2a2a;
        margin: 10px 0;
    }
    
    .hp-bar-container {
        background: #2a2a2a;
        border: 3px solid #2a2a2a;
        border-radius: 10px;
        padding: 3px;
        margin: 10px 0;
        height: 25px;
    }
    
    .hp-bar {
        height: 100%;
        background: linear-gradient(180deg, #6BCF7F 0%, #4CAF50 100%);
        border-radius: 7px;
        transition: width 0.5s ease;
    }
    
    .info-card {
        background: white;
        border: 4px solid #2a2a2a;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 6px 6px 0 #2a2a2a;
        margin: 15px 0;
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FF1F1F 0%, #CC0000 100%);
    }
    
    section[data-testid="stSidebar"] * { color: white !important; }
    </style>
""", unsafe_allow_html=True)

# MBTI별 포켓몬 데이터
mbti_pokemon = {
    "INTJ": {"name": "뮤츠", "id": 150, "type": "psychic", "type_kr": "에스퍼",
             "desc": "전략적이고 지적인 INTJ! 강력한 정신력의 뮤츠가 당신의 운명!",
             "traits": ["🧠 천재 지능", "🔮 초능력", "🎯 전략가", "🌌 독립적"]},
    "INTP": {"name": "알라카잠", "id": 65, "type": "psychic", "type_kr": "에스퍼",
             "desc": "호기심 많은 INTP! IQ 5000의 알라카잠이 최고의 짝꿍!",
             "traits": ["📚 무한 지식", "🥄 사이코키네시스", "💭 깊은 사고", "🔬 분석가"]},
    "ENTJ": {"name": "리자몽", "id": 6, "type": "fire", "type_kr": "불꽃",
             "desc": "타고난 리더 ENTJ! 카리스마 넘치는 리자몽이 당신의 파트너!",
             "traits": ["🔥 리더십", "👑 카리스마", "🏆 승부욕", "⚔️ 결단력"]},
    "ENTP": {"name": "삼삼드래", "id": 635, "type": "dragon", "type_kr": "드래곤",
             "desc": "창의적인 ENTP! 머리 세 개의 삼삼드래처럼 다재다능!",
             "traits": ["💡 창의력", "🗣️ 토론왕", "🌪️ 에너지", "🎭 임기응변"]},
    "INFJ": {"name": "가디안", "id": 282, "type": "fairy", "type_kr": "페어리",
             "desc": "공감 천재 INFJ! 헌신적인 가디안이 당신을 지켜줄 거예요!",
             "traits": ["💝 공감 능력", "🛡️ 헌신적", "✨ 직감", "🌙 통찰력"]},
    "INFP": {"name": "이브이", "id": 133, "type": "normal", "type_kr": "노말",
             "desc": "감수성 풍부한 INFP! 무한한 가능성의 이브이가 딱!",
             "traits": ["🌈 가능성", "💗 따뜻함", "🎨 감수성", "🦋 자유"]},
    "ENFJ": {"name": "해피너스", "id": 242, "type": "normal", "type_kr": "노말",
             "desc": "사랑이 넘치는 ENFJ! 치유의 해피너스가 당신과 함께!",
             "traits": ["💖 배려심", "🌟 긍정", "🤗 치유", "👼 천사"]},
    "ENFP": {"name": "피카츄", "id": 25, "type": "electric", "type_kr": "전기",
             "desc": "에너지 폭발 ENFP! 모두의 사랑 피카츄가 당신의 짝꿍!",
             "traits": ["⚡ 활발함", "😊 매력", "🎉 자유", "🌟 인기"]},
    "ISTJ": {"name": "거북왕", "id": 9, "type": "water", "type_kr": "물",
             "desc": "신뢰의 ISTJ! 든든한 거북왕처럼 책임감 100%!",
             "traits": ["🛡️ 신뢰", "📋 계획", "💪 책임감", "⚓ 안정감"]},
    "ISFJ": {"name": "이상해꽃", "id": 3, "type": "grass", "type_kr": "풀",
             "desc": "헌신적인 ISFJ! 포근한 이상해꽃이 안식처가 되어줄 거예요!",
             "traits": ["🌷 헌신", "🌿 안정", "💚 보호", "🏡 따뜻함"]},
    "ESTJ": {"name": "갸라도스", "id": 130, "type": "water", "type_kr": "물",
             "desc": "리더 ESTJ! 강력한 갸라도스의 압도적 존재감!",
             "traits": ["👑 리더십", "⚔️ 결단력", "🌊 존재감", "🎯 목표"]},
    "ESFJ": {"name": "푸린", "id": 39, "type": "fairy", "type_kr": "페어리",
             "desc": "사교왕 ESFJ! 분위기 메이커 푸린이 당신과 함께!",
             "traits": ["🎵 분위기", "💕 다정함", "🤝 사교성", "🎀 사랑스러움"]},
    "ISTP": {"name": "루카리오", "id": 448, "type": "fighting", "type_kr": "격투",
             "desc": "쿨한 ISTP! 파동의 용사 루카리오가 당신의 파트너!",
             "traits": ["🥋 실력", "🧘 집중력", "⚡ 직관", "🎯 효율"]},
    "ISFP": {"name": "샤미드", "id": 134, "type": "water", "type_kr": "물",
             "desc": "예술가 ISFP! 우아한 샤미드의 부드러운 매력!",
             "traits": ["🎨 예술성", "🌊 부드러움", "💙 평화", "🌸 섬세함"]},
    "ESTP": {"name": "팬텀", "id": 94, "type": "ghost", "type_kr": "고스트",
             "desc": "모험왕 ESTP! 짓궂은 팬텀과 함께 대담한 모험을!",
             "traits": ["😈 장난기", "🎭 대담함", "💨 행동력", "🔥 도전"]},
    "ESFP": {"name": "님피아", "id": 700, "type": "fairy", "type_kr": "페어리",
             "desc": "스타 ESFP! 매력만점 님피아처럼 어디서든 빛나요!",
             "traits": ["💖 매력", "🌸 사교성", "🎀 화려함", "⭐ 스타"]}
}

# 질문 풀
all_questions = {
    "EI": [
        {"q": "🎉 주말에 친구들과 파티 vs 집에서 혼자 쉬기?", "a": ["파티 가자!", "집순이~"]},
        {"q": "💬 처음 만난 사람과 대화할 때?", "a": ["먼저 말 걸어요!", "조용히 있어요"]},
        {"q": "🔋 에너지 충전 방법은?", "a": ["사람들과 어울리기", "혼자만의 시간"]},
        {"q": "📞 친구가 갑자기 전화하면?", "a": ["반갑게 받기!", "문자로 해줘..."]},
        {"q": "🎤 발표할 때 나는?", "a": ["신나게 즐긴다", "긴장되고 떨려"]},
        {"q": "🏖️ 휴가를 보낸다면?", "a": ["사람 많은 핫플", "조용한 자연"]},
    ],
    "SN": [
        {"q": "📚 공부할 때 더 끌리는 것은?", "a": ["실용적인 지식", "이론과 상상"]},
        {"q": "🎨 문제를 풀 때 나는?", "a": ["경험과 사실 기반", "직관과 영감"]},
        {"q": "🌟 평소 더 관심있는 것?", "a": ["현재의 현실", "미래의 가능성"]},
        {"q": "📖 책을 읽을 때 선호하는 장르?", "a": ["실용서/논픽션", "판타지/SF"]},
        {"q": "🗺️ 길을 찾을 때 나는?", "a": ["지도와 정확한 방향", "감과 직관"]},
        {"q": "💭 대화 주제로 좋아하는 것?", "a": ["구체적 사실/경험", "추상적 아이디어"]},
    ],
    "TF": [
        {"q": "🤔 친구가 고민 상담할 때?", "a": ["해결책 제시", "공감하고 위로"]},
        {"q": "⚖️ 결정할 때 중요한 것?", "a": ["논리와 객관성", "감정과 가치관"]},
        {"q": "💭 영화를 볼 때 나는?", "a": ["스토리 분석", "감정에 몰입"]},
        {"q": "😢 친구가 울고 있다면?", "a": ["원인을 분석한다", "함께 슬퍼한다"]},
        {"q": "🎯 비판받을 때 나는?", "a": ["내용을 객관적으로 본다", "마음이 상한다"]},
        {"q": "👥 사람을 평가할 때?", "a": ["능력과 실력 위주", "성격과 마음 위주"]},
    ],
    "JP": [
        {"q": "📅 여행 갈 때 나는?", "a": ["꼼꼼한 계획표", "즉흥적으로!"]},
        {"q": "🗂️ 내 책상은?", "a": ["항상 정리정돈", "창의적 혼돈"]},
        {"q": "⏰ 약속 시간에 나는?", "a": ["미리 도착", "딱 맞춰 or 살짝 늦게"]},
        {"q": "📝 과제를 받으면?", "a": ["미리미리 끝낸다", "마감 직전에 폭주"]},
        {"q": "🛍️ 쇼핑할 때 나는?", "a": ["리스트 작성 후 구매", "끌리는 거 즉흥 구매"]},
        {"q": "🎮 게임할 때 나는?", "a": ["공략 보고 계획적", "그냥 부딪쳐본다"]},
    ]
}


def get_pokemon_celebration_html(pokemon_type, pokemon_id, pokemon_name, mbti):
    """포켓몬 등장 화려한 효과"""
    img_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon_id}.png"
    
    effects = {
        "fire": {"c1": "#ff4500", "c2": "#ffd700", "c3": "#ff6347", "emoji": "🔥"},
        "water": {"c1": "#1e90ff", "c2": "#00ced1", "c3": "#4169e1", "emoji": "💧"},
        "electric": {"c1": "#ffd700", "c2": "#ffff00", "c3": "#ffa500", "emoji": "⚡"},
        "grass": {"c1": "#32cd32", "c2": "#7fff00", "c3": "#00ff7f", "emoji": "🍃"},
        "psychic": {"c1": "#ff1493", "c2": "#da70d6", "c3": "#9370db", "emoji": "✨"},
        "fairy": {"c1": "#ff69b4", "c2": "#ffb6c1", "c3": "#ff1493", "emoji": "💖"},
        "dragon": {"c1": "#8a2be2", "c2": "#4b0082", "c3": "#9400d3", "emoji": "🌀"},
        "ghost": {"c1": "#483d8b", "c2": "#8b008b", "c3": "#4b0082", "emoji": "👻"},
        "fighting": {"c1": "#dc143c", "c2": "#ff4500", "c3": "#b22222", "emoji": "💥"},
        "normal": {"c1": "#ffd700", "c2": "#ffa500", "c3": "#ff8c00", "emoji": "⭐"}
    }
    
    eff = effects.get(pokemon_type, effects["normal"])
    
    confetti = ""
    for i in range(60):
        left = random.randint(0, 100)
        delay = random.uniform(0, 2)
        duration = random.uniform(3, 6)
        color = random.choice([eff['c1'], eff['c2'], eff['c3'], '#ffd700', '#ffffff'])
        size = random.randint(8, 16)
        confetti += f'<div class="confetti" style="left:{left}%; background:{color}; width:{size}px; height:{size}px; animation-delay:{delay}s; animation-duration:{duration}s;"></div>'
    
    particles = ""
    for i in range(40):
        left = random.randint(0, 100)
        delay = random.uniform(0, 3)
        duration = random.uniform(4, 8)
        size = random.randint(25, 55)
        particles += f'<div class="emoji-particle" style="left:{left}%; animation-delay:{delay}s; animation-duration:{duration}s; font-size:{size}px;">{eff["emoji"]}</div>'
    
    rays = ""
    for i in range(12):
        angle = i * 30
        rays += f'<div class="light-ray" style="transform: rotate({angle}deg);"></div>'
    
    html = f"""
    <!DOCTYPE html>
    <html><head>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ overflow: hidden; }}
        .stage {{
            position: relative; width: 100%; height: 650px;
            background: radial-gradient(ellipse at center, {eff['c1']} 0%, {eff['c3']} 40%, #000 100%);
            border: 8px solid #2a2a2a; border-radius: 20px; overflow: hidden;
            box-shadow: inset 0 0 0 4px white, inset 0 0 0 8px #FFCB05, 10px 10px 0 #2a2a2a;
        }}
        .light-ray {{
            position: absolute; top: 50%; left: 50%; width: 200%; height: 8px;
            background: linear-gradient(90deg, transparent, {eff['c2']}, transparent);
            transform-origin: left center; opacity: 0;
            animation: rayBurst 2s ease-out infinite;
        }}
        @keyframes rayBurst {{
            0% {{ opacity: 0; transform: rotate(var(--angle)) scaleX(0); }}
            20% {{ opacity: 1; }}
            100% {{ opacity: 0; transform: rotate(var(--angle)) scaleX(1.5); }}
        }}
        .explosion {{
            position: absolute; top: 50%; left: 50%; width: 100px; height: 100px;
            border-radius: 50%;
            background: radial-gradient(circle, {eff['c2']} 0%, transparent 70%);
            transform: translate(-50%, -50%);
            animation: explode 1.5s ease-out infinite;
        }}
        @keyframes explode {{
            0% {{ width: 50px; height: 50px; opacity: 1; }}
            100% {{ width: 1200px; height: 1200px; opacity: 0; }}
        }}
        .explosion:nth-child(2) {{ animation-delay: 0.5s; }}
        .explosion:nth-child(3) {{ animation-delay: 1s; }}
        .pokeball {{
            position: absolute; top: 50%; left: 50%;
            width: 120px; height: 120px; border-radius: 50%;
            background: linear-gradient(180deg, #FF1F1F 0%, #FF1F1F 50%, white 50%, white 100%);
            border: 6px solid #2a2a2a;
            transform: translate(-50%, -50%); z-index: 15;
            animation: pokeballAppear 1.5s ease-out forwards;
        }}
        .pokeball::before {{
            content: ''; position: absolute; top: 50%; left: -6px; right: -6px;
            height: 6px; background: #2a2a2a; transform: translateY(-50%);
        }}
        .pokeball::after {{
            content: ''; position: absolute; top: 50%; left: 50%;
            width: 35px; height: 35px; background: white;
            border: 6px solid #2a2a2a; border-radius: 50%;
            transform: translate(-50%, -50%);
        }}
        @keyframes pokeballAppear {{
            0% {{ transform: translate(-50%, -200%) rotate(0deg); opacity: 0; }}
            30% {{ transform: translate(-50%, -50%) rotate(360deg); opacity: 1; }}
            80% {{ transform: translate(-50%, -50%) rotate(360deg) scale(1.3); opacity: 1; }}
            100% {{ transform: translate(-50%, -50%) rotate(360deg) scale(3); opacity: 0; }}
        }}
        .pokemon-img {{
            position: absolute; top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            width: 400px; height: 400px; object-fit: contain;
            z-index: 20; opacity: 0;
            filter: drop-shadow(0 0 40px {eff['c2']}) drop-shadow(0 0 80px {eff['c1']});
            animation: pokemonEntry 1s ease-out 1.2s forwards, pokemonDance 2s ease-in-out 2.2s infinite;
        }}
        @keyframes pokemonEntry {{
            0% {{ transform: translate(-50%, -50%) scale(0) rotate(-360deg); opacity: 0; filter: blur(20px); }}
            60% {{ transform: translate(-50%, -50%) scale(1.4) rotate(20deg); opacity: 1; }}
            100% {{ transform: translate(-50%, -50%) scale(1) rotate(0deg); opacity: 1; }}
        }}
        @keyframes pokemonDance {{
            0%, 100% {{ transform: translate(-50%, -50%) translateY(0) rotate(-3deg); }}
            50% {{ transform: translate(-50%, -50%) translateY(-15px) rotate(3deg); }}
        }}
        .confetti {{
            position: absolute; top: -20px; opacity: 0;
            animation: confettiFall linear infinite; border-radius: 2px;
        }}
        @keyframes confettiFall {{
            0% {{ top: -20px; opacity: 1; transform: rotate(0deg); }}
            100% {{ top: 110%; opacity: 0; transform: rotate(720deg) translateX(100px); }}
        }}
        .emoji-particle {{
            position: absolute; bottom: -50px; opacity: 0;
            animation: particleFloat linear infinite; z-index: 18;
        }}
        @keyframes particleFloat {{
            0% {{ bottom: -50px; opacity: 0; transform: scale(0); }}
            10% {{ opacity: 1; }}
            50% {{ transform: scale(1.3) rotate(180deg); }}
            100% {{ bottom: 110%; opacity: 0; transform: scale(0.5) rotate(720deg); }}
        }}
        .mbti-badge {{
            position: absolute; top: 30px; right: 30px;
            background: linear-gradient(180deg, #FFCB05 0%, #FFA500 100%);
            color: #2a2a2a; padding: 15px 30px; border-radius: 15px;
            font-size: 2.2em; font-weight: bold; font-family: 'Jua', sans-serif;
            border: 4px solid #2a2a2a;
            box-shadow: inset 0 0 0 2px white, 5px 5px 0 #2a2a2a;
            z-index: 30;
            animation: badgePop 1s ease-out 1.5s backwards;
        }}
        @keyframes badgePop {{
            0% {{ transform: scale(0) rotate(-180deg); opacity: 0; }}
            100% {{ transform: scale(1) rotate(0deg); opacity: 1; }}
        }}
        .pokemon-name {{
            position: absolute; bottom: 40px; left: 50%;
            transform: translateX(-50%); background: white; color: #2a2a2a;
            padding: 12px 35px; border: 4px solid #2a2a2a; border-radius: 15px;
            font-size: 2em; font-weight: bold; font-family: 'Jua', sans-serif;
            box-shadow: inset 0 0 0 2px white, inset 0 0 0 5px {eff['c1']}, 5px 5px 0 #2a2a2a;
            z-index: 30; opacity: 0;
            animation: nameAppear 0.8s ease-out 2s forwards;
            white-space: nowrap;
        }}
        @keyframes nameAppear {{
            0% {{ opacity: 0; transform: translateX(-50%) translateY(50px) scale(0.5); }}
            100% {{ opacity: 1; transform: translateX(-50%) translateY(0) scale(1); }}
        }}
        .flash {{
            position: absolute; top: 0; left: 0; right: 0; bottom: 0;
            background: white; opacity: 0;
            animation: flashEffect 2s ease-out;
            z-index: 25; pointer-events: none;
        }}
        @keyframes flashEffect {{
            0% {{ opacity: 0; }} 10% {{ opacity: 1; }} 30% {{ opacity: 0; }}
            40% {{ opacity: 0.7; }} 60% {{ opacity: 0; }} 100% {{ opacity: 0; }}
        }}
    </style>
    </head>
    <body>
        <div class="stage">
            <div class="explosion"></div>
            <div class="explosion"></div>
            <div class="explosion"></div>
            {rays}
            {confetti}
            {particles}
            <div class="flash"></div>
            <div class="mbti-badge">{mbti}</div>
            <div class="pokeball"></div>
            <img src="{img_url}" class="pokemon-img" alt="{pokemon_name}">
            <div class="pokemon-name">⚡ {pokemon_name} ⚡</div>
        </div>
    </body></html>
    """
    return html


# 세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state.page = 'intro'
if 'q_idx' not in st.session_state:
    st.session_state.q_idx = 0
if 'mbti' not in st.session_state:
    st.session_state.mbti = ""
if 'question_count' not in st.session_state:
    st.session_state.question_count = 16
if 'selected_questions' not in st.session_state:
    st.session_state.selected_questions = []
if 'answers' not in st.session_state:
    st.session_state.answers = []


def calculate_mbti():
    scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
    for ans in st.session_state.answers:
        scores[ans] += 1
    mbti = ""
    mbti += "E" if scores["E"] >= scores["I"] else "I"
    mbti += "S" if scores["S"] >= scores["N"] else "N"
    mbti += "T" if scores["T"] >= scores["F"] else "F"
    mbti += "J" if scores["J"] >= scores["P"] else "P"
    return mbti, scores


# 헤더
st.markdown('<div class="pokemon-title">POKEMON MBTI</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align:center;"><span class="sub-text">⚡ 당신의 운명의 포켓몬을 찾아보세요! ⚡</span></div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ===== 인트로 페이지 =====
if st.session_state.page == 'intro':
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="info-card">
            <div style='text-align: center;'>
                <h2 style='color: #FF1F1F;'>🎮 환영합니다, 트레이너!</h2>
                <div style='font-size: 4em; margin: 20px 0;'>⚡</div>
                <p style='font-size: 1.2em; line-height: 1.8;'>
                    MBTI 검사를 완료하고<br>
                    당신만의 <b style='color:#3B4CCA;'>운명의 포켓몬</b>을<br>
                    화려한 효과와 함께 만나보세요!
                </p>
                <p style='font-size: 1.5em;'>🔥 💧 ⚡ 🍃 ✨</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-card">
            <h3 style='text-align: center; color: #3B4CCA;'>📝 질문 개수를 선택하세요</h3>
        </div>
        """, unsafe_allow_html=True)
        
        question_count = st.radio("원하는 질문 개수", [16, 20, 24], horizontal=True,
                                   format_func=lambda x: f"🎯 {x}문항")
        st.session_state.question_count = question_count
        
        info_text = {16: "⚡ 빠르게 결과를 보고 싶다면 16문항!",
                     20: "🎯 균형있게 검사하려면 20문항!",
                     24: "💎 가장 정확한 결과를 원한다면 24문항!"}
        
        st.markdown(f'<div class="pokemon-box" style="text-align:center; font-size:1.2em;">{info_text[question_count]}</div>',
                    unsafe_allow_html=True)
        
        if st.button("🚀 모험 시작하기!", use_container_width=True):
            per_category = question_count // 4
            selected = []
            for cat in ["EI", "SN", "TF", "JP"]:
                qs = random.sample(all_questions[cat], per_category)
                for q in qs:
                    q_with_type = q.copy()
                    q_with_type['type'] = cat
                    selected.append(q_with_type)
            random.shuffle(selected)
            st.session_state.selected_questions = selected
            st.session_state.page = 'test'
            st.session_state.q_idx = 0
            st.session_state.answers = []
            st.rerun()

# ===== 테스트 페이지 =====
elif st.session_state.page == 'test':
    idx = st.session_state.q_idx
    questions = st.session_state.selected_questions
    total = len(questions)
    
    progress_pct = int((idx / total) * 100)
    st.markdown(f"""
    <div class="progress-box">
        ⚔️ 진행도 {idx} / {total} ⚔️
        <div class="hp-bar-container">
            <div class="hp-bar" style="width: {progress_pct}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    q = questions[idx]
    
    st.markdown(f"""
    <div class="pokemon-box">
        <div style='font-size: 1.1em; color: #3B4CCA; font-weight: bold; margin-bottom: 10px;'>
            ❓ 질문 {idx + 1}
        </div>
        <div style='font-size: 1.4em; line-height: 1.6;'>
            {q['q']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"▶ {q['a'][0]}", use_container_width=True, key=f"btn0_{idx}"):
            st.session_state.answers.append(q['type'][0])
            st.session_state.q_idx += 1
            if st.session_state.q_idx >= total:
                mbti, _ = calculate_mbti()
                st.session_state.mbti = mbti
                st.session_state.page = 'result'
            st.rerun()
    with col2:
        if st.button(f"▶ {q['a'][1]}", use_container_width=True, key=f"btn1_{idx}"):
            st.session_state.answers.append(q['type'][1])
            st.session_state.q_idx += 1
            if st.session_state.q_idx >= total:
                mbti, _ = calculate_mbti()
                st.session_state.mbti = mbti
                st.session_state.page = 'result'
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_back, col_home = st.columns(2)
    with col_back:
        if idx > 0:
            if st.button("⬅️ 이전 질문으로", use_container_width=True):
                st.session_state.q_idx -= 1
                if st.session_state.answers:
                    st.session_state.answers.pop()
                st.rerun()
        else:
            st.button("⬅️ 이전 질문으로", use_container_width=True, disabled=True)
    with col_home:
        if st.button("🏠 처음부터 다시", use_container_width=True):
            st.session_state.page = 'intro'
            st.session_state.q_idx = 0
            st.session_state.answers = []
            st.rerun()

# ===== 결과 페이지 =====
elif st.session_state.page == 'result':
    mbti = st.session_state.mbti
    pokemon = mbti_pokemon[mbti]
    _, scores = calculate_mbti()
    
    st.balloons()
    
    celebration_html = get_pokemon_celebration_html(pokemon['type'], pokemon['id'], pokemon['name'], mbti)
    components.html(celebration_html, height=680)
    
    st.markdown(f"""
    <div class="info-card" style='text-align: center;'>
        <h2 style='color: #FF1F1F;'>🌟 {pokemon['name']}</h2>
        <div style='display: inline-block; background: #3B4CCA; color: white; padding: 8px 20px; border-radius: 20px; font-weight: bold; margin: 10px 0;'>
            {pokemon['type_kr']} 타입
        </div>
        <p style='font-size: 1.2em; margin: 20px 0; line-height: 1.6;'>{pokemon['desc']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🎯 트레이너의 특성")
    cols = st.columns(4)
    colors = ["#FF6B6B", "#4ECDC4", "#FFE66D", "#A8E6CF"]
    for i, trait in enumerate(pokemon['traits']):
        with cols[i]:
            st.markdown(f"""
            <div style='background: {colors[i]}; border: 4px solid #2a2a2a; padding: 20px; border-radius: 15px; text-align: center; font-size: 1.2em; font-weight: bold; box-shadow: 4px 4px 0 #2a2a2a;'>
                {trait}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📊 나의 MBTI 성향 분석")
    
    total_ei = scores["E"] + scores["I"]
    total_sn = scores["S"] + scores["N"]
    total_tf = scores["T"] + scores["F"]
    total_jp = scores["J"] + scores["P"]
    
    e_pct = round(scores["E"] / total_ei * 100) if total_ei > 0 else 50
    i_pct = 100 - e_pct
    s_pct = round(scores["S"] / total_sn * 100) if total_sn > 0 else 50
    n_pct = 100 - s_pct
    t_pct = round(scores["T"] / total_tf * 100) if total_tf > 0 else 50
    f_pct = 100 - t_pct
    j_pct = round(scores["J"] / total_jp * 100) if total_jp > 0 else 50
    p_pct = 100 - j_pct
    
    def render_bar(left_label, left_pct, right_label, right_pct, left_color, right_color, left_emoji, right_emoji):
        winner_left = "🏆" if left_pct > right_pct else ""
        winner_right = "🏆" if right_pct > left_pct else ""
        bar_html = f"""
        <div style='background: white; border: 4px solid #2a2a2a; padding: 20px; border-radius: 15px; margin: 15px 0; box-shadow: 4px 4px 0 #2a2a2a;'>
            <div style='display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 1.2em; font-weight: bold;'>
                <span style='color: {left_color};'>{winner_left} {left_emoji} {left_label} {left_pct}%</span>
                <span style='color: {right_color};'>{right_pct}% {right_label} {right_emoji} {winner_right}</span>
            </div>
            <div style='display: flex; height: 35px; border: 3px solid #2a2a2a; border-radius: 10px; overflow: hidden;'>
                <div style='width: {left_pct}%; background: {left_color}; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;'>
                    {left_pct if left_pct > 15 else ""}%
                </div>
                <div style='width: {right_pct}%; background: {right_color}; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;'>
                    {right_pct if right_pct > 15 else ""}%
                </div>
            </div>
        </div>
        """
        st.markdown(bar_html, unsafe_allow_html=True)
    
    render_bar("외향 (E)", e_pct, "내향 (I)", i_pct, "#ff6b6b", "#4d96ff", "🎉", "🌙")
    render_bar("감각 (S)", s_pct, "직관 (N)", n_pct, "#6bcf7f", "#a29bfe", "🌳", "✨")
    render_bar("사고 (T)", t_pct, "감정 (F)", f_pct, "#feca57", "#ff9ff3", "🧠", "💖")
    render_bar("판단 (J)", j_pct, "인식 (P)", p_pct, "#48dbfb", "#ff6348", "📅", "🎲")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 다시 테스트하기", use_container_width=True):
            st.session_state.page = 'intro'
            st.session_state.q_idx = 0
            st.session_state.answers = []
            st.rerun()
    with col2:
        if st.button("🎲 다른 MBTI 포켓몬 보기", use_container_width=True):
            random_mbti = random.choice([k for k in mbti_pokemon.keys() if k != mbti])
            st.session_state.mbti = random_mbti
            st.rerun()

# 사이드바
with st.sidebar:
    st.markdown("## 🎮 About")
    st.info("""
    **포켓몬 MBTI 도감** 🌟
    
    🎯 16/20/24문항 선택
    🎲 질문 랜덤 순서
    ⬅️ 뒤로가기 지원
    📊 MBTI 비율 그래프
    🎆 화려한 등장 효과
    """)
    
    st.markdown("---")
    st.markdown("### 💛 Made by")
    st.write("의찬 홍")
