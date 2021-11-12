# Simple Python SQLite
## Installation
```
pip -r requirements.txt
```

## Configuration
The configuration file located on `config/app.py`. You can change the port or database location in here. As default, the database stored in memory, but if you want to change it into permanent database you can set the `db_path` value into file path. SQLite can support .sqlite, .sqlite3 or .db extension.

## Running application
```
python3 app.py
```

## Endpoints
Default base endpoint: http://127.0.0.1:8080

### Create user
#### POST /create_user
Header
```
Content-Type: application/json
```
Request
```
{
    "username": "account_username"
}
```
Responses
```
400 - Username already exists
201 - Success
{
    "token": "123123"
}
```

### Read balance
#### GET /balance_read
Header
```
Authorization: "Bearer 123123"
```
Responses
```
401 - Unauthorized
200 - Success
{
    "balance": 100000.0
}
```

### Topup balance
#### POST /balance_topup
Header
```
Content-Type: application/json
Authorization: "Bearer 123123"
```
Request
```
{
    "amount": 50000
}
```
Responses
```
401 - Unauthorized
400 - Invalid topup amount
200 - Success
{ 
    "message": "Topup successful" 
}
```

### Transfer balance
#### POST /transfer
Header
```
Content-Type: application/json
Authorization: "Bearer 123123"
```
Request
```
{
    "amount": 50000,
    "to_username": "account_username"
}
```
Responses
```
401 - Unauthorized
400 - Invalid topup amount
    - Destination user not found
    - Insufficient balance
204 - Success
```

### Top transaction per user
#### GET /balance_topup
Header
```
Authorization: "Bearer 123123"
```
Responses
```
401 - Unauthorized
200 - Success
[
    { 
        "username": "account_username",
        "amount": 50000.0 
    }
]
```

### Top debit transaction per user
#### GET /balance_topup
Header
```
Authorization: "Bearer 123123"
```
Responses
```
401 - Unauthorized
200 - Success
[
    { 
        "username": "account_username",
        "transacted_value": 50000.0 
    }
]
```
