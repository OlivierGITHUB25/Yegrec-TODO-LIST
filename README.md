## Functions (what the user can do)

Login & Sign up
- Login
- Sign up

Task Operations
- Create task
- Get tasks
- Update task
- Remove task

SubTask Operations
- Create subtask
- Get subtasks
- Update subtask
- Remove subtask

Label Operations
- Create label
- Get labels
- Remove label

Users
- Get users

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
    "success": "yes/no",
    "error" : "InvalidJSONFormat"
              "InternalError"
              "BadPasswordOrUsername"
}
```
2. Sign up
```
data = {
    "server": "response",
    "success": "yes/no",
    "error" : "InvalidJSONFormat"
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
    "name": "name",
    "state": "1/2/3",
    "priority": "1/2/3",
    "date": "2023-10-20 00:00:00",
    "description": "description",
    "labels_id": [],                    #optionnal
    "users_id": []                      #optionnal
}
```
2. Get tasks
```
data = {
    "client": "get_tasks"
}
```
3. Update task
```
data = {
    "client": "update_task",
    "task_id": "id",
    "name": "name",
    "state": "1/2/3",
    "priority": "1/2/3",
    "date": "2023-10-20 00:00:00",
    "description": "description",
    "labels_id": [],                    #optionnal
    "users_id": []                      #optionnal
}
```
4. Remove task
```
data = {
    "client": "remove_task",
    "task_id": "id"
}
```
### Server responses
1. Create task
```
data = {
    "server": "response",
    "success": "yes/no",
    "error": "InvalidJSONFormat"
             "TaskNameAlreadyExist"
             "InternalError"
             "ValueError"
             "NotAuthorized"
}
```
2. Get tasks
```
data = {
    "server": "response_with_content",
    "success": "yes/no",
    "error": "InternalError"
             "NotAuthorized"
    "content":[
        {
            "task_id": "id",
            "name": "name",
            "state": "1/2/3",
            "priority": "1/2/3",
            "date": "date",
            "description": "description",
            "labels_id": [],
            "users_id": []
        }
    ]
}
```
3. Update task
```
data = {
    "server": "response",
    "success": "yes/no",
    "error": "InvalidJSONFormat"
             "TaskNameAlreadyExist"
             "InternalError"
             "ValueError"
             "NotAuthorized"
}
```
4. Remove task
```
data = {
    "server": "response",
    "success": "yes/no",
    "error": "InvalidJSONFormat"
             "InternalError"
             "ValueError"
             "NotAuthorized"
}
```
## SubTasks operations
### Client requests
1. Create subtask
```
data = {
    "client": "create_subtask",
    "name": "name",
    "state": "1/2/3",
    "date": "2023-10-20 00:00:00",
    "labels_id": []                         #optionnal
}
```
2. Get subtasks
```
data = {
    "client": "get_subtasks"
    "task_id": "id"
}
```
3. Update subtask
```
data = {
    "client": "update_subtask",
    "subtask_id": "id",
    "name": "name",
    "state": "1/2/3",
    "date": "2023-10-20 00:00:00",
    "labels_id": []                         #optionnal
}
```
4. Remove subtask
```
data = {
    "client": "remove_subtask",
    "subtask_id": "id"
}
```
### Server responses
1. Create subtask
```
data = {
    "server": "response",
    "success": "yes/no",
    "error": "InvalidJSONFormat"
             "SubTaskNameAlreadyExist"
             "InternalError"
             "ValueError"
             "NotAuthorized"
}
```
2. Get tasks
```
data = {
    "server": "response_with_content",
    "success": "yes/no",
    "error": "InternalError"
             "NotAuthorized"
    "content":[
        {
            "task_id": "id",
            "name": "name",
            "state": "1/2/3",
            "date": "date",
            "labels_id": []
        }
    ]
}
```
3. Update task
```
data = {
    "server": "response",
    "success": "yes/no",
    "error": "InvalidJSONFormat"
             "SubTaskNameAlreadyExist"
             "InternalError"
             "ValueError"
             "NotAuthorized"
}
```
4. Remove task
```
data = {
    "server": "response",
    "success": "yes/no",
    "error": "InvalidJSONFormat"
             "InternalError"
             "ValueError"
             "NotAuthorized"
}
```

## Users
### Client requests
1. Get users
```
data = {
    "client": "get_users"
}
```
### Server responses
1. Get users
```
data = {
    "server": "response_with_content",
    "success": "yes/no",
    "error": "InternalError"
             "NotAuthorized"
    "content":[
        {
            "user_id": "id",
            "username": "username"
        }
    ]
}
```
