import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import cv2
import re
from predict2 import extract_text_from_image
import google.generativeai as genai

# Configure your Gemini API key
genai.configure(api_key="AIzaSyDdi6rv4rBvRJjrNvOxbvGojsEviMN-euA")

def explain_graph_with_gemini(equation: str) -> str:
    prompt = f"Explain the graph of the mathematical equation y = {equation} in simple terms."
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")
    response = model.generate_content(prompt)
    return response.text

def graph_plotter():
    st.title("📈 Graph Plotter")
    st.markdown("Visualize mathematical functions by entering equations below.")
    
    input_method = st.radio("Input method:", ["Type Equation", "Draw Eq"], horizontal=True)
    
    if input_method == "Type Equation":
        equation_input = st.text_input("Enter your equation (e.g., y = 2*x + 1, Use * for multiplication, ** for exponents)")
        
        if st.button("Plot Graph"):
            try:
                equation = equation_input.split('=')[1].strip() if '=' in equation_input else equation_input.strip()
                x = sp.symbols('x')
                expr = sp.sympify(equation)
                f = sp.lambdify(x, expr, modules=['numpy'])

                x_vals = np.linspace(-10, 10, 400)
                y_vals = f(x_vals)
                if np.isscalar(y_vals):
                    y_vals = np.full_like(x_vals, y_vals)

                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(x_vals, y_vals, label=equation_input, color='#22c55e', linewidth=3)
                ax.set_title(f"Graph of {equation_input}")
                ax.set_xlabel("x")
                ax.set_ylabel("y")
                ax.grid(True)
                ax.axhline(0, color='black', linewidth=0.5)
                ax.axvline(0, color='black', linewidth=0.5)
                ax.legend()

                st.pyplot(fig)
                with st.spinner("Explaining the graph..."):
                    explanation = explain_graph_with_gemini(equation)
                    st.markdown("### 🤖 Graph Explanation")
                    st.write(explanation)

            except Exception as e:
                st.error(f"Error plotting equation: {e}. Please check your input format.")

    else:  # Draw Equation
        st.markdown("### ✏️ Draw Your Equation")
        stroke_width = st.slider("Stroke Width", 3, 10, 5, key="canvas_slider_4")

        st.markdown('<div class="canvas-border">', unsafe_allow_html=True)
        canvas_data = st_canvas(
            stroke_width=stroke_width,
            stroke_color="black",
            background_color="white",
            height=300,
            width=1200,
            drawing_mode="freedraw",
            key="graph_canvas",
        )
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("Plot Drawn Equation"):
            if canvas_data.image_data is not None:
                try:
                    img_path = "temp/graph_eq.png"
                    cv2.imwrite(img_path, canvas_data.image_data)

                    equation = extract_text_from_image(img_path)

                    if equation:
                        st.write(f"Extracted Equation: `{equation}`")

                        superscripts = {'²': '2', '³': '3', '¹': '1'}
                        for sup, normal in superscripts.items():
                            equation = equation.replace(sup, f'**{normal}')

                        equation = equation.replace('^', '**')
                        equation = re.sub(r'[^0-9xXyY\+\-\*/\.\=\(\)\s]', '', equation)
                        equation = equation.replace('==', '=')
                        equation = equation.lower().strip()
                        equation = re.sub(r'\bx(\d+)\b', r'x**\1', equation)
                        equation = re.sub(r'(x)\1{2}', r'x**3', equation)
                        equation = re.sub(r'(x)\1{1}', r'x**2', equation)
                        equation = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', equation)
                        equation = re.sub(r'([a-zA-Z])(\()', r'\1*\2', equation)
                        equation = re.sub(r'(\))([a-zA-Z0-9])', r'\1*\2', equation)

                        if '=' in equation:
                            equation = equation.split('=', 1)[1].strip()

                        try:
                            x = sp.symbols('x')
                            expr = sp.sympify(equation)
                            f = sp.lambdify(x, expr, modules=['numpy'])

                            x_vals = np.linspace(-10, 10, 400)
                            y_vals = f(x_vals)
                            if np.isscalar(y_vals):
                                y_vals = np.full_like(x_vals, y_vals)

                            fig, ax = plt.subplots(figsize=(10, 6))
                            ax.plot(x_vals, y_vals, label=f"y = {equation}", color='#22c55e', linewidth=3)
                            ax.set_title(f"Graph of y = {equation}")
                            ax.set_xlabel("x")
                            ax.set_ylabel("y")
                            ax.grid(True)
                            ax.axhline(0, color='black', linewidth=0.5)
                            ax.axvline(0, color='black', linewidth=0.5)
                            ax.legend()

                            st.pyplot(fig)

                            with st.spinner("Explaining the graph..."):
                                explanation = explain_graph_with_gemini(equation)
                                st.markdown("### 🤖 Graph Explanation")
                                st.write(explanation)

                        except Exception as e:
                            st.error(f"Could not parse or evaluate the equation: {equation}. Error: {e}")
                    else:
                        st.warning("Could not recognize the equation. Please try drawing more clearly.")
                except Exception as e:
                    st.error(f"Error processing drawn equation: {e}")
            else:
                st.warning("Please draw an equation first.")