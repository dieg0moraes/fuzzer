"""
Copyright (c) 2021 Diego Moraes. MIT license, see LICENSE file.
"""
import csv
from os import path
from sys import exit as sysexit
from datetime import datetime
from utils import query_yes_no
from .settings import VDOM_PERCENTAGE

class Stats:
    """Statistics for fuzzer requests."""

    def __init__(self, logger, save_results):
        # ¿Las tres estadísticas podrían ponerse en un diccionario?
        # Statistics.
        self.success = 0
        self.fail = 0
        self.exception = 0
        self.timeouts = 0

        # Check Virtual DOM
        self.no_stop = False
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
        self.success += 1
        self.log.lstatus(status_code, url)
        if self.save_results:
            self.store_results(status_code, url)
        if self.check_vdom:
            self.check_vitual_dom()


    def ifail(self, url, status_code):
        """Increment Fail number."""
        self.fail += 1
        self.log.lstatus(status_code, url)
        if self.save_results:
            self.store_results(status_code, url)


    def iexception(self):
        """Increment Exception number."""
        self.exception += 1


    def itimeout(self):
        """
        Checks for too many timeouts
        and increases the time.
        """
        pass


    def get_start_time(self):
        self.start_time = datetime.now()
        # Return?


    def get_end_time(self):
        self.end_time = datetime.now()


    def store_results(self, status_code, url):
        # TODO: ¿Qué códigos guarda?
        if status_code[0] in ("2", "3") or status_code in ("401", "403"):
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
                for result in self.save_list:
                    status_code_row = result[0:3]
                    url_row = result[4:]
                    csv_writer.writerow([status_code_row, url_row])


    def check_vitual_dom(self):
        """Check virtual DOM redirects"""
        total = self.success + self.fail
        if total > 100:  # ¿Qué número debería ser?
            percentage = VDOM_PERCENTAGE
            max_success = round((total * percentage) / 100)
            if self.success >= max_success:
                self.log.lwarn("Too many 200 responses: this may be because of a vitual DOM.")
                if not self.no_stop:
                    if not query_yes_no("Continue?"):
                        # TODO: Esto podría ser cambiado por una
                        # excepción.
                        sysexit(0)

        self.check_vdom = False


    def check_timeouts(self):
        pass
