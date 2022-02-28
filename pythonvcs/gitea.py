"""
Support gitea module.
"""

from multiprocessing.sharedctypes import Value
import requests
from requests import Response
from secrets import SystemRandom
import hashlib

class GiteaTrustModel:
    """Trust model for GiteaRepoOption"""    
    default = "default",
    collaborator = "collaborator",
    committer = "committer",
    collaboratorcomitter = "collaboratorcomitter"

class GiteaOrganization:
    """Gitea organization properties."""
    def __init__(self, avatar_url: str, description: str, full_name: str, giteaid: int, location: str, repo_admin_change_team_access: bool, username: str, visibility: str, website: str):
        """Initalize class

        Args:
            avatar_url (str): Avatar url of Organization
            description (str): Description of Organization
            full_name (str): Full name of Organization
            giteaid (int): ID of Organization
            location (str): Location of Organization
            repo_admin_change_team_access (bool): Repo admin change team access value
            username (str): Username of Organization
            visibility (str): Visibility of Organization
            website (str): Website of Organization
        """
        self.avatar_url = avatar_url
        self.description = description
        self.full_name = full_name
        self.id = giteaid
        self.location = location
        self.repo_admin_change_team_access = repo_admin_change_team_access
        self.username = username
        self.visibility = visibility
        self.website = website

class GiteaTeams:
    """A team in an organization"""
    def __init__(self, can_create_repo: bool, description: str, teamid: int, include_all_repositories: bool, 
                name: str, organization: GiteaOrganization, permission: str, repos_url: str, units: list, units_map: dict):
        """Initalize class

        Args:
            can_create_repo (bool): Can create repository value
            description (str): Description of team
            teamid (int): ID of team
            include_all_repositories (bool): Include all repositories value
            name (str): Name of team
            organization (GiteaOrganization): Organization of team
            permission (str): Permission of team
            repos_url (str): Repos url of team
            units (list): Units of team
            units_map (dict): Units dict of team

        Raises:
            ValueError: If permission value is wrong.
        """
        self.can_create_repo = can_create_repo
        self.description = description
        self.id = teamid
        self.include_all_repositories = include_all_repositories
        self.name = name
        self.organization = organization
        self.permission = permission
        if self.permission not in ["none", "read", "write", "admin", "owner"]:
            raise ValueError("Permission is wrong.")
        self.repos_url = repos_url
        self.units = units
        self.units_map = units_map

class GiteaPermission:
    """Gitea permissions properties."""
    def __init__(self, admin: bool, push: bool, pull: bool):
        """Initalize class

        Args:
            admin (bool): admin permission
            push (bool): push permission
            pull (bool): pull permission
        """
        self.admin = admin
        self.push = push
        self.pull = pull

class GiteaExternalWiki:
    """setting for external wiki"""
    def __init__(self, external_url: str):
        """Initalize Class

        Args:
            external_url (str): external wiki url
        """
        self.external_url = external_url

class GiteaInternalTracker:
    """Gitea internal tracker settings properties."""
    def __init__(self, allow_only_contributors_to_track_time: bool, enable_issue_dependencies: bool, enable_time_tracker: bool):
        """Initalize Class

        Args:
            allow_only_contributors_to_track_time (bool): Let only contributors track time (Built-in issue tracker)
            enable_issue_dependencies (bool): Enable dependencies for issues and pull requests (Built-in issue tracker)
            enable_time_tracker (bool): Enable time tracking (Built-in issue tracker)
        """
        self.allow_only_contributors_to_track_time = allow_only_contributors_to_track_time
        self.enable_issue_dependencies = enable_issue_dependencies
        self.enable_time_tracker = enable_time_tracker

