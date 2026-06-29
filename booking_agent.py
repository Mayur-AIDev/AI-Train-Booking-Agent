from typing import TypedDict, Optional, Annotated
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

class BookingState(TypedDict):
    
    messages: Annotated[list[AnyMessage], add_messages] 
    
    # Context variables extracted by your LLM router
    extracted_source: Optional[str]
    extracted_destination: Optional[str]
    extracted_date: Optional[str]
    extracted_seats: Optional[int]
    extracted_train_no: Optional[str]
    


