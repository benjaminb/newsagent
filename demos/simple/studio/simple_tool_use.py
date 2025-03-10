
from langchain_ollama import ChatOllama
from langgraph.graph import MessagesState, StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.prebuilt import ToolNode, tools_condition

from random import randint
def roll(n: int) -> int:
    """
    Roll a `n` sided die
    
    Args:
        n: The number of sides on the die
    """
    return randint(1, n)

def multiply(a: int, b: int) -> int:
    """Multiply `a` and `b`

    Args:
        a: First number
        b: Second number
    """
    return a * b

tools_in_use = [multiply, roll]
llm = ChatOllama(
    model='mistral:instruct', 
    temperature=0,
    base_url="http://host.docker.internal:11434").bind_tools(tools_in_use)


"""
This is a 'node' function, it takes a state and returns a new state

The built-in `MessagesState` is equivalent to:
class MessagesState(TypedDict):
    messages: Annotated[list[Message], add_message]

Basically, the 'state' is the list of messages written so far between system, human, and AI.
However, LangGraph's default behavior is to overwrite the state with any node function's return value.
Since we want to add messages rather than overwrite them to preserve chat history, we use the `add_message` function.
This simply appends the message to the list and generates some metadata for it.
"""
def tool_calling_llm(state: MessagesState):
    return {"messages": [llm.invoke(state["messages"])]}

builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_node("tools", ToolNode(tools_in_use))
builder.add_edge(START, "tool_calling_llm")

"""
The prebuilt `tools_condition` ONLY returns either "tools" or "__end__" (aliased to END)
Therefore either this node routes to "tools" or ends the invocation, and your ToolNode
MUST be called "tools". 
"""
builder.add_conditional_edges("tool_calling_llm", tools_condition)
builder.add_edge("tools", END)
graph = builder.compile()