class GiteaRepoOption:
    """GiteaRepoOption for making gitea repository"""
    def __init__(self, name: str, auto_init: bool = None, default_branch: str = None, description: str = None, gitignore: str = None,
                    issue_labels: str = None, license_template: str = None, private: bool = None, readme: str = None, template: bool = None,
                    trust_model: GiteaTrustModel = None):
        """Initalize Class

        Args:
            name (str): Repository name
            auto_init (bool, optional): Auto initliaze repository. Defaults to None.
            default_branch (str, optional): Default branch name. Defaults to None.
            description (str, optional): Repository description. Defaults to None.
            gitignore (str, optional): Gitignore template. Defaults to None.
            issue_labels (str, optional): Issue labels tamplate. Defaults to None.
            license_template (str, optional): License template. Defaults to None.
            private (bool, optional): Repository visibility. Defaults to None.
            readme (str, optional): Readme description. Defaults to None.
            template (bool, optional): What template to use. Defaults to None.
            trust_model (GiteaTrustModel, optional): Trust model. Defaults to None.
        """
        self.name = name
        self.auto_init = auto_init
        self.default_branch = default_branch
        self.description = description
        self.gitignore = gitignore
        self.issue_labels = issue_labels
        self.license_template = license_template
        self.private = private
        self.readme = readme
        self.template = template
        self.trust_model = trust_model

class GiteaSettings:
    """Gitea settings properties."""
    def __init__(self, description: str, diff_view_style: str, full_name: str, hide_activity: bool, hide_email: bool, language: str, location: str, theme: str, website: str):
        """Initalize class

        Args:
            description (str): Description of user
            diff_view_style (str): Diff view style of user
            full_name (str): Full name of user
            hide_activity (bool): Hide activity value of user
            hide_email (bool): Hide email value of user
            language (str): Language of user
            location (str): Location of user
            theme (str): Theme of user
            website (str): Website of user
        """        
        self.description = description
        self.diff_view_style = diff_view_style
        self.full_name = full_name
        self.hide_activity = hide_activity
        self.hide_email = hide_email
        self.language = language
        self.location = location
        self.theme = theme
        self.website = website

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

class GiteaRepoTransfer:
    """A pending repo transfer."""
    def __init__(self, doer: GiteaUser, recipient: GiteaUser, teams: list[str]):
        """Initalize class

        Args:
            doer (GiteaUser): The user who initiated the transfer.
            recipient (GiteaUser): The user who will receive the transfer.
            teams (list[str]): The teams that will be transferred.
        """
        self.doer = doer
        self.recipient = recipient
        self.teams: list[GiteaTeams] = []
        for i in teams:
            tempdata = i["organization"]
            organization = GiteaOrganization(tempdata["avatar_url"], tempdata["description"], tempdata["full_name"], tempdata["id"], tempdata["location"], tempdata["repo_admin_change_team_access"],
                                            tempdata["username"], tempdata["visibility"], tempdata["website"])
            self.teams.append(GiteaTeams(i["can_create_repo"], i["description"], i["id"], i["include_all_repositories"], i["name"], organization, i["permission"], i["repo_url"], i["units"], i["units_map"]))


class GiteaExtenalTracker:
    """Gitea settings for external tracker"""
    def __init__(self, external_tracker_format: str, external_tracker_style: str, external_tracker_url: str):
        """Initalize class

        Args:
            external_tracker_format (str): External Issue Tracker URL Format. Use the placeholders {user}, {repo} and {index} for the username, repository name and issue index.
            external_tracker_style (str): External Issue Tracker Number Format, either numeric or alphanumeric
            external_tracker_url (str): URL of external issue tracker.
        """
        self.external_tracker_format: str = external_tracker_format
        self.external_tracker_style: str = external_tracker_style
        self.external_tracker_url: str = external_tracker_url

