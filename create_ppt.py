import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    # Set slide dimensions to widescreen 16:9
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette
    NAVY = RGBColor(0, 51, 102)
    DARK_GRAY = RGBColor(30, 41, 59)
    LIGHT_BG = RGBColor(248, 250, 252)
    CARD_BG = RGBColor(255, 255, 255)
    BORDER_COLOR = RGBColor(226, 232, 240)
    ACCENT_BLUE = RGBColor(14, 116, 144)
    TEXT_MUTED = RGBColor(100, 116, 139)

    def set_bg(slide):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = LIGHT_BG

    def add_header(slide, title_text, category_text="RL DYNAMIC EMERGENCY RESOURCE ALLOCATION"):
        # Header banner
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = category_text.upper()
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = ACCENT_BLUE

        p1 = tf.add_paragraph()
        p1.text = title_text
        p1.font.size = Pt(22)
        p1.font.bold = True
        p1.font.color.rgb = NAVY

    # -------------------------------------------------------------
    # SLIDE 1: Title Slide
    # -------------------------------------------------------------
    slide1 = prs.slides.add_slide(blank_layout)
    set_bg(slide1)

    # Main Card
    card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.0), Inches(11.333), Inches(5.5))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = BORDER_COLOR

    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.8)
    tf.margin_top = Inches(0.8)

    p = tf.paragraphs[0]
    p.text = "Dynamic Emergency Resource Allocation via Deep Reinforcement Learning"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = NAVY

    p2 = tf.add_paragraph()
    p2.text = "A Data-Driven Framework for Urban Emergency Medical Services Dispatching"
    p2.font.size = Pt(18)
    p2.font.color.rgb = ACCENT_BLUE
    p2.space_before = Pt(10)

    p3 = tf.add_paragraph()
    p3.text = "\nPresenters:"
    p3.font.size = Pt(14)
    p3.font.bold = True
    p3.font.color.rgb = DARK_GRAY

    p4 = tf.add_paragraph()
    p4.text = "1. Parimisetty Sneha Deepika (Roll No: AV.SC.U4AIE23034)\n2. Nakka Keerthi (Roll No: AV.SC.U4AIE23032)"
    p4.font.size = Pt(14)
    p4.font.color.rgb = DARK_GRAY

    p5 = tf.add_paragraph()
    p5.text = "\nInstitution: Amrita Vishwa Vidyapeetham\nCourse: Reinforcement Learning\nDataset: NYC EMS Dispatch Data (274,964 Records)"
    p5.font.size = Pt(13)
    p5.font.color.rgb = TEXT_MUTED

    slide1.notes_slide.notes_text_frame.text = "Welcome everyone. Today we present our project on dynamic emergency resource allocation using Deep Reinforcement Learning, evaluated on real-world EMS dispatch data from New York City."

    # -------------------------------------------------------------
    # SLIDE 2: Executive Summary & Motivation
    # -------------------------------------------------------------
    slide2 = prs.slides.add_slide(blank_layout)
    set_bg(slide2)
    add_header(slide2, "1. Executive Summary & Operational Motivation")

    # Left Card - Problem Context
    c1 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    c1.fill.solid()
    c1.fill.fore_color.rgb = CARD_BG
    c1.line.color.rgb = BORDER_COLOR
    tf1 = c1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_top = tf1.margin_right = Inches(0.4)
    
    p = tf1.paragraphs[0]
    p.text = "Operational Challenges in Urban EMS"
    p.font.bold = True
    p.font.size = Pt(18)
    p.font.color.rgb = NAVY

    bullets1 = [
        "High Call Volume: NYC EMS handles ~300,000 emergency calls per quarter across 229 ZIP codes.",
        "Static Dispatch Pitfall: Ambulances default to the physically nearest hospital.",
        "Localized Overcrowding: Multiple emergencies near one area bottleneck a single emergency department (ED).",
        "Ambulance Wall-Time: Waiting for bed availability keeps ambulance units off the road."
    ]
    for b in bullets1:
        pb = tf1.add_paragraph()
        pb.text = "• " + b
        pb.font.size = Pt(13)
        pb.font.color.rgb = DARK_GRAY
        pb.space_before = Pt(8)

    # Right Card - Proposed Solution
    c2 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
    c2.fill.solid()
    c2.fill.fore_color.rgb = CARD_BG
    c2.line.color.rgb = BORDER_COLOR
    tf2 = c2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_top = tf2.margin_right = Inches(0.4)

    p = tf2.paragraphs[0]
    p.text = "Our Dynamic DRL Solution"
    p.font.bold = True
    p.font.size = Pt(18)
    p.font.color.rgb = NAVY

    bullets2 = [
        "Data-Driven Gym Environment: Built on 274,964 clean NYC dispatch records.",
        "Real Road Routing: OpenStreetMap (OSM) Dijkstra shortest path graph + Haversine circuity.",
        "Dynamic Patient Queues: Models hospital stay durations and bed discharge cycles by severity.",
        "Deep Q-Network (DQN): Optimizes multi-attribute reward balancing travel speed and bed capacity."
    ]
    for b in bullets2:
        pb = tf2.add_paragraph()
        pb.text = "• " + b
        pb.font.size = Pt(13)
        pb.font.color.rgb = DARK_GRAY
        pb.space_before = Pt(8)

    slide2.notes_slide.notes_text_frame.text = "In this slide, we contrast standard static nearest-hospital dispatching against our dynamic Deep Reinforcement Learning solution."

    # -------------------------------------------------------------
    # SLIDE 3: Research Problem Statement & Objectives
    # -------------------------------------------------------------
    slide3 = prs.slides.add_slide(blank_layout)
    set_bg(slide3)
    add_header(slide3, "2. Research Problem & Project Objectives")

    # Center Banner Card
    c_prob = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.733), Inches(1.5))
    c_prob.fill.solid()
    c_prob.fill.fore_color.rgb = CARD_BG
    c_prob.line.color.rgb = BORDER_COLOR
    tf_p = c_prob.text_frame
    tf_p.word_wrap = True
    tf_p.margin_left = tf_p.margin_top = Inches(0.4)
    
    p = tf_p.paragraphs[0]
    p.text = "Core Research Question:"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = ACCENT_BLUE

    p2 = tf_p.add_paragraph()
    p2.text = "“Can a Deep Q-Network (DQN) policy dynamically allocate EMS demand across geographically distributed hospitals more effectively than standard proximity rules, balancing transport speed with hospital bed availability?”"
    p2.font.size = Pt(15)
    p2.font.italic = True
    p2.font.color.rgb = NAVY
    p2.space_before = Pt(4)

    # 3 Objective Columns
    objs = [
        ("Objective 1: Spatial-Temporal Simulation", "Build an empirical Gymnasium environment using 274k real NYC incidents, road distances, and hospital capacities."),
        ("Objective 2: Dual-Objective Optimization", "Formulate a reward function that balances patient transport time against hospital occupancy and criticality penalties."),
        ("Objective 3: Rigorous Benchmarking", "Evaluate DQN against 4 baseline strategies across normal, critical, load-fairness, multi-seed, and stress scenarios.")
    ]
    for i, (title, desc) in enumerate(objs):
        left_pos = Inches(0.8 + i * 4.0)
        c_obj = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(3.4), Inches(3.733), Inches(3.4))
        c_obj.fill.solid()
        c_obj.fill.fore_color.rgb = CARD_BG
        c_obj.line.color.rgb = BORDER_COLOR
        tf_o = c_obj.text_frame
        tf_o.word_wrap = True
        tf_o.margin_left = tf_o.margin_top = tf_o.margin_right = Inches(0.3)

        p = tf_o.paragraphs[0]
        p.text = title
        p.font.bold = True
        p.font.size = Pt(15)
        p.font.color.rgb = NAVY

        p_d = tf_o.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(13)
        p_d.font.color.rgb = DARK_GRAY
        p_d.space_before = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 4: Data Pipeline & Spatial Graph Construction
    # -------------------------------------------------------------
    slide4 = prs.slides.add_slide(blank_layout)
    set_bg(slide4)
    add_header(slide4, "3. Data Pipeline & Spatial Graph Construction")

    # Data Source Boxes
    sources = [
        ("NYC Open Data EMS", "300,000 raw incidents\n274,964 clean calls\nOct 23 - Dec 31, 2025\nSeverity: 24.5% Crit, 52.8% Mod, 22.7% Low"),
        ("US Census ZCTA", "229 ZIP Code Centroids\nSpatial demand proxies\nLatitude/Longitude\nNYC Borough Coverage"),
        ("NYS Health Capacity", "12 Major Regional Facilities\nManhattan, Queens, Brooklyn, Bronx\nReal bed capacity figures\nDynamic occupancy tracking"),
        ("OpenStreetMap Graph", "Dijkstra Shortest Paths\nHaversine Circuity (1.35x)\nAverage Speed: 28 km/h\n$229 \\times 12$ Distance Matrix")
    ]

    for i, (stitle, sdesc) in enumerate(sources):
        left_pos = Inches(0.8 + (i % 2) * 5.9)
        top_pos = Inches(1.6 + (i // 2) * 2.7)
        box = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, top_pos, Inches(5.6), Inches(2.4))
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = BORDER_COLOR
        tf_s = box.text_frame
        tf_s.word_wrap = True
        tf_s.margin_left = tf_s.margin_top = Inches(0.3)

        p = tf_s.paragraphs[0]
        p.text = stitle
        p.font.bold = True
        p.font.size = Pt(16)
        p.font.color.rgb = NAVY

        p_d = tf_s.add_paragraph()
        p_d.text = sdesc
        p_d.font.size = Pt(13)
        p_d.font.color.rgb = DARK_GRAY
        p_d.space_before = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 5: Dynamic MDP Environment Architecture
    # -------------------------------------------------------------
    slide5 = prs.slides.add_slide(blank_layout)
    set_bg(slide5)
    add_header(slide5, "4. Dynamic MDP Environment Architecture")

    # State Vector Card
    c_state = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    c_state.fill.solid()
    c_state.fill.fore_color.rgb = CARD_BG
    c_state.line.color.rgb = BORDER_COLOR
    tf_st = c_state.text_frame
    tf_st.word_wrap = True
    tf_st.margin_left = tf_st.margin_top = Inches(0.4)

    p = tf_st.paragraphs[0]
    p.text = "Observation State Vector (258 Dims)"
    p.font.bold = True
    p.font.size = Pt(17)
    p.font.color.rgb = NAVY

    s_items = [
        "1-Hot Spatial Zone (229 values): Identifies incident ZIP code location.",
        "Patient Severity (1 value): 0.0 (Critical), 0.5 (Moderate), 1.0 (Low).",
        "Cyclic Hour Encoding (2 values): sin(2πh/24) & cos(2πh/24) for time of day.",
        "Weekend & Demand Intensity (2 values): Binary weekend flag & normalized hourly demand call rate.",
        "Hospital Occupancy Vector (12 values): Current fraction of beds occupied.",
        "Free Capacity Vector (12 values): Remaining available bed fraction."
    ]
    for item in s_items:
        pb = tf_st.add_paragraph()
        pb.text = "• " + item
        pb.font.size = Pt(12)
        pb.font.color.rgb = DARK_GRAY
        pb.space_before = Pt(6)

    # Action & Queue Card
    c_act = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
    c_act.fill.solid()
    c_act.fill.fore_color.rgb = CARD_BG
    c_act.line.color.rgb = BORDER_COLOR
    tf_ac = c_act.text_frame
    tf_ac.word_wrap = True
    tf_ac.margin_left = tf_ac.margin_top = Inches(0.4)

    p = tf_ac.paragraphs[0]
    p.text = "Action Space & Dynamic Patient Queues"
    p.font.bold = True
    p.font.size = Pt(17)
    p.font.color.rgb = NAVY

    a_items = [
        "Discrete Action Space: Select 1 of 12 candidate regional hospitals.",
        "Severity-Dependent Stay Queues:",
        "  - Critical (Severity 0): 5 to 14 steps stay",
        "  - Moderate (Severity 1): 4 to 11 steps stay",
        "  - Low (Severity 2): 2 to 8 steps stay",
        "Dynamic Discharges: At each step, remaining stay timers decrement; expired timers trigger patient discharge and free bed space."
    ]
    for item in a_items:
        pb = tf_ac.add_paragraph()
        pb.text = "• " + item
        pb.font.size = Pt(13)
        pb.font.color.rgb = DARK_GRAY
        pb.space_before = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 6: Multi-Objective Reward Formulation
    # -------------------------------------------------------------
    slide6 = prs.slides.add_slide(blank_layout)
    set_bg(slide6)
    add_header(slide6, "5. Multi-Objective Reward Function Design")

    # Top Formula Card
    c_f = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.733), Inches(1.8))
    c_f.fill.solid()
    c_f.fill.fore_color.rgb = CARD_BG
    c_f.line.color.rgb = BORDER_COLOR
    tf_f = c_f.text_frame
    tf_f.word_wrap = True
    tf_f.margin_left = tf_f.margin_top = Inches(0.4)

    p = tf_f.paragraphs[0]
    p.text = "Reward Signal Formulation:"
    p.font.bold = True
    p.font.size = Pt(15)
    p.font.color.rgb = ACCENT_BLUE

    p2 = tf_f.add_paragraph()
    p2.text = "Reward = -1.0 * (Travel Time / 10) - 4.0 * (Hospital Utilization)^2 + 5.0 [Success Bonus]"
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = NAVY
    p2.space_before = Pt(6)

    # 3 Reward Components Cards
    r_comps = [
        ("Travel Penalty (-1.0 * T/10)", "Linearly penalizes longer transport times to ensure ambulances prioritize geographically efficient hospital choices."),
        ("Occupancy Penalty (-4.0 * U^2)", "Quadratically penalizes assigning patients to highly utilized facilities, encouraging load balancing across hospitals."),
        ("Safety & Overload Penalties", "Enforces a heavy -30.0 rejection penalty if a hospital is at 100% capacity, plus a -10.0 penalty for sending critical patients to EDs above 85% utilization.")
    ]

    for i, (rtitle, rdesc) in enumerate(r_comps):
        left_pos = Inches(0.8 + i * 4.0)
        c_r = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(3.7), Inches(3.733), Inches(3.1))
        c_r.fill.solid()
        c_r.fill.fore_color.rgb = CARD_BG
        c_r.line.color.rgb = BORDER_COLOR
        tf_r = c_r.text_frame
        tf_r.word_wrap = True
        tf_r.margin_left = tf_r.margin_top = Inches(0.3)

        p = tf_r.paragraphs[0]
        p.text = rtitle
        p.font.bold = True
        p.font.size = Pt(15)
        p.font.color.rgb = NAVY

        p_d = tf_r.add_paragraph()
        p_d.text = rdesc
        p_d.font.size = Pt(13)
        p_d.font.color.rgb = DARK_GRAY
        p_d.space_before = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 7: Deep Q-Network (DQN) Architecture & Training
    # -------------------------------------------------------------
    slide7 = prs.slides.add_slide(blank_layout)
    set_bg(slide7)
    add_header(slide7, "6. Deep Q-Network (DQN) Training Setup")

    # Hyperparams Table Card
    c_tbl = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    c_tbl.fill.solid()
    c_tbl.fill.fore_color.rgb = CARD_BG
    c_tbl.line.color.rgb = BORDER_COLOR
    tf_tb = c_tbl.text_frame
    tf_tb.word_wrap = True
    tf_tb.margin_left = tf_tb.margin_top = Inches(0.4)

    p = tf_tb.paragraphs[0]
    p.text = "DQN Hyperparameters"
    p.font.bold = True
    p.font.size = Pt(18)
    p.font.color.rgb = NAVY

    hparams = [
        ("Policy Network", "Multi-Layer Perceptron (MLP)"),
        ("Hidden Layers", "2 Layers x 256 Units (ReLU)"),
        ("Optimizer", "Adam (Learning Rate = 1e-4)"),
        ("Discount Factor (γ)", "0.98"),
        ("Replay Buffer Size", "50,000 transitions"),
        ("Batch Size", "64 transitions"),
        ("Target Network Update", "Every 2,000 steps"),
        ("Exploration (ε)", "1.00 -> 0.05 over 12.5k steps"),
        ("Total Training Steps", "50,000 timesteps")
    ]
    for k, v in hparams:
        pb = tf_tb.add_paragraph()
        pb.text = f"• {k}: {v}"
        pb.font.size = Pt(12)
        pb.font.color.rgb = DARK_GRAY
        pb.space_before = Pt(4)

    # Strategy Card
    c_strat = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
    c_strat.fill.solid()
    c_strat.fill.fore_color.rgb = CARD_BG
    c_strat.line.color.rgb = BORDER_COLOR
    tf_st = c_strat.text_frame
    tf_st.word_wrap = True
    tf_st.margin_left = tf_st.margin_top = Inches(0.4)

    p = tf_st.paragraphs[0]
    p.text = "Stabilization & Training Dynamics"
    p.font.bold = True
    p.font.size = Pt(18)
    p.font.color.rgb = NAVY

    strat_bullets = [
        "Experience Replay: Decorrelates consecutive EMS calls, sampling random batches of 64 transitions.",
        "Target Q-Network: Periodically syncs parameters to prevent training feedback loops.",
        "Epsilon Decay: Smooth transition from 100% random exploration to policy exploitation.",
        "Stable-Baselines3 Implementation: Ensures reproducible reinforcement learning execution."
    ]
    for b in strat_bullets:
        pb = tf_st.add_paragraph()
        pb.text = "• " + b
        pb.font.size = Pt(13)
        pb.font.color.rgb = DARK_GRAY
        pb.space_before = Pt(10)

    # -------------------------------------------------------------
    # SLIDE 8: Benchmark Dispatch Policies
    # -------------------------------------------------------------
    slide8 = prs.slides.add_slide(blank_layout)
    set_bg(slide8)
    add_header(slide8, "7. Evaluated Benchmark Policies")

    p_boxes = [
        ("1. Nearest Hospital (Nearest)", "Sends patient to geographically closest hospital with available beds. Minimizes driving time but risks emergency room crowding."),
        ("2. Weighted Heuristic (Weighted)", "Multi-attribute rule balancing distance & occupancy. Weights distance higher (0.75) for critical calls and lowers it (0.55) for minor calls."),
        ("3. Deep Q-Network (DQN)", "Trained DRL policy that dynamically evaluates all 258 state features to make long-term capacity-aware hospital choices."),
        ("4. Capacity-First (CapFirst)", "Always routes to the hospital with the highest percentage of empty beds. Maximum load balancing, but ignores distance."),
        ("5. Random Allocation (Random)", "Uniform random choice among hospitals with open beds. Benchmark baseline for unstructured dispatching.")
    ]

    for i, (pname, pdesc) in enumerate(p_boxes):
        top_pos = Inches(1.5 + i * 1.05)
        box = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_pos, Inches(11.733), Inches(0.95))
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = BORDER_COLOR
        tf_p = box.text_frame
        tf_p.word_wrap = True
        tf_p.margin_left = tf_p.margin_top = Inches(0.2)

        p = tf_p.paragraphs[0]
        p.text = pname
        p.font.bold = True
        p.font.size = Pt(14)
        p.font.color.rgb = NAVY

        p_d = tf_p.add_paragraph()
        p_d.text = pdesc
        p_d.font.size = Pt(12)
        p_d.font.color.rgb = DARK_GRAY
        p_d.space_before = Pt(2)

    # -------------------------------------------------------------
    # SLIDE 9: Results: Standard Operational Evaluation
    # -------------------------------------------------------------
    slide9 = prs.slides.add_slide(blank_layout)
    set_bg(slide9)
    add_header(slide9, "8. Experimental Results: Standard Operations")

    # Image Card
    img_path = r"policy_comparison_mean_travel_min.png"
    if os.path.exists(img_path):
        slide9.shapes.add_picture(img_path, Inches(0.8), Inches(1.6), Inches(6.0), Inches(5.2))

    # Results Table Card
    c_res = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.0), Inches(1.6), Inches(5.533), Inches(5.2))
    c_res.fill.solid()
    c_res.fill.fore_color.rgb = CARD_BG
    c_res.line.color.rgb = BORDER_COLOR
    tf_res = c_res.text_frame
    tf_res.word_wrap = True
    tf_res.margin_left = tf_res.margin_top = Inches(0.3)

    p = tf_res.paragraphs[0]
    p.text = "Performance Under Normal Conditions"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = NAVY

    res_bullets = [
        "Nearest: Best mean travel time (12.14 min) and highest reward (3.76).",
        "Weighted Heuristic: Nearly identical performance to Nearest (12.21 min, 3.76 reward).",
        "DQN: Solid capacity management (17.04 min travel time, 3.27 reward) with 0.00% overload rate.",
        "Capacity-First: Massive travel time penalty (38.05 min, 218% increase) due to ignoring distance.",
        "Random: Poor performance (39.13 min travel time, 1.06 reward)."
    ]
    for b in res_bullets:
        pb = tf_res.add_paragraph()
        pb.text = "• " + b
        pb.font.size = Pt(12)
        pb.font.color.rgb = DARK_GRAY
        pb.space_before = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 10: Results: Critical-Case & Patient Safety
    # -------------------------------------------------------------
    slide10 = prs.slides.add_slide(blank_layout)
    set_bg(slide10)
    add_header(slide10, "9. Results: Critical Case Performance")

    img_crit = r"critical_case_performance.png"
    if os.path.exists(img_crit):
        slide10.shapes.add_picture(img_crit, Inches(0.8), Inches(1.6), Inches(6.0), Inches(5.2))

    c_crit = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.0), Inches(1.6), Inches(5.533), Inches(5.2))
    c_crit.fill.solid()
    c_crit.fill.fore_color.rgb = CARD_BG
    c_crit.line.color.rgb = BORDER_COLOR
    tf_cr = c_crit.text_frame
    tf_cr.word_wrap = True
    tf_cr.margin_left = tf_cr.margin_top = Inches(0.3)

    p = tf_cr.paragraphs[0]
    p.text = "High-Acuity Calls (Severity 0)"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = NAVY

    crit_bullets = [
        "Subset Focus: 24.51% of total calls represent critical cardiac arrests / severe trauma.",
        "Weighted Heuristic: Achieves highest reward (3.6869) and fast transport (12.25 min).",
        "Nearest: Delivers critical patients in 12.23 minutes.",
        "DQN Safety Mechanism: Maintains zero critical overloaded ED admissions, averaging 16.56 minutes travel time.",
        "Conclusion: Proximity rules excel when capacities are open, while DQN acts as a safety buffer during surge."
    ]
    for b in crit_bullets:
        pb = tf_cr.add_paragraph()
        pb.text = "• " + b
        pb.font.size = Pt(12)
        pb.font.color.rgb = DARK_GRAY
        pb.space_before = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 11: Results: Resource Equity & Jain's Fairness Index
    # -------------------------------------------------------------
    slide11 = prs.slides.add_slide(blank_layout)
    set_bg(slide11)
    add_header(slide11, "10. Resource Equity & Jain's Fairness Index")

    img_fair = r"fairness_comparison.png"
    if os.path.exists(img_fair):
        slide11.shapes.add_picture(img_fair, Inches(0.8), Inches(1.6), Inches(6.0), Inches(5.2))

    c_fair = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.0), Inches(1.6), Inches(5.533), Inches(5.2))
    c_fair.fill.solid()
    c_fair.fill.fore_color.rgb = CARD_BG
    c_fair.line.color.rgb = BORDER_COLOR
    tf_fa = c_fair.text_frame
    tf_fa.word_wrap = True
    tf_fa.margin_left = tf_fa.margin_top = Inches(0.3)

    p = tf_fa.paragraphs[0]
    p.text = "Systemic Hospital Load Balancing"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = NAVY

    fair_bullets = [
        "Capacity-First: Highest Jain's Index (0.8558) and lowest utilization variance (2.48e-6), but severely delays patients.",
        "DQN Agent: Balanced fairness index (0.5852) with low variance (1.21e-5), distributing loads without sacrificing speed.",
        "Weighted Heuristic: Achieves 0.5812 fairness index while keeping transport times fast.",
        "Nearest: Lowest fairness index (0.5701) due to clustering patients into neighborhood facilities."
    ]
    for b in fair_bullets:
        pb = tf_fa.add_paragraph()
        pb.text = "• " + b
        pb.font.size = Pt(12)
        pb.font.color.rgb = DARK_GRAY
        pb.space_before = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 12: Results: Robustness & Stress Testing
    # -------------------------------------------------------------
    slide12 = prs.slides.add_slide(blank_layout)
    set_bg(slide12)
    add_header(slide12, "11. Robustness & Extreme Stress Testing")

    img_stress = r"stress_test_heatmap.png"
    if os.path.exists(img_stress):
        slide12.shapes.add_picture(img_stress, Inches(0.8), Inches(1.6), Inches(6.0), Inches(5.2))

    c_st = slide12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.0), Inches(1.6), Inches(5.533), Inches(5.2))
    c_st.fill.solid()
    c_st.fill.fore_color.rgb = CARD_BG
    c_st.line.color.rgb = BORDER_COLOR
    tf_str = c_st.text_frame
    tf_str.word_wrap = True
    tf_str.margin_left = tf_str.margin_top = Inches(0.3)

    p = tf_str.paragraphs[0]
    p.text = "Stress Test Scenarios"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = NAVY

    st_bullets = [
        "Multi-Seed Verification: Tested across 5 random seeds (42, 7, 21, 99, 123) with stable metrics.",
        "Critical Shortage (75-95% Occupancy): DQN maintains 13.59 min travel time & 3.47 reward.",
        "Demand Surge (1.75x Call Rate): DQN keeps performance stable at 13.58 min travel time.",
        "High Congestion (55-85% Occupancy): DQN yields 3.55 reward and 13.57 min travel time.",
        "Conclusion: DQN adapts effectively under severe system stress."
    ]
    for b in st_bullets:
        pb = tf_str.add_paragraph()
        pb.text = "• " + b
        pb.font.size = Pt(12)
        pb.font.color.rgb = DARK_GRAY
        pb.space_before = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 13: Operational Insights & Key Takeaways
    # -------------------------------------------------------------
    slide13 = prs.slides.add_slide(blank_layout)
    set_bg(slide13)
    add_header(slide13, "12. Practical Insights & Key Takeaways")

    takeaways = [
        ("1. Proximity is Dominant Under Light Loads", "When hospital beds are open, Nearest routing is optimal because transport time dominates total call duration."),
        ("2. Pure Capacity Routing Fails", "Capacity-First dispatching inflates travel time by over 200%, showing that load balancing cannot ignore road geography."),
        ("3. DQN Provides Adaptive Resilience", "Deep Q-Networks successfully balance travel speed and capacity, preventing overloads during severe bed shortages."),
        ("4. Dispatcher Interpretability Matters", "Rules like Weighted Heuristic provide transparent suggestions that human dispatchers can inspect and trust.")
    ]

    for i, (ttitle, tdesc) in enumerate(takeaways):
        left_pos = Inches(0.8 + (i % 2) * 5.9)
        top_pos = Inches(1.6 + (i // 2) * 2.7)
        box = slide13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, top_pos, Inches(5.6), Inches(2.4))
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = BORDER_COLOR
        tf_t = box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_top = Inches(0.3)

        p = tf_t.paragraphs[0]
        p.text = ttitle
        p.font.bold = True
        p.font.size = Pt(15)
        p.font.color.rgb = NAVY

        p_d = tf_t.add_paragraph()
        p_d.text = tdesc
        p_d.font.size = Pt(12)
        p_d.font.color.rgb = DARK_GRAY
        p_d.space_before = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 14: Conclusion & Future Research
    # -------------------------------------------------------------
    slide14 = prs.slides.add_slide(blank_layout)
    set_bg(slide14)
    add_header(slide14, "13. Conclusion & Future Directions")

    c_c = slide14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    c_c.fill.solid()
    c_c.fill.fore_color.rgb = CARD_BG
    c_c.line.color.rgb = BORDER_COLOR
    tf_c = c_c.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_top = Inches(0.4)

    p = tf_c.paragraphs[0]
    p.text = "Project Summary"
    p.font.bold = True
    p.font.size = Pt(18)
    p.font.color.rgb = NAVY

    c_bullets = [
        "Developed a realistic 258-dim Gymnasium MDP environment on 274,964 NYC EMS calls.",
        "Demonstrated that static nearest routing performs best in uncongested settings (12.1 min).",
        "Proved DQN's resilience in maintaining zero overloads during high congestion and bed shortages.",
        "Highlighted the essential trade-off between driving speed and regional bed fairness."
    ]
    for b in c_bullets:
        pb = tf_c.add_paragraph()
        pb.text = "• " + b
        pb.font.size = Pt(13)
        pb.font.color.rgb = DARK_GRAY
        pb.space_before = Pt(8)

    c_f = slide14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
    c_f.fill.solid()
    c_f.fill.fore_color.rgb = CARD_BG
    c_f.line.color.rgb = BORDER_COLOR
    tf_fut = c_f.text_frame
    tf_fut.word_wrap = True
    tf_fut.margin_left = tf_fut.margin_top = Inches(0.4)

    p = tf_fut.paragraphs[0]
    p.text = "Future Research Directions"
    p.font.bold = True
    p.font.size = Pt(18)
    p.font.color.rgb = NAVY

    fut_bullets = [
        "Multi-Agent RL (MARL): Model individual ambulance units coordinating dispatch and dynamic fleet relocation.",
        "Live Traffic Streams: Integrate real-time API traffic speed updates into the distance matrix.",
        "Action Masking: Apply strict spatial proximity bounds directly to the Q-network action space."
    ]
    for b in fut_bullets:
        pb = tf_fut.add_paragraph()
        pb.text = "• " + b
        pb.font.size = Pt(13)
        pb.font.color.rgb = DARK_GRAY
        pb.space_before = Pt(10)

    # -------------------------------------------------------------
    # SLIDE 15: Thank You Slide
    # -------------------------------------------------------------
    slide15 = prs.slides.add_slide(blank_layout)
    set_bg(slide15)

    card_ty = slide15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.0), Inches(1.5), Inches(9.333), Inches(4.5))
    card_ty.fill.solid()
    card_ty.fill.fore_color.rgb = CARD_BG
    card_ty.line.color.rgb = BORDER_COLOR

    tf_ty = card_ty.text_frame
    tf_ty.word_wrap = True
    tf_ty.margin_left = tf_ty.margin_top = Inches(0.8)

    p = tf_ty.paragraphs[0]
    p.text = "Thank You!"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.alignment = PP_ALIGN.CENTER

    p2 = tf_ty.add_paragraph()
    p2.text = "Questions & Discussion"
    p2.font.size = Pt(22)
    p2.font.color.rgb = ACCENT_BLUE
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(10)

    p3 = tf_ty.add_paragraph()
    p3.text = "\nParimisetty Sneha Deepika (AV.SC.U4AIE23034)\nNakka Keerthi (AV.SC.U4AIE23032)\nAmrita Vishwa Vidyapeetham"
    p3.font.size = Pt(14)
    p3.font.color.rgb = DARK_GRAY
    p3.alignment = PP_ALIGN.CENTER
    p3.space_before = Pt(20)

    output_ppt_path = os.path.join(r"c:\Users\P.SNEHA DEEPIKA\OneDrive\Desktop\RL Project", "RL_Emergency_Allocation_Presentation.pptx")
    prs.save(output_ppt_path)
    print(f"Successfully created presentation: {output_ppt_path}")

if __name__ == "__main__":
    create_presentation()
