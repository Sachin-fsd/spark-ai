import tkinter as tk
from tkinter import scrolledtext, ttk
import time
import random
from cmd_to_py import generate_python_code
from cmd_to_py import execute_python_code
from hotword2 import speak

class AssistantGUI:
    def __init__(self, master):
        self.master = master
        master.title("AI Assistant")

        style = ttk.Style()
        style.theme_use('clam')

        self.command_label = ttk.Label(master, text="Enter Command:")
        self.command_label.pack(pady=5, padx=10, anchor=tk.W)

        self.command_entry = ttk.Entry(master, width=50)
        self.command_entry.pack(pady=5, padx=10, fill=tk.X)
        self.command_entry.bind("<Return>", self.execute_command_from_entry)
        self.command_entry.focus_set()

        self.execute_button = ttk.Button(master, text="Execute", command=self.execute_command)
        self.execute_button.pack(pady=10, padx=10, fill=tk.X)

        self.output_label = ttk.Label(master, text="Output:")
        self.output_label.pack(pady=5, padx=10, anchor=tk.W)

        self.output_text = scrolledtext.ScrolledText(master, width=60, height=15, wrap=tk.WORD)
        self.output_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.output_text.config(state=tk.DISABLED)

        master.columnconfigure(0, weight=1)
        master.rowconfigure(3, weight=1)

        self.acknowledgements = [
            "Processing...",
            "Working...",
            "Let me see...",
            "One moment...",
            "Sure!",
            "Understood.",
            "Executing...",
            "Just a second...",
            "Wait...",
            "Alright!",
            "Doing it sir!"
        ]

    def execute_command(self):
        command = self.command_entry.get()
        self.command_entry.delete(0, tk.END)
        self.process_command(command)

    def execute_command_from_entry(self, event):
        command = self.command_entry.get()
        self.command_entry.delete(0, tk.END)
        self.process_command(command)

    def process_command(self, command):
        if command:
            self.display_output(f"Command: {command}\n")
            acknowledgement = random.choice(self.acknowledgements)
            self.display_output(f"Assistant: {acknowledgement}\n")
            speak(acknowledgement)
            generated_response = generate_python_code(command)
            # self.display_output(f"Generated Response:\n{generated_response}\n\n")
            execution_result = execute_python_code(generated_response)

            if execution_result:
                self.display_output(f"Assistant: {execution_result}\n")
                speak(execution_result)
                
    def display_output(self, text):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    gui = AssistantGUI(root)
    root.mainloop()