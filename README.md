# FSND-Capstone | E-Magazine API
Capstone Project for Udacity's Full Stack Web Developer Nanodegree

## Overview

E-Magazine, an application that enables people to share and acquire knowledge. This Magazine publishes various articles every day for its subscribers. E-Magazine also allows it's subscribers to share their views, opinions on the articles through comments. The E-Magazine API plays a crucial role in backing this application. This RESTful API  helps the application to create, update, read, and delete Articles and Comments in the database. This API also uses Role-Based Access Control for its users to avoid unauthorized actions. 
Roles handled by the API include:

* Public  (Anyone without authorization, Usually general visitor)
* Subscribers (Refers to the members who've subscribed to E-Magazine)
* Authors (Refers to the members who publishes articles in E-Magazine)

Detailed information is available in the API Reference section of this page.

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
  ├── app.py *** the main driver of the app. Includes your SQLAlchemy models.
                    "python app.py" to run after installing dependences
  ├── config.py *** Database URLs, CSRF generation, etc
  ├── error.log
  ├── forms.py *** Your forms
  ├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
  ├── static
  │   ├── css 
  │   ├── font
  │   ├── ico
  │   ├── img
  │   └── js
  └── templates
      ├── errors
      ├── forms
      ├── layouts
      └── pages
  ```



## Setting up Authentication & Accessing live API

### Generating Tokens
### Tokens for project review


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
