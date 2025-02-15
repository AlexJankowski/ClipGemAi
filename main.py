import tkinter as tk
from tkinter import ttk
import google.generativeai as genai
import pyperclip  # For clipboard operations
import pyautogui
import keyboard  # For hotkey binding
import time

# !
# CONFIGURE GEMINI API
# !
genai.configure(api_key="YOUR_API_KEY")  # REPLACE WITH YOUR ACTUAL API KEY 
model = genai.GenerativeModel("gemini-2.0-flash") # CHANGE MODEL ACCORDING TO YOUR NEEDS

# Global variables
popup_window = None
ai_request_entry = None
ai_response_text = None
last_response = ""  # Stores last AI response
original_cursor_position = None  # Stores the original cursor position
response_generated = False  # Tracks if the response has been generated

# !
# ADD MORE STRINGS TO REMOVE FROM PASTED TEXT IF NEEDED
# !
# Dictionary of strings to be removed from the pasted text
strings_to_remove = {
    "```python": "",  # Remove triple backticks with python
    "```": "",  # Remove triple backticks
    # Add more strings here if needed
    # Example: "**": "",  # Remove double asterisks
}


def fetch_ai_response(prompt):
    """Send the prompt to Gemini and get a concise response."""
    try:
        formatted_prompt = f"Provide a concise response:\n\n{prompt}"
        response = model.generate_content(formatted_prompt)
        return response.text if hasattr(response, "text") else "Error: No response text found."
    except Exception as e:
        return f"Error fetching response: {e}"


def show_popup(copied_text=None):
    """Show input popup above the cursor and track cursor position."""
    global popup_window, ai_request_entry, ai_response_text, last_response, original_cursor_position, response_generated

    if popup_window is None or not popup_window.winfo_exists():
        # Create the popup window if it doesn't exist
        popup_window = tk.Toplevel(root)
        popup_window.title("AI Request")
        popup_window.overrideredirect(True)  # Remove title bar
        popup_window.configure(bg="#333333")

        # Input field for user request
        ai_request_entry = tk.Entry(popup_window, width=40, font=("Arial", 12), bg="#222222", fg="#00FF00", insertbackground="#FFD700", relief="solid")
        ai_request_entry.pack(padx=10, pady=5, fill=tk.BOTH, expand=False)
        ai_request_entry.bind('<Return>', handle_enter)  # Handle Enter key
        ai_request_entry.bind('<Escape>', lambda e: hide_popup())

        # Response field (non-editable)
        ai_response_text = tk.Text(popup_window, height=4, wrap=tk.WORD, font=("Arial", 12), bg="#222222", fg="#FFFFFF", relief="solid")
        ai_response_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        ai_response_text.config(state=tk.DISABLED)

        # Buttons
        button_frame = tk.Frame(popup_window, bg="#333333")
        button_frame.pack(pady=5)

        paste_button = ttk.Button(button_frame, text="Paste on Cursor (Enter)", command=paste_ai_response_at_cursor)
        paste_button.grid(row=0, column=0, padx=5)

        copy_button = ttk.Button(button_frame, text="Copy to Clipboard (Ctrl+C)", command=copy_to_clipboard)
        copy_button.grid(row=0, column=1, padx=5)

        # Make the window always on top
        popup_window.attributes('-topmost', True)
        popup_window.protocol("WM_DELETE_WINDOW", hide_popup)

        # Bind FocusOut event to hide the popup when clicked outside
        popup_window.bind("<FocusOut>", lambda e: hide_popup_if_needed())

    # Update the popup's position to the current cursor location
    x, y = root.winfo_pointerx(), root.winfo_pointery() - 120  # Adjusted for above
    popup_window.geometry(f"400x180+{x}+{y}")

    # Reset state when showing the popup
    response_generated = False
    popup_window.deiconify()
    popup_window.focus_force()
    ai_request_entry.focus_set()
    ai_request_entry.delete(0, tk.END)
    ai_response_text.config(state=tk.NORMAL)
    ai_response_text.delete(1.0, tk.END)
    ai_response_text.config(state=tk.DISABLED)

    # Store the original cursor position
    original_cursor_position = pyautogui.position()

    # Paste the copied text into the input field if any
    if copied_text:
        ai_request_entry.insert(0, copied_text)


