## Login and signup
### Client requests
1. Login
```
data = {
    "action": "login",
    "username": "username",
    "password" : "password"
}
```
2. Sign up
```
data = {
    "action": "sign_up",
    "username": "username",
    "password" : "password"
}
```
### Server responses

1. Login
```
data = {
    "server": "response",
    "authorized": "yes/no",
    "error" : "InvalidJSONFormat"           #optionnal
              "InternalError"
              "BadPasswordOrUsername"
}
```
2. Sign up
```
data = {
    "server": "response",
    "authorized": "yes/no",
    "error" : "InvalidJSONFormat"           #optionnal
              "InternalError"
              "AccountAlreadyExist"
              "BadPassword"
              "BadUsername"
}
```
## Tasks operations
### Client requests
1. Create task
```
data = {
    "client": "create_task",
    "content": {
        "name": "name",
        "state": "1/2/3",
        "priority": "1/2/3",
        "date": "2023-10-20 00:00:00",
        "description": "description",
        "labels_id": [],                    #optionnal
        "users_id": []                      #optionnal
    }
}
```
2. Get tasks
```
data = {
    "client": "get_tasks"
}
```
### Server responses
1. Create task
```
data = {
    "server": "response",
    "authorized": "yes/no",
    "error": "InvalidJSONFormat"            #optionnal
             "TaskNameAlreadyExist"
             "InternalError"
             "ValueError"
             "NotAuthorized"
}
```
2. Get tasks
```
data = {
    "server": "response_with_content"
    "error": "InternalError"                #optionnal
             "NotAuthorized"
    "content":[
        {
            "id": "id",
            "name": "name",
            "state": "1/2/3",
            "priority": "1/2/3",
            "date": "date",
            "description": "description",
        }
    ]
}
```
