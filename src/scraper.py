import requests
from bs4 import BeautifulSoup
import time
import random
import csv
from wakepy import keep
import logging
import pickle
import os

URL = r"https://ugadmissions.northeastern.edu/transfercredit/TransferCreditEvaluatedStudent2.asp"
RESULTS_PATH = r"C:\Users\acoullard\Programming\Python\NEU_course_transfer_web_scraper\results"

class NEUTransferScraper():

    def __init__(self):
        self.total_requests = 0
        logging.basicConfig(filename='scraping.log', level=logging.INFO, filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')
        fice_table = self.get_FICE_table()

        fice_list = list(fice_table.keys())[:4]
        
        # with keep.running(): 
        #     with open(RESULTS_PATH + r"\results.csv", "w", newline="") as csvfile:
        #         csv_writer = csv.writer(csvfile)
        #         csv_writer.writerow(["NEUCourse", "TransferCourse","EffectiveDates", "NUCore", "NUPath", "FICE"])

        #         for indx, fice in enumerate(fice_list):
        #             departments = self.get_departments(fice)
        #             print(fice_table[fice], departments, f"({indx+1}/{len(fice_list)})", f"\nTotal requests: {self.total_requests}")
        #             for dept in departments:
        #                 time.sleep(random.uniform(0.5, 1.2))
        #                 try:
        #                     courses = self.get_classes(fice, dept)
        #                 except Exception as e:
        #                     logging.error(f"Error getting classes for {dept} in {fice}: {e}")
        #                     if indx < 200:
        #                         raise e
        #                     continue
                            

        #                 courses = [[*course, fice] for course in courses]
        #                 csv_writer.writerows(courses)
                

    def get_FICE_table(self):
        payload = {"SiteEntered": "FICE", "FICE":"031155", "tseg":"", "TransferCourse":""}

        page = requests.post(url=URL, data=payload)
        self.total_requests += 1
        options = self.get_table(page, 0)

        FICE_table = {option["value"].strip() : option.text for option in options}

        return FICE_table

    def get_departments(self, fice: str):
        page = requests.post(url=URL, data={"SiteEntered": "FICE", "FICE":fice, "tseg":"", "TransferCourse":""})
        self.total_requests += 1
        table = self.get_table(page, 1)
        return [option.text.strip() for option in table]
    
    def get_classes(self, fice:str, department: str):
        page = requests.post(url=URL, data={"SiteEntered": "TSeg", "FICE":fice, "tseg":department, "TransferCourse":""})
        self.total_requests += 1
        soup = BeautifulSoup(page.text, "html.parser")
        tables = soup.form.find_all("table")

        if len(tables) <= 3:
            logging.info(f"No classes found for {department} in {fice}, had to do if statement")
            class_names = tables[2].find_all("option")[-1]
            page = requests.post(url=URL, data={"SiteEntered": "TSeg", "FICE":fice, "tseg":department, "TransferCourse":class_names["value"].strip()})
            self.total_requests += 1
            soup = BeautifulSoup(page.text, "html.parser")
            table = soup.form.find_all("table")[3].find_all("tr")[1:]
        else:   
            table = soup.form.find_all("table")[3].find_all("tr")[1:]

        # print(table[0])
        # transfer course | NEU course | effective dates | NU Core | NUPath
        found_courses = []
        for course in table:
            
            tds = course.find_all("td")
            transfer_course_name = tds[0].text
            neu_course_name = tds[1].text
            # print("newcoursename",neu_course_name)
            effective_dates = tds[2].text if tds[2].text != "." else None
            nu_core = tds[3].b.text if tds[3].b is not None else None
            bu_path = tds[4].b.text if tds[4].b is not None else None

            course_record = [neu_course_name, transfer_course_name, effective_dates, nu_core, bu_path]
            course_record = [item.strip() if item is not None else None for item in course_record]

            found_courses.append(course_record)
        return found_courses


    def get_table(self, page: requests.Response, table_num: int):
        if table_num < 0 or table_num > 3:
            raise ValueError("Invalid table number")
        soup = BeautifulSoup(page.text, "html.parser")
        return soup.form.find_all("table")[2].find_all("tr")[table_num].find_all("option")[1:]
    
    def save_fice_table(self):
        fice_table = self.get_FICE_table()

        print(fice_table["001434"])
        with open(RESULTS_PATH + r"\fice_table.csv", "w", newline="") as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(["FICE", "college"])
                fice_list = [[fice, fice_table[fice]] for fice in fice_table.keys()]
                csv_writer.writerows(fice_list)

class NEUTransferDB():
    def __init__(self, path: str):
        self.path = path
        self.db = None
        self.fice_table = None

    def connect_to_db(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "rb") as f:
                    self.db = pickle.load(f)
            except Exception as e:
                raise Exception(f"Failed to load database at path {self.path}\n{str(e)}")
        else:
            print("Creating new DB...")
            self.db = {}

    # def create_new_db(self, csv_path, fice_table_path):
    #     with open(csv_path, "r") as f:
    #         csv_reader = csv.reader(f)
    #         next(csv_reader)
    #         for row in csv_reader:
    #             self.db[row[0]] = row[1:]

    #     with open(fice_table_path, "r") as f:
    #         csv_reader = csv.reader(f)
    #         next(csv_reader)
    #         self.fice_table = {row[0]: row[1] for row in csv_reader}
        
    
if __name__ == "__main__":
    NEUTransferScraper()