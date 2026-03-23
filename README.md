# 🌲 WildfireGuard-AI: Autonomous Wildfire Response Coordinator

### *Intelligent Real-time Response Orchestration with Streaming Decision Agents & Online Replanning*

![Title Animation](https://raw.githubusercontent.com/aniket-work/WildfireGuard-AI/main/images/title-animation.gif)

## 📌 Overview

**WildfireGuard-AI** is an experimental Proof-of-Concept (PoC) demonstrating how autonomous agentic workflows can manage high-stakes, rapidly shifting environments. Built on **LangGraph**, it implements a "Streaming Decision" architecture where real-time sensor data triggers dynamic "Online Replanning" to optimize fire containment strategies.

In a wildfire scenario, conditions (wind, fire spread, fuel) change by the second. A static plan is a failed plan. **WildfireGuard-AI** treats strategy as a living process, constantly evaluating sensor streams and re-routing assets (Aerial Tankers, Ground Crews) the moment a containment breach is detected.

## 🏗️ Architecture

The system is designed as a multi-agent state machine where state is shared and updated through a unified graph:

![Architecture](https://raw.githubusercontent.com/aniket-work/WildfireGuard-AI/main/images/architecture_diagram.png)

### Key Components:
1.  **Sensor Ingest Node**: Processes high-frequency telemetry (thermal, wind, humidity).
2.  **Threat Analyzer Agent**: Uses heuristic "Shift Detection" to identify if the current perimeter is failing.
3.  **Strategy Optimizer Agent**: Performs **Online Replanning** to generate a new containment boundary.
4.  **Dispatcher Agent**: Manages asset queues and executes tactical deployments.

## 🔄 Sequence Flow

The interaction between the environment simulation and the agentic core follows a strictly cyclical feedback loop:

![Sequence](https://raw.githubusercontent.com/aniket-work/WildfireGuard-AI/main/images/sequence_diagram.png)

## 🚀 Key Features

-   **Streaming State Management**: Uses LangGraph to handle asynchronous updates and state persistence.
-   **Dynamic Replanning**: Triggered automatically when the `Analyzer` detects a "Critical Shift".
-   **Resource Optimization**: Dynamic allocation of limited assets to high-impact hotspots.
-   **Stochastic Environment**: A built-in forest fire simulation with wind bias and random spread.

## 🛠️ Tech Stack

-   **Core**: Python 3.10+
-   **Agent Framework**: [LangGraph](https://github.com/langchain-ai/langgraph)
-   **State Validation**: Pydantic
-   **Simulation**: Custom Grid-World logic
-   **Visuals**: Mermaid.js, PIL

## 🏁 Getting Started

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/aniket-work/WildfireGuard-AI.git
    cd WildfireGuard-AI
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the simulation**:
    ```bash
    python -m main
    ```

## 📊 Logic Flow

The following flowchart illustrates the internal decision-making process for triggering a replan:

![Flow](https://raw.githubusercontent.com/aniket-work/WildfireGuard-AI/main/images/flow_diagram.png)

---

### ⚖️ Disclaimer

*This project is an experimental PoC and is NOT intended for real-world fire management or life-safety applications. It is a technical demonstration of agentic workflows and streaming decision architectures.*
