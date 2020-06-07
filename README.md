# FSND-Capstone | E-Magazine API
Capstone Project for Udacity's Full Stack Web Developer Nanodegree

## Overview

### Introduction
E-Magazine, an application that enables people to share and acquire knowledge. This Magazine publishes various articles every day for its subscribers. E-Magazine also allows it's subscribers to share their views, opinions on the articles through comments. The E-Magazine API plays a crucial role in backing this application. This RESTful API  helps the application to create, update, read, and delete Articles and Comments in the database. This API also uses Role-Based Access Control for its users to avoid unauthorized actions. 
Roles handled by the API include:

* Public  (Anyone without authorization, Usually general visitor)
* Subscribers (Refers to the members who've subscribed to E-Magazine)
* Authors (Refers to the members who publishes articles in E-Magazine)

Detailed information is available in the [API Reference](https://github.com/Somanath-KC/FSND-Capstone/blob/master/README.md#api-refrence) section of this page.

### Tech Stack

* **SQLAlchemy ORM** to be our ORM library of choice
* **PostgreSQL** as our database of choice
* **Python3** and **Flask** as our server language and server framework
* **Auth0** as our auth service 
* **Docker** for easy deployments
* **Heroku** as our hosting platform
### Project Structure

  ```sh
  ├── README.md
  ├── test_api.py *** E-Magazine API test using python unittest module
  ├── config.py *** Database URLs, etc
  ├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
  ├── Dockerfile *** Used to build docker images
  ├── .gitignore 
  ├── .dockerignore *** ignores secrets, unwanted file in build process.
  └── src	
      ├── api
	  │   ├── __init__.py
	  │   ├── controller.py *** The main driver of API which includes all endpoints.
	  │   └── error.py API *** sepecific errors were handled by this script.
      ├── auth
      │   ├── __init__.py
      │   └── handler.py *** Reponsible for verifing authorization and authentication of requests
      ├── errors
      │   ├── __init__.py
      │   └── handler.py *** Application level errros were handled here.
      ├── models
      │   └── __init__.py ** Database models required for application were here.
      └── __init__.py *** Acts as application factory for gunicorn server
  ```



## Setting up Authentication & Accessing live API


### Generating Tokens

The front-end usually handles the token from the url fragment and stores it in the client-side on successful login, which will be used to authenticate API calls . 
**For our API testing purpose, we need to manually grab the token from url fragment.**
+   Use login URL to authenticate
+  Grab the token from url after successful authentication

[Click here](https://somanath-kc.auth0.com/authorize?audience=Emagazine&response_type=token&client_id=Dzo92uMPMyL7Ph3WeXz2F3v6bgOiSCu0&redirect_uri=https://e-magazine-fsnd-capstone.herokuapp.com/auth/) to redirect to external auth service (AUTH0) 

### Tokens for project review

Subscriber Role Token
```
yJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlRzT1dpbWQxTENEWDFiamlPekQtZSJ9.eyJpc3MiOiJodHRwczovL3NvbWFuYXRoLWtjLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWRiYzU1Y2EzNmViMjAwMTk3OWI0MzgiLCJhdWQiOiJFbWFnYXppbmUiLCJpYXQiOjE1OTE1NTQyOTAsImV4cCI6MTU5MTY0MDY5MCwiYXpwIjoiRHpvOTJ1TVBNeUw3UGgzV2VYejJGM3Y2YmdPaVNDdTAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpjb21tZW50IiwicG9zdDpjb21tZW50IiwicmVhZDphcnRpY2xlIiwicmVhZDpjb21tZW50Il19.Q4t-ukBMfynKdBNQjOtFyQ-IpvGN4uX74D4ZCCLt8gAIZ1qST40hOQ5ReJAoR5iM-SIVs408oZfpdJSsqaSVTnN6o4P-vd7GOnKq9dujsA1gdmE33x84pkkazI7UYbGfMxUBm6NZ0Dm_C8JL5pinIoRboetfWvTkyXHQKO0pdMozZ26rRQ09htJVNCinZ6wBTeDtVULEINtb3UO5xK3qYE5Pjnvytuth54i6F8Zp-y-7xyb5-kOecBmiqNXKSTnBhCS09MGARDZU8Bip2GR2NeUB3kXsZndvImPyqAME98IAQlzGsGRXGaKI08-_cLUalZZAXp3PNf3c1KJwpMYUOg&expires_in=86400
```

Author Role Token
```
yJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlRzT1dpbWQxTENEWDFiamlPekQtZSJ9.eyJpc3MiOiJodHRwczovL3NvbWFuYXRoLWtjLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWRiYzU1Y2EzNmViMjAwMTk3OWI0MzgiLCJhdWQiOiJFbWFnYXppbmUiLCJpYXQiOjE1OTE1NTQyOTAsImV4cCI6MTU5MTY0MDY5MCwiYXpwIjoiRHpvOTJ1TVBNeUw3UGgzV2VYejJGM3Y2YmdPaVNDdTAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpjb21tZW50IiwicG9zdDpjb21tZW50IiwicmVhZDphcnRpY2xlIiwicmVhZDpjb21tZW50Il19.Q4t-ukBMfynKdBNQjOtFyQ-IpvGN4uX74D4ZCCLt8gAIZ1qST40hOQ5ReJAoR5iM-SIVs408oZfpdJSsqaSVTnN6o4P-vd7GOnKq9dujsA1gdmE33x84pkkazI7UYbGfMxUBm6NZ0Dm_C8JL5pinIoRboetfWvTkyXHQKO0pdMozZ26rRQ09htJVNCinZ6wBTeDtVULEINtb3UO5xK3qYE5Pjnvytuth54i6F8Zp-y-7xyb5-kOecBmiqNXKSTnBhCS09MGARDZU8Bip2GR2NeUB3kXsZndvImPyqAME98IAQlzGsGRXGaKI08-_cLUalZZAXp3PNf3c1KJwpMYUOg&expires_in=86400
```

### Accessing Live Application
Application URL
```
https://e-magazine-fsnd-capstone.herokuapp.com/
```

API Base URL
```
https://e-magazine-fsnd-capstone.herokuapp.com/api
```



## API Refrence

### Role Based Access Control (RBAC)

### Error Handling 

### Resource Endpoint Library



## Local Development & Hosting Instructions

### Development Setup

### Running API Locally

### Heroku Deployment



## Testing

### Python Unittest Module
### Postman Application


## Acknowledgements
_github.com/amyhua, _github.com/grutt, _github.com/cmccarthy15, _github.com/kbehrman
