# 🚑 Dynamic Emergency Resource Allocation via Deep Reinforcement Learning

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-ee4c2c.svg)](https://pytorch.org/)
[![Stable-Baselines3](https://img.shields.io/badge/Stable--Baselines3-DQN-brightgreen.svg)](https://stable-baselines3.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A data-driven Deep Reinforcement Learning framework for urban Emergency Medical Services (EMS) dispatching and dynamic hospital resource balancing, evaluated on **274,964 real-world emergency call incidents** across New York City.

---

## 📌 Executive Summary

Urban emergency dispatch systems traditionally rely on myopic heuristics—such as sending patients strictly to the nearest facility. In high-density metropolitan areas like New York City, this creates severe hospital bottlenecks, uneven bed occupancy, and extended offload delays during peak surge periods.

This project introduces a **Markov Decision Process (MDP)** formulation resolved via a **Deep Q-Network (DQN)** agent that dynamically coordinates patient routing. By weighing transit time against facility occupancy, triage severity, and long-term capacity pressure, the agent achieves:
- **100% Service Success Rate** with zero unserviced emergency calls.
- **0.0% Overload Rate**, strictly avoiding catastrophic over-admissions.
- **Superior Inter-Hospital Resource Equity** (**Jain's Fairness Index 0.585 vs 0.570** for Nearest Heuristic) with an average transit time buffer of only ~1.4 minutes.

---

## 🏙️ System Architecture & Problem Formulation

```
Incoming 911 Call (Severity, Zone, Hour, Demand)
                   │
                   ▼
     ┌────────────────────────────┐
     │  219-Dimensional State     │
     │  Observation Vector        │
     └─────────────┬──────────────┘
                   │
                   ▼
     ┌────────────────────────────┐
     │  Deep Q-Network (DQN)      │
     │  Policy (219 -> 256 -> 12) │
     └─────────────┬──────────────┘
                   │
        Q-Values across 12 Hubs
                   │
                   ▼
     ┌────────────────────────────┐
     │ Selected Hospital Hub      │
     │ (Balanced Routing Action)  │
     └─────────────┬──────────────┘
                   │
       Real-Time Transition & Queues
                   │
                   ▼
     ┌────────────────────────────┐
     │ Dynamic Service Duration   │
     │ & Future Discharges        │
     └────────────────────────────┘
```

### 1. State Space ($\mathcal{S} \in \mathbb{R}^{219}$)
* **Spatial Origin:** 190-dimensional one-hot encoded vector indicating the incident ZIP centroid.
* **Temporal & Demand Context (5 features):**
  * Triage Severity Level ($0 = \text{Critical}$, $1 = \text{Moderate}$, $2 = \text{Low}$).
  * Cyclic diurnal components: $\sin(2\pi \cdot \text{hour}/24)$ and $\cos(2\pi \cdot \text{hour}/24)$.
  * Weekend indicator (binary).
  * City-wide normalized hourly call demand intensity.
* **System Occupancy Profile (24 features):**
  * Instantaneous occupancy fraction for each of the 12 hospital facilities ($U_{h,t} \in [0, 1]$).
  * Remaining free-capacity fraction for each facility.

### 2. Action Space ($\mathcal{A}$)
Discrete choice among the **12 primary NYC emergency hospital networks** across Manhattan, Brooklyn, Queens, and the Bronx.

### 3. Multi-Factor Reward Function
$$R_t = -\alpha T_t - \beta U_{h,t}^2 - \gamma O_t - \eta \cdot \mathbb{I}(\text{critical and high load}) + \delta S_t$$

* $-\alpha T_t$: Transit time penalty (minutes).
* $-\beta U_{h,t}^2$: Convex penalty penalizing disproportionate hospital congestion.
* $-\gamma O_t$: Catastrophic overload penalty if admitted above certified capacity.
* $-\eta$: Critical safety barrier preserving ICU capacity for life-threatening calls.
* $+\delta S_t$: Terminal completion bonus for successful patient intake.

---

## 📊 Empirical Evaluation & Benchmark Results

The DQN policy was benchmarked against four foundational dispatch strategies over **80 evaluation episodes** across **5 independent random initialization seeds** ($42, 7, 21, 99, 123$):

| Policy | Mean Reward | Mean Transit (min) | Overload Rate | Success Rate | Jain's Fairness Index |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **DQN (Proposed RL)** | **3.610** | **13.65** | **0.0%** | **100.0%** | **0.585** |
| Nearest Hospital Heuristic | 3.756 | 12.20 | 0.0% | 100.0% | 0.570 |
| Weighted Heuristic | 3.754 | 12.27 | 0.0% | 100.0% | 0.581 |
| Capacity-First Heuristic | 1.102 | 38.87 | 0.0% | 100.0% | 0.852 |
| Random Allocation | 1.014 | 39.62 | 0.0% | 100.0% | 0.613 |

### Robustness under Operational Shocks
The policy was further evaluated under four synthetic operational stress tests:
1. **Normal Operational Flow:** Baseline hospital load ($30\% - 55\%$).
2. **Demand Surge:** $1.75\times$ arrival rate multiplier simulating major urban emergencies.
3. **High Traffic Congestion:** Transit delays scaled by $1.25\times$.
4. **Critical Bed Shortage:** Pre-existing system occupancy at $75\% - 95\%$.

---

## 🖥️ Streamlit Interactive Command Center

The interactive web dashboard (`app.py`) provides a visual control suite:

1. **📊 Executive Summary & KPIs:** Real-time metrics, policy matrix, and multi-objective radar comparison.
2. **🤖 Live RL Dispatch Simulator:** Configure custom incident borough, triage severity, hour of day, and base congestion to observe the trained DQN agent make decisions with real-time $Q$-value distributions across all 12 facilities.
3. **🗺️ Geospatial Hospital Network:** Embedded interactive Folium / Leaflet GIS map with geocoded call points and hospital registry.
4. **📈 Policy Benchmarks & Stress Tests:** Interactive Plotly charts for shock scenario breakdowns and multi-seed stability error bars.
5. **🖼️ Research Results & Figures:** A dedicated visual gallery displaying all 12 publication-grade empirical plots with a high-resolution zoom and download inspector.
6. **📋 Data Explorer & Export:** Raw benchmark CSV inspection and one-click data downloads.

---

## 🚀 Getting Started

### Local Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SnehaDeepikaP/RL-Emergency-Resource-Allocation.git
   cd RL-Emergency-Resource-Allocation
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Streamlit dashboard:**
   ```bash
   python -m streamlit run app.py
   ```
   Open your browser at `http://localhost:8501`.

---

## ☁️ Deployment on Streamlit Community Cloud

1. Fork or push this repository to your GitHub account.
2. Go to [share.streamlit.io](https://share.streamlit.io) and log in with GitHub.
3. Click **"New app"**.
4. Set:
   - **Repository:** `SnehaDeepikaP/RL-Emergency-Resource-Allocation`
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Click **Deploy!**

---

## 📂 Repository Structure

```
├── app.py                     # Streamlit multi-tab executive dashboard
├── requirements.txt            # Python dependencies for local & cloud runtime
├── .gitignore                  # Git ignore rules
├── results/                    # Research artifacts and evaluation data
│   ├── dqn_emergency_allocation.zip  # Trained Deep Q-Network checkpoint
│   ├── nyc_emergency_map.html        # Interactive geospatial Folium map
│   ├── normal_policy_results.csv     # Baseline benchmark figures
│   ├── stress_policy_results.csv     # Stress scenario evaluation data
│   ├── fairness_results.csv          # Jain's fairness index metrics
│   ├── multi_seed_results.csv        # Multi-seed stability metrics
│   ├── hospitals.csv                 # NYC hospital registry with GIS coords
│   ├── final_summary.json            # Consolidated JSON metrics
│   └── *.png                         # High-res publication evaluation plots
└── RL_Dynamic_Emergency_Resource_Allocation_RealData.ipynb  # Training notebook
```

---

## 📜 License
This project is released under the [MIT License](LICENSE).
