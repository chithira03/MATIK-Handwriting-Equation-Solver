import streamlit as st
from streamlit_drawable_canvas import st_canvas
import os
import cv2
from predict import predict
from predict2 import predict_and_solve
from theory_app import theory_solver
import time
import random
import requests
import base64
import json
import numpy as np
import streamlit_lottie as st_lottie

# --- App Config ---
st.set_page_config(page_title="Matik AI Solver", layout="wide", page_icon="📐")
os.makedirs("temp", exist_ok=True)

# --- Load custom theme directly here ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

* {
    font-family: 'Inter', sans-serif !important;
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

html, body, [class*="css"] {
    background-color: #0f172a;
    color: #e2e8f0;
}

/* Sidebar Title */
.sidebar-title {
    font-size: 24px;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    color: #38bdf8;
    text-align: center;
    margin-bottom: 20px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Headings */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #38bdf8;
    margin-bottom: 0.5rem;
}

/* Card Layout */
.card {
    background-color: #1e293b;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 2px 12px rgba(0, 255, 255, 0.05);
    height: 100%;
    text-align: center;
    margin-bottom: 1.5rem;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.card:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 20px rgba(56, 189, 248, 0.2);
}

/* Circular Team Images */
.circular-img {
    border-radius: 50%;
    width: 150px;
    height: 150px;
    object-fit: cover;
    border: 3px solid #38bdf8;
    margin-bottom: 15px;
    transition: transform 0.3s ease;
}
.circular-img:hover {
    transform: scale(1.1);
}

/* Button Custom Styling */
.stButton > button {
    background-color: #38bdf8;
    color: white;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 600;
    text-transform: uppercase;
    border: none;
    cursor: pointer;
    transition: background-color 0.3s ease;
}
.stButton > button:hover {
    background-color: #0284c7;
}

/* Spacing and Layout Enhancements */
h3 {
    margin-top: 2rem;
    margin-bottom: 1rem;
}
.team-bio {
    margin-top: 1rem;
    margin-bottom: 1.5rem;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


# --- Session State for Navigation ---
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"
if "last_page" not in st.session_state:
    st.session_state.last_page = "Home"

# --- Sidebar Navigation ---
pages = ["Home", "Equation Solver", "Linear Solver", "Theory", "About"]
st.sidebar.markdown("<div class='sidebar-title'>Matik AI</div>", unsafe_allow_html=True)
menu = st.sidebar.radio("Navigate", pages, index=pages.index(st.session_state.current_page))
st.session_state.current_page = menu

# --- Page Transition Effect ---
if st.session_state.current_page != st.session_state.last_page:
    with st.spinner("Loading..."):
        time.sleep(0.4)
    st.session_state.last_page = st.session_state.current_page

# --- Home Page ---
if st.session_state.current_page == "Home":
    def load_lottie_url(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    lottie_animation = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_qp1q7mct.json")

    st.markdown("""
    <div class="card">
        <h1>Matik AI Solver</h1>
        <p>Visual AI-powered tool to solve math through drawing. Ideal for learners, educators, and visual problem solvers.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.columns([1, 2, 1])[1]:
        st_lottie.st_lottie(lottie_animation, speed=1, height=280, key="hero_anim")

    st.markdown("### Features")
    col1, col2, col3 = st.columns(3)
    feature_cards = [
        ("Draw Equations", "Sketch math problems naturally using an intuitive canvas."),
        ("AI Recognition", "Real-time visual recognition of equations and expressions."),
        ("Learn by Solving", "Explore theory and step-by-step solutions.")
    ]
    for col, (title, desc) in zip([col1, col2, col3], feature_cards):
        with col:
            st.markdown(f"""
            <div class='card' style='min-height: 200px;'>
                <h4>{title}</h4>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    facts = [
    " The word *'mathematics'* comes from the Greek *'mathema'*, meaning 'knowledge' or 'learning'.",
    " Zero is the only number that can't be represented in Roman numerals.",
    " A palindrome date like 02/02/2020 reads the same forward and backward—a math and calendar rarity!",
    " A googol has more zeros than the estimated number of atoms in the observable universe.",
    " The symbol for infinity (∞) was introduced by mathematician John Wallis in 1655.",
    " Ancient Babylonians used base-60 instead of base-10, which is why we have 60 seconds in a minute!"
    ]

    st.markdown(f"""
    <div class='card' style='margin:auto; max-width: 800px;'>
        <h4>Did You Know?</h4>
        <p>{random.choice(facts)}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    st.markdown("### Explore")
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)  # Adds spacing
    colA, colB, colC = st.columns(3)
    if colA.button("Equation Solver", key="eq_btn"):
        st.session_state.current_page = "Equation Solver"
    if colB.button("Linear Solver", key="lin_btn"):
        st.session_state.current_page = "Linear Solver"
    if colC.button("Theory", key="theory_btn"):
        st.session_state.current_page = "Theory"

    st.markdown("""
    <hr style="margin-top: 3rem; margin-bottom: 1rem;">
    <div style='text-align:center; font-size: 14px; color:#94a3b8;'>
    Made with ❤️ by Team Matik | 
    <a href='https://linkedin.com' target='_blank' style='color:#38bdf8;'>LinkedIn</a> | 
    <a href='mailto:support@matik.ai' style='color:#38bdf8;'>Contact</a>
    </div>
    """, unsafe_allow_html=True)
   
# --- EQUATION SOLVER PAGE ---
if st.session_state.current_page == "Equation Solver":
    st.header("Equation Solver")
    st.markdown("Draw a math problem below and click Solve!")
    stroke_width = st.slider("Pen Thickness", 2, 10, 4)
    data = st_canvas(
    stroke_width=stroke_width,
    stroke_color="#000000",  # Black stroke
    background_color="#FFFFFF",  # White canvas
    height=400,
    width=1000,
    drawing_mode="freedraw",
    key="canvas",
)

    col1, col2 = st.columns(2)
    solve_clicked = col1.button("Solve", use_container_width=True)
    if col2.button("Clear Canvas", use_container_width=True):
        st.session_state.current_page = "Equation Solver"

    if data.image_data is not None and solve_clicked:
        with st.spinner("Analyzing Equation..."):
            img_path = "temp/temp.png"
            cv2.imwrite(img_path, data.image_data)
            try:
                result = predict(img_path)
                equation, boxed_answer, step_by_step_solution = result
            except Exception as e:
                st.error(f"Error: {e}")
    elif not solve_clicked:
        st.info("Draw and click Solve to continue.")

# --- LINEAR SOLVER PAGE ---
if st.session_state.current_page == "Linear Solver":
    st.header("Linear Equation Solver")
    degree = st.radio("Select number of variables:", ["2-variable", "3-variable"], horizontal=True)
    stroke_width = st.slider("Stroke Width", 3, 10, 5, key="canvas_slider_2")
    eq_paths = []
    canvas_configs = [("Equation 1", "eq1_canvas"), ("Equation 2", "eq2_canvas")] if degree == "2-variable" else [
        ("Equation 1", "eq3_canvas"),
        ("Equation 2", "eq4_canvas"),
        ("Equation 3", "eq5_canvas"),
    ]
    for idx, (label, key) in enumerate(canvas_configs):
        st.markdown(f"### Draw {label}")
        canvas = st_canvas(
            stroke_width=stroke_width,
            stroke_color="#000000",  # Black stroke
            background_color="#FFFFFF",  # White canvas
            height=400,
            width=1000,
            drawing_mode="freedraw",
            key=key,
        )
        if canvas.image_data is not None:
            path = f"temp/eq_{idx + 1}.png"
            cv2.imwrite(path, canvas.image_data)
            eq_paths.append(path)

    if st.button("Solve Linear System"):
        expected = 2 if degree == "2-variable" else 3
        if len(eq_paths) != expected:
            st.warning("Please draw all required equations.")
        else:
            try:
                result = predict_and_solve(eq_paths)
                st.markdown("### Recognized Equations:")
                for _, eq, _, _ in result:
                    st.markdown(f"<div class='card'>{eq}</div>", unsafe_allow_html=True)
                if result:
                    _, _, solution, steps = result[0]
                    st.markdown("### Step-by-step solution:")
                    st.markdown(f"<div class='card'>{steps}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error solving equations: {e}")

# --- THEORY PAGE ---
if st.session_state.current_page == "Theory":
    st.header("Theory Learning Hub")
    st.markdown("""
    <div class='card'>
        <h3>Concepts and Formulas</h3>
        <p>Explore math rules and logic. Reinforce learning with explanations and examples.</p>
    </div>
    """, unsafe_allow_html=True)
    theory_solver()

# --- ABOUT PAGE --- 
if st.session_state.current_page == "About":
    st.header("About Matik AI")
    st.markdown("""
    <div class='card' style='margin-bottom: 2rem;'>
        <h3>Our Mission</h3>
        <p>At Matik AI, we strive to make mathematics easier, visual, and smarter using AI technology. We aim to enhance learning and problem-solving skills, empowering students and educators to achieve success in math.</p>
    </div>
    """, unsafe_allow_html=True)

    # Team Bios Section with Circular Images and Hover Effects
    st.markdown("### Meet the Team")
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.markdown(f"""
        <div class='team-bio'>
            <img src='data:image/jpeg;base64,{base64.b64encode(open('swathi.jpeg', 'rb').read()).decode()}' class='circular-img'>
            <div class='card'>
                <h4>Swathi</h4>
                <p><strong>Role:</strong> Frontend/UI Developer</p>
                <p>Designed and built the interactive user experience, ensuring usability and responsiveness.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='team-bio'>
            <img src='data:image/jpeg;base64,{base64.b64encode(open('sejal.jpeg', 'rb').read()).decode()}' class='circular-img'>
            <div class='card'>
                <h4>Sejal</h4>
                <p><strong>Role:</strong> AI & Backend Developer</p>
                <p>Integrated advanced AI models for equation recognition and solver logic.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class='team-bio'>
            <img src='data:image/jpeg;base64,{base64.b64encode(open('chithira.jpeg', 'rb').read()).decode()}' class='circular-img'>
            <div class='card'>
                <h4>Chithira</h4>
                <p><strong>Role:</strong> Lead & Backend Developer</p>
                <p>Developed the learning modules, focusing on clear explanations and logical step-by-step solutions.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

else:           
    st.markdown("""
    <style>
    .sidebar-title {
        font-size: 24px;
        font-weight: bold;
        color: #38bdf8;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)    