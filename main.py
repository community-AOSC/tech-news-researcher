import os
from graph import create_agentic_workflow

def main():
    # کامپایل ساختار گراف مأمورین
    app = create_agentic_workflow()
    
    # شبیه‌سازی ترسیم معماری برای نمایش در ردیت/گیت‌هاب
    try:
        png_data = app.get_graph().draw_mermaid_png()
        # فایل عکس رو دقیقاً کنار خود اسکریپت‌ها ذخیره می‌کنه
        with open("graph_architecture.png", "wb") as f:
            f.write(png_data)
        print("[System] Architecture diagram rendered and saved as 'graph_architecture.png'.")
    except Exception as e:
        print("[System] Visualizer node rendering skipped:", e)

    # کانفیگ و ورودی‌های اولیه گراف
    initial_input = {
        "topic": "Stateful Multi-Agent Orchestration",
        "research_notes": "",
        "final_article": "",
        "review_feedback": "",
        "revision_count": 0
    }
    
    config = {"configurable": {"thread_id": "reddit_showcase_session"}}
    
    print("\n--- 🚀 Initiating LangGraph Orchestrator ---")
    final_state = app.invoke(initial_input, config=config)
    print("--- 🏁 Execution Sequence Ended ---\n")
    
    print("================ FINAL APPROVED ARTICLE ================")
    print(final_state["final_article"])
    print("========================================================")

if __name__ == "__main__":
    main()