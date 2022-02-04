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

    ValueError: When dictionary is wrong. 
    GiteaAPIError: When gitea api status code does not 201(success).

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
