import logging
import sys
from repositories_data_manager import RepositoriesDataManager

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def main():
    try:
        current_repo_index = int(sys.argv[1])
        number_of_repos_to_analise = int(sys.argv[2])

        logger.info(f'Current repository index: {current_repo_index}')
        logger.info(f'Number of repositories to analise: {number_of_repos_to_analise}')

        data_manager = RepositoriesDataManager()
        data_manager.analyse_repository(1)
        data_manager.save_data()
        data_manager.clean_up()
    except ValueError:
        logger.error('Incorrect arguments types.')
        logger.error(
            'Correct usage: python code_analysis {current_repo_index: int} {number_of_repos_to_analise: int}.')
    except IndexError:
        logger.error('Incorrect number of arguments.')
        logger.error(
            'Correct usage: python code_analysis {current_repo_index: int} {number_of_repos_to_analise: int}.')
    except FileNotFoundError:
        logger.error('API results csv file not found. Run the github_fetch.py module first.')
    except Exception as e:
        logger.warning('Unknown exception caught')
        logger.error(e)


if __name__ == '__main__':
    main()
