import pandas as pd
import re




stations_df=pd.read_excel("/Users/tamaraobando/Desktop/IC25/Metro_Stations.xlsx")  


# load dataset to dataframe
crime_files = {
    "jan": "/Users/tamaraobando/Desktop/IC25/jan_crime_data.xlsx",
    "feb": "/Users/tamaraobando/Desktop/IC25/feb_crime_data.xlsx",
    "mar": "/Users/tamaraobando/Desktop/IC25/mar_crime_data.xlsx",

}

# converts addresses in stations_df to match the format of crime_df
def address_key(address):
    

    address=address.strip().lower() # remove whitespaces and convert lowercase
    address=re.sub(r"[.,]","",address) # remove dots and commas
    match=re.search(r"^\d{1,5}[-\s]?\S+",address) # extract first nummber and the following value
    return match.group(0) if match else None

# pass each row in address and location column through address key function for better comparison
stations_df['Key']=stations_df['ADDRESS'].apply(address_key)

# categorize times into periods 

def categorize_time(time):

    hour = time.hour
    minute = time.minute
    time_decimal = hour + (minute/60)
    
    if 0 <= time_decimal < 1:
        return "Late Night (12am-Close)"
    elif 5.5<= time_decimal < 9.5:
        return "AM Peak (Open-9:30am)"
    elif 9.5 <= time_decimal < 15:
        return "Midday (9:30am-3pm)"
    elif 15 <= time_decimal <= 19:
        return "PM Peak (3pm-7pm)"
    elif 19 <= time_decimal < 24:
        return "Evening (7pm-12am)"
    else: 
        return "Closed (1am - 5:30am)"

# Function to clean crime type by removing jurisdiction prefixes
def clean_crime_type(crime):
    
    return re.sub(r"^[A-Z]{2,3} -\s*", "", crime)  # Remove jurisdiction code

for month, crime_file_path in crime_files.items():

    crime_df=pd.read_excel(crime_file_path)

    # match locations to stations
    crime_df['Key']=crime_df['Location'].apply(address_key)
    crime_df=crime_df.merge(stations_df[["NAME","Key"]], on="Key", how="inner")

    # drop columns
    crime_df.drop(columns=["Location","Key"], inplace=True)

    # convert to datetime
    crime_df["Date"] = pd.to_datetime(crime_df["Date"], format="%m/%d/%Y")
    crime_df["Time"] = pd.to_datetime(crime_df["Time"], format="%H:%M:%S")

    # categorize into time periods
    crime_df["Time Period"] = crime_df["Time"].apply(categorize_time)

    # Clean the Offense column (remove "MD -", "PG -", "DC -", etc.)
    crime_df["Offense"] = crime_df["Offense"].apply(clean_crime_type)


    crime_df.rename(columns={"NAME": "Station"}, inplace=True)

    # Save cleaned dataset
    output_path = f"/Users/tamaraobando/Desktop/IC25/{month}_crime_to_stations.xlsx"
    crime_df.to_excel(output_path, index=False)

    # Print summary
    print(f"saved to: {output_path}")

