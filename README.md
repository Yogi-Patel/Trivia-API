# API Development and Documentation Final Project

## Trivia App
The objective of this project is to create an API for a Trivia application.  
The project is made using Python, Flask, SQLAlchemy and unittest (for testing).

## Prerequisites
For the project, you need to have Python (backend) and Node.js (frontend) installed.

## Getting Started
### Cloning the repository
You can clone the repository using the following command in git:
`git clone https://github.com/Yogi-Patel/Trivia-API.git`

### Creating the environment
Create a virtual environment using the following command: 
`python -m venv env`
You need to have **virtualenv** library installed

Activate the virtual environment using the following command:
`env\Scripts\activate`

### Installing the necessary modules
After activating the environment, navigate to the backend folder and run the following command:
`pip install -r requirements.txt`

## Running the project 
#### Running the backend server:
Navigate to the backend folder and run:
`flask run --reload`

#### Running the frontend:
Navigate to the frontend folder and run:
`npm install` (run only once)
then 
`npm start`

#### Running the test:
Run the following code to run the test: 
`python test_flaskr.py`
in the backend folder

## API Reference
`GET '/categories'`

- Request Arguments: None
- Response body:
```json
{
  "success": True,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

---

`GET '/questions?page=${integer}'`

- Request Arguments: `page` - integer
- Response body:

```json
{
  "success": True,
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 2
    }
  ],
  "total_questions": 19,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": " "
}
```

---

`GET '/categories/${id}/questions'`

- Request Arguments: `id` - integer
- Response body:

```json
{
  "success": True,
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 4
    }
  ],
  "total_questions": 19,
  "current_category": " "
}
```

---

`DELETE '/questions/${id}'`

- Request Arguments: `id` - integer
- Response body: 
```json
{
  "success": True
}
```

---

`POST '/quizzes'`

- Request Body:

```json
{
    'previous_questions': [1, 4, 20, 15],
    quiz_category': 'int_current_category'
 }
```

- Returns: a single new question object

```json
{
  "success": True,
  "question": {
    "id": 19,
    "question": "This is a question",
    "answer": "This is an answer",
    "difficulty": 5,
    "category": 4
  }
}
```

---

`POST '/questions'`
- Request Body:

```json
{
  "question": "Heres a new question string",
  "answer": "Heres a new answer string",
  "difficulty": 1,
  "category": 3
}
```

- Returns: 
```json
{
    "success": True
}
```
---

`POST '/questions'`

- Request Body:

```json
{
  "searchTerm": "this is the term the user is looking for"
}
```

- Returns: 
any array of questions, a number of totalQuestions that met the search term and the current category string

```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 5
    }
  ],
  "totalQuestions": 19,
  "currentCategory": " "
}
```

