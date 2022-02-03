import requests
from requests import Response

class GiteaHandler:
    def __init__(self, name: str, password: str or None, url: str, token: str or None = None): # type: ignore
        self.name = name
        self.url = url
        if self.url.endswith('/'):
            self.url = self.url.removesuffix('/')
        if token is None:
            response: Response = requests.post(f"{self.url}/users/{self.name}/tokens", auth=(self.name, password))
            if response.status_code != 201:
                raise GiteaAPIError(response, response.status_code)
            else:
                self.token: str = response.json()["sha1"]
        else:
            self.token = token
        self.defaultparam: dict[str, str] = {"token": self.token}
        self.user = GiteaUser(requests.get(f"{self.url}/user", params=self.defaultparam))

class GiteaAPIError(Exception):
    def __init__(self, raw_data: Response, response_status_code: int):
        super().__init__()
        self.raw_data = raw_data
        self.response_status_code = response_status_code

class GiteaUser:
    def __init__(self, response: Response):
        responsejson: dict = response.json()
        self.active: bool = responsejson["active"]
        self.avatar_url = responsejson["avatar_url"]
        self.created_at = responsejson["created"]
        self.email = responsejson["email"]
        self.followers_count = responsejson["followers_count"]
        self.following_count = responsejson["following_count"]
        self.name = responsejson["full_name"]
        self.id = responsejson["id"]
        self.is_admin = responsejson["is_admin"]
        self.language = responsejson["language"]
        self.last_login = responsejson["last_login"]
        self.location = responsejson["location"]
        self.username = responsejson["login"]
        self.prohibit_login = responsejson["prohibit_login"]
        self.restricted = responsejson["restricted"]
        self.starred_count = responsejson["starred_repos_count"]
        self.visibility = responsejson["visibility"] # TODO will make visibility class.
        self.website = responsejson["website"]