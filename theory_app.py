import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from predict import explain_math_concept
import math


def generate_graph(expression):
    import re
    x = sp.symbols('x')

    try:
        # Fix implicit multiplication and power syntax
        if '=' in expression:
            lhs, rhs = expression.split('=')
            expression = rhs.strip()
        expression = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expression)
        expression = expression.replace("^", "**")

        expr = sp.sympify(expression)
        f = sp.lambdify(x, expr, "numpy")

        x_vals = np.linspace(-10, 10, 400)
        y_vals = f(x_vals)

        fig, ax = plt.subplots(figsize=(5, 3))  # Set a smaller figure size
        ax.plot(x_vals, y_vals, label=f"${sp.latex(expr)}$")
        ax.set_title("Graph")
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.grid(True)
        ax.legend()

        # Adjust layout for better spacing and remove unnecessary parts
        plt.tight_layout(pad=1.0)  # Adding padding to reduce the need for scrolling
        st.pyplot(fig)
        return True
    except Exception as e:
        st.error(f"Graph generation failed: {e}")
        return False





def theory_solver():
    st.title("🧠 Math Theory Solver")

    st.markdown("### Ask any math theory question:")
    question = st.text_area(
        "Enter your question (e.g., 'Explain quadratic equations', 'Graph of sin(x)')",
        height=150,
        key="theory_question"
    )

    if st.button("Generate Explanation"):
        if question.strip():
            with st.spinner("Generating detailed explanation..."):
                explanation = explain_math_concept(question)

            st.markdown("### 📚 Detailed Explanation")
            st.markdown(explanation)

            # Optional: Try to detect if the question involves plotting
            if any(word in question.lower() for word in ["graph", "plot"]):
                # Try to extract a mathematical expression from the question
                import re
                match = re.search(r"(?:graph|plot)\s+(?:of\s+)?(.+)", question.lower())
                if match:
                    expression = match.group(1)
                    st.markdown("### 📈 Generated Graph")
                    generate_graph(expression)
                else:
                    st.info("Couldn't extract a valid expression for graphing.")
        else:
            st.warning("Please enter a question first.")

if __name__ == "__main__":
    theory_solver()
