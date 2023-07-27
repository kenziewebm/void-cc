# API Routes
## `GET /getAccounts`
Returns a list of accounts in the following format:
```
username password token
username password token
username password token
...
```
This route requires HTTP authentication.

### Request
- Method: GET
- Headers:
  - Authorization: Basic \<base64 encoded username:password> (required for authentication)

### Response
- Status Code: 200 OK
- Content-Type: text/plain
- Body: see above

### Example
Request:
```
GET /getAccounts HTTP/1.1
Host: example.com
Authorization: Basic QWxhZGRpbjpPcGVuU2VzYW1l
```
Response:
```
200 OK
Content-Type: text/plain

user1 pass1 abcdefghijklmnop
user2 pass2 qrstuvwxyz123456
user3 pass3 7890abcdefghij
```


## `GET /addAccount`
Adds an account to the account list

### Request
- Method: GET
- Headers:
  - Authorization: Basic \<base64 encoded username:password> (required for authentication)
- Query parameters:
  - `user`: The username for the new account (required)
  - `pass`: The password for the new account (required)
  - `token`: The token for the new account (required)

### Response
- Status code: 200 OK
- Content-Type: text/plain
- Body: A success message

### Example
Request:
```
GET /addAccount?user=newuser&pass=newpass&token=abcdef HTTP/1.1
Host: example.com
Authorization: Basic QWxhZGRpbjpPcGVuU2VzYW1l
```
Response:
```
200 OK
Content-Type: text/plain

User 'newuser' added successfully!
```

## `GET /getPid`
(internal usage) Returns the PID of the server process.

### Request
- Method: GET

### Response
- Status code: 200 OK
- Content-Type: text/plain
- Body: PID of the server process

### Example
Request:
```
GET /getPid HTTP/1.1
Host: example.com
```
Response:
```
200 OK
Content-Type: text/plain

12345
```
