import pandas as pd
import os

##---------------------------- Put csv files into a single Excel file ---------------------------------##
csv_folder = "/Users/khwezikgalema/PycharmProjects/SMMEs_Data_Extraction"  
excel_file = "smme_data.xlsx"

with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
    for filename in os.listdir(csv_folder):
        if filename.endswith(".csv"):
            file_path = os.path.join(csv_folder, filename)
            df = pd.read_csv(file_path)
            sheet_name = os.path.splitext(filename)[0]
            df.to_excel(writer, sheet_name=sheet_name, index=False)
##---------------------------- Put csv files into a single Excel file ---------------------------------##

