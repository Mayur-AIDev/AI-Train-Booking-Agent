
from agent_nodes import llm  
from langchain_core.utils.function_calling import convert_to_openai_tool
from booking_agent import BookingState
from schemas import TrainDetailsExtractor
from booking_tools import check_train_availability, book_train_ticket


def assistant_node(state: BookingState):
    """Analyzes conversation and triggers tool calls using a Hugging Face backbone."""
    messages = state["messages"]
    

    hf_tools = [check_train_availability, book_train_ticket, TrainDetailsExtractor]
    llm_with_tools = llm.bind_tools(hf_tools)
    
   
    response = llm_with_tools.invoke(messages)
    
    
    state_updates = {"messages": [response]}
    
    
    if response.tool_calls:
        for tool_call in response.tool_calls:
            args = tool_call["args"]
            
            # If the model uses our structural extraction schema, cache the variables
            if tool_call["name"] == "TrainDetailsExtractor":
                if "source" in args: state_updates["extracted_source"] = args["source"]
                if "destination" in args: state_updates["extracted_destination"] = args["destination"]
                if "travel_date" in args: state_updates["extracted_date"] = args["travel_date"]
                if "seats" in args: state_updates["extracted_seats"] = args["seats"]
                if "train_no" in args: state_updates["extracted_train_no"] = args["train_no"]
                
    return state_updates
