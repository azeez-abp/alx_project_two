# Introduction 

# ALX PROJECT (Building Farm Inventory Application)

[Author LinkedIn Profile](https://www.linkedin.com/in/adio-azeez-adeyori-a70430148/) <br>

## Code quality tools 
- black -> code formater
- flake8 -> style checker
- mypy -> type checker
- isort -> order import tool

Must include link to your deployed site, final project blog article, author(s) LinkedIn
# Installation
- This  is a web based application the frontend and backend is deployed on different server

## To run the application locally, clone the repo
### Frontend
- Ensure you have install node v20.11 or more. this version run on node v20.11.0
- cd to frontend and 
```
npm install
npm run dev
```
### Backend
- cd backend
- Install  python 3.12.0 
- install mysql database
- Fill the value of .env-example and remane to .env
- run ./deploy.sh

# Usage
- to use the application, you have to register as a user  and login to see the what the dashbaord look like
# Contributing
- to contribute to the application, fork the project and create your branch. this is not trunk based push
- once your code meet the requiremnet, your request will be merged
- You mush have all the code quality tools menstion above

# Related projects
-  No related project yet
#  Licensing
- The project is licensed under MIT


# Cookie issue

```
Most times when you are workin with an application with both frontend and backend setting cookie may not 
appear in the browse

if you are using axio use  ``` axios.defaults.withCredentials = true ```

if you are using fetch 

fetch('http://localhost:5000/login', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    credentials: 'include', // This is crucial for sending cookies with requests
    body: JSON.stringify({ email: 'user@example.com', password: 'password' })
})

for tour backensd 
 response.set_cookie(
            "farm",
            str(uuid.uuid4()),
            expires=expires,
            secure=False,  # Set to True if using HTTPS
            httponly=True,
            samesite='Lax'
        )

```
