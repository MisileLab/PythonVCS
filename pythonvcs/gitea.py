"""
Support gitea module.
"""

import requests
from requests import Response
from secrets import SystemRandom
import hashlib

class GiteaEmail:
    def __init__(self, email: str, primary: bool, verified: bool):
        """
        Gitea email properties.

        Args:
            email (str): Email address.
            primary (bool): Is primary email.
            verified (bool): Is verified email.
        """
        self.email: str = email
        self.primary: bool = primary
        self.verified: bool = verified

class GiteaAPIError(Exception):
    """raised when api does not success."""
    def __init__(self, raw_data: Response, response_status_code: int):
        super().__init__(f"GiteaAPIError with status code: {response_status_code}")
        self.raw_data = raw_data
        self.response_status_code = response_status_code

class WrongJSONError(Exception):
    """raised when JSON does not have right key."""
    def __init__(self, data: dict):
        super().__init__(f"Wrong json key: {data}")
        self.data = data

class Visibility:
    """Visibility for vaild visibility property."""
    public = "public"
    limited = "limited"
    private = "private"

class GiteaUser:
    """Class for find gitea user properties easily."""
    def __init__(self, jsondict: dict):
        """
        Dict to gitea user properties.

        Args:
            jsondict (dict) : The response json.

        Raises:
            WrongJSONError: When JSON is invaild.
        """
        try:
            self.active: bool = jsondict["active"]
        except (TypeError, KeyError, ValueError):
            raise WrongJSONError(jsondict)
        self.avatar_url: str = jsondict["avatar_url"]
        self.created_at: str = jsondict["created"]
        self.email: str = jsondict["email"]
        self.followers_count: int = jsondict["followers_count"]
        self.following_count: int = jsondict["following_count"]
        self.name: str = jsondict["full_name"]
        self.id: int = jsondict["id"]
        self.is_admin: bool = jsondict["is_admin"]
        self.language: str = jsondict["language"]
        self.last_login: str = jsondict["last_login"]
        self.location: str = jsondict["location"]
        self.username: str = jsondict["login"]
        self.prohibit_login: bool = jsondict["prohibit_login"]
        self.restricted: bool = jsondict["restricted"]
        self.starred_count: int = jsondict["starred_repos_count"]
        self.visibility: str = self.string_to_visibility(jsondict["visibility"])
        self.website: str = jsondict["website"]

    @staticmethod
    def string_to_visibility(string: str) -> Visibility or None: # type: ignore
        """Check visibility.
        Args:
            string (str): String that will be checked.

        Returns:
            str or None: if visibility is vaild, return visibility class. else, return None
        """
        if string == "public":
            return Visibility.public
        elif string == "private":
            return Visibility.private
        elif string == "limited":
            return Visibility.limited
        else:
            return None

