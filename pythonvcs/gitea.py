"""
Support gitea module.
"""

from multiprocessing.sharedctypes import Value
import requests
from requests import Response
from secrets import SystemRandom
import hashlib

class GiteaPublicKey:
    """Gitea public key object."""
    def __init__(self, responsejson: dict):
        """Generate gitea public key.

        Args:
            responsejson (dict): Response json.

        Raises:
            WrongJSONError: If response json is not valid, raise this error.
        """
        try:
            self.created_at: str = responsejson['created_at']
        except (ValueError, KeyError, TypeError) as e:
            raise WrongJSONError(responsejson) from e
        self.fingerprint: str = responsejson['fingerprint']
        self.public_key_id: int = responsejson['id']
        self.key: str = responsejson['key']
        self.key_type: str = responsejson['key_type']
        self.read_only: bool = responsejson['read_only']
        self.title: str = responsejson['title']
        self.url: str = responsejson['url']
        self.user = GiteaUser(responsejson['user'])

class GPGKeyEmail:
    def __init__(self, email: str, verified: bool):
        """
        GPG key email properties.

        Args:
            email (str): Email address.
            verified (bool): Is verified email.
        """
        self.email: str = email
        self.verified: bool = verified

class GiteaEmail(GPGKeyEmail):
    def __init__(self, email: str, primary: bool, verified: bool):
        """
        Gitea email properties.

        Args:
            email (str): Email address.
            primary (bool): Is primary email.
            verified (bool): Is verified email.
        """
        super().__init__(email, verified)
        self.primary: bool = primary

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

