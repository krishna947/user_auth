# Project API Documentation

## Overview
This project is a Django-based API that allows user authentication, including login and logout functionalities. It utilizes JWT for token-based authentication and supports token blacklisting for logout functionality.

---

## Table of Contents
1. [Setup](#setup)
2. [API Endpoints](#api-endpoints)
    - [POST /api/user/create/](#post-apipathusercreate)
    - [POST /api/user/login/](#post-apipathuserlogin)
    - [POST /api/user/logout/](#post-apipathuserlogout)
    - [GET /api/user/info/](#get-apipathuserinfo)
3. [Docker Setup](#docker-setup)
4. [Testing](#testing)

---

## Setup

### 1. Clone the Repository
Clone the project repository to your local machine:

```bash
git clone https://github.com/krishna947/user_auth.git
cd user_auth

# Create a virtual environment (optional)
python -m venv myenv
source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`

# Install required dependencies
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
 ```


## API Endpoints
### POST /api/user/create/
This endpoint allows the creation of a new user. The user must provide their first_name, last_name, email, password, and phone number.


```bash
POST /api/user/create/
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "user@example.com",
  "password": "yourpassword",
  "phone": "123-456-7890"
}
```

```bash
Response
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "user@example.com",
  "phone": "123-456-7890"
}
```


### POST /api/user/login/
This endpoint allows the user to log in and receive JWT access and refresh tokens.

```bash
Request
POST /api/user/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

```bash
Response

{
  "access": "your-jwt-access-token",
  "refresh": "your-jwt-refresh-token"
}
```



### GET /api/user/info/
This endpoint returns the user’s information. It requires the user to be authenticated using a valid access token.

```bash
GET /api/user/info/
Authorization: Bearer <your-access-token>

```

```bash
Response

{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "user@example.com",
  "phone": "123-456-7890"
}
```



## Docker Setup
Ensure you have Docker and Docker Compose installed on your machine. Follow these steps to run the project in a Docker container.

### Build the Docker image:
```bash
docker-compose build
```

### Start the containers:
```bash
docker-compose up
```
This will start the Django app, and it will be available at http://localhost:8000.


### Running Migrations in Docker
After running the Docker containers, apply the migrations inside the running container:

```bash
docker-compose exec web python manage.py migrate
```