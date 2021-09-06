import logging
import shutil

import git
import os

PATH_TO_CLONED_REPO_DIRECTORY = 'ClonedRepository'

logger = logging.getLogger(__name__)


class RepositoriesCodeAnalyser:
    def __init__(self):
        self.current_repo = None
        self.repo_index = None

    def analyse(self, repo_index, repo_url):
        """Analyse the passed repo"""

        self.repo_index = repo_index
        os.mkdir(PATH_TO_CLONED_REPO_DIRECTORY)
        self.current_repo = git.Git(PATH_TO_CLONED_REPO_DIRECTORY).clone(repo_url)

    def clean_up(self):
        """Remove the downloaded code from the current analysed directory"""

        logger.info('Cleaning up...')
        shutil.rmtree(PATH_TO_CLONED_REPO_DIRECTORY)
        self.current_repo = None
        self.repo_index = None