class GiteaGPGKey:
    """GPGKey a user GPG key to sign commit and tag in repository"""
    def __init__(self, jsondict: dict):
        """Generate GPG Key properties from jsondict.

        Args:
            jsondict (dict): Gitea GPGKey json dict.

        Raises:
            WrongJSONError: When JSON does not have right key.
        """
        try:
            self.certify: bool = jsondict["can_certify"]
        except (KeyError, ValueError, TypeError) as e:
            raise WrongJSONError(jsondict) from e
        self.encrypt_comms: bool = jsondict["can_encrypt_comms"]
        self.encrypt_storage: bool = jsondict["can_encrypt_storage"]
        self.sign: bool = jsondict["can_sign"]
        self.created_at: bool = jsondict["created_at"]
        self.emails: list[GPGKeyEmail] = [
            GPGKeyEmail(i["email"], i["verified"]) for i in jsondict["emails"]
        ]
        self.expired_at: str = jsondict["expired_at"]
        self.id: int = jsondict["id"]
        self.key_id: str = jsondict["key_id"]
        self.primary_key_id: str = jsondict["primary_key_id"]
        self.public_key: str = jsondict["public_key"]
        self.verified: bool = jsondict["verified"]
        super().__init__(jsondict)
        self.subkey: list[GiteaGPGKey] or None = None
        if jsondict["subkeys"] != "null":
            self.subkey = [GiteaGPGKey(i) for i in jsondict["subkeys"]]

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
        except (TypeError, KeyError, ValueError) as e:
            raise WrongJSONError(jsondict) from e
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
    def string_to_visibility(string: str) -> Visibility or None:
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
    def __init__(self, name: str, password: str or None, url: str, token: str or None = None, cleanup: bool = True):
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

    def get_followers(self, page: int = None, limit: int = None) -> list[GiteaUser] or None:
        """Get followers of token owner.

        Args:
            page (int, optional): page number of results to return (1-based). Defaults to None.
            limit (int, optional): page size of results. Defaults to None.

        Raises:
            GiteaAPIError: When gitea api status code does not 200(success).

        Returns:
            list[GiteaUser] or None: return followers of token owner if has followers. else return None.
        """
        params = self.__pagelimitdetect__(page, limit)
        followersresponse = requests.get(f"{self.url}/user/followers", params=self.defaultparam | params )
        if followersresponse.status_code != 200:
            raise GiteaAPIError(followersresponse, followersresponse.status_code)
        if followersresponse.json == []:
            return None
        else:
            return [GiteaUser(i) for i in followersresponse.json()]

    def get_followings(self, page: int = None, limit: int = None) -> list[GiteaUser] or None:
        """Get following users of token owner.

        Args:
            page (int, optional): page number of results to return (1-based). Defaults to None.
            limit (int, optional): page size of results. Defaults to None.

        Raises:
            GiteaAPIError: When gitea api status code does not 200(success).

        Returns:
            list[GiteaUser] or None: return followings of token owner if has following users. else return None.
        """
        params = self.__pagelimitdetect__(page, limit)
        followingsresponse = requests.get(f"{self.url}/user/following", params=self.defaultparam | params)
        if followingsresponse.status_code != 200:
            raise GiteaAPIError(followingsresponse, followingsresponse.status_code)
        if followingsresponse.json == []:
            return None
        else:
            return [GiteaUser(i) for i in followingsresponse.json()]

    def __pagelimitdetect__(self, page: int,limit: int):
        params = {"page": page, "limit": limit}
        if page is None:
            del params["page"]
        if limit is None:
            del params["limit"]
        return params

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

    def get_gpg_keys(self, page: int = None, limit: int = None) -> list[GiteaGPGKey] or None:
        """Get gpg keys of token owner.

        Args:
            page (int, optional): page number of results to return (1-based). Defaults to None.
            limit (int, optional): page size of results. Defaults to None.

        Raises:
            GiteaAPIError: When gitea api status code does not 200(success).

        Returns:
            list[GiteaGPGKey] or None: GPG keys of token owner if has gpg keys. else, return None.
        """
        params = {"page": page, "limit": limit}
        if page is None:
            del params["page"]
        if limit is None:
            del params["limit"]
        response = requests.get(f"{self.url}/user/gpg_keys", params=self.defaultparam | params)
        if response.status_code != 200:
            raise GiteaAPIError(response, response.status_code)
        if response.json() == {}:
            return None
        else:
            return [GiteaGPGKey(i) for i in response.json()]

    def add_gpg_key(self, public_key: str, signature: str = None):
        """Add gpg key to token owner.

        Args:
            public_key (str): Public key that will be added.
            signature (str, optional): Signature of public key. Defaults to None.

        Raises:
            GiteaAPIError: When gitea api status code does not 201(success).

        Returns:
            GiteaGPGKey: GPG key that was added.
        """
        dataparam = {"public_key": public_key, "signature": signature}
        if signature is None:
            del dataparam["signature"]
        response = requests.post(
            f"{self.url}/user/gpg_keys",
            data=dataparam,
            params=self.defaultparam,
        )
        if response.status_code != 201:
            raise GiteaAPIError(response, response.status_code)
        return GiteaGPGKey(response.json())

    def get_gpg_key(self, id: int) -> GiteaGPGKey:
        """Get gpg key of token owner.

        Args:
            id (int): ID of gpg key that will be get.

        Raises:
            GiteaAPIError: When gitea api status code does not 200(success).

        Returns:
            GiteaGPGKey: GPG key that was get.
        """
        response = requests.get(f"{self.url}/user/gpg_keys/{id}", params=self.defaultparam)
        if response.status_code != 200:
            raise GiteaAPIError(response, response.status_code)
        return GiteaGPGKey(response.json())

    def delete_gpg_key(self, id: int):
        """Delete gpg key of token owner.

        Args:
            id (int): ID of gpg key that will be delete.

        Raises:
            GiteaAPIError: When gitea api status code does not 204(success).
        """
        response = requests.delete(f"{self.url}/user/gpg_keys/{id}", params=self.defaultparam)
        if response.status_code != 204:
            raise GiteaAPIError(response, response.status_code)

    def get_public_keys(self, fingerprint: str = None, page: int = None, limit: int = None) -> list[GiteaPublicKey] or None:
        """Get public keys of token owner.

        Args:
            fingerprint (str, optional): fingerprint of key. Defaults to None.
            page (int, optional): page number of results to return (1-based). Defaults to None.
            limit (int, optional): page size of results. Defaults to None.

        Raises:
            GiteaAPIError: When gitea api status code does not 200(success).

        Returns:
            list[GiteaPublicKey] or None: return Public keys of token owner if has public keys. else, return None.
        """
        params = self.__pagelimitdetect__(page, limit)
        if fingerprint is not None:
            params["fingerprint"] = fingerprint
        response = requests.get(f"{self.url}/user/keys", params=self.defaultparam | params)
        if response.status_code != 200:
            raise GiteaAPIError(response, response.status_code)
        if response.json() == []:
            return None
        return [GiteaPublicKey(i) for i in response.json()]

    def add_public_key(self, key: str, title: str, read_only: bool = None) -> GiteaPublicKey:
        """Add public key to token owner.

        Args:
            key (str): Public key that will be added.
            title (str): Title of public key.
            read_only (bool, optional): Describe if the key has only read access or read/write. Defaults to None.

        Raises:
            GiteaAPIError: When gitea api status code does not 201(success).

        Returns:
            GiteaPublicKey: Public key that was added.
        """
        params = {"key": key, "title": title}
        if read_only is not None:
            params["read_only"] = read_only
        response = requests.post(f"{self.url}/user/keys", params=self.defaultparam | params)
        if response.status_code != 201:
            raise GiteaAPIError(response, response.status_code)
        return GiteaPublicKey(response.json())

    def get_public_key(self, id: int) -> GiteaPublicKey:
        """Get public key of token owner.

        Args:
            id (int): ID of public key that will be get.

        Raises:
            GiteaAPIError: When gitea api status code does not 200(success).

        Returns:
            GiteaPublicKey: Public key that was get.
        """
        response = requests.get(f"{self.url}/user/keys/{id}", params=self.defaultparam)
        if response.status_code != 200:
            raise GiteaAPIError(response, response.status_code)
        return GiteaPublicKey(response.json())

    def delete_public_key(self, id: int):
        """Delete public key of token owner.

        Args:
            id (int): ID of public key that will be delete.

        Raises:
            GiteaAPIError: When gitea api status code does not 204(success).
        """
        response = requests.delete(f"{self.url}/user/keys/{id}", params=self.defaultparam)
        if response.status_code != 204:
            raise GiteaAPIError(response, response.status_code)

def random_key() -> str:
    """Random key for secure random."""
    return hashlib.sha3_512(str(SystemRandom().randint(1, 10000000)).encode('utf-8')).hexdigest()
