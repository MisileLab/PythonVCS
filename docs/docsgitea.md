# Documentation for Gitea

- [Documentation for Gitea](#documentation-for-gitea)
  - [Class GiteaHandler](#class-giteahandler)
    - [Arguments](#arguments)
    - [Raises](#raises)
    - [Method get_emails](#method-get_emails)
      - [Return](#return)
    - [Method add_emails](#method-add_emails)
      - [Arguments](#arguments-1)
      - [Raises](#raises-1)
      - [Return](#return-1)
    - [Method remove_emails](#method-remove_emails)
      - [Arguments](#arguments-2)
      - [Raises](#raises-2)
    - [Method get_followers](#method-get_followers)
      - [Arguments](#arguments-3)
      - [Raises](#raises-3)
      - [Return](#return-2)
    - [Method get_followings](#method-get_followings)
      - [Arguments](#arguments-4)
      - [Raises](#raises-4)
      - [Return](#return-3)
    - [Method follow_user](#method-follow_user)
      - [Arguments](#arguments-5)
      - [Raises](#raises-5)
    - [Method unfollow_user](#method-unfollow_user)
      - [Arguments](#arguments-6)
    - [Method get_gpg_keys](#method-get_gpg_keys)
      - [Arguments](#arguments-7)
      - [Raises](#raises-6)
      - [Returns](#returns)
    - [Method add_gpg_key](#method-add_gpg_key)
      - [Arguments](#arguments-8)
      - [Raises](#raises-7)
      - [Returns](#returns-1)
    - [Method get_gpg_key](#method-get_gpg_key)
      - [Arguments](#arguments-9)
      - [Raises](#raises-8)
      - [Returns](#returns-2)
    - [Method delete_gpg_key](#method-delete_gpg_key)
      - [Arguments](#arguments-10)
      - [Raises](#raises-9)
    - [Method get_public_keys](#method-get_public_keys)
      - [Arguments](#arguments-11)
      - [Raises](#raises-10)
      - [Returns](#returns-3)
    - [Method add_public_key](#method-add_public_key)
      - [Arguments](#arguments-12)
      - [Raises](#raises-11)
      - [Returns](#returns-4)
    - [Method get_public_key](#method-get_public_key)
      - [Arguments](#arguments-13)
      - [Raises](#raises-12)
      - [Returns](#returns-5)
    - [Method delete_public_key](#method-delete_public_key)
      - [Arguments](#arguments-14)
      - [Raises](#raises-13)
    - [Method get_repos](#method-get_repos)
      - [Raises](#raises-14)
      - [Returns:](#returns-6)
  - [Class GiteaAPIError: Exception](#class-giteaapierror-exception)
  - [Class WrongJSONError: Exception](#class-wrongjsonerror-exception)
  - [Class GiteaUser](#class-giteauser)
    - [Arguments](#arguments-15)
    - [Raises](#raises-15)
  - [Class Visibility](#class-visibility)
    - [Values](#values)
  - [Method random_key](#method-random_key)
    - [Return](#return-4)
  - [Class GPGKeyEmail](#class-gpgkeyemail)
    - [Arguments](#arguments-16)
  - [Class GiteaEmail: GPGKeyEmail](#class-giteaemail-gpgkeyemail)
    - [Arguments](#arguments-17)
  - [Class GiteaGPGKey](#class-giteagpgkey)
    - [Arguments](#arguments-18)
    - [Raises](#raises-16)

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
