import logging
import os

import numpy as np
import pandas as pd

from repositories_data_manager.repository_code_analyser import RepositoriesCodeAnalyser

GITHUB_DATA_CSV_FILENAME = 'api_results.csv'
# Could not find a way to import from the other module

ANALYSED_DATA_CSV_FILENAME = 'analysed_data.csv'

logger = logging.getLogger(__name__)


class RepositoriesDataManager:

    def __init__(self):
        self.repositories_code_analyser = RepositoriesCodeAnalyser()
        self.repos_data = self._check_for_previous_data()

    def analyse_repository(self, repo_index):
        """TODO"""

        analysed_repo = self.repos_data.iloc[repo_index]
        logger.info(f'Analysing repo: \n{analysed_repo}')
        self.repositories_code_analyser.analyse(repo_index, analysed_repo['url'])

    def save_data(self):
        """Save analysed data into .csv file"""

        logger.info(f'Saving data into {ANALYSED_DATA_CSV_FILENAME}...')
        self.repos_data.to_csv(ANALYSED_DATA_CSV_FILENAME, index=False)
        logger.info(f'Data saved.')

    def clean_up(self):
        self.repositories_code_analyser.clean_up()

    @staticmethod
    def _check_for_previous_data() -> pd.DataFrame:
        if os.path.isfile(ANALYSED_DATA_CSV_FILENAME):
            logger.info('Previously analysed data csv found.')
            return pd.read_csv(ANALYSED_DATA_CSV_FILENAME)
        elif os.path.isfile(GITHUB_DATA_CSV_FILENAME):
            logger.info('GitHub data csv found.')
            df = pd.read_csv(GITHUB_DATA_CSV_FILENAME)
            try:
                df = df.assign(
                    loc=pd.Series(np.zeros(1000)).values,
                    cbo=pd.Series(np.zeros(1000)).values,
                    dit=pd.Series(np.zeros(1000)).values,
                    lcom=pd.Series(np.zeros(1000)).values
                )
            except Exception as e:
                logger.warning(e)
                raise Exception('There was an error while assigning the new columns to the DataFrame')
            return df
        else:
            raise FileNotFoundError()
