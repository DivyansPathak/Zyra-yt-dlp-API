from ddgs import DDGS
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, BaseMessage
from typing import TypedDict, Annotated, Sequence
import operator
from dotenv import load_dotenv

load_dotenv()

# define the state to manage a list of messages
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

# tools
@tool
def web_search(query: str) -> str:
    """This is a web search tool to get responses from the web for a query.
    Return the findings as a string.

    Args:
        query (str): The search query.

    Returns:
        str: A string containing the search results.
    """
    results = DDGS().text(query, max_results=5)
    return str(results)

tools = [web_search]

# model
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
llm_with_tools = llm.bind_tools(tools)

# nodes functions
def llm_node(state: AgentState):
    """Invokes the LLM with the current state's messages."""
    response = llm_with_tools.invoke(state['messages'])
    return {"messages": [response]}

tool_node = ToolNode(tools)

# graph node and edges
graph = StateGraph(AgentState)

graph.add_node("llm_node", llm_node)
graph.add_node("tools", tool_node)

graph.add_edge(START, "llm_node")
graph.add_conditional_edges(
    "llm_node",
    tools_condition,
    {
        "tools": "tools",
        END: END
    }
)
graph.add_edge("tools", "llm_node")

recommender_model = graph.compile()

def recommender_function(song: str) -> list:
    """Generate song recommendations related to song.

    Args:
        song (str): song, related to which recommendations are required.

    Returns:
        list: list of recommended songs.
    """
    song_title = song
    initial_prompt = f"""
    You are a music recommendation assistant. You also have access to a web search tool which you can use by sending a query.
    I will give you the title of a song. Based on that song, recommend exactly 10 other songs with the following mix:
    - At least 2 songs by the same artist (if available).
    - At least 2 songs from the same movie/album (if applicable).
    - At least 2 songs of the same genre.
    - At least 2 songs in the same language.
    - The rest can be popular similar songs from any of the above categories.

    Your final output should be ONLY the list of 10 song titles. Do not add any other text. do not add song number.

    Give recommendations for the song: {song_title}
    """

    inputs = {"messages": [HumanMessage(content=initial_prompt)]}

    
    try:
        final_state = recommender_model.invoke(inputs)
        recommendations = final_state['messages'][-1].content
        recommendations_list = recommendations.split("\n")

    except Exception as e:
        print("Error in getting recommendations")
        recommendations_list = []
    
    return recommendations_list
