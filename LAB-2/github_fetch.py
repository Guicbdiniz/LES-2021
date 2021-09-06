import json
import requests
import os
import pandas as pd
import logging

from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

GITHUB_DATA_CSV_FILENAME = 'api_results.csv'


def query_github_api(filter, quantity, cursor):
    headers = {"Authorization": f"token {token}"}
    query = '''
    query{
        search(query:"''' + filter + '''", type:REPOSITORY, first:''' + quantity + ''', after:"''' + cursor + '''"){
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
                    releases{
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
    filter = "language:java"
    quantity = "100"
    cursor = "Y3Vyc29yOjAK"  # Page = 0
    csv = []

    while has_next_page and (num_pages > 0):
        data = query_github_api(filter, quantity, cursor)['data']
        num_pages = num_pages - 1
        has_next_page = data['search']['pageInfo']['hasNextPage']
        cursor = data['search']['pageInfo']['endCursor']
        result = [format_repo_data(repo_data) for repo_data in data['search']['nodes']]
        logger.debug(json.dumps(result, indent=4, sort_keys=True))
        csv += result
        if not has_next_page:
            logger.info("Has_next_page returned False")

    return csv


def format_repo_data(repo_data):
    return {
        'nameWithOwner': repo_data['nameWithOwner'],
        'url': repo_data['url'],
        'stargazers': repo_data['stargazers']['totalCount'],
        'releases': repo_data['releases']['totalCount'],
        'age': get_age_from_date_string(repo_data['createdAt'][:10])
    }


def get_age_from_date_string(date_str):
    date_time = datetime.strptime(date_str, '%Y-%m-%d')
    difference = (datetime.now() - date_time).days // 365
    return difference


def main():
    if token is None:
        raise Exception("Invalid token")
    logger.info(f'Token used: {token}')

    logger.info('Fetching API...')
    results = get_paginated_data_from_repositories(10)

    results_dt = pd.DataFrame(results)
    logger.info(results_dt)
    logger.info(f'Results saved in "{GITHUB_DATA_CSV_FILENAME}"')
    results_dt.to_csv(GITHUB_DATA_CSV_FILENAME)


if __name__ == '__main__':
    token = os.getenv('GITHUB_TOKEN')

    try:
        main()
    except Exception as e:
        logger.warning(e)
