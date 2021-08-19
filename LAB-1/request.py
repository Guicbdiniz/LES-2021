import requests
import os
import json

token = os.getenv('GITHUB_TOKEN')
headers = {"Authorization": f"token {token}"}

query = """
query{
	search(query:"stars:>100", type:REPOSITORY, first:100){
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
"""

def run_query(query):
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception(f"Query failed to run by returning code of {request.status_code}. {query}")

result = run_query(query)
print(json.dumps(result, indent=4, sort_keys=True))# Prettify result

print(f"\nResults count: {len(result)}")
