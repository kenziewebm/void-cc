# API Routes
To convert curl examples to python, use https://curlconverter.com/. Due to a bug in curlconverter, make sure to replace `&` with `\&` in the curl command before pasting.

## `GET /getAccounts`
Returns a list of accounts in the following format:
```
username password cookies
username password cookies
username password cookies
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
$ curl example:hunter2@example.com/getAccounts
> GET /getAccounts HTTP/1.1
> Host: example.com
> Authorization: Basic QWxhZGRpbjpPcGVuU2VzYW1l
```
Response:
```
< 200 OK
< Content-Type: text/plain
< 
< user1 pass1 abcdefghijklmnop
< user2 pass2 qrstuvwxyz123456
< user3 pass3 7890abcdefghij
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
  - `cookies`: The cookies for the new account (required)

### Response
- Status code: 200 OK
- Content-Type: text/plain
- Body: A success message

### Example
Request:
```
$ curl example:hunter2@example.com/addAccount?user=newuser&pass=newpass&cookies=abcdef
> GET /addAccount?user=newuser&pass=newpass&cookies=abcdef HTTP/1.1
> Host: example.com
> Authorization: Basic QWxhZGRpbjpPcGVuU2VzYW1l
```
Response:
```
< 200 OK
< Content-Type: text/plain
< 
< User 'newuser' added successfully!
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
$ curl example.com/getPid
> GET /getPid HTTP/1.1
> Host: example.com
```
Response:
```
< 200 OK
< Content-Type: text/plain
<
< 12345
```

## `GET /getTorrc`
Returns an example torrc, to be used with voidproxy.

### Request
- Method: GET

### Response:
- Status code: 200OK
- Content-Type: text/plain
- Body: example torrc file

### Example
Request:
```
$ curl example.com/getTorrc
> GET /getTorrc HTTP/1.1
> Host: example.com
```
Response:
```
< 200 OK
< Content-Type: text/plain
<
< # Created by voidproxy
< SocksPort 9050
< Log notice file torlog.txt
< DataDirectory tordata
< HiddenServiceDir servicedir
< HiddenServicePort 7273 127.0.0.1:7273
< ORPort 9001
< Nickname PLACEHOLDER-PROXYNAME
< RelayBandwidthRate 5 MB
< RelayBandwidthBurst 10 MB
< ContactInfo PLACEHOLDER-PROXYHOSTER
```
