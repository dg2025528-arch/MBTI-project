import streamlit as st
import random

# 페이지 설정
st.set_page_config(
    page_title="MBTI 포켓몬 매칭 🎮",
    page_icon="⚡",
    layout="centered"
)

# CSS 스타일 (귀엽게 꾸미기)
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
    }
    .title-text {
        text-align: center;
        font-size: 3em;
        color: #ff6b6b;
        text-shadow: 2px 2px 4px #ffd93d;
        font-weight: bold;
    }
    .sub-text {
        text-align: center;
        font-size: 1.2em;
        color: #4a4a4a;
    }
    .pokemon-card {
        background: white;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        text-align: center;
        margin-top: 20px;
    }
    .stButton>button {
        background: linear-gradient(45deg, #ff6b6b, #ffd93d);
        color: white;
        border-radius: 30px;
        border: none;
        padding: 10px 30px;
        font-size: 1.1em;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# MBTI별 포켓몬 데이터
mbti_pokemon = {
    "INTJ": {
        "name": "뮤츠 (Mewtwo)",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/150.png",
        "description": "전략적이고 지적인 INTJ에게는 강력한 정신력을 가진 뮤츠가 어울려요!",
        "traits": "🧠 천재적인 지능 | 🔮 강력한 초능력 | 🎯 완벽한 전략가"
    },
    "INTP": {
        "name": "알라카잠 (Alakazam)",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/65.png",
        "description": "호기심 많고 분석적인 INTP에게는 IQ 5000의 알라카잠이 딱이에요!",
        "traits": "📚 무한한 지식 | 🥄 강력한 사이코키네시스 | 💭 깊은 사고"
    },
    "ENTJ": {
        "name": "리자몽 (Charizard)",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/6.png",
        "description": "리더십 강한 ENTJ에게는 카리스마 넘치는 리자몽이 어울려요!",
        "traits": "🔥 강력한 리더십 | 👑 카리스마 | 🏆 승부욕"
    },
    "ENTP": {
        "name": "겟핵스 (Hydreigon)",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/635.png",
        "description": "창의적이고 토론을 즐기는 ENTP에게는 머리가 세 개인 삼삼드래!",
        "traits": "💡 창의적 사고 | 🗣️ 다방면 토론 | 🌪️ 에너지 폭발"
    },
    "INFJ": {
        "name": "가디안 (Gardevoir)",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/282.png",
        "description": "공감 능력이 뛰어난 INFJ에게는 트레이너를 지키는 가디안이 완벽!",
        "traits": "💝 깊은 공감 | 🛡️ 헌신적 보호 | ✨ 신비로운 직감"
    },
    "INFP": {
        "name": "이브이 (Eevee)",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/133.png",
        "description": "감수성 풍부한 INFP에게는 무한한 가능성을 가진 이브이가 어울려요!",
        "traits": "🌈 무한한 가능성 | 💗 따뜻한 마음 | 🎨 다양한 진화"
    },
    "ENFJ": {
        "name": "해피너스 (Blissey)",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/242.png",
        "description": "타인을 챙기는 ENFJ에게는 모두를 치유하는 해피너스가 딱!",
        "traits": "💖 따뜻한 배려 | 🌟 긍정 에너지 | 🤗 치유의 능력"
    },
    "ENFP": {
        "name": "피카츄 (Pikachu)",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png",
        "description": "밝고 에너지 넘치는 ENFP에게는 사랑스러운 피카츄가 최고!",
        "traits": "⚡ 활발한 에너지 | 😊 친근한 매력 | 🎉 자유로운 영혼"
    },
    "ISTJ": {
        "name": "거북왕 (Blastoise)",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/9.png",
        "description": "책임감 강하고 신중한 ISTJ에게는 든든한 거북왕이 어울려요!",
        "traits": "🛡️ 단단한 신뢰 | 📋 철저한 계획 | 💪 책임감"
    },
    "ISFJ": {
        "name": "이상해꽃 (Venusaur)",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/3.png",
        "description": "헌신적이고 따뜻한 ISFJ에게는 포근한 이상해꽃이 딱!",
        "traits": "🌷 따뜻한 헌신 | 🌿 안정감 | 💚 보호 본능"
    },
    "ESTJ": {
        "name": "갸라도스 (Gyarados)",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/130.png",
        "description": "리더십과 결단력의 ESTJ에게는 강력한 갸라도스가 어울려요!",
        "traits": "👑 강한 리더십 | ⚔️ 결단력 | 🌊 압도적 존재감"
    },
    "ESFJ": {
        "name": "푸린 (Jigglypuff)",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/39.png",
        "description": "사교적이고 다정한 ESFJ에게는 모두를 웃게 하는 푸린이 최고!",
        "traits": "🎵 즐거운 분위기 | 💕 다정함 | 🤝 사교성"
    },
    "ISTP": {
        "name": "루카리오 (Lucario)",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/448.png",
        "description": "쿨하고 실용적인 ISTP에게는 파동을 다루는 루카리오가 어울려요!",
        "traits": "🥋 뛰어난 실력 | 🧘 차분한 집중 | ⚡ 직관적 판단"
    },
    "ISFP": {
        "name": "이브이→샤미드 (Vaporeon)",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/134.png",
        "description": "예술적이고 부드러운 ISFP에게는 우아한 샤미드가 딱!",
        "traits": "🎨 예술적 감각 | 🌊 부드러운 흐름 | 💙 평화로움"
    },
    "ESTP": {
        "name": "팬텀 (Gengar)",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/94.png",
        "description": "장난스럽고 모험적인 ESTP에게는 짓궂은 팬텀이 어울려요!",
        "traits": "😈 장난기 만점 | 🎭 대담한 모험 | 💨 빠른 행동력"
    },
    "ESFP": {
        "name": "이브이→블래키 반대 님피아 (Sylveon)",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/700.png",
        "description": "사랑스럽고 인기 많은 ESFP에게는 매력적인 님피아가 최고!",
        "traits": "💖 사랑스러운 매력 | 🌸 사교성 | 🎀 화려한 존재감"
    }
}

# 헤더
st.markdown('<p class="title-text">⚡ MBTI 포켓몬 매칭 ⚡</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">당신의 MBTI에 어울리는 포켓몬을 찾아보세요! 🎮✨</p>', unsafe_allow_html=True)
st.markdown("---")

# MBTI 선택
st.markdown("### 🔮 당신의 MBTI를 선택하세요!")

col1, col2 = st.columns(2)
with col1:
    ei = st.radio("외향성 vs 내향성", ["E (외향형)", "I (내향형)"], horizontal=True)
    sn = st.radio("감각 vs 직관", ["S (감각형)", "N (직관형)"], horizontal=True)
with col2:
    tf = st.radio("사고 vs 감정", ["T (사고형)", "F (감정형)"], horizontal=True)
    jp = st.radio("판단 vs 인식", ["J (판단형)", "P (인식형)"], horizontal=True)

mbti = ei[0] + sn[0] + tf[0] + jp[0]

st.markdown(f"### 🎯 선택한 MBTI: **{mbti}**")

# 결과 보기 버튼
if st.button("🎁 내 포켓몬 만나기!", use_container_width=True):
    if mbti in mbti_pokemon:
        pokemon = mbti_pokemon[mbti]
        
        st.balloons()  # 풍선 효과!
        
        st.markdown('<div class="pokemon-card">', unsafe_allow_html=True)
        st.markdown(f"## 🎉 {mbti}님의 운명의 포켓몬은...")
        st.markdown(f"# ✨ {pokemon['name']} ✨")
        
        st.image(pokemon['image'], width=300)
        
        st.markdown(f"### 💌 {pokemon['description']}")
        st.markdown(f"#### {pokemon['traits']}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.success(f"🌟 {pokemon['name']}와 함께 즐거운 모험을 떠나보세요!")

# 사이드바
with st.sidebar:
    st.markdown("## 🎮 About")
    st.info("""
    이 앱은 **MBTI 성격 유형**에 따라
    어울리는 **포켓몬을 추천**해주는
    재미있는 웹앱이에요! 🌈
    
    16가지 MBTI 유형마다
    특별한 포켓몬이 기다리고 있어요! ⚡
    """)
    
    st.markdown("## 🌟 Made by")
    st.write("당곡고등학교 학생 💛")
    
    if st.button("🎲 랜덤 MBTI 추천!"):
        random_mbti = random.choice(list(mbti_pokemon.keys()))
        st.write(f"오늘의 추천 MBTI: **{random_mbti}**")
        st.write(f"포켓몬: {mbti_pokemon[random_mbti]['name']}")
