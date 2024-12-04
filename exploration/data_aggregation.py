import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Directory containing the CSV files
csv_dir = 'c:/Users/erick/Documents/kaust/gpu-burn-analysis/exploration/normal_behavior'

# Read all CSV files and combine them into a single DataFrame
all_data = []
for file in os.listdir(csv_dir):
    if file.endswith('.csv'):
        file_path = os.path.join(csv_dir, file)
        df = pd.read_csv(file_path)
        if 'ClientCalcs' in df.columns and 'Temperature' in df.columns:
            all_data.append(df[['ClientCalcs', 'Temperature']])
        else:
            raise ValueError(f"'ClientCalcs' or 'Temperature' column not found in {file}")

# Concatenate all dataframes
if all_data:
    combined_df = pd.concat(all_data)
else:
    raise ValueError("No CSV files found in the directory.")

# Group by ClientCalcs and calculate the average for each ClientCalcs
average_df = combined_df.groupby('ClientCalcs').mean().reset_index()

# Apply a rolling average to smooth the curve
average_df['SmoothedTemperature'] = average_df['Temperature'].rolling(window=5).mean()

# Calculate the overall median temperature
overall_median_temp = average_df['Temperature'].median()
print(f"Overall Median Temperature: {overall_median_temp}")

# Directory containing the attack behavior CSV files
attack_dir = 'c:/Users/erick/Documents/kaust/gpu-burn-analysis/exploration/attack_behavior'
attack_file = 'gpu_burn_log_post_attack.csv'

attack_file_path = os.path.join(attack_dir, attack_file)
attack_df = pd.read_csv(attack_file_path)

if 'ClientCalcs' in attack_df.columns and 'Temperature' in attack_df.columns:
    attack_df = attack_df[['ClientCalcs', 'Temperature']]
else:
    raise ValueError(f"'ClientCalcs' or 'Temperature' column not found in {attack_file}")

# Group by ClientCalcs and calculate the average for each ClientCalcs
attack_df = attack_df.groupby('ClientCalcs').mean().reset_index()

# Apply a rolling average to smooth the curve with a smaller window
attack_df['SmoothedTemperature'] = attack_df['Temperature'].rolling(window=5).mean()

# Plotting normal and attack behavior data
plt.figure(figsize=(14, 6))

# Box plot
plt.subplot(1, 3, 1)
combined_df.boxplot(column='Temperature')
plt.axhline(y=overall_median_temp, color='k', linestyle='--', label='Overall Median Temperature')
plt.title('Box Plot of Normal Behavior Temperature Data')
plt.legend()

plt.subplot(1, 3, 2)
attack_df.boxplot(column='Temperature')
plt.axhline(y=overall_median_temp, color='k', linestyle='--', label='Overall Median Temperature')
plt.title('Box Plot of Post Attack Analysis Temperature Data')
plt.legend()

# Curve plot
plt.subplot(1, 3, 3)
colors = plt.cm.winter(np.linspace(0.3, 0.9, 2))
plt.plot(average_df['ClientCalcs'], average_df['SmoothedTemperature'], label='Normal Temperature', color=colors[0], linestyle='-')
plt.plot(attack_df['ClientCalcs'], attack_df['SmoothedTemperature'], label='Post Attack Temperature', color=colors[1], linestyle='--')
plt.axhline(y=overall_median_temp, color='k', linestyle='--', label='Overall Median Temperature')
plt.title('Curve Plot of Normal and Post Attack Analysis Data')
plt.xlabel('ClientCalcs')
plt.ylabel('Temperature')
plt.legend()

plt.tight_layout()
plt.show()
