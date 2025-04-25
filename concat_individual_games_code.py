import pandas as pd
import os
import glob

# Set the path to your CSV files
csv_folder = 'csvfolder'  # e.g., './data'

# Use glob to get all the CSV files in the folder
csv_files = glob.glob(os.path.join(csv_folder, '*.csv'))

# Read and concatenate all CSV files
df_list = [pd.read_csv(file) for file in csv_files]
merged_df = pd.concat(df_list, ignore_index=True)

# Save the merged CSV
merged_df.to_csv('elite_chess_games.csv', index=False)

print("CSV files merged successfully into 'elite_chess_games.csv'")
