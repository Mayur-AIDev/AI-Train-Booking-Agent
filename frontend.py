import streamlit as st
import requests
import uuid

# 1. Page Configuration Setup
st.set_page_config(page_title="AI Rail Passenger Agent", layout="wide", page_icon="🎫")
st.title("🚂 AI Train Booking Companion")
st.caption("Powered by LangGraph, Hugging Face Llama-3.1, and FastAPI")

# 2. Maintain Persistent User Chat Session State across re-renders
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())  # Creates a unique random thread session key
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Internal storage list of tuples [("user", text), ("agent", text)]
if "current_slots" not in st.session_state:
    st.session_state.current_slots = {"source": "None", "destination": "None", "date": "None", "seats": "None", "train_no": "None"}

# FastAPI backend endpoint URL configuration 
BACKEND_URL = "http://127.0.0.1:8000/chat"

# 3. Create Web Page UI Layout Grid columns
chat_col, sidebar_col = st.columns([2, 1])

# Layout Column 1: Active Chat View Layer
with chat_col:
    st.subheader("Conversation")
    
    # Render all message history logs on screen
    for role, text in st.session_state.chat_history:
        with st.chat_message(role):
            st.write(text)
            
    # Capture user typing input string text box
    user_input = st.chat_input("Ask about train availability or request a booking...")
    
    if user_input:
        # Display user input in UI immediately
        with st.chat_message("user"):
            st.write(user_input)
        st.session_state.chat_history.append(("user", user_input))
        
        # Fire HTTP request payload payload structure to our active FastAPI backend server
        payload = {"message": user_input, "thread_id": st.session_state.thread_id}
        
        with st.spinner("Agent is thinking and accessing backend JSON records..."):
            try:
                res = requests.post(BACKEND_URL, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    agent_reply = data["agent_response"]
                    
                    # Store agent reply and state parameters checklist data
                    with st.chat_message("assistant"):
                        st.write(agent_reply)
                    st.session_state.chat_history.append(("assistant", agent_reply))
                    st.session_state.current_slots = data["slots"]
                    
                    # Refresh the web screen view state instantly
                    st.rerun()
                else:
                    st.error(f"Backend Server Error: {res.json().get('detail')}")
            except Exception as conn_error:
                st.error(f"Failed connecting to FastAPI backend instance: {str(conn_error)}")

# Layout Column 2: Live Tracking Diagnostics Sidebar Layer
with sidebar_col:
    st.subheader("🎯 Active Agent Caching Slots")
    st.info(f"**Session Thread ID:**\n`{st.session_state.thread_id}`")
    
    # Render a clear visualization tracking status indicators dashboard box
    slots = st.session_state.current_slots
    st.metric(label="Departure City (Source)", value=str(slots.get("source") or "Empty"))
    st.metric(label="Arrival City (Destination)", value=str(slots.get("destination") or "Empty"))
    st.metric(label="Travel Date", value=str(slots.get("date") or "Empty"))
    st.metric(label="Requested Seats Number", value=str(slots.get("seats") or "Empty"))
    st.metric(label="Selected Train Number", value=str(slots.get("train_no") or "Empty"))
