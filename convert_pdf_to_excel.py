import pdfplumber
import pandas as pd
import re

pdf_files = {
    "jan": "/Users/tamaraobando/Desktop/IC25/jan_crime_data.pdf",
    "feb": "/Users/tamaraobando/Desktop/IC25/feb_crime_data.pdf",
    "mar": "/Users/tamaraobando/Desktop/IC25/mar_crime_data.pdf"
}

# loop through each pdf file 
for month, crime_pdf_path in pdf_files.items():
    print(f"\ Processing: {month.capitalize()} - {crime_pdf_path}")
    cleaned_data = []


    with pdfplumber.open(crime_pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                header = table[0]  # First row is the header
                prev_row = None  # Track previous row 
            
                for row in table[1:]:  # Skip the header row
                    if all(cell is None for cell in row[:-1]):  
                    # If the row is only an offense (all None except last column), append it to prev_row
                        if prev_row:
                            prev_row[-1] += f"; {row[-1]}"  # Concatenate offenses
                    else:
                        cleaned_data.append(row)  # Store normal rows
                        prev_row = row  # Update previous row
    # Convert to Pandas DataFrame
    crime_stats_df = pd.DataFrame(cleaned_data, columns=['Date', 'Time', 'Dispo', 'Location', 'Offense'])

    # drop Dispo col
    crime_stats_df.drop(columns=['Dispo'],inplace = True)

    # fill missing date and time values with previous line
    crime_stats_df[['Date', 'Time']] = crime_stats_df[['Date', 'Time']].fillna(method='ffill')

    # drop locations that begin with a letter
    crime_stats_df = crime_stats_df[crime_stats_df["Location"].str.match(r"^\d", na=False)]


    # Save to Excel
    output_path = f"/Users/tamaraobando/Desktop/IC25/{month}_crime_data.xlsx"
    crime_stats_df.to_excel(output_path, index=False)

    print(f"\nsaved to: {output_path}")




    


