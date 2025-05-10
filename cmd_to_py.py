import os
import re
import subprocess
import webbrowser
import platform
import psutil  # For process management
from groq import Groq
from store import API_KEY
from hotword2 import speak

def generate_python_code(command: str) -> str:
    """Generates Python code based on the user's command using the Groq API."""
    client = Groq(api_key=API_KEY())

    system_prompt = """You are an expert programmer. Convert the user's command into a working Python script if it requires code execution.
Return ONLY the code without any explanations or markdown formatting when code is needed. No explanations like here is the code, just return code
Ensure the code is safe and does not contain infinite loops.

If the user's command is a simple statement or question that doesn't require code execution, respond directly with the answer as a plain string.

For system-level commands like volume and brightness control, prioritize platform-independent Python libraries if available. If platform-specific commands are necessary, ensure they are standard and widely available on the target OS.

On Windows, consider using the 'winsound' module for basic sound operations or platform-specific APIs via libraries like 'pycaw' (if the user is likely to have it installed, otherwise avoid external dependencies). For brightness, avoid relying on external executables unless explicitly requested by the user.

Focus on the following types of commands that require code:
- Opening websites (webbrowser module).
- Controlling specific applications (taskkill/start on Windows, osascript on macOS, pkill/killall/xdg-open on Linux).
- Basic system interactions (volume, brightness) using platform-appropriate and preferably built-in or very common tools/libraries.

Structure your response appropriately:
- If code is needed, return a complete, executable Python code snippet, including necessary imports and robust error handling.
- If no code is needed, return a plain string response.

Do not use libraries like pyautogui for UI automation unless absolutely necessary and explicitly requested. Avoid relying on external executables like nircmd unless you can be reasonably sure the user has them installed and configured in their PATH."""

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": command}
            ],
            model="llama3-70b-8192",
            temperature=0.3
        )
        content = response.choices[0].message.content.strip()
        # Improved code extraction to remove any surrounding text
        code_match = re.search(r"```python\s*(.*?)\s*```", content, re.DOTALL)
        if code_match:
            cleaned_code = code_match.group(1).strip()
            return cleaned_code
        else:
            return content  # Return as a plain string if no code block is clearly detected
    except Exception as e:
        return f"Error generating response: {str(e)}"

def execute_python_code(code_or_text):
    """Attempts to execute Python code and returns the result or the original text if execution fails."""
    if code_or_text.startswith("Error generating"):
        return code_or_text

    try:
        print("Attempting to execute generated code...")
        namespace = {}
        exec(code_or_text, globals(), namespace)
        if "output" in namespace:
            output = namespace["output"]
            print("Generated output:", output)
            return output
        elif code_or_text.strip():
            return "Command executed successfully."
        else:
            return None  # No output
    except Exception as e:
        print("Execution failed, returning as direct response:", code_or_text)
        return code_or_text