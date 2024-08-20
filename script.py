import requests

def handle_project_activation(response_data):
    headers = {
    "authorization": f"Token {api_token}" 
    }
    for i in response_data:
        status = i.get("attributes").get("status")
        # if project is not active 
        if status != "active":

            project_id = i.get("id")
            activate_project_url = f"https://api.snyk.io/v1/org/{org_id}/project/{project_id}/activate"
            response = requests.post(activate_project_url, headers=headers)

            # if response is successful 
            if response.status_code == 200:
                print(f"Project ID {project_id} was activated")
            else: 
                print(f"Error while activating project ID: {project_id}")

def get_projects_in_org(org_id, api_token,api_version,limit):
    headers = {
        "authorization": f"Token {api_token}" 
    }
    # empty list of projects
    projects = []
    get_projects_url = f"https://api.snyk.io/rest/orgs/{org_id}/projects/?version={api_version}&limit={limit}"
    response = requests.get(get_projects_url, headers=headers)
    response =response.json()

    # builds next_url 
    next_url = "https://api.snyk.io/" + response.get("links").get("next")

    # while we have a next_url
    while next_url:
        response_data = response.get("data")
        # append all requests data to projects list
        for i in response_data:
            projects.append(i)
        
        # fetch data from the next url 
        response = requests.get(next_url, headers=headers)
        response = response.json()
        response_data = response.get("data")

        # evaluate if there is a next url
        if response.get("links").get("next"):
            next_url = "https://api.snyk.io/" + response.get("links").get("next")
        else:
            next_url = None

    return projects


if __name__ == "__main__":
    # Variables to be used 
    org_id = "ORG_ID"
    api_token = "API_TOKEN"
    api_version = "2024-08-15"
    # project limits per request
    limit=100

    response_data = get_projects_in_org(org_id, api_token,api_version,limit)
    handle_project_activation(response_data)