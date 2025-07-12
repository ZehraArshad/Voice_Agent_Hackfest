import streamlit as st
import time
import main  # Import the conversation_log from your voice agent

st.set_page_config(page_title="Voice Agent", page_icon="🎙️")

st.title("🎙️ Voice Agent Console")
st.caption("Displays voice input and agent response in real time.")

# Start the voice agent in a background thread if not already running
if "started" not in st.session_state:
    import threading
    t = threading.Thread(target=main.run_voice_agent, daemon=True)
    t.start()
    st.session_state.started = True

# Chat display
placeholder = st.empty()

while True:
    with placeholder.container():
        for role, text in main.conversation_log[-10:]:  # Show last 10 messages
            st.markdown(f"**{role}** {text}")
    time.sleep(1.5)
