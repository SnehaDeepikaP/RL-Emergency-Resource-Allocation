import os

beamer_tex = r'''\documentclass[aspectratio=169, 10pt]{beamer}

% --- THEME & PACKAGES ---
\usetheme{Madrid}
\usecolortheme{default}
\usepackage[utf8]{inputenc}
\usepackage{booktabs}
\usepackage{graphicx}
\usepackage{tikz}

% --- COLOR SETTINGS (BLACK & NAVY MONOCHROME) ---
\setbeamercolor{structure}{fg=black}
\setbeamercolor{title}{fg=black}
\setbeamercolor{frametitle}{fg=black, bg=white}
\setbeamercolor{block title}{fg=black, bg=gray!20}
\setbeamercolor{block body}{fg=black, bg=gray!5}
\setbeamertemplate{navigation symbols}{}
\setbeamertemplate{footline}[page number]

% --- TITLE SLIDE METADATA ---
\title[RL Emergency Allocation]{Dynamic Emergency Resource Allocation via Deep Reinforcement Learning}
\subtitle{A Data-Driven Framework for Urban Emergency Medical Services Dispatching}

\author[Deepika \& Keerthi]{
    \textbf{Parimisetty Sneha Deepika} (AV.SC.U4AIE23034) \\
    \textbf{Nakka Keerthi} (AV.SC.U4AIE23032)
}

\institute[Amrita]{
    Amrita Vishwa Vidyapeetham \\
    Course: Reinforcement Learning \\
    Dataset: NYC EMS Dispatch Data (274,964 Records)
}

\date{October 2026}

\begin{document}

% SLIDE 1: Title
\begin{frame}
    \titlepage
\end{frame}

% SLIDE 2: Table of Contents
\begin{frame}{Presentation Outline}
    \tableofcontents
\end{frame}

% SECTION 1: Introduction & Problem Statement
\section{Introduction \& Problem Statement}

\begin{frame}{Operational Challenges in Urban EMS}
    \begin{itemize}[<+-| alert@+>]
        \item \textbf{High Dispatch Demand:} Major metropolitan areas handle hundreds of thousands of EMS calls annually across large spatial footprints.
        \item \textbf{Static Proximity Dispatching:} Standard protocols default to transporting patients to the geographically nearest hospital.
        \item \textbf{Systemic Inefficiencies:}
        \begin{itemize}
            \item \textbf{Hospital Overcrowding:} Neighboring emergencies funnel into a single emergency department (ED).
            \item \textbf{Ambulance Wall Time:} Units spend hours waiting to transfer patients, reducing overall fleet availability.
            \item \textbf{Surge Vulnerability:} Static routing fails rapidly during major events or capacity shortages.
        \end{itemize}
    \end{itemize}
\end{frame}

\begin{frame}{Research Objectives}
    \begin{block}{Core Research Question}
        \textit{Can a Deep Q-Network (DQN) policy route emergency patients across a city's hospital network more effectively than standard proximity rules, balancing fast transport times with hospital bed availability?}
    \end{block}

    \vspace{0.3cm}
    \textbf{Key Project Goals:}
    \begin{enumerate}
        \item Build a dynamic Gymnasium simulation environment using \textbf{274,964 clean NYC EMS calls}.
        \item Model real road geometry via OpenStreetMap Dijkstra graphs and Haversine circuity.
        \item Implement dynamic patient stay queues and severity-dependent discharge cycles.
        \item Evaluate DQN against 4 benchmark dispatch policies under normal, critical, fairness, and stress conditions.
    \end{enumerate}
\end{frame}

% SECTION 2: Methodology & Environment Setup
\section{Methodology \& Environment Setup}

\begin{frame}{Empirical Data Pipeline}
    \begin{table}
        \centering
        \caption{Summary of Data Infrastructure}
        \resizebox{0.95\textwidth}{!}{%
        \begin{tabular}{ll}
            \toprule
            \textbf{Dataset / Resource} & \textbf{Details \& Features} \\
            \midrule
            NYC EMS Dispatch Data & 300,000 raw $\rightarrow$ 274,964 clean incidents (Oct--Dec 2025) \\
            US Census ZCTA Gazetteer & 229 ZIP Code spatial centroids \\
            NYS Department of Health & 12 major healthcare facilities across NYC boroughs \\
            OpenStreetMap Driving Graph & Dijkstra shortest paths + Haversine circuity ($229 \times 12$ matrix) \\
            Patient Acuity Breakdown & 24.5\% Critical (Sev 0), 52.8\% Moderate (Sev 1), 22.7\% Low (Sev 2) \\
            \bottomrule
        \end{tabular}%
        }
    \end{table}
\end{frame}

\begin{frame}{Dynamic MDP Environment Architecture}
    \begin{itemize}
        \item \textbf{State Vector (258 Dimensions):}
        \begin{itemize}
            \item One-hot spatial zone encoding (229 values).
            \item Patient severity, time of day ($\sin/\cos$), weekend flag, demand intensity (5 values).
            \item Hospital bed occupancy fractions (12 values).
            \item Hospital remaining free capacity fractions (12 values).
        \end{itemize}
        \item \textbf{Action Space:} Select 1 of 12 candidate destination hospitals.
        \item \textbf{Dynamic Discharge Queues:} Patient stay durations sampled by severity:
        \begin{itemize}
            \item Critical: 5--14 steps \quad | \quad Moderate: 4--11 steps \quad | \quad Low: 2--8 steps
        \end{itemize}
    \end{itemize}
\end{frame}

\begin{frame}{Multi-Objective Reward Function}
    \begin{block}{Reward Signal Formulation}
        $$\text{Reward} = -1.0 \times \left(\frac{\text{Travel Min}}{10}\right) - 4.0 \times (\text{Occupancy})^2 + 5.0 \, [\text{if admitted}]$$
    \end{block}

    \vspace{0.2cm}
    \begin{itemize}
        \item \textbf{Travel Penalty:} Penalizes driving duration to encourage geographic efficiency.
        \item \textbf{Occupancy Penalty:} Quadratically penalizes assigning patients to busy hospitals.
        \item \textbf{Full Capacity Penalty:} -30.0 heavy rejection penalty if hospital is 100\% full.
        \item \textbf{Critical Safety Penalty:} Extra -10.0 penalty for sending critical calls to EDs above 85\% capacity.
    \end{itemize}
\end{frame}

% SECTION 3: Deep Q-Network & Policies
\section{DQN Policy \& Baselines}

\begin{frame}{Deep Q-Network (DQN) Architecture}
    \begin{columns}
        \begin{column}{0.5\textwidth}
            \begin{block}{Model Settings}
                \begin{itemize}
                    \item \textbf{Policy Network:} MLP ($256 \times 256$)
                    \item \textbf{Optimizer:} Adam ($\text{lr} = 10^{-4}$)
                    \item \textbf{Discount Factor:} $\gamma = 0.98$
                    \item \textbf{Replay Buffer:} 50,000 transitions
                    \item \textbf{Batch Size:} 64 transitions
                    \item \textbf{Total Timesteps:} 50,000 steps
                \end{itemize}
            \end{block}
        \end{column}
        \begin{column}{0.5\textwidth}
            \begin{block}{Evaluated Baseline Policies}
                \begin{enumerate}
                    \item \textbf{Nearest:} Routes to geographically closest available hospital.
                    \item \textbf{Weighted Heuristic:} Scores hospitals using distance + utilization.
                    \item \textbf{DQN:} Trained DRL agent.
                    \item \textbf{Capacity-First:} Routes to hospital with highest open bed \%.
                    \item \textbf{Random:} Uniform random choice.
                \end{enumerate}
            \end{block}
        \end{column}
    \end{columns}
\end{frame}

% SECTION 4: Experimental Results
\section{Experimental Results}

\begin{frame}{Standard Operational Results}
    \begin{columns}
        \begin{column}{0.5\textwidth}
            \includegraphics[width=\textwidth]{policy_comparison_mean_travel_min.png}
        \end{column}
        \begin{column}{0.5\textwidth}
            \begin{table}
                \resizebox{\textwidth}{!}{%
                \begin{tabular}{lcccc}
                    \toprule
                    \textbf{Policy} & \textbf{Reward} & \textbf{Travel Min} & \textbf{Overload} & \textbf{Success} \\
                    \midrule
                    \textbf{Nearest} & \textbf{3.76} & \textbf{12.14} & 0.0\% & 100\% \\
                    \textbf{Weighted} & 3.76 & 12.21 & 0.0\% & 100\% \\
                    \textbf{DQN} & 3.27 & 17.04 & 0.0\% & 100\% \\
                    \textbf{CapFirst} & 1.18 & 38.05 & 0.0\% & 100\% \\
                    \textbf{Random} & 1.06 & 39.13 & 0.0\% & 100\% \\
                    \bottomrule
                \end{tabular}%
                }
            \end{table}
            \small
            Nearest and Weighted Heuristic achieve the shortest travel times (~12.1 min). Capacity-First increases travel time by 218\% (38.05 min).
        \end{column}
    \end{columns}
\end{frame}

\begin{frame}{Critical Case Performance \& Load Fairness}
    \begin{columns}
        \begin{column}{0.5\textwidth}
            \includegraphics[width=\textwidth]{critical_case_performance.png}
            \centerline{\small Critical Case (Severity 0) Transport}
        \end{column}
        \begin{column}{0.5\textwidth}
            \includegraphics[width=\textwidth]{fairness_comparison.png}
            \centerline{\small Jain's Fairness Index Across Policies}
        \end{column}
    \end{columns}
\end{frame}

\begin{frame}{Stress Testing Scenarios}
    \begin{columns}
        \begin{column}{0.55\textwidth}
            \includegraphics[width=\textwidth]{stress_test_heatmap.png}
        \end{column}
        \begin{column}{0.45\textwidth}
            \begin{block}{Key Stress Insights}
                \begin{itemize}
                    \item \textbf{Shortage (75-95\% Occupancy):} DQN maintains 13.59 min travel time \& 3.47 reward.
                    \item \textbf{Surge (1.75x Call Rate):} DQN maintains 13.58 min travel time.
                    \item \textbf{Adaptability:} DQN adapts effectively under severe capacity shortages.
                \end{itemize}
            \end{block}
        \end{column}
    \end{columns}
\end{frame}

% SECTION 5: Discussion & Conclusion
\section{Discussion \& Conclusion}

\begin{frame}{Operational Discussion}
    \begin{enumerate}
        \item \textbf{Nearest Dominance Under Light Load:} Driving time is the dominant penalty, so nearest routing is optimal when beds are available.
        \item \textbf{DQN Resilience:} Deep Q-Networks balance capacity and distance, achieving zero hospital overloads.
        \item \textbf{Capacity-First Failure:} Ignoring geographic distance inflates travel times to over 38 minutes.
        \item \textbf{Interpretability:} Weighted Heuristics provide transparent suggestions for real dispatch control rooms.
    \end{enumerate}
\end{frame}

\begin{frame}{Conclusion \& Future Research}
    \begin{block}{Summary of Achievements}
        Constructed a 258-dim Gym environment on 274,964 NYC EMS calls, proving that dynamic RL prevents overloads while proximity rules optimize travel speed.
    \end{block}

    \vspace{0.3cm}
    \textbf{Future Work:}
    \begin{itemize}
        \item \textbf{Multi-Agent RL:} Coordinate ambulance fleet dispatch and repositioning.
        \item \textbf{Live Traffic Feeds:} Integrate dynamic GPS speeds.
        \item \textbf{Action Masking:} Enforce hard spatial proximity bounds.
    \end{itemize}
\end{frame}

\begin{frame}
    \centering
    \Huge \textbf{Thank You!} \\
    \vspace{0.5cm}
    \Large Questions \& Discussion \\
    \vspace{0.8cm}
    \small Parimisetty Sneha Deepika \& Nakka Keerthi \\
    Amrita Vishwa Vidyapeetham
\end{frame}

\end{document}
'''

with open(r"c:\Users\P.SNEHA DEEPIKA\OneDrive\Desktop\RL Project\RL_Emergency_Allocation_Beamer.tex", "w", encoding="utf-8") as f:
    f.write(beamer_tex)

print("Successfully generated Beamer LaTeX file.")
