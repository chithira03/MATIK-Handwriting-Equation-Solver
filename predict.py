import cv2
import numpy as np
from keras.models import load_model  # type: ignore
import streamlit as st
import google.generativeai as genai
import sympy as sp

# Define 
labels ={0: '(', 1: ')', 2: '0', 3: '1', 4: '2', 5: '3', 6: '4', 7: '5', 8: '6', 9: '7', 10: '8', 11: '9', 12: '=', 13: '[', 14: 'c', 15: ']', 16: '+', 17: 'd', 18: '/', 19: '∫', 20: '*', 21: '-', 22: 'x', 23: 'y', 24: 'z', 25: '{', 26: '}'}

# Load CNN model
model = load_model('cnn_model.h5')

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyAMlKDfIRupFqX6bQH3TEcQElwOHw90vE8" 
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("models/gemini-1.5-flash")


def fix_x_vs_multiplication(equation_chars):
    fixed = []
    for i, ch in enumerate(equation_chars):
        if ch == '*':
            if (i > 0 and equation_chars[i - 1].isalnum()) and (i + 1 < len(equation_chars) and equation_chars[i + 1].isalnum()):
                fixed.append('x')
            else:
                fixed.append('*')
        else:
            fixed.append(ch)
    return ''.join(fixed)


def get_step_by_step_solution(equation):
    prompt = f"""
You are a math tutor.

Simplify or solve the following math input step-by-step with clear *explanations*.

📌 Instructions:
- If it's an expression (like 2*3+5), simplify it step-by-step
- If it's an equation (like 2x + 3 = 7), solve it
- Explain what is happening in each step
- Use this structure:

Step 1: Explain the action  
Formula: *...*

Step 2: Explain the next step  
Formula: *...*

...

Final Answer: ...

Now solve this:

{equation}
"""
    try:
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating solution: {e}"



def get_final_answer_from_gemini(equation):
    prompt = f"""
You are a calculator. Simplify or solve the following and return only the final answer.

Input: {equation}

Final Answer:
"""
    try:
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error solving with Gemini: {e}"


def get_final_answer_from_gemini(equation):
    prompt = f"Solve this equation and only show the final answer: {equation}"
    try:
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error solving with Gemini: {e}"


def predict(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    bounding_boxes = [cv2.boundingRect(c) for c in contours]
    sorted_indices = sorted(range(len(bounding_boxes)), key=lambda i: bounding_boxes[i][0])
    sorted_contours = [contours[i] for i in sorted_indices]
    bounding_boxes = [bounding_boxes[i] for i in sorted_indices]

    rois = []
    for contour in sorted_contours:
        x, y, w, h = cv2.boundingRect(contour)
        roi = image[max(0, y - 10): y + h + 10, max(0, x - 10): x + w + 10]
        roi = cv2.resize(roi, (32, 32))
        rois.append(roi)

    rois = np.array(rois) / 255.0
    rois = np.expand_dims(rois, axis=-1)
    predictions = model.predict(rois)
    predicted_labels = np.argmax(predictions, axis=1)

    # Merge two consecutive '-' as '='
    merged_labels = []
    skip_next = False
    i = 0
    while i < len(predicted_labels):
        if skip_next:
            skip_next = False
            i += 1
            continue

        current_label = predicted_labels[i]

        if (current_label == 15  # '-'
                and i + 1 < len(predicted_labels)
                and predicted_labels[i + 1] == 15):

            # Get bounding boxes to check alignment
            x1, y1, w1, h1 = bounding_boxes[i]
            x2, y2, w2, h2 = bounding_boxes[i + 1]

            # Check if they are horizontally aligned and close
            if abs(y1 - y2) < 10 and abs(h1 - h2) < 10:
                merged_labels.append(10)  # '='
                skip_next = True
            else:
                merged_labels.append(current_label)
        else:
            merged_labels.append(current_label)
        i += 1

    raw_equation = [labels[i] for i in merged_labels]
    lhs_equation = fix_x_vs_multiplication(raw_equation)

    # Use the full equation
    full_equation = lhs_equation

    # Draw predicted symbols
    image_color = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    for i, contour in enumerate(sorted_contours):
        x, y, w, h = cv2.boundingRect(contour)
        if i < len(merged_labels):
            label = labels[merged_labels[i]]
            cv2.rectangle(image_color, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(image_color, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    st.image(cv2.cvtColor(image_color, cv2.COLOR_BGR2RGB))

    # Get Gemini output
    steps = get_step_by_step_solution(full_equation)
    final_answer = get_final_answer_from_gemini(full_equation)

    # Clean unwanted trailing div
    if steps.strip().endswith("</div>"):
        steps = steps.strip()[:-6].strip()

    # Display
    st.subheader("Recognized Equation:")
    st.write(full_equation)

    st.subheader("📘 Step-by-Step Solution")
    st.markdown(
        f"""
        <div style="
            background-color: #0d1117;
            color: white;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #22c55e;
            font-size: 16px;
            white-space: pre-wrap;
        ">{steps}</div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Final Answer:")
    st.write(final_answer)

    return full_equation, final_answer, steps


def explain_math_concept(question):
    prompt = f"""
You are a math tutor.

Solve the following math or logic question with a very clean, step-by-step explanation.

📌 Instructions:
- Start solving immediately (no definitions or theory)
- Break the solution into numbered steps
- Explain what's being done in each step
- Write all formulas bold and on their own separate lines
- Ensure correct integer logic (no approximations unless explicitly required)
- End with the final answer clearly labeled and on its own line

📘 Use this format exactly:
Step 1: ...
Formula: ...
Step 2: ...
Formula: ...
...
Final Answer: ...

Now solve the question:

Question: {question}

Answer:
"""
    try:
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating explanation: {e}"