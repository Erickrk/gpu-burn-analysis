import csv
import os
import matplotlib.pyplot as plt

def print_temperature_readings(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            date = row[0].strip()
            gpu_temperature = row[3].strip()
            print(f"Date: {date}, GPU Temperature: {gpu_temperature} °C")

def list_files_and_print_graph_names(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            print(f"Graph name: {filename}")
            print_temperature_readings(os.path.join(directory, filename))

def plot_temperature_readings(file_path):
    dates = []
    temperatures = []

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Skip the header row
        for row in reader:
            dates.append(row[0].strip())
            try:
                temperatures.append(float(row[3].strip()))
            except ValueError:
                continue  # Skip rows with invalid temperature values

    plt.plot(dates, temperatures, label=os.path.basename(file_path))

def plot_all_temperature_readings(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            plot_temperature_readings(os.path.join(directory, filename))

    plt.xlabel('Date')
    plt.ylabel('GPU Temperature (°C)')
    plt.title('GPU Temperature Readings')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

directory = 'c:/Users/silvae/Documents/GitHub/gpu-burn-analysis/exploration/cs380'
list_files_and_print_graph_names(directory)
plot_all_temperature_readings(directory)
