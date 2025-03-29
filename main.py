import sys
import os  # Import the os module
import google.generativeai as genai  # Import the Gemini library
from dotenv import load_dotenv  # Import dotenv

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QTextEdit)

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API key
try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "API key not found. Make sure it's set in the .env file.")
    genai.configure(api_key=api_key)
    # Create the model instance (e.g., gemini-1.5-flash)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"Error configuring AI model: {e}")
    # Optionally: disable button or show error message in UI
    model = None  # Indicate that the model couldn't be loaded


# Function to be called when the button is clicked
def on_button_click():
    if not model:
        text_area.append(
            "Error: AI Model not initialized. Check API key and configuration."
        )
        return

    print("Button 'I Got an Idea!' clicked! Calling AI...")
    text_area.append("Okay, let's brainstorm your new idea... (Calling AI)")

    # --- Make the API Call ---
    # This is a simple, *blocking* call. The UI will freeze temporarily.
    try:
        # Define a simple starting prompt
        prompt = "You are a helpful brainstorming assistant. A user has clicked 'I Got an Idea!'. Start a short, encouraging conversation to help them begin describing their idea. Ask one open-ended question."
        response = model.generate_content(prompt)

        # Append the AI's response to the text area
        text_area.append("\nAI Assistant:")
        text_area.append(
            response.text)  # Use response.text to get the string content

    except Exception as e:
        print(f"Error during AI generation: {e}")
        text_area.append(f"\nError communicating with AI: {e}")
    # --- End API Call ---


# --- UI Setup (mostly unchanged) ---
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('Isekai Developer - Brainstorm Assistant')
window.setGeometry(200, 200, 500, 400)

idea_button = QPushButton("I Got an Idea!")
text_area = QTextEdit()
text_area.setReadOnly(True)

main_layout = QVBoxLayout()
main_layout.addWidget(idea_button)
main_layout.addWidget(text_area)
window.setLayout(main_layout)

# Disable button if model failed to load
if not model:
    idea_button.setEnabled(False)
    idea_button.setText("AI Error - Check Console")  # Update button text

idea_button.clicked.connect(on_button_click)
window.show()
sys.exit(app.exec_())
