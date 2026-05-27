import streamlit as st
import streamlit.components.v1 as components
import random

# 페이지 설정
st.set_page_config(
    page_title="MBTI 포켓몬 매칭 🎮",
    page_icon="⚡",
    layout="wide"
)

# 기본 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Jua', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 50%, #fbc2eb 100%);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    
    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    
    .title-text {
        text-align: center;
        font-size: 3.5em;
        background: linear-gradient(45deg, #ff6b6b, #ffd93d, #6bcf7f, #4d96ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 100% {transform: translateY(0);}
        50% {transform: translateY(-10px);}
    }
    
    .sub-text {
        text-align: center;
        font-size: 1.3em;
        color: #fff;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .stButton>button {
        background: linear-gradient(45deg, #ff6b6b, #ffd93d);
        color: white;
        border-radius: 30px;
        border: none;
        padding: 15px 40px;
        font-size: 1.3em;
        font-weight: bold;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    
    .question-box {
        background: rgba(255, 255, 255, 0.95);
        padding: 30px;
        border-radius: 20px;
        margin: 15px 0;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        border-left: 6px solid #ff6b6b;
    }
    
    .progress-text {
        text-align: center;
        font-size: 1.2em;
        color: white;
        font-weight: bold;
    }
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

# 질문 풀 (24개 - 각 카테고리별 6개씩)
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
    """프리미어리그 골 셀러브레이션 스타일의 화려한 효과!"""
    img_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon_id}.png"
    
    # 타입별 색상 및 효과 설정
    effects = {
        "fire": {"c1": "#ff4500", "c2": "#ffd700", "c3": "#ff6347", "emoji": "🔥", "name": "FIRE BLAST"},
        "water": {"c1": "#1e90ff", "c2": "#00ced1", "c3": "#4169e1", "emoji": "💧", "name": "HYDRO PUMP"},
        "electric": {"c1": "#ffd700", "c2": "#ffff00", "c3": "#ffa500", "emoji": "⚡", "name": "THUNDER"},
        "grass": {"c1": "#32cd32", "c2": "#7fff00", "c3": "#00ff7f", "emoji": "🍃", "name": "SOLAR BEAM"},
        "psychic": {"c1": "#ff1493", "c2": "#da70d6", "c3": "#9370db", "emoji": "✨", "name": "PSYCHIC"},
        "fairy": {"c1": "#ff69b4", "c2": "#ffb6c1", "c3": "#ff1493", "emoji": "💖", "name": "MOONBLAST"},
        "dragon": {"c1": "#8a2be2", "c2": "#4b0082", "c3": "#9400d3", "emoji": "🌀", "name": "DRAGON RUSH"},
        "ghost": {"c1": "#483d8b", "c2": "#8b008b", "c3": "#4b0082", "emoji": "👻", "name": "SHADOW BALL"},
        "fighting": {"c1": "#dc143c", "c2": "#ff4500", "c3": "#b22222", "emoji": "💥", "name": "MEGA PUNCH"},
        "normal": {"c1": "#ffd700", "c2": "#ffa500", "c3": "#ff8c00", "emoji": "⭐", "name": "HYPER BEAM"}
    }
    
    eff = effects.get(pokemon_type, effects["normal"])
    
    # 폭죽 파티클 (50개)
    confetti = ""
    for i in range(60):
        left = random.randint(0, 100)
        delay = random.uniform(0, 2)
        duration = random.uniform(3, 6)
        color = random.choice([eff['c1'], eff['c2'], eff['c3'], '#ffd700', '#ffffff'])
        size = random.randint(8, 16)
        confetti += f'<div class="confetti" style="left:{left}%; background:{color}; width:{size}px; height:{size}px; animation-delay:{delay}s; animation-duration:{duration}s;"></div>'
    
    # 파티클 이모지 (40개)
    particles = ""
    for i in range(40):
        left = random.randint(0, 100)
        delay = random.uniform(0, 3)
        duration = random.uniform(4, 8)
        size = random.randint(25, 55)
        particles += f'<div class="emoji-particle" style="left:{left}%; animation-delay:{delay}s; animation-duration:{duration}s; font-size:{size}px;">{eff["emoji"]}</div>'
    
    # 광선 효과 (12개)
    rays = ""
    for i in range(12):
        angle = i * 30
        rays += f'<div class="light-ray" style="transform: rotate({angle}deg);"></div>'
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ overflow: hidden; }}
        
        .stage {{
            position: relative;
            width: 100%;
            height: 650px;
            background: radial-gradient(ellipse at center, {eff['c1']} 0%, {eff['c3']} 40%, #000 100%);
            border-radius: 25px;
            overflow: hidden;
            box-shadow: 0 25px 80px rgba(0,0,0,0.6);
            border: 6px solid {eff['c2']};
        }}
        
        /* 스타디움 라이트 효과 */
        .stadium-light {{
            position: absolute;
            top: -50%;
            left: 50%;
            transform: translateX(-50%);
            width: 200%;
            height: 200%;
            background: radial-gradient(ellipse at center top, rgba(255,255,255,0.3) 0%, transparent 50%);
            animation: lightMove 3s ease-in-out infinite;
        }}
        
        @keyframes lightMove {{
            0%, 100% {{ transform: translateX(-50%) rotate(-5deg); }}
            50% {{ transform: translateX(-50%) rotate(5deg); }}
        }}
        
        /* 광선 효과 */
        .light-ray {{
            position: absolute;
            top: 50%;
            left: 50%;
            width: 200%;
            height: 8px;
            background: linear-gradient(90deg, transparent, {eff['c2']}, transparent);
            transform-origin: left center;
            opacity: 0;
            animation: rayBurst 2s ease-out infinite;
        }}
        
        @keyframes rayBurst {{
            0% {{ opacity: 0; transform: rotate(var(--angle)) scaleX(0); }}
            20% {{ opacity: 1; transform: rotate(var(--angle)) scaleX(1); }}
            100% {{ opacity: 0; transform: rotate(var(--angle)) scaleX(1.5); }}
        }}
        
        .light-ray:nth-child(1) {{ animation-delay: 0s; }}
        .light-ray:nth-child(2) {{ animation-delay: 0.1s; }}
        .light-ray:nth-child(3) {{ animation-delay: 0.2s; }}
        .light-ray:nth-child(4) {{ animation-delay: 0.3s; }}
        .light-ray:nth-child(5) {{ animation-delay: 0.4s; }}
        .light-ray:nth-child(6) {{ animation-delay: 0.5s; }}
        
        /* 폭발 원형 효과 */
        .explosion {{
            position: absolute;
            top: 50%;
            left: 50%;
            width: 100px;
            height: 100px;
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
        
        /* 포켓몬 이미지 */
        .pokemon-img {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 400px;
            height: 400px;
            object-fit: contain;
            z-index: 20;
            filter: drop-shadow(0 0 40px {eff['c2']}) drop-shadow(0 0 80px {eff['c1']}) drop-shadow(0 0 120px white);
            animation: pokemonEntry 1.2s cubic-bezier(0.68, -0.55, 0.265, 1.55), pokemonDance 2s ease-in-out 1.2s infinite;
        }}
        
        @keyframes pokemonEntry {{
            0% {{ 
                transform: translate(-50%, -50%) scale(0) rotate(-720deg);
                opacity: 0;
                filter: blur(20px);
            }}
            50% {{
                transform: translate(-50%, -50%) scale(1.4) rotate(-180deg);
                opacity: 1;
                filter: blur(0px);
            }}
            70% {{
                transform: translate(-50%, -50%) scale(0.9) rotate(20deg);
            }}
            100% {{ 
                transform: translate(-50%, -50%) scale(1) rotate(0deg);
                opacity: 1;
            }}
        }}
        
        @keyframes pokemonDance {{
            0%, 100% {{ transform: translate(-50%, -50%) translateY(0) rotate(-3deg); }}
            25% {{ transform: translate(-50%, -55%) translateY(-15px) rotate(0deg); }}
            50% {{ transform: translate(-50%, -50%) translateY(0) rotate(3deg); }}
            75% {{ transform: translate(-50%, -55%) translateY(-15px) rotate(0deg); }}
        }}
        
        /* 폭죽 (Confetti) */
        .confetti {{
            position: absolute;
            top: -20px;
            opacity: 0;
            animation: confettiFall linear infinite;
            border-radius: 2px;
        }}
        
        @keyframes confettiFall {{
            0% {{ 
                top: -20px; 
                opacity: 1;
                transform: rotate(0deg) translateX(0);
            }}
            100% {{ 
                top: 110%; 
                opacity: 0;
                transform: rotate(720deg) translateX(100px);
            }}
        }}
        
        /* 이모지 파티클 */
        .emoji-particle {{
            position: absolute;
            bottom: -50px;
            opacity: 0;
            animation: particleFloat linear infinite;
            z-index: 15;
        }}
        
        @keyframes particleFloat {{
            0% {{ 
                bottom: -50px; 
                opacity: 0;
                transform: scale(0) rotate(0deg);
            }}
            10% {{ opacity: 1; }}
            50% {{ transform: scale(1.3) rotate(180deg); }}
            100% {{ 
                bottom: 110%; 
                opacity: 0;
                transform: scale(0.5) rotate(720deg);
            }}
        }}
        
        /* 기술 이름 (골 표시처럼) */
        .move-name {{
            position: absolute;
            top: 30px;
            left: 50%;
            transform: translateX(-50%);
            color: white;
            font-size: 4em;
            font-weight: 900;
            font-family: 'Jua', sans-serif;
            text-shadow: 
                0 0 20px {eff['c2']},
                0 0 40px {eff['c1']},
                4px 4px 0 #000,
                -2px -2px 0 #000,
                2px -2px 0 #000,
                -2px 2px 0 #000;
            z-index: 30;
            animation: moveNameSlide 1s ease-out, moveNamePulse 1.5s ease-in-out 1s infinite;
            letter-spacing: 5px;
        }}
        
        @keyframes moveNameSlide {{
            0% {{ transform: translateX(-50%) translateY(-200px) scale(0); opacity: 0; }}
            60% {{ transform: translateX(-50%) translateY(20px) scale(1.2); opacity: 1; }}
            100% {{ transform: translateX(-50%) translateY(0) scale(1); opacity: 1; }}
        }}
        
        @keyframes moveNamePulse {{
            0%, 100% {{ transform: translateX(-50%) scale(1); }}
            50% {{ transform: translateX(-50%) scale(1.08); }}
        }}
        
        /* 포켓몬 이름 (하단) */
        .pokemon-name {{
            position: absolute;
            bottom: 40px;
            left: 50%;
            transform: translateX(-50%);
            color: white;
            font-size: 3em;
            font-weight: bold;
            font-family: 'Jua', sans-serif;
            text-shadow: 
                0 0 15px {eff['c2']},
                3px 3px 0 #000,
                -2px -2px 0 #000,
                2px -2px 0 #000,
                -2px 2px 0 #000;
            z-index: 30;
            animation: nameAppear 1.5s ease-out, nameGlow 2s ease-in-out 1.5s infinite;
        }}
        
        @keyframes nameAppear {{
            0% {{ opacity: 0; transform: translateX(-50%) translateY(50px); }}
            100% {{ opacity: 1; transform: translateX(-50%) translateY(0); }}
        }}
        
        @keyframes nameGlow {{
            0%, 100% {{ text-shadow: 0 0 15px {eff['c2']}, 3px 3px 0 #000, -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000; }}
            50% {{ text-shadow: 0 0 40px {eff['c2']}, 0 0 60px {eff['c1']}, 3px 3px 0 #000, -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000; }}
        }}
        
        /* MBTI 뱃지 */
        .mbti-badge {{
            position: absolute;
            top: 30px;
            right: 30px;
            background: linear-gradient(135deg, {eff['c1']}, {eff['c2']});
            color: white;
            padding: 15px 25px;
            border-radius: 50px;
            font-size: 2em;
            font-weight: bold;
            font-family: 'Jua', sans-serif;
            box-shadow: 0 5px 20px rgba(0,0,0,0.5);
            z-index: 30;
            border: 3px solid white;
            animation: badgePop 1s ease-out 0.5s backwards, badgePulse 2s ease-in-out 1.5s infinite;
        }}
        
        @keyframes badgePop {{
            0% {{ transform: scale(0) rotate(-180deg); opacity: 0; }}
            100% {{ transform: scale(1) rotate(0deg); opacity: 1; }}
        }}
        
        @keyframes badgePulse {{
            0%, 100% {{ transform: scale(1); box-shadow: 0 5px 20px rgba(0,0,0,0.5); }}
            50% {{ transform: scale(1.1); box-shadow: 0 8px 30px {eff['c2']}; }}
        }}
        
        /* 플래시 효과 */
        .flash {{
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: white;
            opacity: 0;
            animation: flashEffect 2s ease-out;
            z-index: 25;
            pointer-events: none;
        }}
        
        @keyframes flashEffect {{
            0% {{ opacity: 0; }}
            10% {{ opacity: 1; }}
            30% {{ opacity: 0; }}
            40% {{ opacity: 0.7; }}
            60% {{ opacity: 0; }}
            70% {{ opacity: 0.4; }}
            100% {{ opacity: 0; }}
        }}
        
        /* 스포트라이트 */
        .spotlight {{
            position: absolute;
            top: 50%;
            left: 50%;
            width: 600px;
            height: 600px;
            background: radial-gradient(circle, rgba(255,255,255,0.4) 0%, transparent 60%);
            transform: translate(-50%, -50%);
            animation: spotlightPulse 2s ease-in-out infinite;
            z-index: 10;
        }}
        
        @keyframes spotlightPulse {{
            0%, 100% {{ opacity: 0.5; transform: translate(-50%, -50%) scale(1); }}
            50% {{ opacity: 1; transform: translate(-50%, -50%) scale(1.2); }}
        }}
    </style>
    </head>
    <body>
        <div class="stage">
            <div class="stadium-light"></div>
            <div class="spotlight"></div>
            <div class="explosion"></div>
            <div class="explosion"></div>
            <div class="explosion"></div>
            {rays}
            {confetti}
            {particles}
            <div class="flash"></div>
            <div class="move-name">{eff['name']}!</div>
            <div class="mbti-badge">{mbti}</div>
            <img src="{img_url}" class="pokemon-img" alt="{pokemon_name}">
            <div class="pokemon-name">⚡ {pokemon_name} ⚡</div>
        </div>
    </body>
    </html>
    """
    return html


# 세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state.page = 'intro'
if 'q_idx' not in st.session_state:
    st.session_state.q_idx = 0
if 'scores' not in st.session_state:
    st.session_state.scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
if 'mbti' not in st.session_state:
    st.session_state.mbti = ""
if 'question_count' not in st.session_state:
    st.session_state.question_count = 16
if 'selected_questions' not in st.session_state:
    st.session_state.selected_questions = []


# 헤더
st.markdown('<p class="title-text">⚡ MBTI 포켓몬 매칭 ⚡</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">✨ MBTI 검사 후 운명의 포켓몬을 화려하게 만나보세요! ✨</p>', unsafe_allow_html=True)
st.markdown("---")

# ===== 인트로 페이지 =====
if st.session_state.page == 'intro':
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='background: rgba(255,255,255,0.95); padding: 40px; border-radius: 30px; text-align: center; box-shadow: 0 15px 35px rgba(0,0,0,0.2);'>
            <h2>🎮 환영합니다, 트레이너!</h2>
            <p style='font-size: 1.2em; margin: 20px 0;'>
                MBTI 검사를 완료하고<br>
                <b>프리미어리그 골 셀러브레이션</b>처럼<br>
                화려한 효과와 함께 포켓몬을 만나보세요!
            </p>
            <p style='font-size: 1.5em;'>🔥 💧 ⚡ 🍃 ✨ 🎆</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📝 질문 개수를 선택하세요")
        
        question_count = st.radio(
            "원하는 질문 개수를 골라주세요!",
            [16, 20, 24],
            horizontal=True,
            format_func=lambda x: f"🎯 {x}문항 ({'간단' if x==16 else '보통' if x==20 else '정확'})"
        )
        st.session_state.question_count = question_count
        
        info_text = {
            16: "⚡ 빠르게 결과를 보고 싶다면 16문항!",
            20: "🎯 균형있게 검사하려면 20문항!",
            24: "💎 가장 정확한 결과를 원한다면 24문항!"
        }
        st.info(info_text[question_count])
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 테스트 시작하기!", use_container_width=True):
            # 각 카테고리에서 질문 균등하게 선택
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
            st.session_state.scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
            st.rerun()

# ===== 테스트 페이지 =====
elif st.session_state.page == 'test':
    idx = st.session_state.q_idx
    questions = st.session_state.selected_questions
    total = len(questions)
    
    # 진행률
    progress = idx / total
    st.progress(progress)
    st.markdown(f'<p class="progress-text">📍 질문 {idx + 1} / {total}</p>', unsafe_allow_html=True)
    
    q = questions[idx]
    
    st.markdown(f'<div class="question-box">', unsafe_allow_html=True)
    st.markdown(f"### Q{idx + 1}. {q['q']}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(f"✨ {q['a'][0]}", use_container_width=True, key=f"btn0_{idx}"):
            st.session_state.scores[q['type'][0]] += 1
            st.session_state.q_idx += 1
            if st.session_state.q_idx >= total:
                s = st.session_state.scores
                mbti = ""
                mbti += "E" if s["E"] >= s["I"] else "I"
                mbti += "S" if s["S"] >= s["N"] else "N"
                mbti += "T" if s["T"] >= s["F"] else "F"
                mbti += "J" if s["J"] >= s["P"] else "P"
                st.session_state.mbti = mbti
                st.session_state.page = 'result'
            st.rerun()
    
    with col2:
        if st.button(f"🌟 {q['a'][1]}", use_container_width=True, key=f"btn1_{idx}"):
            st.session_state.scores[q['type'][1]] += 1
            st.session_state.q_idx += 1
            if st.session_state.q_idx >= total:
                s = st.session_state.scores
                mbti = ""
                mbti += "E" if s["E"] >= s["I"] else "I"
                mbti += "S" if s["S"] >= s["N"] else "N"
                mbti += "T" if s["T"] >= s["F"] else "F"
                mbti += "J" if s["J"] >= s["P"] else "P"
                st.session_state.mbti = mbti
                st.session_state.page = 'result'
            st.rerun()
    
    st.markdown("---")
    if st.button("🔄 처음부터 다시"):
        st.session_state.page = 'intro'
        st.rerun()

# ===== 결과 페이지 =====
elif st.session_state.page == 'result':
    mbti = st.session_state.mbti
    pokemon = mbti_pokemon[mbti]
    scores = st.session_state.scores
    
    st.balloons()
    st.snow()
    
    # 화려한 포켓몬 등장!
    celebration_html = get_pokemon_celebration_html(pokemon['type'], pokemon['id'], pokemon['name'], mbti)
    components.html(celebration_html, height=670)
    
    # 포켓몬 정보
    st.markdown(f"""
    <div style='background: rgba(255,255,255,0.95); padding: 30px; border-radius: 25px; margin-top: 20px; text-align: center; box-shadow: 0 15px 35px rgba(0,0,0,0.2);'>
        <h2>🌟 {pokemon['name']} ({pokemon['type_kr']} 타입)</h2>
        <p style='font-size: 1.3em; margin: 20px 0;'>{pokemon['desc']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 특성
    st.markdown("### 🎯 당신의 특성")
    cols = st.columns(4)
    for i, trait in enumerate(pokemon['traits']):
        with cols[i]:
            st.markdown(f"""
            <div style='background: linear-gradient(45deg, #ffeaa7, #fab1a0); padding: 20px; border-radius: 20px; text-align: center; font-size: 1.2em; font-weight: bold; box-shadow: 0 5px 15px rgba(0,0,0,0.1);'>
                {trait}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ===== MBTI 비율 그래프 =====
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
        <div style='background: white; padding: 20px; border-radius: 20px; margin: 15px 0; box-shadow: 0 5px 15px rgba(0,0,0,0.1);'>
            <div style='display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 1.2em; font-weight: bold;'>
                <span style='color: {left_color};'>{winner_left} {left_emoji} {left_label} {left_pct}%</span>
                <span style='color: {right_color};'>{right_pct}% {right_label} {right_emoji} {winner_right}</span>
            </div>
            <div style='display: flex; height: 35px; border-radius: 20px; overflow: hidden; box-shadow: inset 0 2px 5px rgba(0,0,0,0.2);'>
                <div style='width: {left_pct}%; background: linear-gradient(90deg, {left_color}, {left_color}dd); display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;'>
                    {left_pct if left_pct > 15 else ""}%
                </div>
                <div style='width: {right_pct}%; background: linear-gradient(90deg, {right_color}dd, {right_color}); display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;'>
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
    
    # 분석 코멘트
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 25px; border-radius: 20px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.2);'>
        <h3>📈 분석 결과</h3>
        <p style='font-size: 1.2em; margin-top: 15px;'>
            당신은 <b>{mbti}</b> 유형으로,<br>
            E/I: {max(e_pct, i_pct)}% ({'외향' if e_pct > i_pct else '내향'}) | 
            S/N: {max(s_pct, n_pct)}% ({'감각' if s_pct > n_pct else '직관'}) |<br>
            T/F: {max(t_pct, f_pct)}% ({'사고' if t_pct > f_pct else '감정'}) | 
            J/P: {max(j_pct, p_pct)}% ({'판단' if j_pct > p_pct else '인식'}) 성향이 강해요!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 버튼
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 다시 테스트하기", use_container_width=True):
            st.session_state.page = 'intro'
            st.session_state.q_idx = 0
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
    **MBTI 포켓몬 매칭** 🌟
    
    ⚽ **프리미어리그 골 셀러브레이션**
    스타일의 화려한 효과!
    
    📊 **MBTI 비율 그래프**로
    내 성향을 정확히 분석!
    
    🎯 **16/20/24문항** 선택 가능
    
    🔥 타입별 특수효과:
    - 🔥 불꽃 | 💧 물 | ⚡ 전기
    - 🍃 풀 | ✨ 에스퍼 | 💖 페어리
    - 🌀 드래곤 | 👻 고스트
    - 💥 격투 | ⭐ 노말
    """)
    
    st.markdown("---")
    st.markdown("### 💛 Made by")
    st.write("당곡고등학교 학생")
    st.caption("⚡ Powered by Streamlit")
