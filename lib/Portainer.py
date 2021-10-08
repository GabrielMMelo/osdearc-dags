import json
import requests


class PortainerAPI:
    def __init__(self, username, password, host="localhost", port=7999, ssl=False):
        self.host = host
        self.port = port
        self.ssl = ssl
        self.username = username,
        self.password = password,
        self.url = "http{use_ssl}://{host}:{port}/api".format(
            use_ssl="s" if self.ssl else "",
            host=host,
            port=port
        )
        self.base_headers = {
            "Authorization": "Bearer {jwt}".format(
                jwt=self._get_jwt()
            )
        }
        self.stacks = self._get_stacks()

    def _get_jwt(self):
        url = self.url + "/auth"
        data = {
            "username": self.username,
            "password": self.password
        }

        response = requests.post(url=url, data=json.dumps(data))
        try:
            return response.json()["jwt"]
        except KeyError:
            return None

    def _get_stacks(self):
        url = self.url + "/stacks"
        response = requests.get(url=url, headers=self.base_headers)
        stacks = response.json()
        return {stack["Name"]: stack["Id"] for stack in stacks}

    def stop_stack_by_name(self, stack_name):
        url = self.url + "/stacks/{id}/stop".format(id=self.stacks[stack_name])
        response = requests.post(url=url, headers=self.base_headers)
        return response.json() is not None

    def start_stack_by_name(self, stack_name):
        url = self.url + "/stacks/{id}/start".format(id=self.stacks[stack_name])
        response = requests.post(url=url, headers=self.base_headers)
        return response.json() is not None
