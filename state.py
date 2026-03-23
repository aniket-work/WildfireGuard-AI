from typing import List, Tuple, Dict, Annotated, TypedDict
from pydantic import BaseModel, Field
import operator

Coord = Tuple[int, int]

class AgentState(TypedDict):
    # The current map knowledge (may be incomplete)
    heat_map: Dict[Coord, str]
    # Current active plan (coordinates to target)
    active_plan: List[Coord]
    # Available assets and their status
    assets: Dict[str, Dict]
    # History of events
    logs: Annotated[List[str], operator.add]
    # Criticality score (0.0 to 1.0)
    criticality: float
    # Current step count
    step: int
    # Flag to trigger replanning
    replan_required: bool
    # Latest sensor update
    latest_update: Dict
