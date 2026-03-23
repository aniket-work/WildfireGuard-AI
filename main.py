import sys
import os
import time
from langgraph.graph import StateGraph, END
from .state import AgentState
from .environment import WildfireWorld
from .agents import sensor_node, analyzer_node, strategist_node, operator_node

def build_graph():
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("sensor_ingest", sensor_node)
    workflow.add_node("threat_analyzer", analyzer_node)
    workflow.add_node("strategy_optimizer", strategist_node)
    workflow.add_node("dispatcher", operator_node)
    
    # Define edges
    workflow.set_entry_point("sensor_ingest")
    workflow.add_edge("sensor_ingest", "threat_analyzer")
    workflow.add_edge("threat_analyzer", "strategy_optimizer")
    workflow.add_edge("strategy_optimizer", "dispatcher")
    workflow.add_edge("dispatcher", END)
    
    return workflow.compile()

def run_simulation(steps=20):
    env = WildfireWorld(width=20, height=20, fire_start=(10, 10))
    app = build_graph()
    
    state = {
        "heat_map": env.grid,
        "active_plan": [],
        "assets": {"tanker_1": {"status": "idle"}},
        "logs": ["System: WildfireGuard-AI initialized."],
        "criticality": 0.0,
        "step": 0,
        "replan_required": False
    }

    print("\n" + "="*50)
    print("  WILDFIREGUARD-AI: AUTONOMOUS COORDINATOR")
    print("="*50 + "\n")

    for i in range(steps):
        # 1. Environment Step (Stochastic Spread)
        env_update = env.step()
        
        # 2. Agent Workflow Step
        # Feed current map to agent
        state["heat_map"] = env.grid
        state["latest_update"] = env_update
        
        # Execute Graph
        result = app.invoke(state)
        state.update(result)
        
        # 3. Apply Agent Action to Environment
        if "latest_action" in result:
            action = result["latest_action"]
            env.apply_action(action["pos"], action["type"])
            print(f"[*] ACTION: {action['type']} at {action['pos']}")
            
        # 4. Reporting (Logging)
        for log in result.get("logs", []):
            if "CRITICAL" in log:
                print(f"\033[91m{log}\033[0m") # Red for critical
            else:
                print(log)
        
        # ASCII Visualization (Mini)
        fire_count = sum(1 for v in env.grid.values() if v == 'fire')
        print(f"Status: Step {i} | Fire Cells: {fire_count} | Criticality: {state['criticality']:.2f}")
        time.sleep(0.5)

    print("\nSimulation Complete.")
    print(f"Final Fire Status: {fire_count} active cells.")

if __name__ == "__main__":
    run_simulation(steps=15)
