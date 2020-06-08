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
The roles handeled by this API and their permissions were listed in detail.

 - PUBLIC
	 - Can view list of articles titles

 - SUBSCRIBER
	 - All permissions PUBLIC have
	 - Read all Articles
	 - Read all comments
	 - Delete their own comments

 - AUTHOR
	 - All permissions SUBSCRIBER have
	 - Post new articles
	 - Update new articles
	 - Delete his/her own articles
	 - Delete any comment under his/her own articles

### Error Handling 
Errors are returned as JSON objest in the below format:
```
 {
	'success':  False,
	'error':  500,
	'message':  'Error in API'
  }
```
The API may return following of errors:

-   400: Bad Request
-   401: Not permitted
-   404: Not Found
-   422: Unprocessable Entity
-   500: Error in API

### Resource Endpoint Library
Supported endpoints for Articles
```
GET		'/articles'
GET		'/articles/<article_id>'
POST		'/articles'
PATCH		'/articles'
DELETE		'/articles/<article_id>'
```

Supported endpoints for Article Comments
```
GET		'/articles/<int:article_id>/comments'
POST		'/articles/<int:article_id>/comments'
DELETE		'/articles/<int:article_id>/comments'
```
### Endpoints Ussage

GET	/articles

-   Fetches all the available article titles.
-   Request Arguments: None
-   Returns a JSON object with success value and Articles

Sample Output

```
GET	/articles

{
"Articles: [
     	     {
   	      "id": 5,
 	      "publish_date_time": "Sat, 06 Jun 2020 10:26:24 GMT",
	      "title": "Testing Title"
	     },
	  ],
"success":  true
}
```

GET	/articles/<article_id>

-   Fetches the complete article matching the given id in URL.
-   Request Arguments: None
-   Returns a JSON object with success value and Articles

Sample Output
```
GET	/articles/<article_id>
{
"Articles: [
	     {
		"id": 5,
		"publish_date_time": "Sat, 06 Jun 2020 10:26:24 GMT",
		"title": "Testing Title"			
	     },
	   ],
"success":  true
}
```


POST /articles

-   Posts the new article.
-   Request Arguments: None
-   Returns a JSON object with success value and Articles


Sample Request Body
```
{
	"title": "New Title",
	"content": "It is a long established fact that a reader will be distracted by the readable content of a page when looking at its 		     layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to 		    using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web 			    page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web                       sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on   			    purpose (injected humour and the like)."
}
```

Sample Output
```
POST /articles
{

"Articles": [
		{
		"author": "auth0|5edb85d556d0620013307ae7",
		"content": "It is a long established fact that a reader 						
			will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that 
			it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look 
			like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model 
			text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved 
			over the years, sometimes by accident, sometimes on purpose (injected humour and the like).",
		"id": 94,
		"publish_date_time": "Sun, 07 Jun 2020 19:33:49 GMT",
		"title": "Newg Title"
		 }
	   ],
"success": true
}
```


PATCH /articles

-   Updates the article matching given article id in body.
-   Request Arguments: None
-   Returns a JSON object with success value and Articles


Sample Request Body
```
{
	"id": 14,
	"content": "Updated Content"
}
```

Sample Output
```
PATCH /articles
{
	"Articles": [
			{
			"author": "auth0|5edb85d556d0620013307ae7",
			"content": "Updated Content",
			"id": 15,
			"publish_date_time": "Sun, 07 Jun 2020 05:07:17 GMT",
			"title": "Test Title"
			}
	            ],
	"success": true
}
```

DELETE 	/articles/<article_id>

-   Deletes the article matching given id in URL.
-   Request Arguments: None
-   Returns a JSON object with success value.


Sample Output
```
DELETE /articles/<article_id>
{
	"success": True
}
```

GET	/articles/<article_id>/comments

-   Fetches all the comments of article matching the given id in URL.
-   Request Arguments: None
-   Returns a JSON object with success value and Article, Article_)id, comments

Sample Output
```
GET  /articles/<article_id>/comments
{
	"Article": "Newg Title",
	"Article_id": 11,
	"comments": [
		      {
			"author": "auth0|5edbc55ca36eb2001979b438",
			"content": "This is a checking comment",
			"date_time": "Sun, 07 Jun 2020 19:49:56 GMT",
			"id": 21
         	      }
	  	   ],
	"success": true
}
```

POST	/articles/<article_id>/comments

