# ✍️ Matik: Handwritten Equation Solver
Matik is an advanced web-based application built using Deep Learning (CNN) and Streamlit, designed to recognize and solve handwritten mathematical equations. Whether it’s simple arithmetic or systems of linear equations, Matik turns handwritten inputs into accurate results in just a few seconds.

### 🧭 App Tabs Overview
The Matik app is divided into three functional tabs, each designed to simplify different aspects of solving and understanding mathematical problems:

#### 🧮 1. Equation Solver Tab
In this tab, users can write equations directly on a canvas using a stylus or mouse. Once the equation is recognized by the CNN model, Matik processes and solves it in real-time. It supports:

**✅ Basic Arithmetic Equations**
Examples: 5 + 3 * 2, 12 / 4 - 1

**✅ Algebraic Expressions**
Examples: 2x + 3 = 9, x^2 + 5x + 6 = 0

**✅ Calculus Operations**
Derivatives: d/dx (x^3 + 2x)
Integrals: ∫ (2x) dx

**🔍 Detailed Explanation:**
After identifying the handwritten input, Matik reconstructs it into a valid equation and provides a step-by-step solution using symbolic mathematics libraries like **SymPy.**

#### 📐 2. Linear Solver Tab
This tab specializes in solving linear systems of equations with 2 or 3 variables. After writing multiple equations (e.g., one below the other), the model recognizes each, forms a system, and computes the solution.

#### 📘 3. Theory Tab
This tab is powered by Gemini API and is designed for conceptual learning. Users can type any theoretical math question such as:

"What is the derivative of a function?"
"What are the properties of linear equations?"

**📖 Output:**
The app fetches a detailed, easy-to-understand explanation using LLMs, making it ideal for revision and foundational understanding.


