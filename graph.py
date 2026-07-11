from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

# تعریف ساختار وضعیت مرکزی (Agent State)
class AgentState(TypedDict):
    topic: str
    research_notes: str
    final_article: str
    review_feedback: str
    revision_count: int

# مأمور تحقیق
def research_agent(state: AgentState) -> dict:
    print(f"\n[Research Agent] 🔍 Collecting data for: '{state['topic']}'...")
    simulated_data = (
        f"--- Research Intelligence Core ---\n"
        f"- Trend: Massive adoption of stateful local AI architectures in 2026.\n"
        f"- Challenge: High synchronization complexity across edge devices.\n"
    )
    return {"research_notes": simulated_data}

# مأمور نویسنده
def writer_agent(state: AgentState) -> dict:
    current_revisions = state.get("revision_count", 0) + 1
    print(f"[Writer Agent] ✍️ Drafting article (Revision {current_revisions})...")
    
    notes = state.get("research_notes", "No research found.")
    feedback = state.get("review_feedback", "")
    
    if feedback and feedback != "APPROVED":
        article_body = (
            f"# Advanced Insights: {state['topic']}\n\n"
            f"**[Revised via Quality Feedback: {feedback}]**\n"
            f"Implementing enterprise-grade encryption protocols within the LangGraph checkpointer layer "
            f"fully addresses the synchronization challenges.\n\n"
            f"**Core Intelligence Gathered:**\n{notes}"
        )
    else:
        article_body = (
            f"# Advanced Insights: {state['topic']}\n\n"
            f"Stateful Multi-Agent environments are taking over production setups.\n\n"
            f"**Data Telemetry:**\n{notes}"
        )
        
    return {"final_article": article_body, "revision_count": current_revisions}

# مأمور ارزیاب کیفیت
def reviewer_agent(state: AgentState) -> dict:
    print("[Reviewer Agent] 🛡️ Analyzing generated artifact quality...")
    article = state.get("final_article", "")
    
    if "encryption" not in article.lower():
        print("[Reviewer Agent] ❌ Critique: Missing security protocols.")
        return {"review_feedback": "The article focuses too much on trends; please provide explicit encryption details."}
    
    print("[Reviewer Agent] ✅ Quality checks passed!")
    return {"review_feedback": "APPROVED"}

# روتر مدیریت چرخه و جلوگیری از لوپ بی‌نهایت
def router_logic(state: AgentState) -> Literal["writer", "__end__"]:
    if state.get("review_feedback") == "APPROVED":
        return END
    if state.get("revision_count", 0) >= 3:
        print("[Router] ⚠️ Max revisions hit. Breaking loop to secure token budget.")
        return END
    return "writer"

# تابع اصلی برای اسمبل و کامپایل کردن گراف
def create_agentic_workflow():
    workflow = StateGraph(AgentState)
    
    # افزودن گره‌ها
    workflow.add_node("researcher", research_agent)
    workflow.add_node("writer", writer_agent)
    workflow.add_node("reviewer", reviewer_agent)
    
    # تنظیم مسیرها
    workflow.add_edge(START, "researcher")
    workflow.add_edge("researcher", "writer")
    workflow.add_edge("writer", "reviewer")
    
    # افزودن منطق شرطی بازخورد
    workflow.add_conditional_edges("reviewer", router_logic)
    
    # فعال‌سازی لایه حافظه زنده لنگ‌گراف
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)