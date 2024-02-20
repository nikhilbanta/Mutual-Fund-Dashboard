import os
import json
import requests

class MutualFund:
    def __init__(self, api_url):
        self.api_url = api_url
    
    def fetch_api_data(self):
        response = requests.get(self.api_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch data from API. Status code: {response.status_code}")
            return None
    
    def filter_mutual_fund(self, filename, include_substrings=None, exclude_substrings=None):
        api_data = self.fetch_api_data()
        if api_data is None:
            return
        
        if include_substrings is None:
            include_substrings = []
        if exclude_substrings is None:
            exclude_substrings = []
        
        filtered_data = []
        for scheme in api_data:
            scheme_name = scheme["schemeName"]
            include_matched = any(all(substring in scheme_name for substring in sublist) for sublist in include_substrings)
            exclude_matched = all(substring not in scheme_name for substring in exclude_substrings)
            
            if include_matched and exclude_matched:
                filtered_data.append(scheme)
        
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        output_path = os.path.join(output_dir, filename)
        with open(output_path, "w") as outfile:
            json.dump(filtered_data, outfile)
        return "File Created successfully"
    
# api_url = "https://api.mfapi.in/mf"
# filter_instance = MutualFund(api_url)
# include_lists = [["Growth", "Direct","TAX"],["Growth", "Direct","ELSS"],["SBI LONG TERM EQUITY FUND","DIRECT","GROWTH"]]
# exclude_list = ["REGULAR"]
# output_filename = "elss_mf.json"
# filter_instance.filter_mutual_fund(output_filename, include_substrings=include_lists, exclude_substrings=exclude_list)