import streamlit as st
import streamlit.components.v1 as components
import random
import time

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
    }
    
    .question-box {
        background: rgba(255, 255, 255, 0.95);
        padding: 25px;
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

# MBTI별 포켓몬 데이터 (타입별 효과 포함)
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

# 성격 테스트 질문 (12개)
questions = [
    {"q": "🎉 주말에 친구들과 파티 vs 집에서 혼자 쉬기?", "a": ["파티 가자!", "집순이~"], "type": "EI"},
    {"q": "💬 처음 만난 사람과 대화할 때?", "a": ["먼저 말 걸어요!", "조용히 있어요"], "type": "EI"},
    {"q": "🔋 에너지 충전 방법은?", "a": ["사람들과 어울리기", "혼자만의 시간"], "type": "EI"},
    {"q": "📚 공부할 때 더 끌리는 것은?", "a": ["실용적인 지식", "이론과 상상"], "type": "SN"},
    {"q": "🎨 문제를 풀 때 나는?", "a": ["경험과 사실 기반", "직관과 영감"], "type": "SN"},
    {"q": "🌟 평소 더 관심있는 것?", "a": ["현재의 현실", "미래의 가능성"], "type": "SN"},
    {"q": "🤔 친구가 고민 상담할 때?", "a": ["해결책 제시", "공감하고 위로"], "type": "TF"},
    {"q": "⚖️ 결정할 때 중요한 것?", "a": ["논리와 객관성", "감정과 가치관"], "type": "TF"},
    {"q": "💭 영화를 볼 때 나는?", "a": ["스토리 분석", "감정에 몰입"], "type": "TF"},
    {"q": "📅 여행 갈 때 나는?", "a": ["꼼꼼한 계획표", "즉흥적으로!"], "type": "JP"},
    {"q": "🗂️ 내 책상은?", "a": ["항상 정리정돈", "창의적 혼돈"], "type": "JP"},
    {"q": "⏰ 약속 시간에 나는?", "a": ["미리 도착", "딱 맞춰 or 살짝 늦게"], "type": "JP"},
]

# 세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state.page = 'intro'
if 'q_idx' not in st.session_state:
    st.session_state.q_idx = 0
if 'scores' not in st.session_state:
    st.session_state.scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
if 'mbti' not in st.session_state:
    st.session_state.mbti = ""


def get_pokemon_effect_html(pokemon_type, pokemon_id, pokemon_name):
    """포켓몬 타입에 따른 특수효과 HTML 생성"""
    img_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon_id}.png"
    
    # 타입별 효과 설정
    effects = {
        "fire": {
            "bg": "radial-gradient(circle, #ff6b35 0%, #f7931e 50%, #c1272d 100%)",
            "particles": "🔥",
            "color1": "#ff6b35", "color2": "#ffd93d",
            "animation": "flameRise"
        },
        "water": {
            "bg": "radial-gradient(circle, #4d96ff 0%, #0077be 50%, #003d82 100%)",
            "particles": "💧",
            "color1": "#4d96ff", "color2": "#a8d8ea",
            "animation": "waterSplash"
        },
        "electric": {
            "bg": "radial-gradient(circle, #ffd93d 0%, #f7c52d 50%, #e6a800 100%)",
            "particles": "⚡",
            "color1": "#ffd93d", "color2": "#fff700",
            "animation": "electricShock"
        },
        "grass": {
            "bg": "radial-gradient(circle, #6bcf7f 0%, #4a9d5e 50%, #2d6b3f 100%)",
            "particles": "🍃",
            "color1": "#6bcf7f", "color2": "#a8e6a3",
            "animation": "leafSwirl"
        },
        "psychic": {
            "bg": "radial-gradient(circle, #f368e0 0%, #be2edd 50%, #8854d0 100%)",
            "particles": "✨",
            "color1": "#f368e0", "color2": "#d980fa",
            "animation": "psychicWave"
        },
        "fairy": {
            "bg": "radial-gradient(circle, #ffb8d1 0%, #ff8fb1 50%, #ff6090 100%)",
            "particles": "💖",
            "color1": "#ffb8d1", "color2": "#ffd6e8",
            "animation": "fairyDust"
        },
        "dragon": {
            "bg": "radial-gradient(circle, #6c5ce7 0%, #4834d4 50%, #2c2c54 100%)",
            "particles": "🌀",
            "color1": "#6c5ce7", "color2": "#a29bfe",
            "animation": "dragonRoar"
        },
        "ghost": {
            "bg": "radial-gradient(circle, #6c5b7b 0%, #355c7d 50%, #1a1a2e 100%)",
            "particles": "👻",
            "color1": "#6c5b7b", "color2": "#a29bfe",
            "animation": "ghostFloat"
        },
        "fighting": {
            "bg": "radial-gradient(circle, #c0392b 0%, #922b21 50%, #641e16 100%)",
            "particles": "💥",
            "color1": "#c0392b", "color2": "#e74c3c",
            "animation": "powerPunch"
        },
        "normal": {
            "bg": "radial-gradient(circle, #ffeaa7 0%, #fdcb6e 50%, #e17055 100%)",
            "particles": "⭐",
            "color1": "#ffeaa7", "color2": "#fab1a0",
            "animation": "sparkle"
        }
    }
    
    eff = effects.get(pokemon_type, effects["normal"])
    
    # 파티클 30개 생성
    particles_html = ""
    for i in range(30):
        left = random.randint(0, 100)
        delay = random.uniform(0, 3)
        duration = random.uniform(2, 5)
        size = random.randint(20, 45)
        particles_html += f'<div class="particle" style="left:{left}%; animation-delay:{delay}s; animation-duration:{duration}s; font-size:{size}px;">{eff["particles"]}</div>'
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        .scene {{
            position: relative;
            width: 100%;
            height: 500px;
            background: {eff['bg']};
            border-radius: 30px;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(0,0,0,0.4);
            border: 5px solid white;
        }}
        
        .pokemon-img {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 350px;
            height: 350px;
            object-fit: contain;
            z-index: 10;
            filter: drop-shadow(0 0 30px {eff['color2']}) drop-shadow(0 0 50px {eff['color1']});
            animation: pokemonAppear 1.5s ease-out, pokemonFloat 3s ease-in-out 1.5s infinite;
        }}
        
        @keyframes pokemonAppear {{
            0% {{ transform: translate(-50%, -50%) scale(0) rotate(720deg); opacity: 0; }}
            60% {{ transform: translate(-50%, -50%) scale(1.2) rotate(0deg); opacity: 1; }}
            100% {{ transform: translate(-50%, -50%) scale(1) rotate(0deg); opacity: 1; }}
        }}
        
        @keyframes pokemonFloat {{
            0%, 100% {{ transform: translate(-50%, -50%) translateY(0); }}
            50% {{ transform: translate(-50%, -55%) translateY(-15px); }}
        }}
        
        .particle {{
            position: absolute;
            bottom: -50px;
            opacity: 0;
            animation: {eff['animation']} linear infinite;
            z-index: 5;
        }}
        
        /* 불꽃 효과 */
        @keyframes flameRise {{
            0% {{ bottom: -50px; opacity: 0; transform: rotate(0deg) scale(0.5); }}
            20% {{ opacity: 1; }}
            100% {{ bottom: 110%; opacity: 0; transform: rotate(360deg) scale(1.5); }}
        }}
        
        /* 물 효과 */
        @keyframes waterSplash {{
            0% {{ bottom: -50px; opacity: 0; transform: translateY(0) scale(0.5); }}
            20% {{ opacity: 1; }}
            100% {{ bottom: 110%; opacity: 0; transform: translateY(-50px) scale(1.2); }}
        }}
        
        /* 전기 효과 */
        @keyframes electricShock {{
            0% {{ bottom: 100%; opacity: 0; transform: scale(0); }}
            10% {{ opacity: 1; transform: scale(1.3); }}
            50% {{ opacity: 1; transform: scale(0.8); }}
            100% {{ bottom: -10%; opacity: 0; transform: scale(1); }}
        }}
        
        /* 잎사귀 효과 */
        @keyframes leafSwirl {{
            0% {{ bottom: -50px; left: 0%; opacity: 0; transform: rotate(0deg); }}
            20% {{ opacity: 1; }}
            100% {{ bottom: 110%; left: 100%; opacity: 0; transform: rotate(720deg); }}
        }}
        
        /* 사이코 효과 */
        @keyframes psychicWave {{
            0% {{ bottom: 50%; opacity: 0; transform: scale(0) rotate(0deg); }}
            50% {{ opacity: 1; transform: scale(2) rotate(180deg); }}
            100% {{ bottom: 50%; opacity: 0; transform: scale(3) rotate(360deg); }}
        }}
        
        /* 페어리 효과 */
        @keyframes fairyDust {{
            0% {{ bottom: -50px; opacity: 0; transform: scale(0); }}
            30% {{ opacity: 1; transform: scale(1); }}
            100% {{ bottom: 110%; opacity: 0; transform: scale(0.5) rotate(360deg); }}
        }}
        
        /* 드래곤 효과 */
        @keyframes dragonRoar {{
            0% {{ bottom: 50%; left: 50%; opacity: 0; transform: scale(0); }}
            50% {{ opacity: 1; transform: scale(2); }}
            100% {{ bottom: 50%; left: 50%; opacity: 0; transform: scale(4) rotate(720deg); }}
        }}
        
        /* 고스트 효과 */
        @keyframes ghostFloat {{
            0% {{ bottom: -50px; opacity: 0; transform: translateX(0); }}
            30% {{ opacity: 0.8; }}
            70% {{ opacity: 0.8; }}
            100% {{ bottom: 110%; opacity: 0; transform: translateX(50px); }}
        }}
        
        /* 격투 효과 */
        @keyframes powerPunch {{
            0% {{ bottom: 50%; opacity: 0; transform: scale(0); }}
            50% {{ opacity: 1; transform: scale(2); }}
            100% {{ bottom: 50%; opacity: 0; transform: scale(3); }}
        }}
        
        /* 노말 효과 */
        @keyframes sparkle {{
            0% {{ bottom: -50px; opacity: 0; transform: scale(0) rotate(0deg); }}
            50% {{ opacity: 1; transform: scale(1.5) rotate(180deg); }}
            100% {{ bottom: 110%; opacity: 0; transform: scale(0.5) rotate(360deg); }}
        }}
        
        .pokemon-name {{
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            color: white;
            font-size: 2.5em;
            font-weight: bold;
            text-shadow: 3px 3px 0 {eff['color1']}, -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000;
            z-index: 20;
            font-family: 'Jua', sans-serif;
            animation: nameGlow 2s ease-in-out infinite;
        }}
        
        @keyframes nameGlow {{
            0%, 100% {{ text-shadow: 3px 3px 0 {eff['color1']}, -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000, 0 0 20px white; }}
            50% {{ text-shadow: 3px 3px 0 {eff['color1']}, -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000, 0 0 40px {eff['color2']}; }}
        }}
        
        .flash {{
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: white;
            opacity: 0;
            animation: flash 1.5s ease-out;
            z-index: 15;
            pointer-events: none;
        }}
        
        @keyframes flash {{
            0% {{ opacity: 0; }}
            10% {{ opacity: 1; }}
            100% {{ opacity: 0; }}
        }}
    </style>
    </head>
    <body>
        <div class="scene">
            <div class="flash"></div>
            {particles_html}
            <img src="{img_url}" class="pokemon-img" alt="{pokemon_name}">
            <div class="pokemon-name">⚡ {pokemon_name} ⚡</div>
        </div>
    </body>
    </html>
    """
    return html


# 헤더
st.markdown('<p class="title-text">⚡ MBTI 포켓몬 매칭 ⚡</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">✨ 12가지 질문으로 운명의 포켓몬을 찾아보세요! ✨</p>', unsafe_allow_html=True)
st.markdown("---")

# ===== 인트로 페이지 =====
if st.session_state.page == 'intro':
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='background: rgba(255,255,255,0.9); padding: 40px; border-radius: 30px; text-align: center; box-shadow: 0 15px 35px rgba(0,0,0,0.2);'>
            <h2>🎮 환영합니다, 트레이너!</h2>
            <p style='font-size: 1.2em; margin: 20px 0;'>
                12가지 질문에 답하고<br>
                당신만의 운명의 포켓몬을 만나보세요!
            </p>
            <p style='font-size: 1.5em;'>🔥 💧 ⚡ 🍃 ✨</p>
            <p style='margin-top: 20px;'>각 포켓몬마다 <b>특별한 효과</b>가 펼쳐져요!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 테스트 시작하기!", use_container_width=True):
            st.session_state.page = 'test'
            st.session_state.q_idx = 0
            st.session_state.scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
            st.rerun()

# ===== 테스트 페이지 =====
elif st.session_state.page == 'test':
    idx = st.session_state.q_idx
    total = len(questions)
    
    # 진행률 표시
    progress = (idx) / total
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
                # MBTI 계산
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
    
    # 결과 발표
    st.markdown(f"<h1 style='text-align:center; color:white; text-shadow: 2px 2px 4px #000;'>🎉 당신의 MBTI는 {mbti}! 🎉</h1>", unsafe_allow_html=True)
    
    st.balloons()
    
    # 포켓몬 등장 (특수효과!)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align:center; color:white;'>✨ 당신의 운명의 포켓몬을 소환합니다... ✨</h2>", unsafe_allow_html=True)
    
    # HTML 특수효과 렌더링
    effect_html = get_pokemon_effect_html(pokemon['type'], pokemon['id'], pokemon['name'])
    components.html(effect_html, height=520)
    
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
    
    # 다시 하기 버튼
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
    
    12개 질문으로 MBTI 검사 후
    당신의 운명의 포켓몬을
    화려한 특수효과와 함께 만나보세요!
    
    🔥 불꽃 - 타오르는 불길
    💧 물 - 시원한 물방울
    ⚡ 전기 - 번쩍이는 번개
    🍃 풀 - 흩날리는 잎사귀
    ✨ 에스퍼 - 신비한 파동
    💖 페어리 - 반짝이는 가루
    👻 고스트 - 떠도는 영혼
    🌀 드래곤 - 강력한 소용돌이
    """)
    
    st.markdown("---")
    st.markdown("### 💛 Made by")
    st.write("의찬 홍.")
    st.caption("⚡ Powered by Streamlit")
