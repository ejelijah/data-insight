import pandas as pd
from pathlib import Path

csv_path = Path.home() / "Desktop" / "side_quest" / "PLC_permit.csv"
print("this is:", csv_path.exists())  
df = pd.read_csv(csv_path)

print("Rows and columns:", df.shape)
print(df.head())  

