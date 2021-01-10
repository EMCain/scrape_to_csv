import os
from csv import DictWriter
from datetime import datetime

from requests import get

class ResultCompiler:
    def __init__(
            self, 
            url_iterable, 
            project_name, 
            column_names,
            parse_callback,
            output_folder_path=None, 
            base_filename="data"
        ):
        """
        Set up the parser/writer for a single URL pattern, like https://www.example.com/<arg_1>/items?param=<arg_2>. 

        Using BeautifulSoup to create parse_column is recommended. See examples folder.

        :url_iterable: an iterable (list or generator) that returns the full URLs you want to scrape
        :project_name: a filepath-friendly string used to identify this project's results
        :column_names: list of column headers in the order you want them to appear on the finished spreadsheet
        :parse_callback: function that takes an HTML page's text and returns a dict with column_names as keys,
        and scraped data from that response as the values
        """
        self.url_iterable = url_iterable  # TODO: generalize to allow parsing a list of .html files
        self.project_name = project_name
        self.column_names = column_names
        self.parse_callback = parse_callback

        if output_folder_path is None: 
            self.output_folder_path = f"results/{project_name}"
        else:
            self.output_folder_path = output_folder_path

        self.aggregate_results = {
            "successes": 0,
            "failed_requests": [],
            "exceptions": [],
        }


    # TODO create an option for using FileIO instead of open(filepath)
    # TODO create the option to paginate the results into multiple CSVs 
    def write_results(self):
        if not os.path.exists(self.output_folder_path):
            os.makedirs(self.output_folder_path)

        timestamp = datetime.now().strftime("%Y-%m-%d_%k:%M:%S")

        file_path = f"{self.output_folder_path}/{timestamp}.csv"

        with open(file_path, 'a') as csv_file:
            writer = DictWriter(csv_file, fieldnames=self.column_names)

            writer.writeheader()

            for page in self.url_iterable:
                response = get(page)

                if response.status_code < 400:
                    line = self.parse_callback(response.text, page)
                    writer.writerow(line)
                    self.aggregate_results["successes"] += 1

                else: 
                    error_summary = {
                        "url": page,
                        "code": response.status_code,
                        "message": response.text
                    }
        print(file_path)
        print(self.aggregate_results)
        return self.aggregate_results

