import requests
import os
import pandas as pd
import json

token = os.getenv('GITHUB_TOKEN')

def run_query(cursor):
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
        raise Exception(f"Query failed to run by returning code of {request.status_code}. {query}")

def paginate(pages):
    has_next_page = True
    cursor="Y3Vyc29yOjAK" # Page = 0
    csv = []

    while (has_next_page and (pages > 0)):
        data = run_query(cursor)['data']
        pages = pages - 1
        has_next_page = data['search']['pageInfo']['hasNextPage']
        cursor = data['search']['pageInfo']['endCursor']
        result = data['search']['nodes']
        # print(json.dumps(result, indent=4, sort_keys=True))# Prettify result # Debug
        csv.append(result)  
        if not has_next_page:
            print("has_next_page returned false")
       
    return csv

results = paginate(10)
pd.DataFrame(results).to_csv('results.csv')
