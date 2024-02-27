import json
import requests
import pandas as pd
import os

def json_csv_creator(file_address, output_csv_path):

    """
    This Function create csv file for nav data for mutual fund
    present in input list of json file.
    Need to provide address of input json file and output csv file. 
    """
    
    try:
        # Create an empty dataframe to store the result
        result_df = pd.DataFrame()

        with open(file_address, 'r') as file:
            data = json.load(file)

            # Check if the data is a list of JSON objects
            if isinstance(data, list):
                for idx, json_object in enumerate(data, start=1):
                    scheme_code = json_object.get('schemeCode')

                    # Check if 'schemeCode' is present in the JSON object
                    if scheme_code is not None:
                        api_url = f'https://api.mfapi.in/mf/{scheme_code}'
                        response = requests.get(api_url)

                        if response.status_code == 200:
                            mf_data = response.json()['data']

                            # Create a dataframe for each API response
                            df = pd.DataFrame(mf_data, columns=['date', 'nav'])
                            col_name = json_object.get('schemeName')
                            df = df.rename(columns={'nav': col_name})

                            # Merge with the result dataframe based on the "date" column
                            if result_df.empty:
                                result_df = df
                            else:
                                result_df = pd.merge(result_df, df, on='date', how='outer')
                        else:
                            print(f'Failed to fetch data for scheme code {scheme_code}. Status code: {response.status_code}')
                    else:
                        print(f'Missing schemeCode in JSON object {idx}.')

                # Convert "date" column to datetime format
                result_df['date'] = pd.to_datetime(result_df['date'], format='%d-%m-%Y')

                # Sort the merged dataframe based on the "date" column
                result_df = result_df.sort_values(by='date')

                # Save the dataframe to a CSV file without index
                result_df.to_csv(output_csv_path, index=False)

                print(f'Merged, Converted, and Sorted DataFrame saved to: {output_csv_path}')
            else:
                print("Invalid JSON format. The file should contain a list of JSON objects.")

    except FileNotFoundError:
        print(f"File not found: {file_address}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file {file_address}: {e}")
    return result_df


def clean_column_names_csv(file_path,new_file_path):
    """
    This function takes a CSV file path and new CSV file path as input,
    reads the CSV file into a pandas DataFrame, cleans the column names,
    and saves the cleaned DataFrame to the new CSV file path.
    """
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(file_path)

        # Clean column names by removing extra spaces, substring after hyphen,
        # and everything after "ELSS" or "TAX" (case-insensitive)
        df.columns = [col.strip().split('-')[0].split('ELSS', 1)[0].split('TAX', 1)[0] for col in df.columns]


        df.to_csv(new_file_path, index=False)
        print("Column names updated successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    return df

