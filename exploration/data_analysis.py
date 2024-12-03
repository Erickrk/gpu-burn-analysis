import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Function to clean data by removing redundant lines
def clean_data(df):
    df = df.drop_duplicates()
    return df

# Function to read and clean CSV files
def read_and_clean_csv_files(folder_path):
    data_frames = []
    file_names = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            df = clean_data(df)
            data_frames.append(df)
            file_names.append(file_name)
    return data_frames, file_names

# Function to smooth data using a moving average
def smooth_data(y_values, window_size=5):
    return np.convolve(y_values, np.ones(window_size)/window_size, mode='valid')

# Function to plot data
def plot_data(data_frames, file_names):
    plt.figure(figsize=(10, 6))
    colors = plt.cm.winter(np.linspace(0, 1, len(data_frames)))
    
    stats = {'File Name': [], 'Average': [], 'Median': [], 'Mode': [], 'Standard Deviation': []}
    
    for df, file_name, color in zip(data_frames, file_names, colors):
        x_values = df.iloc[:, 0].values
        y_values = df.iloc[:, 2].values
        y_values_smooth = smooth_data(y_values)
        x_values_smooth = x_values[:len(y_values_smooth)]
        
        unique_x = set()
        for i in range(len(x_values_smooth)):
            while x_values_smooth[i] in unique_x:
                x_values_smooth[i] += 1
            unique_x.add(x_values_smooth[i])
        
        plt.plot(x_values_smooth, y_values_smooth, linestyle='-', color=color, label=f'Data from {file_name}')
        
        # Calculate statistics
        avg = np.mean(y_values)
        median = np.median(y_values)
        mode = pd.Series(y_values).mode().values[0]
        std_dev = np.std(y_values)
        
        # Append statistics to the table
        stats['File Name'].append(file_name)
        stats['Average'].append(avg)
        stats['Median'].append(median)
        stats['Mode'].append(mode)
        stats['Standard Deviation'].append(std_dev)
        
    plt.ylabel('Temperature')
    plt.title('Temperature through time')
    plt.legend()
    plt.show()
    
    # Create a DataFrame for the statistics
    stats_df = pd.DataFrame(stats)
    print(stats_df)
    


# Main execution
folder_path = os.path.dirname(os.path.abspath(__file__))
data_frames, file_names = read_and_clean_csv_files(folder_path)
plot_data(data_frames, file_names)