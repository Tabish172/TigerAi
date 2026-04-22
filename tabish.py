import streamlit as st
import json
import os
import time
from datetime import datetime

# ----------------------------
# PAGE CONFIG — must be FIRST st call
# ----------------------------
st.set_page_config(page_title="TigerAI", layout="wide", page_icon="🐯")

# ----------------------------
# TIGER SKIN CSS
# ----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Rajdhani:wght@400;600;700&display=swap');

.stApp {
    background-color: #1a0a00;
    background-image:
        repeating-linear-gradient(45deg, rgba(0,0,0,0.45) 0px, rgba(0,0,0,0.45) 18px, transparent 18px, transparent 38px),
        repeating-linear-gradient(-45deg, rgba(0,0,0,0.3) 0px, rgba(0,0,0,0.3) 12px, transparent 12px, transparent 32px),
        linear-gradient(160deg, #c46200 0%, #7a2e00 40%, #3d1200 70%, #1a0a00 100%);
    font-family: 'Rajdhani', sans-serif;
}

h1, h2, h3 {
    font-family: 'Bebas Neue', sans-serif !important;
    letter-spacing: 4px !important;
    color: #ffb347 !important;
    text-shadow: 0 0 20px #ff6b00, 2px 2px 0px #000 !important;
    text-align: center;
}

.login-container {
    max-width: 420px;
    margin: 60px auto;
    background: rgba(20, 8, 0, 0.92);
    border: 2px solid #c46200;
    border-radius: 18px;
    padding: 40px 36px 32px;
    box-shadow: 0 0 40px #ff6b0055, 0 0 80px #c4620033;
}
.login-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.8rem;
    letter-spacing: 6px;
    color: #ffb347;
    text-shadow: 0 0 20px #ff6b00;
    text-align: center;
    margin-bottom: 6px;
}
.login-subtitle {
    text-align: center;
    color: #c46200;
    font-family: 'Rajdhani', sans-serif;
    font-size: 1rem;
    letter-spacing: 2px;
    margin-bottom: 28px;
}

.stChatMessage {
    background: rgba(30, 10, 0, 0.75) !important;
    border: 1px solid rgba(255, 140, 0, 0.3) !important;
    border-radius: 14px !important;
    padding: 12px 16px !important;
    backdrop-filter: blur(8px);
    margin-bottom: 10px;
}

[data-testid="stChatMessageContent"] p {
    color: #ffe8cc !important;
    font-size: 1.05rem !important;
    font-family: 'Rajdhani', sans-serif !important;
}

[data-testid="stSidebar"] {
    background: rgba(15, 5, 0, 0.97) !important;
    border-right: 2px solid #c46200 !important;
}
[data-testid="stSidebar"] * {
    color: #ffb347 !important;
    font-family: 'Rajdhani', sans-serif !important;
}

