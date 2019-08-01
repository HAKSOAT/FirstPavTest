# **QUIZOR API**

The API has the following end points:  
- Register users: /user/register
- Create quiz: /quiz/create
- View quiz: /quiz/\<int:quiz_id>/view
- Solve quiz (requires verification): /quiz/\<int:quiz_id>/solve

Samples:

#### Register users

curl -d '{"username":"haks", "password":"12345"}' -H 'Content-Type: application/json' http://quizor.herokuapp.com/user/register


#### Create quiz

curl -F 'data=@tests/sample.csv' http://quizor.herokuapp.com/quiz/create

#### View quiz

curl -v http://quizor.herokuapp.com/quiz/1/view

#### Solve quiz

curl -u haks:12345 -d '{"answers": ["England", "England", "Spain", "Italy", "Nigeria", "Scotland", "Germany", "Spain", "Netherlands", "France", "Portugal", "Ghana", "Swaziland"]}' -H 'Content-Type: application/json' http://quizor.herokuapp.com/quiz/3/solve

**NB**: To use through code, username and password should be encoded in base64 and sent in as a header:  

credentials = base64.b64encode(b'haks:12345').decode('utf-8')  
headers = {'Authorization': 'Basic ' + credentials}

