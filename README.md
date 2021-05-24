# EVOX

REST API written in FastAPI framework.


## API

### Endpoints list

| HTTP method   | Authentication required   | Path               | Description             | Possible HTTP codes
| ------------- | -------------             | -------------      | -------------           | -------------
| GET           | NO                        | `/messages/{id}`   | Get message by id with counter increment      | 200, 400, 401, 404
| POST          | YES                       | `/messages`        | Create new message      | 200, 400, 401
| PUT           | YES                       | `/messages/{id}`   | Update existing message | 200, 400, 401, 404
| DELETE        | YES                       | `/messages/{id}`   | Delete message          | 200, 400, 401, 404


### REST API Documentation using swagger:
[https://evox-koziel.herokuapp.com/docs](https://evox-koziel.herokuapp.com/docs)



### REST API Documentation using redoc:
[https://evox-koziel.herokuapp.com/redoc](https://evox-koziel.herokuapp.com/redoc)


## Implementation details

### Data format

Request and response bodies are formatted in JSON.

Example of request body:
```json
{
    "content": "New content"
}
```

Example of response body:
```json
{
    "content": "New content",
    "counter": 5,
    "id": 1
}
```


### Authentication
##### Some endpoints are being protected and require providing API Key. 

```
HTTP Header:
Authorization: 8ucof2zKmuG3RNxofGBfKLiuVnBNDXfhNPoAdFqNF40
```
API Key for Heroku server is being set as environmental variable.

### Unit and integration tests

API is being coverd with usage of pytest library. Tests focus on checking if all API endpoints and database connection work properly.

### Deployment
This app is currently deployed on Heroku.

Application is listening on the following URL: [https://evox-koziel.herokuapp.com/messages/](https://evox-koziel.herokuapp.com/messages/)


## API usage examples

Examples for `https://evox-koziel.herokuapp.com`

With API Key as mentioned before `API_KEY=8ucof2zKmuG3RNxofGBfKLiuVnBNDXfhNPoAdFqNF40`

Remember to replace `{ID}` when running commands.

### Create message

```sh
curl -X 'POST' \
  'https://evox-koziel.herokuapp.com/messages/' \
  -H 'accept: application/json' \
  -H 'Authorization: 8ucof2zKmuG3RNxofGBfKLiuVnBNDXfhNPoAdFqNF40' \
  -H 'Content-Type: application/json' \
  -d '{
  "content": "new content"
}'
```

### View message

```sh
curl -X 'GET' \
  'https://evox-koziel.herokuapp.com/messages/{ID}' \
  -H 'accept: application/json'
```

### Update message

```sh
curl -X 'PUT' \
  'https://evox-koziel.herokuapp.com/messages/{ID}' \
  -H 'accept: application/json' \
  -H 'Authorization: 8ucof2zKmuG3RNxofGBfKLiuVnBNDXfhNPoAdFqNF40' \
  -H 'Content-Type: application/json' \
  -d '{
  "content": "modified content"
}'
```

### Delete message

```sh
curl -X 'DELETE' \
  'https://evox-koziel.herokuapp.com/messages/{ID}' \
  -H 'accept: application/json' \
  -H 'Authorization: 8ucof2zKmuG3RNxofGBfKLiuVnBNDXfhNPoAdFqNF40'
```
