from agent_nodes import llm  
from booking_agent import BookingState
from schemas import TrainDetailsExtractor
from booking_tools import check_train_availability, book_train_ticket
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode,tools_condition
from assistant_nodes import assistant_node
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver

workflow = StateGraph(BookingState)

workflow.add_node("assistant", assistant_node)

workflow.add_node("tools",ToolNode([check_train_availability, book_train_ticket]))

workflow.add_edge(START,"assistant")

workflow.add_conditional_edges(
    "assistant",
    tools_condition,
)
workflow.add_edge("tools", "assistant")
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

