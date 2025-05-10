import time
# from hotword2 import listen_for_hotword
# from hotword2 import transcribe
from hotword2 import speak
from cmd_to_py import generate_python_code
from cmd_to_py import execute_python_code


# if __name__ == "__main__":
#     print("Voice Controlled Selenium Automation")
#     while True:
#         if listen_for_hotword():
#             command = transcribe()
#             if command:
#                 print("Your command:", command)
#                 speak("Doing it sir")
#                 execute_python_code(generate_python_code(command))
                
#         time.sleep(0.1) # Small delay to reduce CPU usage in the loop
if __name__ == "__main__":
    while True:
        command = input("Enter command: ")
        if command:
            # print("Your command:", command)
            speak("Doing it sir")
            execute_python_code(generate_python_code(command))