class GiteaHandler:
    """Handler for gitea."""
    def __init__(self, name: str, password: str or None, url: str, token: str or None = None, cleanup: bool = True):    # type: ignore
        """
        Generate gitea handler.

        Args:
            name (str): The name of gitea user.
            password (str or None): The password of gitea user. Need for cleanup and token generation.
            url (str): The url of gitea.
            token (str or None, optional): Token for gitea. Defaults to None.
            cleanup (bool, optional): Cleanup token that giteahandler made. Defaults to True.

        Raises:
            ValueError: When token and password is None or password is None and cleanup is True.
            GiteaAPIError: When gitea api status code does not 201(success).
        """
        if (token is None and password is None) or password is None and cleanup:
            raise ValueError("not right parameter.")
        self.name = name
        self.url = url
        if self.url.endswith('/'):
            self.url = self.url.removesuffix('/')
        self.url = f'{self.url}/api/v1'
        if token is None and password is not None:
            responseget: Response = requests.get(f"{self.url}/users/{self.name}/tokens", auth=(self.name, password))
            if cleanup:
                for i in responseget.json():
                    namea: str = i["name"]
                    if namea.startswith("gitea-pythonvcs-"):
                        requests.delete(f"{self.url}/users/{self.name}/tokens/{namea}", auth=(self.name, password))
            data: dict[str, str] = {
                "name": "gitea-pythonvcs-" + random_key()
            }
            response: Response = requests.post(f"{self.url}/users/{self.name}/tokens", auth=(self.name, password), data=data)
            if response.status_code != 201:
                raise GiteaAPIError(response, response.status_code)
            else:
                self.token: str = response.json()["sha1"]
        else:
            self.token = token
        self.defaultheader: dict[str, str] = {
            "accept": "application/json",
            "Authorization": f'token {self.token}',
        }
        self.defaultparam: dict[str, str] = {"token": self.token}
        self.user = GiteaUser(requests.get(f"{self.url}/user", headers=self.defaultheader).json())

    def get_emails(self) -> list[GiteaEmail]:
        """Get emails of token owner.

        Returns:
            list[GiteaEmail]: Emails of token owner.
        """
        emails = requests.get(f"{self.url}/user/emails", params=self.defaultparam).json()
        return [GiteaEmail(i["email"], i["primary"], i["verified"]) for i in emails]

    def add_emails(self, emails: list[str]) -> list[GiteaEmail]:
        """Add emails to token owner.

        Args:
            emails (list[str]): Emails that will be added.

        Raises:
            GiteaAPIError: When gitea api status code does not 201(success).

        Returns:
            list[GiteaEmail]: Emails that was added.
        """
        emailresponse = requests.post(f"{self.url}/user/emails", data={"emails": emails}, params=self.defaultparam)
        if emailresponse.status_code != 201:
            raise GiteaAPIError(emailresponse, emailresponse.status_code)
        return [
            GiteaEmail(i["email"], i["primary"], i["verified"])
            for i in emailresponse.json()
        ]

    def remove_emails(self, emails: list[str]):
        """Remove emails from token owner.

        Args:
            emails (list[str]): Emails that will be removed.

        Raises:
            GiteaAPIError: When gitea api status code does not 204(success).
        """
        emailresponse = requests.delete(f"{self.url}/user/emails", json={"emails": emails}, params=self.defaultparam, headers=self.defaultheader)
        if emailresponse.status_code != 204:
            raise GiteaAPIError(emailresponse, emailresponse.status_code)

    def get_followers(self) -> list[GiteaUser] or None:    # type: ignore
        """Get followers of token owner.

        Raises:
            GiteaAPIError: When gitea api status code does not 200(success).

        Returns:
            list[GiteaUser] or None: Followers of token owner if has followers. else, return None.
        """
        followersresponse = requests.get(f"{self.url}/user/followers", params=self.defaultparam)
        if followersresponse.status_code != 200:
            raise GiteaAPIError(followersresponse, followersresponse.status_code)
        if followersresponse.json == []:
            return None
        else:
            return [GiteaUser(i) for i in followersresponse.json()]

    def get_followings(self) -> list[GiteaUser] or None: # type: ignore
        """Get following users of token owner.

        Raises:
            GiteaAPIError: When gitea api status code does not 200(success).

        Returns:
            list[GiteaEmail] or None: Followings of token owner if has following users. else, return None.
        """
        followingsresponse = requests.get(f"{self.url}/user/following", params=self.defaultparam)
        if followingsresponse.status_code != 200:
            raise GiteaAPIError(followingsresponse, followingsresponse.status_code)
        if followingsresponse.json == []:
            return None
        else:
            return [GiteaUser(i) for i in followingsresponse.json()]

    def follow_user(self, username: str):
        """Follow user.

        Args:
            username (str): Username that will be follow.

        Raises:
            GiteaAPIError: When gitea api status code does not 204(success).
        """
        followresponse = requests.put(f"{self.url}/user/following/{username}", params=self.defaultparam)
        if followresponse.status_code != 204:
            raise GiteaAPIError(followresponse, followresponse.status_code)

    def unfollow_user(self, username: str):
        """Unfollow user.

        Args:
            username (str): Username that will be unfollow.

        Raises:
            GiteaAPIError: When gitea api status code does not 204(success).
        """
        response = requests.delete(f"{self.url}/user/following/{username}", params=self.defaultparam)
        if response.status_code != 204:
            raise GiteaAPIError(response, response.status_code)

def random_key() -> str:
    """Random key for secure random."""
    return hashlib.sha3_512(str(SystemRandom().randint(1, 10000000)).encode('utf-8')).hexdigest()
