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
    - [Method remove_gpg_key](#method-remove_gpg_key)
  - [Class GiteaAPIError: Exception](#class-giteaapierror-exception)
  - [Class WrongJSONError: Exception](#class-wrongjsonerror-exception)
  - [Class GiteaUser](#class-giteauser)
    - [Static method string_to_visibility](#static-method-string_to_visibility)
  - [Class Visibility](#class-visibility)
  - [Method random_key](#method-random_key)
  - [Class GPGKeyEmail](#class-gpgkeyemail)
  - [Class GiteaEmail: GPGKeyEmail](#class-giteaemail-gpgkeyemail)
  - [Class GiteaGPGKey](#class-giteagpgkey)

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

#### Raises

    GiteaAPIError: When gitea api status code does not 200(success).

#### Return

    list[GiteaUser] or None: Followers of token owner if has followers. else, return None.

### Method get_followings

Get followings of token owner.

#### Raises

    GiteaAPIError: When gitea api status code does not 200(success).

#### Return

    list[GiteaEmail] or None: Followings of token owner if has following users. else, return None.

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

### Method remove_gpg_key

Delete gpg key of token owner.

#### Arguments

    id (int): ID of gpg key that will be delete.

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

### Static method string_to_visibility

Check visibility property.

#### Arguments

    string (str): String that will be checked.

#### Return

    Visibility or None: if visibility is vaild, return visibility class. else, return None

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
