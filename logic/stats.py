"""
Copyright (c) 2021 Diego Moraes. MIT license, see LICENSE file.
"""
import csv
from os import path
from datetime import datetime
from .settings import VDOM_PERCENTAGE, STATUS_TO_SAVE

class Stats:
    """Statistics for fuzzer requests."""

    def __init__(self, logger, save_results):
        # ¿Las tres estadísticas podrían ponerse en un diccionario?
        # Statistics.
        self.req_stats = {
            'success': 0,
            'fail': 0,
            'exception': 0,
            'timeout': 0
        }

        # Check Virtual DOM
        self.check_vdom = True

        # Time
        self.start_time = None
        self.end_time = None

        # Logger.
        self.log = logger

        # Save results.
        self.save_results = save_results
        self.save_list = []


    def isuccess(self, url, status_code):
        """Increment Success number."""
        self.req_stats['success'] += 1
        self.log.lstatus(status_code, url)
        if self.save_results:
            self.store_results(status_code, url)
        if self.check_vdom:
            self.check_vitual_dom()


    def ifail(self, url, status_code):
        """Increment Fail number."""
        self.req_stats['fail'] += 1
        self.log.lstatus(status_code, url)
        if self.save_results:
            self.store_results(status_code, url)


    def iexception(self):
        """Increment Exception number."""
        self.req_stats['exception'] += 1


    def itimeout(self):
        """Increment Timeout number."""
        self.req_stats['timeout'] += 1


    def get_start_time(self):
        self.start_time = datetime.now()
        # Return?


    def get_end_time(self):
        self.end_time = datetime.now()
        # Return?


    def store_results(self, status_code, url):
        if status_code[0] in STATUS_TO_SAVE or status_code in STATUS_TO_SAVE:
            self.save_list.append(f"{status_code}|{url}")


    def export_results(self):
        if self.save_results and self.save_list:
            num = 1

            # Get file name.
            while True:
                file_name = f"save{num}.csv"
                if path.isfile(file_name):
                    num += 1
                else:
                    break

            # Export results to csv file.
            with open(file_name, "w") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(["status code", "url"])
                for result in self.save_list:
                    # Trim save_list string before writing.
                    status_code_row = result[0:3]
                    url_row = result[4:]
                    csv_writer.writerow([status_code_row, url_row])


    def check_vitual_dom(self):
        """Check virtual DOM redirects"""
        total = self.req_stats['success'] + self.req_stats['fail']
        if total > 100:  # TODO: Mover a settings.
            percentage = VDOM_PERCENTAGE
            max_success = round((total * percentage) / 100)
            if self.req_stats['success'] >= max_success:
                self.check_vdom = False
                self.log.lwarn("Too many 200 responses: this may be because of a vitual DOM.")


    def check_timeouts(self):
        pass


    def reset_stats(self):
        """Reset all statistics"""
        for key in self.req_stats:
            self.req_stats[key] = 0
        self.start_time = None
        self.end_time = None
        self.save_list = []
        self.check_vdom = True
