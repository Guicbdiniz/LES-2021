import logging
import shutil
import subprocess

import git
import os

import pandas as pd

PATH_TO_CLONED_REPO_DIRECTORY = 'ClonedRepository'

logger = logging.getLogger(__name__)


class RepositoriesCodeAnalyser:
    def __init__(self):
        self.current_repo = None
        self.repo_index = None
        self.df = None

    def analyse(self, repo_index, repo_url):
        """Analyse the passed repo"""
        try:
            self.repo_index = repo_index
            os.mkdir(str(self.repo_index))
            self.current_repo = git.Git(str(self.repo_index)).clone(repo_url)
            os.system(f'java -jar ck.jar {str(self.repo_index)} false 0 false {str(self.repo_index)}')
            self.df = pd.read_csv(f'{str(self.repo_index)}/class.csv')
            cbo = self.df['cbo'].sum()
            dit = self.df['dit'].sum()
            lcom = self.df['lcom'].sum()
            loc = self.df['loc'].sum()
        except Exception as e:
            raise Exception(e)
        return cbo, dit, lcom, loc

    def clean_up(self):
        """Remove the downloaded code from the current analysed directory"""

        logger.info('Cleaning up...')
        shutil.rmtree(str(self.repo_index))
        self.current_repo = None
        self.repo_index = None
