# Documentation for Gitea

- [Documentation for Gitea](#documentation-for-gitea)
  - [Class GiteaHandler](#class-giteahandler)
    - [Method get_emails](#method-get_emails)
    - [Method add_emails](#method-add_emails)
    - [Method remove_emails](#method-remove_emails)
    - [Method get_followers](#method-get_followers)
    - [Method get_followings](#method-get_followings)
    - [Method follow_user](#method-follow_user)
    - [Method unfollow_user](#method-unfollow_user)
    - [Method get_gpg_keys](#method-get_gpg_keys)
    - [Method add_gpg_key](#method-add_gpg_key)
    - [Method get_gpg_key](#method-get_gpg_key)
    - [Method delete_gpg_key](#method-delete_gpg_key)
    - [Method get_public_keys](#method-get_public_keys)
    - [Method add_public_key](#method-add_public_key)
    - [Method get_public_key](#method-get_public_key)
    - [Method delete_public_key](#method-delete_public_key)
    - [Method get_repos](#method-get_repos)
    - [Method create_repository](#method-create_repository)
    - [Method get_settings](#method-get_settings)
    - [Method change_settings](#method-change_settings)
    - [Method change_setting](#method-change_setting)
    - [Method get_starred_repositories](#method-get_starred_repositories)
    - [Method star_repository](#method-star_repository)
    - [Method unstar_repository](#method-unstar_repository)
  - [Class GiteaAPIError: Exception](#class-giteaapierror-exception)
  - [Class WrongJSONError: Exception](#class-wrongjsonerror-exception)
  - [Class GiteaUser](#class-giteauser)
  - [Class Visibility](#class-visibility)
  - [Method random_key](#method-random_key)
  - [Class GPGKeyEmail](#class-gpgkeyemail)
  - [Class GiteaEmail: GPGKeyEmail](#class-giteaemail-gpgkeyemail)
  - [Class GiteaGPGKey](#class-giteagpgkey)
  - [Class GiteaSettings](#class-giteasettings)
  - [Class GiteaRepository](#class-gitearepository)
  - [Class GiteaExternalTracker](#class-giteaexternaltracker)
  - [Class GiteaInternalTracker](#class-giteainternaltracker)
  - [Class GiteaPermission](#class-giteapermission)
  - [Class GiteaRepoTransfer](#class-gitearepotransfer)
  - [Class GiteaTeams](#class-giteateams)
  - [Class GiteaOrganization](#class-giteaorganization)

## Class GiteaHandler

Handler for gitea.

### Arguments

    name (str): The name of gitea user.  
    password (str or None): The password of gitea user. Need for cleanup and token generation.  
    url (str): The url of gitea.  
    token (str or None, optional): Token for gitea. Defaults to None.  
    cleanup (bool, optional): Cleanup token that giteahandler made. Defaults to True.  

### Raises

    ValueError: When token and password is None or password is None and cleanup is True.
    GiteaAPIError: When gitea api status code does not 201(success).

### Method get_emails

Get emails of token owner.

#### Return

    list[GiteaEmail]: Emails of token owner.

### Method add_emails

Add emails to token owner.

#### Arguments

    emails (list[str]): Emails that will be added.

#### Raises

    GiteaAPIError: When gitea api status code does not 201(success).

#### Return

    list[GiteaEmail]: Emails that was added.

### Method remove_emails

Remove emails from token owner.

#### Arguments

    emails (list[str]): Emails that will be removed.

#### Raises

    GiteaAPIError: When gitea api status code does not 204(success).

### Method get_followers

Get followers of token owner.

#### Arguments

    page (int, optional): page number of results to return (1-based). Defaults to None.
    limit (int, optional): page size of results. Defaults to None.

#### Raises

    GiteaAPIError: When gitea api status code does not 200(success).

#### Return

    list[GiteaUser] or None: Followers of token owner if has followers. else, return None.

### Method get_followings

Get followings of token owner.

#### Arguments

    page (int, optional): page number of results to return (1-based). Defaults to None.
    limit (int, optional): page size of results. Defaults to None.

#### Raises

    GiteaAPIError: When gitea api status code does not 200(success).

#### Return

    list[GiteaUser] or None: Followings of token owner if has following users. else, return None.

### Method follow_user

Follow user.

#### Arguments

    username (str): Username that will be follow.

#### Raises

    GiteaAPIError: When gitea api status code does not 204(success).

### Method unfollow_user

Unfollow user.

#### Arguments

    username (str): Username that will be unfollow.

### Method get_gpg_keys

Get gpg keys of token owner.

#### Arguments

    page (int, optional): page number of results to return (1-based). Defaults to None.
    limit (int, optional): page size of results. Defaults to None.

#### Raises

    GiteaAPIError: When gitea api status code does not 200(success).

#### Returns

    list[GiteaGPGKey] or None: GPG keys of token owner if has gpg keys. else, return None.

### Method add_gpg_key

Add gpg key to token owner.

#### Arguments

    public_key (str): Public key that will be added.
    signature (str, optional): Signature of public key. Defaults to None.

#### Raises

    GiteaAPIError: When gitea api status code does not 201(success).

#### Returns

    GiteaGPGKey: GPG key that was added.

### Method get_gpg_key

Get gpg key of token owner.

#### Arguments

    id (int): ID of gpg key that will be get.

#### Raises

    GiteaAPIError: When gitea api status code does not 200(success).

#### Returns

    GiteaGPGKey: GPG key that was get.

### Method delete_gpg_key

Delete gpg key of token owner.

#### Arguments

    id (int): ID of gpg key that will be delete.

#### Raises

    GiteaAPIError: When gitea api status code does not 204(success).

### Method get_public_keys

Get public keys of token owner.

#### Arguments

    fingerprint (str, optional): fingerprint of key. Defaults to None.
    page (int, optional): page number of results to return (1-based). Defaults to None.
    limit (int, optional): page size of results. Defaults to None.

#### Raises

    GiteaAPIError: When gitea api status code does not 200(success).

#### Returns

    list[GiteaPublicKey] or None: return Public keys of token owner if has public keys. else, return None.

### Method add_public_key

Add public key to token owner.

#### Arguments

    key (str): Public key that will be added.
    title (str): Title of public key.
    read_only (bool, optional): Describe if the key has only read access or read/write. Defaults to None.

#### Raises

    GiteaAPIError: When gitea api status code does not 201(success).

#### Returns

    GiteaPublicKey: Public key that was added.

### Method get_public_key

Get public key of token owner.

#### Arguments

    id (int): ID of public key that will be get.

#### Raises

    GiteaAPIError: When gitea api status code does not 200(success).

#### Returns

    GiteaPublicKey: Public key that was get.

### Method delete_public_key

Delete public key of token owner.

#### Arguments

    id (int): ID of public key that will be delete.

#### Raises

    GiteaAPIError: When gitea api status code does not 204(success).

### Method get_repos

    get repositories of token owner.

#### Raises

    GiteaAPIError: When gitea api status code does not 200(success).

#### Returns

    list[GiteaRepository]: Repositories that was get.

### Method create_repository

    Create repository of token owner.

#### Arguments

    option (GiteaRepoOption): Repository option that will be created.

#### Raises

    GiteaAPIError: When gitea api status code does not 201(success).

#### Returns

    GiteaRepository: Repository that was created.

### Method get_settings

Get settings of token owner.

#### Raises

    GiteaAPIError: When gitea api status code does not 200(success).

#### Returns

    GiteaSettings: Settings that was get.

### Method change_settings

    Change settings of token owner.

#### Arguments

    new_settings (GiteaSettings): New settings that will be changed.

#### Raises

    GiteaAPIError: When gitea api status code does not 200(success).

#### Returns

    GiteaSettings: Settings that was changed.

### Method change_setting

Change setting of token owner.

#### Arguments

    new_setting_name (str): Name of setting that will be changed.
    new_setting_value (bool or str): Value of setting that will be changed.

#### Raises

    GiteaAPIError: When gitea api status code does not 200(success).

#### Returns

    GiteaSettings: Settings that was changed.

### Method get_starred_repositories

    Get starred repositories of token owner.

#### Raises

    GiteaAPIError: When gitea api status code does not 200(success).

#### Returns

    list[GiteaRepository] or list: Starred repositories that was get.

### Method star_repository

    Star repository.

#### Arguments

    owner (str): Owner of repository that will be starred.
    repo (str): Repository that will be starred.

#### Raises

    GiteaAPIError: When gitea api status code does not 204(success).

### Method unstar_repository

    Unstar repository.

#### Arguments

    owner (str): Owner of repository that will be unstarred.
    repo (str): Repository that will be unstarred.

#### Raises

    GiteaAPIError: When gitea api status code does not 204(success).

## Class GiteaAPIError: Exception

raised when api does not success.

## Class WrongJSONError: Exception

raised when JSON does not have right key.

## Class GiteaUser

Class for find gitea user properties easily.

### Arguments

    jsondict (jsondict): The /user response json.

### Raises

    WrongJSONError: When JSON is invaild.

## Class Visibility

Visibility for vaild visibility property.

### Values

    public = "public"
    limited = "limited"
    private = "private"

## Method random_key

Random key for secure random.

### Return

    str: Return key encrypted with random value and sha3-512.

## Class GPGKeyEmail

GPG key email properties.

### Arguments

    email (str): Email address.
    verified (bool): Is verified email.

## Class GiteaEmail: GPGKeyEmail

Gitea email properties.

### Arguments

    email (str): Email address.
    primary (bool): Is primary email.
    verified (bool): Is verified email.

## Class GiteaGPGKey

GPGKey a user GPG key to sign commit and tag in repository.

### Arguments

    jsondict (dict): Gitea GPGKey json dict.

### Raises

    WrongJSONError: When JSON does not have right key.

## Class GiteaSettings

    Gitea settings properties.

### Arguments

    description (str): Description of user
    diff_view_style (str): Diff view style of user
    full_name (str): Full name of user
    hide_activity (bool): Hide activity value of user
    hide_email (bool): Hide email value of user
    language (str): Language of user
    location (str): Location of user
    theme (str): Theme of user
    website (str): Website of user

## Class GiteaRepository

    Gitea repository properties.

## Class GiteaExternalTracker

    Gitea settings for external tracker

### Arguments

    external_tracker_format (str): External Issue Tracker URL Format. Use the placeholders {user}, {repo} and {index} for the username, repository name and issue index.
    external_tracker_style (str): External Issue Tracker Number Format, either numeric or alphanumeric
    external_tracker_url (str): URL of external issue tracker.

## Class GiteaInternalTracker

    Gitea internal tracker settings properties.

### Arguments

    allow_only_contributors_to_track_time (bool): Let only contributors track time (Built-in issue tracker)
    enable_issue_dependencies (bool): Enable dependencies for issues and pull requests (Built-in issue tracker)
    enable_time_tracker (bool): Enable time tracking (Built-in issue tracker)

## Class GiteaPermission

    Gitea permissions properties.

### Arguments

    admin (bool): admin permission
    push (bool): push permission
    pull (bool): pull permission

## Class GiteaRepoTransfer

    A pending repo transfer.

### Arguments

    doer (GiteaUser): The user who initiated the transfer.
    recipient (GiteaUser): The user who will receive the transfer.
    teams (list[str]): The teams that will be transferred

## Class GiteaTeams

    A team in an organization.

### Arguments

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

### Raises

    ValueError: If permission value is wrong.

## Class GiteaOrganization

    Gitea organization properties.

### Arguments

    avatar_url (str): Avatar url of Organization
    description (str): Description of Organization
    full_name (str): Full name of Organization
    giteaid (int): ID of Organization
    location (str): Location of Organization
    repo_admin_change_team_access (bool): Repo admin change team access value
    username (str): Username of Organization
    visibility (str): Visibility of Organization
    website (str): Website of Organization
