import random
from typing import Dict, List, Tuple
from .state import AgentState

def sensor_node(state: AgentState) -> Dict:
    """Simulates receiving streaming sensor data."""
    # In a real scenario, this would poll an API or hook into a stream
    step = state.get("step", 0)
    # Simulate some new fire detections or wind shifts
    new_logs = [f"Step {step}: Receiving satellite thermal telemetry..."]
    
    # We pass the 'latest_update' which would come from the environment in main.py
    return {"logs": new_logs, "step": step + 1}

def analyzer_node(state: AgentState) -> Dict:
    """Analyzes the current heat map to detect critical shifts."""
    heat_map = state.get("heat_map", {})
    active_plan = state.get("active_plan", [])
    
    # Simple logic: if fire is detected at a coordinate NOT in our plan, or if fire count > threshold
    fire_count = sum(1 for v in heat_map.values() if v == "fire")
    
    replan = False
    criticality = min(1.0, fire_count / 100.0)
    
    # If fire is near a 'protected zone' (simulated) or just spreading fast
    if fire_count > 10 and not active_plan:
        replan = True
    elif fire_count > len(active_plan) * 1.5:
        replan = True
        
    msg = "Analyzer: " + ("CRITICAL shift detected. Initiating replan." if replan else "Situation stable.")
    return {"replan_required": replan, "criticality": criticality, "logs": [msg]}

def strategist_node(state: AgentState) -> Dict:
    """Generates a new containment strategy."""
    if not state.get("replan_required", False) and state.get("active_plan"):
        return {} # Keep current plan
        
    heat_map = state.get("heat_map", {})
    fire_cells = [k for k, v in heat_map.items() if v == "fire"]
    
    if not fire_cells:
        return {"active_plan": [], "replan_required": False, "logs": ["Strategist: No active fire. Standing down."]}
    
    # Simple Strategy: Target the 'perimeter' of the fire
    # In a real system, this would be a complex A* or PDE solver
    new_plan = sorted(fire_cells, key=lambda x: random.random())[:5]
    
    return {
        "active_plan": new_plan, 
        "replan_required": False, 
        "logs": [f"Strategist: New plan generated. Targeting {len(new_plan)} hotspots."]
    }

def operator_node(state: AgentState) -> Dict:
    """Executes actions based on the current plan."""
    plan = state.get("active_plan", [])
    if not plan:
        return {"logs": ["Operator: No active targets. Monitoring..."]}
        
    # Execute one action from the plan
    target = plan[0]
    # We return the action to be applied to the environment in the main loop
    msg = f"Operator: Aerial tanker dispatched to {target}."
    
    # Remove the target from plan once 'action' is issued
    remaining_plan = plan[1:]
    
    return {
        "active_plan": remaining_plan, 
        "logs": [msg],
        "latest_action": {"pos": target, "type": "water_drop"}
    }
