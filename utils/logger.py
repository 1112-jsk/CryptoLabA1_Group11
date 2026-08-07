import datetime
import os

def log_execution(selected_option):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = f"Date/Time: {current_time} | Menu Option Selected: {selected_option}\n"
    
    with open("outputs/execution_log.txt", "a") as log_file:
        log_file.write(log_entry)