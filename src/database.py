import pandas as pd
import re

DF_CSV_PATH = r'../results/database.csv'
FICE_TABLE_CSV_PATH = r'../results/fice_table.csv'

class Database:
    def __init__(self):
        self.df = pd.read_csv(DF_CSV_PATH)
        fice_table = pd.read_csv(FICE_TABLE_CSV_PATH)
        self.fice_dict = self._create_FICE_LUT(fice_table)

    def _create_FICE_LUT(self, fice_df: pd.DataFrame):
        return fice_df.set_index('FICE')['college'].to_dict()

    def _find_courses_by_code(self, NEU_code: str) -> list:
        '''Find all the possible courses that can be transfered for credit on
        a specific NEU course.

        :param NEU_course: The NEU course to target.
        Format should be: 'CS3500' with no spaces (quotes not included).
        :type NEU_course: str
        '''
        found_entries = self.df[self.df['NEUCode'] == NEU_code]
        found_entries['College'] = found_entries['FICE'].map(self.fice_dict)
        results = found_entries[['TransferCourse', 'College']].to_numpy()
        # print(results)
        return list(results)
    
    def get_available_NEU_codes(self) -> list:
        return list(self.df['NEUCode'].unique())
    
    def get_codes_by_dept_dict(self) -> dict:
        codes = self.get_available_NEU_codes()
        results = {}
        pattern = r"(?P<dept>[A-Z]+)(?P<number>\d+)"
        for code in codes:
            match = re.search(pattern, code)
            dept = match.group('dept')
            number = match.group('number')

            dept_bucket = results.get(dept)

            if dept_bucket:
                dept_bucket.append(number)
            else:
                results[dept] = [number]

        return results


if __name__ == '__main__':
    database = Database()
    # print(database.get_available_NEU_codes())
    print(database.get_codes_by_dept_dict())
    # database._find_courses_by_code("MATH1365")


    
    