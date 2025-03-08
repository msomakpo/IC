import pandas as pd
import matplotlib.pyplot as plt


crime_files = {
    "jan": "/Users/tamaraobando/Desktop/IC25/jan_crime_to_stations.xlsx",
    "feb": "/Users/tamaraobando/Desktop/IC25/feb_crime_to_stations.xlsx",
    "mar": "/Users/tamaraobando/Desktop/IC25/mar_crime_to_stations.xlsx"
}

# Loop through each file and load the data
for month, file_path in crime_files.items():

    crime_df = pd.read_excel(file_path)

   

    # Extract day and month for analysis
    crime_df["Day"] = crime_df["Date"].dt.day
    crime_df["Month"] = crime_df["Date"].dt.month

    crime_data_for_tableau = (
        crime_df.groupby(["Date", "Month", "Station", "Time Period", "Offense"])
        .size()
        .reset_index(name="Crime Count")  # Rename count column
    )

    output_path = f"/Users/tamaraobando/Desktop/IC25/{month}_crime_data_for_tableau.xlsx"
    crime_data_for_tableau.to_excel(output_path, index=False)

    print(f"saved to: {output_path}")



