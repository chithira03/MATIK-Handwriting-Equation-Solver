import cv2
import numpy as np
import sympy as sp
from tensorflow.keras.models import load_model  # type: ignore
import google.generativeai as genai

# Define labels used by CNN model
labels ={0: '(', 1: ')', 2: '0', 3: '1', 4: '2', 5: '3', 6: '4', 7: '5', 8: '6', 9: '7', 10: '8', 11: '9', 12: '=', 13: '[', 14: 'c', 15: ']', 16: '+', 17: 'd', 18: '/', 19: '∫', 20: '*', 21: '-', 22: 'x', 23: 'y', 24: 'z', 25: '{', 26: '}'}

# Load your CNN model
cnn_model = load_model("cnn_model.h5")

# Configure Gemini
GEMINI_API_KEY = "AIzaSyAMlKDfIRupFqX6bQH3TEcQElwOHw90vE8"
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("models/gemini-1.5-flash")


def extract_text_from_image(image_path: str) -> str:
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    bounding_boxes = [cv2.boundingRect(c) for c in contours]
    sorted_indices = sorted(range(len(bounding_boxes)), key=lambda i: bounding_boxes[i][0])
    sorted_contours = [contours[i] for i in sorted_indices]

    chars = []
    for contour in sorted_contours:
        x, y, w, h = cv2.boundingRect(contour)
        roi = image[max(0, y - 10): y + h + 10, max(0, x - 10): x + w + 10]
        roi = cv2.resize(roi, (32, 32))
        roi = roi / 255.0
        roi = np.expand_dims(roi, axis=-1)
        roi = np.expand_dims(roi, axis=0)

        prediction = cnn_model.predict(roi)
        predicted_class = np.argmax(prediction)
        chars.append(labels.get(predicted_class, '?'))

    return ''.join(chars).strip()


def solve_symbolic_system(equations: list) -> str:
    """Solves a system of equations symbolically."""
    try:
        exprs = []
        for eq in equations:
            lhs, rhs = eq.split('=')
            exprs.append(sp.sympify(lhs) - sp.sympify(rhs))

        variables = sorted(set().union(*(expr.free_symbols for expr in exprs)), key=lambda s: str(s))
        sol = sp.solve(exprs, variables)

        return str(sol)
    except Exception as e:
        return f"❌ Error solving system: {e}"


def get_step_by_step_from_gemini(equation_list: list) -> str:
    """Gets a step-by-step solution from Gemini API for system of equations."""
    prompt = "Solve this system of equations step-by-step:\n" + "\n".join(equation_list)
    try:
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Gemini Error: {e}"


def predict_and_solve(image_paths: list):
    """Handles multiple images, solves system of equations."""
    raw_equations = []
    results = []

    for image_path in image_paths:
        raw_text = extract_text_from_image(image_path)
        raw_equations.append(raw_text)
        results.append((image_path, raw_text))  # store for UI/debug

    if all('=' in eq for eq in raw_equations):
        solution = solve_symbolic_system(raw_equations)
        steps = get_step_by_step_from_gemini(raw_equations)
    else:
        solution = "❌ One or more equations are invalid."
        steps = "No solution steps"

    final_results = []
    for path, eq in results:
        final_results.append((path, eq, solution, steps))

    return final_results
