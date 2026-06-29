import os
from fastapi import FastAPI, HTTPException
from graph import app as graph_app
from langchain_core.messages import HumanMessage
from pydantic import BaseModel
from typing import Optional,List

app =FastAPI(title="Ai Train Booking Agent API",version="1.0")

class ChatRequest(BaseModel):
    message: str
    thread_id: str  

class ChatResponse(BaseModel):
    agent_response: str
    slots: dict

@app.post("/chat", response_model=ChatResponse)
async def chat_with_agent(payload: ChatRequest):
    try:
        config = {"configurable": {"thread_id": payload.thread_id}}
        input_state = {"messages": [HumanMessage(content=payload.message)]}
        final_state = None
        async for event in graph_app.astream(input_state, config, stream_mode="values"):
            final_state = event
        if not final_state or "messages" not in final_state:
            raise HTTPException(status_code=500, detail="Graph failed to compute a valid response state.")


        last_message = final_state["messages"][-1]

        current_slots = {
            "source": final_state.get("extracted_source"),
            "destination": final_state.get("extracted_destination"),
            "date": final_state.get("extracted_date"),
            "seats": final_state.get("extracted_seats"),
            "train_no": final_state.get("extracted_train_no")
        }
        
        return ChatResponse(
            agent_response=last_message.content,
            slots=current_slots
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
