# streamlit_app.py
import streamlit as st
import random
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="해양 보호 게임", page_icon="🐟", layout="wide")

# 세션 상태 초기화
if "fish_pos" not in st.session_state:
    st.session_state.fish_pos = 5   # 물고기 위치 (1~10)
if "objects" not in st.session_state:
    st.session_state.objects = []  # (이모지, x좌표, y좌표)
if "score" not in st.session_state:
    st.session_state.score = 0
if "health" not in st.session_state:
    st.session_state.health = 5
if "tick" not in st.session_state:
    st.session_state.tick = 0
if "running" not in st.session_state:
    st.session_state.running = False

# CSS 꾸미기
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(#00bfff, #001f3f);
        color: white;
    }
    .game-row {
        font-size: 28px;
        font-family: "Noto Emoji", sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🌊 해양 보호 게임 🐟")
st.write("플라스틱 🗑️, 기름 ⚫ 을 피하고, 거품 🫧 을 먹어 체력을 회복하세요!")

# 조작 버튼
col1, col2, col3 = st.columns([1,1,1])
with col1:
    if st.button("⬅️ 왼쪽"):
        if st.session_state.fish_pos > 1:
            st.session_state.fish_pos -= 1
with col3:
    if st.button("➡️ 오른쪽"):
        if st.session_state.fish_pos < 10:
            st.session_state.fish_pos += 1

# 시작/중지 버튼
if not st.session_state.running:
    if st.button("▶️ 게임 시작"):
        st.session_state.running = True
else:
    if st.button("⏸️ 게임 중지"):
        st.session_state.running = False

# 자동 새로고침 (500ms = 0.5초마다 새로고침)
if st.session_state.running:
    st_autorefresh(interval=500, key="game_refresh")

# 게임 로직
if st.session_state.running and st.session_state.health > 0:
    st.session_state.tick += 1

    # 일정 주기마다 오브젝트 생성
    if st.session_state.tick % 3 == 0:
        kind = random.choice(["plastic", "oil", "bubble", "plastic"])
        if kind == "plastic":
            st.session_state.objects.append(["🗑️", random.randint(1, 10), 10])
        elif kind == "oil":
            st.session_state.objects.append(["⚫", random.randint(1, 10), 10])
        elif kind == "bubble":
            st.session_state.objects.append(["🫧", random.randint(1, 10), 10])

    # 오브젝트 이동
    new_objects = []
    for obj, x, y in st.session_state.objects:
        y -= 1
        if y > 0:
            new_objects.append([obj, x, y])
    st.session_state.objects = new_objects

    # 충돌 판정
    for obj, x, y in st.session_state.objects:
        if y == 1 and x == st.session_state.fish_pos:
            if obj in ["🗑️", "⚫"]:
                st.session_state.health -= 1
            elif obj == "🫧":
                st.session_state.health += 1
            st.session_state.objects.remove([obj, x, y])

    # 점수 증가
    st.session_state.score += 1

# 게임 화면 출력
grid = [["🌊"] * 10 for _ in range(10)]
for obj, x, y in st.session_state.objects:
    grid[10 - y][x - 1] = obj
grid[9][st.session_state.fish_pos - 1] = "🐟"

for row in grid:
    st.markdown('<div class="game-row">' + "".join(row) + "</div>", unsafe_allow_html=True)

# 상태 출력
st.metric("점수", st.session_state.score)
st.metric("물고기 체력", st.session_state.health)

# 게임 오버
if st.session_state.health <= 0:
    st.error("💀 물고기가 오염물질을 너무 많이 먹었어요! 게임 오버")
    if st.button("다시 시작"):
        st.session_state.fish_pos = 5
        st.session_state.objects = []
        st.session_state.score = 0
        st.session_state.health = 5
        st.session_state.tick = 0
        st.session_state.running = False
