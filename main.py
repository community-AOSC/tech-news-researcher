import os
from graph import create_agentic_workflow

def main():
    # Compile the multi-agent graph structure
    app = create_agentic_workflow()
    
    # Render and export graph architecture diagram for Reddit/GitHub showcase
    try:
        png_data = app.get_graph().draw_mermaid_png()
        # Saves the generated png image right next to the execution scripts
        with open("graph_architecture.png", "wb") as f:
            f.write(png_data)
        print("[System] Architecture diagram rendered and saved as 'graph_architecture.png'.")
    except Exception as e:
        print("[System] Visualizer node rendering skipped:", e)

    # Configure state initialization and graph input parameters
    initial_input = {
        "topic": "Stateful Multi-Agent Orchestration",
        "research_notes": "",
        "final_article": "",
        "review_feedback": "",
        "revision_count": 0
    }
    
    # Define execution context with a persistent thread ID for memory tracking
    config = {"configurable": {"thread_id": "reddit_showcase_session"}}
    
    print("\n--- 🚀 Initiating LangGraph Orchestrator ---")
    final_state = app.invoke(initial_input, config=config)
    print("--- 🏁 Execution Sequence Ended ---\n")
    
    # Output the finalized and fully audited article asset
    print("================ FINAL APPROVED ARTICLE ================")
    print(final_state["final_article"])
    print("========================================================")

if __name__ == "__main__":
    main()