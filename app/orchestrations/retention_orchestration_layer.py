from typing import Dict, TypedDict, Any
from langgraph.graph import StateGraph, END
from app.orchestrations.retention_node import ml_node, llm_node, context_node, risk_node, validation_node
from app.schema.retention import RetentionState

graph = StateGraph(RetentionState)

graph.add_node("ml", ml_node)
graph.add_node("risk", risk_node)
graph.add_node("context", context_node)
graph.add_node("llm", llm_node)
graph.add_node("validation", validation_node)

graph.set_entry_point("ml")

graph.add_edge("ml", "risk")

def route_risk(state: RetentionState):
    """Route low-risk customers to workflow completion and high-risk customers to retention processing."""
    return END if state["risk"] == "low" else "context"

graph.add_conditional_edges(
    "risk",
    route_risk,
    {
        END: END,
        "context": "context"
    }
)

graph.add_edge("context", "llm")
graph.add_edge("llm", "validation")
graph.add_edge("validation", END)
retention_graph = graph.compile()