class GiteaRepository:
    """Gitea repository properties."""
    def __init__(self, response: dict):
        """Initalize class

        Args:
            response (dict): The response json.
        """        
        self.allow_merge_commits: bool = response["allow_merge_commits"]
        self.allow_rebase: bool = response["allow_rebase"]
        self.allow_rebase_explicit: bool = response["allow_rebase_explicit"]
        self.archived: bool = response["archived"]
        self.avatar_url: str = response["avatar_url"]
        self.clone_url: str = response["clone_url"]
        self.created_at: str = response["created_at"]
        self.default_branch: str = response["default_branch"]
        self.default_merge_style: str = response["default_merge_style"]
        self.description: str = response["description"]
        self.empty: bool = response["empty"]
        try:
            tempdata = response["external_tracker"]
        except (TypeError, KeyError):
            self.external_tracker = None
        else: 
            self.external_tracker: GiteaExtenalTracker = GiteaExtenalTracker(tempdata["external_tracker_format"], tempdata["external_tracker_style"], tempdata["external_tracker_url"])
        self.fork: bool = response["fork"]
        self.forks_count: int = response["forks_count"]
        self.full_name: str = response["full_name"]
        self.has_issues: bool = response["has_issues"]
        self.has_projects: bool = response["has_projects"]
        self.has_pull_requests: bool = response["has_pull_requests"]
        self.has_wiki: bool = response["has_wiki"]
        self.html_url: str = response["html_url"]
        self.id: int = response["id"]
        self.ignore_whitespace_conflicts: bool = response["ignore_whitespace_conflicts"]
        self.internal: bool = response["internal"]
        tempdata = response["internal_tracker"]
        self.internal_tracker: GiteaInternalTracker = GiteaInternalTracker(tempdata["allow_only_contributors_to_track_time"], tempdata["enable_issue_dependencies"], tempdata["enable_time_tracker"])
        self.mirror: bool = response["mirror"]
        self.mirror_interval: str = response["mirror_interval"]
        self.mirror_updated: str = response["mirror_updated"]
        self.name: str = response["name"]
        self.open_issues_count: str = response["open_issues_count"]
        self.open_pr_counter: int = response["open_pr_counter"]
        self.url: str = response["original_url"]
        if not self.url:
            self.url = response["html_url"]
        self.owner: GiteaUser = GiteaUser(response["owner"])
        self.parent: str = response["parent"]
        tempdata = response["permissions"]
        self.permissions: GiteaPermission = GiteaPermission(tempdata["admin"], tempdata["push"], tempdata["pull"])
        self.private: bool = response["private"]
        self.release_counter: int = response["release_counter"]
        tempdata = response["repo_transfer"]
        try:
            self.repo_transfer: GiteaRepoTransfer = GiteaRepoTransfer(GiteaUser(tempdata["doer"]), GiteaUser(tempdata["recipient"]), tempdata["teams"])
        except (TypeError, KeyError):
            self.repo_transfer = None
        self.size: int = response["size"]
        self.ssh_url: str = response["ssh_url"]
        self.stars: int = response["stars_count"]
        self.template: bool = response["template"]
        self.updated_at: str = response["updated_at"]
        self.watchers_count: int = response["watchers_count"]

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
            data: dict[str, str] = {"name": f'gitea-pythonvcs-{random_key()}'}
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

    def get_repositories(self) -> list[GiteaRepository]:
        """Get repositories of token owner.

        Raises:
            GiteaAPIError: When gitea api status code does not 200(success).

        Returns:
            list[GiteaRepository]: Repositories that was get.
        """
        response = requests.get(f"{self.url}/user/repos", params=self.defaultparam)
        if response.status_code != 200:
            raise GiteaAPIError(response, response.status_code)
        return [GiteaRepository(i) for i in response.json()]

    def create_repository(self, option: GiteaRepoOption) -> GiteaRepository:
        """Create repository of token owner.

        Args:
            option (GiteaRepoOption): Repository option that will be created.

        Raises:
            GiteaAPIError: When gitea api status code does not 201(success).

        Returns:
            GiteaRepository: Repository that was created.
        """
        options = option.__dict__
        for i, i2 in enumerate(options):
            if i2 is None:
                del options[i]
        response = requests.post(f"{self.url}/user/repos", data=options, params=self.defaultparam)
        if response.status_code != 201:
            raise GiteaAPIError(response, response.status_code)
        return GiteaRepository(response.json())

    def get_settings(self) -> GiteaSettings:
        """Get settings of token owner.

        Raises:
            GiteaAPIError: When gitea api status code does not 200(success).

        Returns:
            GiteaSettings: Settings that was get.
        """        
        response = requests.get(f"{self.url}/user/settings", params=self.defaultparam)
        if response.status_code != 200:
            raise GiteaAPIError(response, response.status_code)
        return self.__response_to_settings__(response.json())

    def change_settings(self, new_settings: GiteaSettings) -> GiteaSettings:
        """Change settings of token owner.

        Args:
            new_settings (GiteaSettings): New settings that will be changed.

        Raises:
            GiteaAPIError: When gitea api status code does not 200(success).

        Returns:
            GiteaSettings: Settings that was changed.
        """
        response = requests.patch(f"{self.url}/user/settings", params=self.defaultparam, data=new_settings.__dict__)
        if response.status_code != 200:
            raise GiteaAPIError(response, response.status_code)
        return self.__response_to_settings__(response.json())

    def change_setting(self, new_setting_name: str, new_setting_value: bool or str) -> GiteaSettings:
        """Change setting of token owner.

        Args:
            new_setting_name (str): Name of setting that will be changed.
            new_setting_value (bool or str): Value of setting that will be changed.

        Raises:
            GiteaAPIError: When gitea api status code does not 200(success).

        Returns:
            GiteaSettings: Settings that was changed.
        """
        setting = self.get_settings()
        setting.__setattr__(new_setting_name, new_setting_value)
        return self.change_settings(setting)

    def get_starred_repositories(self) -> list[GiteaRepository] or list:
        """Get starred repositories of token owner.

        Raises:
            GiteaAPIError: When gitea api status code does not 200(success).

        Returns:
            list[GiteaRepository] or list: Starred repositories that was get.
        """        
        response = requests.get(f"{self.url}/user/starred", params=self.defaultparam)
        if response.status_code != 200:
            raise GiteaAPIError(response, response.status_code)
        if response.json() == []:
            return []
        else:
            return [GiteaRepository(i) for i in response.json()]

    def star_repository(self, owner: str, repo: str):
        """Star repository.

        Args:
            owner (str): Owner of repository that will be starred.
            repo (str): Repository that will be starred.

        Raises:
            GiteaAPIError: When gitea api status code does not 204(success).
        """
        response = requests.put(f"{self.url}/user/starred/{owner}/{repo}", params=self.defaultparam)
        if response.status_code != 204:
            raise GiteaAPIError(response, response.status_code)

    def unstar_repository(self, owner: str, repo: str):
        """Unstar repository.

        Args:
            owner (str): Owner of repository that will be unstarred.
            repo (str): Repository that will be unstarred.

        Raises:
            GiteaAPIError: When gitea api status code does not 204(success).
        """        
        response = requests.delete(f"{self.url}/user/starred/{owner}/{repo}", params=self.defaultparam)
        if response.status_code != 204:
            raise GiteaAPIError(response, response.status_code)

    def __response_to_settings__(self, response: dict) -> GiteaSettings:
        """Convert response to settings.

        Args:
            response (dict): Response that will be converted.

        Returns:
            GiteaSettings: Settings that was converted.
        """
        return GiteaSettings(response["description"], response["diff_view_style"], response["full_name"], response["hide_activity"], response["hide_email"], response["language"], response["location"],
                    response["theme"], response["website"])

def random_key() -> str:
    """Random key for secure random."""
    return hashlib.sha3_512(str(SystemRandom().randint(1, 10000000)).encode('utf-8')).hexdigest()
