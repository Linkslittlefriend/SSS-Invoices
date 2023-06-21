import datetime
import sys
import os

def print_with_time(*args, **kwargs):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{timestamp}]', *args, **kwargs)

def open_log_file():
    # Get the current date
    today = datetime.date.today()

    # Format the date as a string
    date_string = today.strftime('%Y-%m-%d')

    # Construct the log file name
    log_file_name = f'Assets/Logs/log-{date_string}.txt'

    # Check if the Logs directory exists and create it if it doesn't
    os.makedirs(os.path.dirname(log_file_name), exist_ok=True)

    # Open the log file in write mode
    log_file = open(log_file_name, 'a')

    # Redirect the standard output and standard error streams to the log file
    sys.stdout = log_file
    sys.stderr = log_file

    return log_file

def close_log_file(file):
    #Close the log file
    file.close()