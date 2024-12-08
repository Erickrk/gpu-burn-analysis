import pandas as pd
import os
import matplotlib.pyplot as plt

# Define the path to the folder containing the CSV files
csv_folder_path = 'C:\Users\silvae\Documents\GitHub\gpu-burn-analysis\exploration\normal_behavior'

# Initialize an empty DataFrame to store all temperature data
all_data = pd.DataFrame()

# Loop through all files in the folder
for filename in os.listdir(csv_folder_path):
    if filename.endswith('.csv'):
        csv_file_path = os.path.join(csv_folder_path, filename)
        
        # Read the CSV file
        data = pd.read_csv(csv_file_path)
        
        # Check if 'Temperature' column exists in the data
        if 'Temperature' in data.columns:
            # Extract the last word from the filename (without extension)
            label = os.path.splitext(filename)[0].split('_')[-1]
            # Append the temperature data to the all_data DataFrame
            all_data = pd.concat([all_data, data[['Temperature']].assign(label=label)], ignore_index=True)

# Check if all_data is not empty before plotting
if not all_data.empty:
    # Create a box plot for all temperature data
    all_data.boxplot(by='label', column='Temperature', grid=False)
    plt.title('Normal state analysis')
    plt.suptitle('')  # Suppress the default title to avoid overlap
    plt.ylabel('Temperature')
    plt.xlabel('')  # Clear the x-axis label
    plt.xticks(rotation=90)
    plt.style.use('seaborn-darkgrid')  # Use the winter theme
    plt.savefig('temperature_analysis.png', dpi=300)  # Save the plot as a high-resolution image
    plt.show()
else:
    print("No temperature data available to plot.")
