import json
from datetime import datetime
import matplotlib.pyplot as plt

import requests
import os
import pandas as pd
import logging

CHARTS_FOLDER_NAME = 'charts'

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def query_github_api(cursor):
    headers = {"Authorization": f"token {token}"}
    query = '''
    query{
        search(query:"stars:>0", type:REPOSITORY, first:100, after:"''' + cursor + '''"){
            pageInfo{
                hasNextPage
                endCursor
            }
            nodes{
                ...on Repository{
                    nameWithOwner
                    url
                    stargazers{
                        totalCount
                    }
                    createdAt
                    pullRequests(states: MERGED){
                        totalCount
                    }
                    releases{
                        totalCount
                    }
                    updatedAt
                    primaryLanguage{
                        name
                    }
                    total: issues{
                        totalCount
                    }
                    closed: issues(states:CLOSED){
                        totalCount
                    }
                }
            }
        }
    }
    '''
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        logger.warning(request.text)
        raise Exception(f"Query failed to run by returning code of {request.status_code}. {query}")


def get_paginated_data_from_repositories(num_pages) -> list:
    has_next_page = True
    cursor = "Y3Vyc29yOjAK"  # Page = 0
    csv = []

    while has_next_page and (num_pages > 0):
        data = query_github_api(cursor)['data']
        num_pages = num_pages - 1
        has_next_page = data['search']['pageInfo']['hasNextPage']
        cursor = data['search']['pageInfo']['endCursor']
        result = data['search']['nodes']
        logger.debug(json.dumps(result, indent=4, sort_keys=True))
        csv += result
        if not has_next_page:
            logger.info("Has_next_page returned False")

    return csv


def save_charts_from_csv(results):
    # Repo ages
    repo_ages = [get_age_from_date_string(data['createdAt'][:10]) for data in results]
    repo_age_series = pd.Series(repo_ages)
    logger.info(f'Repositories average age: {sum(repo_ages) / len(repo_ages)}')
    chart = repo_age_series.plot.box()
    chart.set_xticklabels(['Repositories'])
    chart.title.set_text('Age')
    chart.figure.savefig(f'{CHARTS_FOLDER_NAME}/repo_ages.png')
    plt.close('all')

    # Total Pull Requests
    total_pull_requests = [data['pullRequests']['totalCount'] for data in results]
    total_pull_requests_series = pd.Series(total_pull_requests)
    logger.info(f'Repositories average number of PR: {sum(total_pull_requests) / len(total_pull_requests)}')
    chart = total_pull_requests_series.plot.box()
    chart.set_xticklabels(['Repositories'])
    chart.title.set_text('Pull Requests')
    chart.figure.savefig(f'{CHARTS_FOLDER_NAME}/total_pull_requests.png')
    plt.close('all')

    # Total releases
    total_releases = [data['releases']['totalCount'] for data in results]
    total_releases_series = pd.Series(total_releases)
    logger.info(f'Repositories average number of releases: {sum(total_releases) / len(total_releases)}')
    chart = total_releases_series.plot.box()
    chart.set_xticklabels(['Repositories'])
    chart.title.set_text('Releases')
    chart.figure.savefig(f'{CHARTS_FOLDER_NAME}/total_releases.png')
    plt.close('all')

    # Time since update
    repo_updates = [get_days_from_date_string(data['updatedAt'][:10]) for data in results]
    repo_updates_series = pd.Series(repo_updates)
    logger.info(f'Repositories average number of days since last update: {sum(repo_updates) / len(repo_updates)}')
    chart = repo_updates_series.plot.box()
    chart.set_xticklabels(['Repositories'])
    chart.title.set_text('Updates')
    chart.figure.savefig(f'{CHARTS_FOLDER_NAME}/repo_updates.png')
    plt.close('all')

    # Primary Language
    repo_languages = [get_primary_language_name_from_object(data) for data in results]
    repo_languages_dict = get_languages_dict_from_list(repo_languages)
    repo_languages_series = pd.Series(repo_languages_dict)
    chart = repo_languages_series.plot.barh(fontsize=5)
    chart.title.set_text('Primary Language')
    chart.figure.savefig(f'{CHARTS_FOLDER_NAME}/repo_languages.png')
    plt.close('all')

    # Closed Issues / Total Issues
    repo_closed_issues_ratio = [
        get_closed_issues_ratio_from_object(data['total']['totalCount'], data['closed']['totalCount']) for data in
        results]
    logger.info(
        f'Repositories average closed issues ratio: {sum(repo_closed_issues_ratio) / len(repo_closed_issues_ratio)}')
    repo_closed_issues_series = pd.Series(repo_closed_issues_ratio)
    chart = repo_closed_issues_series.plot.box()
    chart.title.set_text('Closed Issues Ratio')
    chart.figure.savefig(f'{CHARTS_FOLDER_NAME}/repo_closed_issues.png')
    plt.close('all')


def get_age_from_date_string(date_str):
    date_time = datetime.strptime(date_str, '%Y-%m-%d')
    difference = (datetime.now() - date_time).days // 365
    return difference


def get_days_from_date_string(date_str):
    date_time = datetime.strptime(date_str, '%Y-%m-%d')
    difference = (datetime.now() - date_time).days + 1
    return difference


def get_primary_language_name_from_object(data):
    return data['primaryLanguage']['name'] if data['primaryLanguage'] is not None else 'None'


def get_total_count_as_int(total_count):
    return total_count if total_count is not None else total_count


def get_languages_dict_from_list(lang_list):
    lang_dict = {}
    for lang in set(lang_list):
        lang_dict[lang] = len([lang_rep for lang_rep in lang_list if lang_rep == lang])
    return lang_dict


def get_closed_issues_ratio_from_object(total, closed):
    return closed / (total if total > 0 else 1)


def main():
    if token is None:
        raise Exception("Invalid token")
    logger.info(f'Token used: {token}')

    logger.info('Fetching API...')
    results = get_paginated_data_from_repositories(10)
    results_dt = pd.DataFrame(results)

    logger.info('Results saved in "results.csv"')
    results_dt.to_csv('results.csv')

    logger.info('Plotting charts...')
    save_charts_from_csv(results)


if __name__ == '__main__':
    token = os.getenv('GITHUB_TOKEN')

    try:
        main()
    except Exception as e:
        logger.warning(e)
