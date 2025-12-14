import pandas as pd
import numpy as np


# create function to read excel file
def read_excel_file_sheet(filename, sheetname):

    df_raw = pd.read_excel(filename, sheet_name=sheetname, header=None)
    return df_raw


# create function to extract the years from the spreadsheet
def extract_years(df_raw):
    # Extract year headers from row 4 (index 1), starting from column 1:21
    years = df_raw.iloc[1, 1:21].tolist()
    return years


# create a function to extract data from the spreadsheet
def extract_data(df_raw, 
                 years, 
                 data_label, 
                 start_row, 
                 end_row, 
                 start_col, 
                 end_col, 
                 attr_label, 
                 attr_row, 
                 attr_col):
    # Extract data from column 1, starting at start_row to end_row
    data_groups = df_raw.iloc[start_row:end_row, 0].tolist()
    # remove footnotes, if any
    data_groups = [x.split("\\")[0] for x in data_groups]

    # Extract the numeric matrix (start_row onward, start_col onward)
    values = df_raw.iloc[start_row:end_row, start_col:end_col]

    # Extract Label as a value
    attr = df_raw.iloc[attr_row:attr_row+1, attr_col:attr_col+1]
    attr_val = attr.iloc[0][0]
    # clean ":" from the string, if any
    attr_val = attr_val.replace(":", "")

    # Build the DataFrame
    df = pd.DataFrame(values.values, columns=years)

    # Add data_label as a column
    df.insert(0, data_label, data_groups)

    # Add sex as a column
    df.insert(0, attr_label, attr_val)
    return df


# create function to process the raw data into matrices
def convert_raw_to_matrix(df_raw, years, od_cause):
    # extract age-groups
    df_age1 = extract_data(df_raw, years, 'age_group', 5, 14, 1, 21, 'sex', 2, 0)
    #df_age1.head(15)

    df_age2 = extract_data(df_raw, years, 'age_group', 17, 26, 1, 21, 'sex', 14, 0)
    #df_age2.head(15)

    df_age3 = extract_data(df_raw, years, 'age_group', 29, 38, 1, 21, 'sex', 26, 0)
    #df_age3.head(15)

    df_age = pd.concat([df_age1, df_age2, df_age3], ignore_index=True)
    #df_age

    # Add od_cause as a column
    df_age.insert(0, "od_cause", od_cause)

    # extract race
    df_race1 = extract_data(df_raw, years, 'race', 40, 51, 1, 21, 'sex', 39, 0)
    # df_race1.head(15)

    df_race2 = extract_data(df_raw, years, 'race', 52, 63, 1, 21, 'sex', 51, 0)
    #df_race2.head(15)

    df_race = pd.concat([df_race1, df_race2], ignore_index=True)
    #df_race

    # Add od_cause as a column
    df_race.insert(0, "od_cause", od_cause)

    return [df_age, df_race]


# create function to convert matrices to tables
def convert_matrix_to_tables(df_age, df_race):
    # Replace ellipses with NaN
    df_age = df_age.replace("…", np.nan)

    # Replace ellipses with NaN
    df_race = df_race.replace("…", np.nan)

    # Melt the year columns into a table
    table_age = df_age.melt(
        id_vars=["od_cause", "sex", "age_group"],
        var_name="year",
        value_name="rate"
    )

    # Melt the year columns into a table
    table_race = df_race.melt(
        id_vars=["od_cause", "sex", "race"],
        var_name="year",
        value_name="rate"
    )

    # Convert types
    table_age["year"] = pd.to_numeric(table_age["year"], errors="coerce")
    table_age["rate"] = pd.to_numeric(table_age["rate"], errors="coerce")

    # Convert types
    table_race["year"] = pd.to_numeric(table_race["year"], errors="coerce")
    table_race["rate"] = pd.to_numeric(table_race["rate"], errors="coerce")

    return [table_age, table_race]

