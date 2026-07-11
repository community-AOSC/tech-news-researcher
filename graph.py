from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
#Any type of API
from langchain_groq import ChatGroq 
import os

# Initialize the ultra-fast, cloud-based Groq LLM
#Any type of API
model = ChatGroq(
    model="llama3-8b-8192", 
    api_key="your_api_key_here"
)

# Centralized State definition for data mutation across agents
class AgentState(TypedDict):
    topic: str
    research_notes: str
    final_article: str
    review_feedback: str
    revision_count: int

# Researcher Agent: Simulates data gathering without heavy local computation
def research_agent(state: AgentState) -> dict:
    print(f"\n[Research Agent] 🔍 Collecting data for: '{state['topic']}'...")
    simulated_data = (
        f"--- Research Intelligence Core ---\n"
        f"- Trend: Massive adoption of stateful local AI architectures in 2026.\n"
        f"- Challenge: High synchronization complexity across edge devices.\n"
    )
    return {"research_notes": simulated_data}

# Writer Agent: Communicates with cloud LLM to generate/refine articles
def writer_agent(state: AgentState) -> dict:
    current_revisions = state.get("revision_count", 0) + 1
    print(f"[Writer Agent] ✍️ Drafting article via Groq Cloud (Revision {current_revisions})...")
    
    notes = state.get("research_notes", "No research found.")
    feedback = state.get("review_feedback", "")
    
    # Constructing dynamic prompt based on whether it is a first draft or a revision
    prompt = (
        f"You are an expert tech journalist. Write a short, engaging article about: {state['topic']}.\n"
        f"Use these core research notes to guide the content:\n{notes}\n\n"
    )
    
    if feedback and feedback != "APPROVED":
        # Pass critique directly back to the LLM for self-correction
        prompt += f"CRITICAL FIX REQUIRED FROM REVIEWER: {feedback}\nUpdate the article immediately to address this."
    else:
        prompt += "Write the first draft now."

    # Cloud execution protects local low-spec system hardware from freezing
    response = model.invoke(prompt)
    
    return {"final_article": response.content, "revision_count": current_revisions}

# Reviewer Agent: Evaluates artifact quality and enforces safety constraints
def reviewer_agent(state: AgentState) -> dict:
    print("[Reviewer Agent] 🛡️ Analyzing generated artifact quality...")
    article = state.get("final_article", "")
    
    # Check if the generated content satisfies the security token requirements
    if "encryption" not in article.lower() and "security" not in article.lower():
        print("[Reviewer Agent] ❌ Critique: Missing security protocols.")
        return {"review_feedback": "The article is good but lacks depth on cybersecurity. Please mention enterprise-grade encryption or network security."}
    
    print("[Reviewer Agent] ✅ Quality checks passed!")
    return {"review_feedback": "APPROVED"}

# Router Logic: Manages state transitions and acts as a token budget circuit-breaker
def router_logic(state: AgentState) -> Literal["writer", "__end__"]:
    if state.get("review_feedback") == "APPROVED":
        return END
    if state.get("revision_count", 0) >= 3:
        print("[Router] ⚠️ Max revisions hit. Breaking loop to secure token budget.")
        return END
    return "writer"

# Main pipeline compilation
def create_agentic_workflow():
    workflow = StateGraph(AgentState)
    
    # Register graph nodes
    workflow.add_node("researcher", research_agent)
    workflow.add_node("writer", writer_agent)
    workflow.add_node("reviewer", reviewer_agent)
    
    # Establish standard deterministic edges
    workflow.add_edge(START, "researcher")
    workflow.add_edge("researcher", "writer")
    workflow.add_edge("writer", "reviewer")
    
    # Inject conditional edge loop (critique loop mechanism)
    workflow.add_conditional_edges("reviewer", router_logic)
    
    # Enable persistence layer using MemorySaver for state checkpointing
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)