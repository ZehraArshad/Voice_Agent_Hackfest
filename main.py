# main.py

from speech import start_stream
from agent import agent
from langchain_core.messages import HumanMessage

def handle_transcript(transcript: str):
    print(f"\n🗣️ You said: {transcript}")
    result = agent.invoke({"messages": [HumanMessage(content=transcript)]})
    response = result["messages"][-1].content
    print(f"🤖 Agent: {response}")
    # (Optional) send response to TTS

if __name__ == "__main__":
    print("🔊 Voice agent started. Speak your command...")
    start_stream(on_transcript_callback=handle_transcript)