def hide_popup_if_needed():
    """Hide the popup window if focus is lost."""
    global popup_window
    if popup_window and popup_window.winfo_exists():
        # Check if the focus is still within the popup window
        if not popup_window.focus_get():
            hide_popup()


def hide_popup():
    """Hide the popup window."""
    global popup_window
    if popup_window:
        popup_window.withdraw()


def handle_enter(event=None):
    """Handle Enter key: Generate response on first press, paste on second press."""
    global last_response, response_generated

    if not response_generated:
        # First Enter: Generate response
        request = ai_request_entry.get().strip()
        if request:
            ai_response = fetch_ai_response(request)
            last_response = ai_response  # Store for pasting/copying

            ai_response_text.config(state=tk.NORMAL)
            ai_response_text.delete(1.0, tk.END)
            ai_response_text.insert(tk.END, ai_response)
            ai_response_text.config(state=tk.DISABLED)  # Lock response field
            response_generated = True
    else:
        # Second Enter: Paste response at original cursor position
        paste_ai_response_at_cursor()
        hide_popup()


def remove_unwanted_strings(text):
    """Remove unwanted strings from the text based on the dictionary."""
    for string_to_remove, replacement in strings_to_remove.items():
        text = text.replace(string_to_remove, replacement)
    return text


def paste_ai_response_at_cursor():
    """Paste stored AI response at the original cursor position."""
    global last_response, original_cursor_position
    if last_response:
        hide_popup()
        pyautogui.moveTo(original_cursor_position.x, original_cursor_position.y)
        pyautogui.click()
        
        # Remove trailing whitespace and newline characters
        cleaned_response = last_response.rstrip()
        
        # Remove unwanted strings (e.g., triple backticks)
        cleaned_response = remove_unwanted_strings(cleaned_response)
        
        # Copy the cleaned response to the clipboard
        pyperclip.copy(cleaned_response)
        
        # Simulate Ctrl+V to paste the text
        pyautogui.hotkey('ctrl', 'v')


def copy_to_clipboard():
    """Copy AI response to clipboard."""
    global last_response
    if last_response:
        pyperclip.copy(last_response)
        ai_response_text.config(state=tk.NORMAL)
        ai_response_text.insert(tk.END, "\n\nCopied to clipboard!")
        ai_response_text.config(state=tk.DISABLED)


def on_hotkey():
    """Handle the hotkey press (Shift+Win+V) and ensure text is copied before opening popup."""
    # Save current clipboard content
    previous_clipboard = pyperclip.paste()

    # Clear clipboard to detect new copied text
    pyperclip.copy("")  
    time.sleep(0.1)  # Small delay to allow clipboard to clear

    # Simulate Ctrl+C (forcing copy)
    pyautogui.hotkey('ctrl', 'c')

    # Wait for clipboard to update (max 0.1 sec)
    timeout = 0.1  # Maximum wait time in seconds
    start_time = time.time()
    copied_text = ""

    while time.time() - start_time < timeout:
        copied_text = pyperclip.paste().strip()
        if copied_text and copied_text != previous_clipboard:  # Ensure clipboard actually updated
            break
        time.sleep(0.05)  # Check clipboard every 50ms

    # If clipboard is still empty, force a second Ctrl+C attempt
    if not copied_text:
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.1)  # Give it some time to update
        copied_text = pyperclip.paste().strip()

    # Open popup with copied text (if available)
    show_popup(copied_text=copied_text if copied_text else None)


# Initialize Tkinter window
root = tk.Tk()
root.withdraw()  # Hide main window

# !
# CHANGE POPUP HOTKEY IF NEEDED
# !
# Hotkey binding (Shift+Win+V to show the popup)
keyboard.add_hotkey("shift+win+v", on_hotkey)

root.mainloop()


