import json
import git
import requests
import os
import pandas as pd
import logging

CHARTS_FOLDER_NAME = 'charts'

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def query_github_api(filter, quantity, cursor):
    headers = {"Authorization": f"token {token}"}
    query = '''
    query{
        search(query:"''' + filter + '''", type:REPOSITORY, first:"''' + quantity + '''", after:"''' + cursor + '''"){
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
    filter = "language:java sort:stars"
    quantity = "100"
    cursor = "Y3Vyc29yOjAK"  # Page = 0
    csv = []

    while has_next_page and (num_pages > 0):
        data = query_github_api(filter, quantity, cursor)['data']
        num_pages = num_pages - 1
        has_next_page = data['search']['pageInfo']['hasNextPage']
        cursor = data['search']['pageInfo']['endCursor']
        result = data['search']['nodes']
        logger.debug(json.dumps(result, indent=4, sort_keys=True))
        csv += result
        if not has_next_page:
            logger.info("Has_next_page returned False")

    return csv


def main():
    if token is None:
        raise Exception("Invalid token")
    logger.info(f'Token used: {token}')

    logger.info('Fetching API...')
    results = get_paginated_data_from_repositories(10)
    results_dt = pd.DataFrame(results)

    logger.info('Results saved in "results.csv"')
    results_dt.to_csv('results.csv')


if __name__ == '__main__':
    token = os.getenv('GITHUB_TOKEN')

    try:
        main()
    except Exception as e:
        logger.warning(e)
