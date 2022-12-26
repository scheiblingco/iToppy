# iTop Library for Python
iTop CMDB/Service Management Rest API library for Python

## Todo
- base (__init__.yml)
- models.py


# Usage
## Authentication
Authentication can be performed two ways:

### Form
This method works only when iTop doesn't have the form login disabled (e.g. direct auth when using the itop-saml extension).

### Basic
This method can be used if you have the SAML plugin and want users to be automatically forwarded to the IDP when loading the page, but still want to be able to use the API. Make sure that basic is the first authentication method in the list in the configuration file, e.g.
```php
	'allowed_login_types' => 'basic|saml|external',
```
### Examples
```python
from iToppy import iTop, iTopAuth

# Form Authentication (default)
connection = iTop(
    url='https://itop.example.com/webservices/rest.php', 
    username='username', 
    password='password', 
    version='1.3',
    auth=iTopAuth.FORM
)

# Basic Authentication
connection = iTop(
    url='https://itop.example.com/webservices/rest.php', 
    username='username', 
    password='password', 
    version='1.3',
    auth=iTopAuth.BASIC
)
```

## Querying
### Get objects
```python
# Get all objects of class UserRequest
user_requests = connection.get('UserRequest')

# Full Get syntax
connection.get(
    
    # The class of object/objects to receive
    itop_class="UserRequest",
    
    # A string representing the key, OQL query in string form or iTopOQLQuery object
    key="1",
    
    # The fields to retrieve
    fields=["title", "description"]
    
    # Limit the number of results per page
    ,limit=10,

    # The page to retrieve
    page=1
)
```