.stButton > button {
    background: linear-gradient(135deg, #c46200, #ff8c00) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1rem !important;
    letter-spacing: 2px !important;
    padding: 10px 24px !important;
    box-shadow: 0 4px 15px rgba(255, 100, 0, 0.5) !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: scale(1.05) !important;
    box-shadow: 0 6px 25px rgba(255, 140, 0, 0.8) !important;
}

.stTextInput > div > input {
    background: rgba(40, 15, 0, 0.85) !important;
    color: #ffe8cc !important;
    border: 1.5px solid #c46200 !important;
    border-radius: 12px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem !important;
}

.stChatInput textarea {
    background: rgba(40, 15, 0, 0.8) !important;
    color: #ffe8cc !important;
    border: 1.5px solid #c46200 !important;
    border-radius: 12px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem !important;
}

.badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-family: 'Rajdhani', sans-serif;
    letter-spacing: 1px;
    font-weight: 700;
}
.badge-online { background: #1a4d1a; color: #7fff7f; border: 1px solid #3a9a3a; }
.badge-session { background: #4d2500; color: #ffb347; border: 1px solid #c46200; }

.stProgress > div > div { background: linear-gradient(90deg, #c46200, #ff8c00) !important; }
.stSpinner > div { color: #ffb347 !important; }

.stAlert {
    background: rgba(40, 15, 0, 0.85) !important;
    border-left: 4px solid #ff8c00 !important;
    color: #ffcc88 !important;
}

hr { border-color: #c46200 !important; opacity: 0.4; }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #1a0a00; }
::-webkit-scrollbar-thumb { background: #c46200; border-radius: 4px; }

.hist-card {
    background: rgba(30,10,0,0.7);
    border: 1px solid rgba(196,98,0,0.4);
    border-radius: 10px;
    padding: 8px 12px;
    margin-bottom: 8px;
    cursor: pointer;
    transition: border 0.2s;
}
.hist-card:hover { border: 1px solid #ff8c00; }
.hist-time { font-size: 0.75rem; color: #c46200; letter-spacing: 1px; }
.hist-preview { font-size: 0.92rem; color: #ffcc88; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# USER ACCOUNTS
# ----------------------------
USERS = {
    "admin": "tiger123",
    "demo": "demo123",
}

HISTORY_FILE = "tigerai_history.json"

# ----------------------------
# SESSION STATE INIT
# ----------------------------
def init_state():
    defaults = {
        "logged_in": False,
        "username": "",
        "started": False,
        "messages": [],
        "liked": {},
        "muted": False,
        "all_sessions": [],
        "active_session_id": None,
        "login_error": "",
        "voice_transcript": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ----------------------------
# HISTORY PERSISTENCE
# ----------------------------
def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_history(username, sessions):
    data = load_history()
    data[username] = sessions
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass  # On read-only filesystems (some cloud envs), silently skip

def get_user_sessions(username):
    data = load_history()
    return data.get(username, [])

# ----------------------------
# TTS — gTTS (works on Streamlit Cloud, no system drivers needed)
# ----------------------------
def speak_tiger(text):
    """Generate audio with gTTS and play it in the browser."""
    if st.session_state.muted:
        return
    try:
        from gtts import gTTS
        import io
        tts = gTTS(text=text[:500], lang="en", slow=False)  # limit length
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        st.audio(audio_bytes, format="audio/mp3", autoplay=True)
    except Exception as e:
        st.caption(f"🔇 Voice unavailable: {e}")

# ----------------------------
# AI RESPONSE — Anthropic API
# Uses st.secrets["ANTHROPIC_API_KEY"] set in Streamlit Cloud secrets
# ----------------------------
def ask_ai(prompt):
    """
    Call Anthropic claude API.
    Set ANTHROPIC_API_KEY in your Streamlit Cloud secrets.
    Falls back to a stub message if key is missing.
    """
    api_key = st.secrets.get("ANTHROPIC_API_KEY", os.environ.get("ANTHROPIC_API_KEY", ""))
    if not api_key:
        return (
            "⚠️ No API key found. Please add ANTHROPIC_API_KEY to your Streamlit secrets. "
            "Go to your Streamlit Cloud dashboard → App settings → Secrets."
        )

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)

        # Build message history (last 20 turns to stay within context)
        history = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages[-20:]
            if m["role"] in ("user", "assistant")
        ]
        history.append({"role": "user", "content": prompt})

        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1024,
            system=(
                "You are TigerAI — a powerful, fierce, and intelligent AI assistant "
                "with the spirit of a tiger. Be helpful, concise, and confident. "
                "Add occasional tiger-themed flair to your responses."
            ),
            messages=history,
        )
        return response.content[0].text

    except Exception as e:
        return f"❌ AI Error: {str(e)}"

# ----------------------------
# VOICE INPUT — uses Streamlit's built-in audio_input (no PyAudio needed)
# ----------------------------
def render_voice_input():
    """
    Uses st.audio_input (Streamlit ≥1.31) — records from browser mic,
    then transcribes with OpenAI Whisper API or a fallback.
    """
    st.markdown(
        "<p style='font-family:Bebas Neue;font-size:1rem;letter-spacing:2px;color:#ffb347;'>🎤 VOICE INPUT</p>",
        unsafe_allow_html=True,
    )
    audio_value = st.audio_input("Click to record your message")

    if audio_value is not None:
        # Try to transcribe with OpenAI Whisper if key available
        openai_key = st.secrets.get("OPENAI_API_KEY", os.environ.get("OPENAI_API_KEY", ""))
        if openai_key:
            try:
                import openai
                client = openai.OpenAI(api_key=openai_key)
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=("audio.wav", audio_value, "audio/wav"),
                )
                return transcript.text
            except Exception as e:
                st.warning(f"Transcription failed: {e}. Type your message instead.")
                return None
        else:
            st.info(
                "🎤 Audio recorded! To enable auto-transcription, add OPENAI_API_KEY to secrets. "
                "For now, please type your message below."
            )
            return None
    return None

# ----------------------------
# RESPONSE ACTIONS
# ----------------------------
def render_response_actions(msg_index: int, content: str):
    liked = st.session_state.liked.get(msg_index, False)
    like_label = "❤️ Liked!" if liked else "🤍 Like"
    col_copy, col_like, _ = st.columns([1, 1, 6])
    with col_copy:
        st.code(content[:80] + "..." if len(content) > 80 else content, language=None)
    with col_like:
        if st.button(like_label, key=f"like_{msg_index}"):
            st.session_state.liked[msg_index] = not liked
            st.rerun()

# ----------------------------
# SAVE CURRENT SESSION
# ----------------------------
def save_current_session():
    if not st.session_state.messages:
        return
    sessions = get_user_sessions(st.session_state.username)
    session = {
        "id": st.session_state.active_session_id or datetime.now().strftime("%Y%m%d_%H%M%S"),
        "timestamp": datetime.now().strftime("%d %b %Y, %I:%M %p"),
        "preview": st.session_state.messages[0]["content"][:60] if st.session_state.messages else "Empty",
        "messages": st.session_state.messages,
    }
    found = False
    for i, s in enumerate(sessions):
        if s["id"] == session["id"]:
            sessions[i] = session
            found = True
            break
    if not found:
        sessions.insert(0, session)
    sessions = sessions[:20]
    save_history(st.session_state.username, sessions)
    st.session_state.active_session_id = session["id"]

# =============================================
# SCREEN 1: LOGIN
# =============================================
if not st.session_state.logged_in:
    st.markdown("""
    <div class='login-container'>
        <div class='login-title'>🐯 TIGER AI</div>
        <div class='login-subtitle'>SECURE INTELLIGENCE PORTAL</div>
    </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        st.markdown("### 🔐 LOGIN")
        username = st.text_input("Username", placeholder="Enter your username", key="login_user")
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_pass")

        if st.session_state.login_error:
            st.error(st.session_state.login_error)

        if st.button("🐯  LOGIN", use_container_width=True):
            if username in USERS and USERS[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.login_error = ""
                st.session_state.all_sessions = get_user_sessions(username)
                st.rerun()
            else:
                st.session_state.login_error = "❌ Invalid username or password."
                st.rerun()

        st.markdown("""
        <div style='margin-top:20px; padding:14px; background:rgba(196,98,0,0.12);
             border:1px solid rgba(196,98,0,0.35); border-radius:10px;
             font-family:Rajdhani; font-size:0.88rem; color:#c46200; text-align:center;'>
            Demo accounts:<br>
            <b style='color:#ffb347'>admin</b> / tiger123 &nbsp;|&nbsp;
            <b style='color:#ffb347'>demo</b> / demo123
        </div>
        """, unsafe_allow_html=True)

    st.stop()

# =============================================
# SCREEN 2: LOADING ANIMATION (once per login)
# =============================================
if not st.session_state.started:
    st.markdown("<h1>🐯 TIGER AI — INITIALIZING</h1>", unsafe_allow_html=True)
    st.markdown(
        f"<p style='text-align:center;color:#c46200;font-family:Rajdhani;letter-spacing:2px;'>"
        f"Welcome back, <b style='color:#ffb347'>{st.session_state.username.upper()}</b></p>",
        unsafe_allow_html=True,
    )

    progress = st.progress(0)
    status = st.empty()
    steps = [
        "🐾 Waking the tiger...",
        "🔥 Loading neural core...",
        "🎙️ Initializing voice engine...",
        "📡 Connecting to AI...",
        "🐯 TigerAI is ready to roar!",
    ]
    for i in range(101):
        time.sleep(0.02)
        progress.progress(i)
        step_idx = min(i // 20, len(steps) - 1)
        status.markdown(
            f"<p style='text-align:center;color:#ffb347;font-family:Rajdhani;font-size:1.1rem;"
            f"letter-spacing:2px;'>{steps[step_idx]}</p>",
            unsafe_allow_html=True,
        )

    st.session_state.started = True
    st.rerun()

# =============================================
# SCREEN 3: MAIN APP
# =============================================

# ----------------------------
# SIDEBAR
# ----------------------------
with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center; padding: 10px 0 4px;'>
        <span style='font-family:Bebas Neue; font-size:2rem; color:#ffb347; letter-spacing:4px;'>🐯 TIGER AI</span><br>
        <span class='badge badge-online'>● ONLINE</span>
        &nbsp;
        <span class='badge badge-session'>{st.session_state.username.upper()}</span>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    st.markdown(
        "<p style='font-family:Bebas Neue;font-size:1.1rem;letter-spacing:3px;color:#ffb347;'>🔊 VOICE SETTINGS</p>",
        unsafe_allow_html=True,
    )
    mute_label = "🔇 MUTED — Click to Unmute" if st.session_state.muted else "🔊 SOUND ON — Click to Mute"
    if st.button(mute_label, key="mute_toggle", use_container_width=True):
        st.session_state.muted = not st.session_state.muted
        st.rerun()

    st.divider()

    st.markdown(
        "<p style='font-family:Bebas Neue;font-size:1.1rem;letter-spacing:3px;color:#ffb347;'>💬 SESSIONS</p>",
        unsafe_allow_html=True,
    )
    if st.button("➕  NEW CHAT", use_container_width=True):
        save_current_session()
        st.session_state.messages = []
        st.session_state.liked = {}
        st.session_state.active_session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.session_state.all_sessions = get_user_sessions(st.session_state.username)
        st.rerun()

    sessions = get_user_sessions(st.session_state.username)
    if sessions:
        st.markdown(
            "<p style='font-size:0.85rem;color:#c46200;letter-spacing:1px;margin-top:10px;'>RECENT HISTORY</p>",
            unsafe_allow_html=True,
        )
        for s in sessions[:10]:
            is_active = s["id"] == st.session_state.active_session_id
            border_color = "#ff8c00" if is_active else "rgba(196,98,0,0.4)"
            st.markdown(f"""
            <div class='hist-card' style='border-color:{border_color}'>
                <div class='hist-time'>{s["timestamp"]}</div>
                <div class='hist-preview'>{s["preview"]}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Load", key=f"load_{s['id']}", use_container_width=True):
                save_current_session()
                st.session_state.messages = s["messages"]
                st.session_state.active_session_id = s["id"]
                st.session_state.liked = {}
                st.rerun()
    else:
        st.markdown("<p style='color:#c46200;font-size:0.85rem;'>No history yet.</p>", unsafe_allow_html=True)

    st.divider()

    if st.button("🗑️  CLEAR HISTORY", use_container_width=True):
        save_history(st.session_state.username, [])
        st.session_state.all_sessions = []
        st.toast("History cleared!", icon="🗑️")
        st.rerun()

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    if st.button("🚪  LOGOUT", use_container_width=True):
        save_current_session()
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# ----------------------------
# MAIN HEADER
# ----------------------------
try:
    st.image("tiger.png", width=480)
except Exception:
    st.markdown("<h1>🐯</h1>", unsafe_allow_html=True)

st.markdown("""
<h1>🐯 TIGER AI</h1>
<p style='text-align:center;color:white;font-family:Rajdhani;letter-spacing:3px;font-size:0.95rem;margin-top:-10px;'>
POWERED BY SYED TABISH ASKARI RAZA &nbsp;|&nbsp; PRESENTED BY SYED TABISH ASKARI RAZA
</p>
""", unsafe_allow_html=True)

mute_status = "🔇 Voice Muted" if st.session_state.muted else "🔊 Voice Active"
mute_bg = "#2a2a2a" if st.session_state.muted else "#3a1a00"
mute_col = "#888" if st.session_state.muted else "#ffb347"
st.markdown(f"""
<div style='text-align:center;margin-bottom:12px;'>
    <span style='background:{mute_bg};color:{mute_col};border:1px solid {mute_col};
    border-radius:20px;padding:4px 18px;font-family:Rajdhani;font-size:0.88rem;letter-spacing:2px;'>
    {mute_status}
    </span>
</div>
""", unsafe_allow_html=True)

st.divider()

# ----------------------------
# CHAT HISTORY DISPLAY
# ----------------------------
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant":
            render_response_actions(i, msg["content"])

# ----------------------------
# VOICE INPUT (browser-based, no PyAudio)
# ----------------------------
with st.expander("🎤 Voice Input (click to expand)", expanded=False):
    voice_transcript = render_voice_input()
    if voice_transcript:
        st.session_state.voice_transcript = voice_transcript
        st.success(f"🎤 Transcribed: {voice_transcript}")

# ----------------------------
# TEXT INPUT
# ----------------------------
text_input = st.chat_input("Type your message to TigerAI...")

# Use voice transcript if available
if st.session_state.get("voice_transcript") and not text_input:
    text_input = st.session_state.voice_transcript
    st.session_state.voice_transcript = None

# ----------------------------
# RESPONSE FLOW
# ----------------------------
if text_input:
    st.session_state.messages.append({"role": "user", "content": text_input})
    with st.chat_message("user"):
        st.write(text_input)

    with st.spinner("🐯 TigerAI is growling a response..."):
        response = ask_ai(text_input)

    msg_index = len(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.write(response)
        render_response_actions(msg_index, response)

    save_current_session()
    speak_tiger(response)
    st.rerun()