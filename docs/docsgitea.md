# Documentation for Gitea

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

## Class GiteaAPIError: Exception

raised when api does not success.

## Class WrongJSONError: Exception

raised when JSON does not have right key.

## Class GiteaUser

Class for find gitea user properties easily.

### Arguments

    response (Response): The /user response.

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

## Class GiteaEmail

Gitea email properties.

### Arguments

    email (str): Email address.
    primary (bool): Is primary email.
    verified (bool): Is verified email.
