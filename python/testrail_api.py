import requests

class TestRailAPI:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.auth = (username, password)
        self.headers = {"Content-Type": "application/json"}

    def add_result_for_case(self, run_id, case_id, status_id, comment):
        url = f"{self.base_url}/index.php?/api/v2/add_result_for_case/{run_id}/{case_id}"
        data = {"status_id": status_id, "comment": comment}
        response = requests.post(url, json=data, auth=self.auth, headers=self.headers)
        return response.json()

    def get_run_id(self, project_id, suite_id):
        url = f"{self.base_url}/index.php?/api/v2/get_runs/{project_id}&suite_id={suite_id}"
        response = requests.get(url, auth=self.auth, headers=self.headers)
        runs = response.json()
        return runs[0]['id'] if runs else None
