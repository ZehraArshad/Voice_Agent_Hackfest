from speech import start_stream
from agent import agent
from langchain_core.messages import HumanMessage
from speech_utils import speak 
conversation_log = []
last_transcript = None  # Global memory of last transcript

def handle_transcript(transcript: str):
    global last_transcript
    transcript = transcript.strip()

    if not transcript or transcript == last_transcript:
        return  # Ignore duplicates or empty
    last_transcript = transcript  # Update memory

    print(f"\n🗣️ You said: {transcript}")
    result = agent.invoke({"messages": [HumanMessage(content=transcript)]})
    response = result["messages"][-1].content
    print(f"🤖 Agent: {response}")
    # speak(response)
    conversation_log.append(("🗣️ You said:", transcript))
    conversation_log.append(("🤖 Agent:", response))

def run_voice_agent():
    
    print("🔊 Voice agent started. Speak your command...")
    start_stream(on_transcript_callback=handle_transcript)
