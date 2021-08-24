import json

import requests
import os
import pandas as pd
import logging

token = os.getenv('GITHUB_TOKEN')
logger = logging.Logger(name=__name__, level=logging.DEBUG)


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
                    releases(first:1){
                        totalCount
                    }
                    updatedAt
                    primaryLanguage{
                        name
                    }
                    open: issues(states:OPEN){
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
        logger.info(json.dumps(result, indent=4, sort_keys=True))
        csv.append(result)
        if not has_next_page:
            logger.info("Has_next_page returned False")

    return csv


if __name__ == '__main__':
    try:
        results = get_paginated_data_from_repositories(10)
        pd.DataFrame(results).to_csv('results.csv')
        logger.info('Results saved in "results.csv"')
    except Exception as e:
        logger.warning(e)
