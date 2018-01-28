# django-rest-experemental
first try with django-rest-framework

base authentication:

`curl -X POST http://url/api-token-auth/ -d '{"username": "test", "password":"testrest"}'`

words:

`curl -X GET http://url/api/words/ -H 'authorization: Token $TOKEN'`
parameters:
    [page]

add word:

`curl -X POST http://example.com/api/words -H 'authorization: Token $TOKEN' 
  -H 'content-type: application/json' \
  -d '{"key_word": "Python"}'`
  
del word: 

`curl -X DELETE http://example.com/api/words/{id} -H 'authorization: Token $TOKEN'` 


vacancies:

`curl -X GET http://127.0.0.1:5000/api/words/{id}/vacancies/ -H 'authorization: Token $TOKEN'`

parameters: 
    [date__gte, date__lte, page] 