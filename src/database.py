import pandas as pd

DF_CSV_PATH = r'../results/database.csv'
FICE_TABLE_CSV_PATH = r'../results/fice_table.csv'

class Database:
    def __init__(self):
        self.df = pd.read_csv(DF_CSV_PATH)
        fice_table = pd.read_csv(FICE_TABLE_CSV_PATH)
        self.fice_dict = self._create_FICE_LUT(fice_table)

    def _create_FICE_LUT(self, fice_df: pd.DataFrame):
        return fice_df.set_index('FICE')['college'].to_dict()

    def _find_courses(self, NEU_course: str):
        '''Find all the possible courses that can be transfered for credit on
        a specific NEU course.

        :param NEU_course: The NEU course to target.
        Format should be: 'CS3500' with no spaces (quotes not included).
        :type NEU_course: str
        '''
        found_entries = self.df[self.df['NEUCode'] == NEU_course]
        print(found_entries[['TransferCourse', 'FICE']].to_numpy())


database = Database()
database._find_courses("CS3000")


    
    