
from typing import TypedDict, Literal

class State(TypedDict):
    internal_state: str

from langgraph.graph import StateGraph, START, END

def node_1(state: State):
    print("===at node 1===")
    return {'internal_state': state['internal_state'] + ' and we should query '}

def node_2(state: State):
    print("===at node 2===")
    return {'internal_state': state['internal_state'] + 'Wikipedia'}

def node_3(state: State):
    print("===at node 3===")
    return {'internal_state': state['internal_state'] + 'Google'}

from random import random
def router(state: State) -> Literal["node_2", "node_3"]:
    print("===router===")
    return "node_2" if random() > 0.5 else "node_3"
    

builder = StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

# START and END are just constants for the literals "__start__" and "__end__"
# But LangGraph uses these for start and end nodes in the graph
builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", router)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)
graph = builder.compile()