-   Post new in article matching the given id in URL.
-   Request Arguments: None
-   Returns a JSON object with success value and Article, Article_)id, comments

Sample Request Body
```
{
	"content": "This is a checking comment"
}
```
Sample Output
```
POST  /articles/<article_id>/comments
{
	"Article": "Newg Title",
	"Article_id": 11,
	"comments": [
			{
 			 "author": "auth0|5edbc55ca36eb2001979b438",
 			 "content": "This is a checking comment",
			 "date_time": "Sun, 07 Jun 2020 19:49:56 GMT",
			"id": 21
			}
		  ],
	"success": true
}
```

DELETE /articles/<article_id>/comments

-   Deletes the comment of id provided in body in article matching given id in URL.
-   Request Arguments: None
-   Returns a JSON object with success value.


Sample Request Body
```
DELETE /articles/<article_id>/comments
{
	"id": 7
}
```

Sample Output
```
DELETE /articles/<article_id>/comments
{
	"success": True
}
```


## Local Development & Hosting Instructions

### Development Setup
First,  make sure your machine statisifies below requirements and clone this repo.

**Requirements**
+ Python3
+ pip3
+ virtualenv
+ git
+ postgres


To start and run the local development server,

1.  Initial Setup
```
$ git clone https://github.com/Somanath-KC/FSND-Capstone.git
$ cd FSND-Capstone
$ createdb emagazine_fsnd *** This will be use by the app during development
$ createdb test_emagazine_fsnd *** This will used by API test suite.
```

2. Setting up required environment variables file (file format for env_vars.sh) 
```
export DATABASE_URL=''
export AUTH0_DOMAIN=''
export ALGORITHMS=''
export API_AUDIENCE=''
export AUTH0_LOGIN_URL=''
export TEST_DATABASE_URL=''
export AUTHOR1_JWT=''
export SUBSCRIBER_JWT=''
```

3.  Initialize and activate a virtualenv:

```
$ python3 -m virtualenv ./venv
$ source venv/bin/activate

```

4.  Install the dependencies and exporting env variables:

```
$ pip install -r requirements.txt
$ source ./env_vars.sh # Contains DB-URI,TOKENS, etc

```

5.  Run the development server:

```
$ export FLASK_APP=src
$ export FLASK_ENV=development # enables debug mode
$ flask run

```

6.  Accessing Application
+ Navigate to Home page  [http://localhost:5000](http://localhost:5000/)
+ Accessing API Base URL [http://localhost:5000/api](http://localhost:5000/api) 


### Running API Locally
To easily run the app locally

 1. Make sure below env variables were present in evn_docker file and docker installed on your machine.
 ```
 DATABASE_URL=VAL
 PORT=5000
 AUTH0_DOMAIN=VAL
 ALGORITHMS=VAL
 API_AUDIENCE=VAL
 AUTH0_LOGIN_URL=VAL
 ```
 2. Running the app
 ```
 docker pull somanathkc/fsnd_capstone
 docker run --env-file env_docker -p 5000:5000 somanathkc/fsnd_capstone
 ```

### Heroku Deployment
Usually Heroku supports deployment usnig git and container registry. For this project we'll be using container registry method for smoother deployments.

Before starting up setup the below env variables in your heroku app through dashboard or cli
```
 AUTH0_DOMAIN=VAL
 ALGORITHMS=VAL
 API_AUDIENCE=VAL
 AUTH0_LOGIN_URL=VAL
```
**Note: PORT and DATABASE_URL env variable were taken care by heroku.**

You must have Docker set up locally to continue. You should see output when you run this command.
```
$ docker ps
```
Deployment Instructions
 1. Download and install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-command-line).
 2.  Login in to heroku cli
	 ```
	 $ heroku login
	 ```
3. Log in to Container Registry
	```
	$ heroku container:login
	```
4.  Push your Docker-based app
	
	Build the Dockerfile in the current directory and push the Docker image.
	```
	$ heroku container:push web
	```

5. Deploy the changes
	
	Release the newly pushed images to deploy your app.
	```
	$ heroku container:release web
	$ heroku ps:scale web=1
	```
6. Hurray! Now you can now access your app using heroku application URL.


## Testing

### Python Unittest Module
### Postman Application


## Acknowledgements
_github.com/amyhua, _github.com/grutt, _github.com/cmccarthy15, _github.com/kbehrman
