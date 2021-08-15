import requests
import os
import json

token = os.getenv('GITHUB_TOKEN')
headers = {"Authorization": f"token {token}"}

query = """
query example {
  search(query: "stars:>1", type: REPOSITORY, first: 100) {
    nodes {
      ... on Repository {
        nameWithOwner
        createdAt
        stargazerCount
      }
    }
  }
}
"""

def run_query(query):
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))
  
result = run_query(query)# Execute the query
print(json.dumps(result, indent=4, sort_keys=True))# Prettify result