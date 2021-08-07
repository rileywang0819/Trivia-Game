# Trivia API Doc

## Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
- Authentication: No authentication or API keys.

## Error Handling

Errors are returned as JSON objects in the following format:

```bash
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```

This API will return four error types when request fails,

- 400: Bad Request
- 404: Resource Not Found
- 405: Not Allowed Method
- 422: UnProcessable

## Endpoint Library

### GET: /categories

- General:
  - Fetches a dictionary of categories, in which the keys are ids and the value is the corresponding string of the category.
  - Request Arguments: None
- Sample: curl http://127.0.0.1:5000/categories

```js
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

### GET: /questions

- General:
  - Fetches a paginated set of questions, total number of all questions, all categories and current category string. 
  - Request Argument: page - integer
- Sample: curl http://127.0.0.1:5000/questions?page=1

```js
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": "5",
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": "5",
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    ...
    ...
    ...
    {
      "answer": "The Palace of Versailles",
      "category": "3",
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 20
}
```

### GET: /categories/{category_id}/questions

- General:
  - Fetches questions for a cateogry specified by category_id request argument.
  - Request Argument: category_id - integer
- Sample: curl http://127.0.0.1:5000/categories/1/questions

```js
{
  "current_category": "Science",
  "questions": [
    {
      "answer": "The Liver",
      "category": "1",
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    ...
    ...
    {
      "answer": "Answer",
      "category": "1",
      "difficulty": 1,
      "id": 24,
      "question": "Question"
    }
  ],
  "success": true,
  "total_questions": 4
}
```

### DELETE /questions/{question_id}

- General:
  - Deletes a specified question using the id of the question
  - Request Arguments: question_id - integer 
- Sample: curl -X DELETE http://127.0.0.1:5000/questions/12

```js
{
  "success": true
}
```

### POST /quizzes

- General:
  - Sends a post request in order to get the next question 
  - Request Body: {`previous_questions`:  an array of question id's such as [1, 4, 20, 15],
`quiz_category`: a string of the current category such as {'id': 4}}
- Sample: curl -X POST -H "Content-Type: application/json" -d '{"previous_questions": [5, 9, 12], "quiz_category": {"id": "4"}}' http://127.0.0.1:5000/quizzes

```js
{
  "question": {
    "answer": "Scarab",
    "category": "4",
    "difficulty": 4,
    "id": 23,
    "question": "Which dung beetle was worshipped by the ancient Egyptians?"
  },
  "success": true
}
```

### POST /questions

- General:
  - Sends a post request in order to add a new question.
  - Request Body:
```js
{
    'question':  'Heres a new question string',
    'answer':  'Heres a new answer string',
    'difficulty': 1,
    'category': 3,
}
```
- Sample: curl -X POST -H "Content-Type: application/json" -d '{"question": "Heres a new question string", "answer": "Heres a new answer string", "difficulty": "1", "category": 3}' http://127.0.0.1:5000/questions

```js
{
  "success": true
}
```

### POST /questions

- General:
  - Sends a post request in order to search for a specific question by search term 
  - Request Body: 
```js
{
    'searchTerm': 'this is the term the user is looking for'
}
```
- Sample: curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "world"}' http://127.0.0.1:5000/questions

```js
{
  "currentCategory": null,
  "questions": [
    {
      "answer": "Brazil",
      "category": "6",
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": "6",
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ],
  "success": true,
  "totalQuestions": 2
}
```

