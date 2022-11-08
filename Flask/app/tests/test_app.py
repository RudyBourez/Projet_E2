import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client   


# -----------------------------------V1---------------------------------------------
def test_index(client):
    response = client.get('/')
    assert b'<h1> Welcome </h1>' in response.data
    assert response.status_code == 200
    
def test_predict_logged_in(client):
    email = 'user@example.com'
    password = '123456'
    client.post('/login', data={'email' : email, 'password' : password})
    response = client.get('/predict')
    assert response.status_code == 200
    
def test_prediction(client):
    email = 'user@example.com'
    password = '123456'
    client.post('/login', data={'email' : email, 'password' : password})
    response = client.post('/predict', data={'Age_house':20, 'Total Bsmt SF':50, '1st Flr SF':50,
                                             'Gr Liv Area':120,'Garage Area':30, 'Garage Cars':2,
                                             'Overall_Qual':5, 'Bath':2, 'Bsmt Qual':"Good",
                                             'Kitchen Qual': "Excellent", 'Neighborhood': "Crawford"})
    assert b'<p> La maison vaut: 69011</p>' in response.data
 
# -----------------------------------V2---------------------------------------------

def test_signup(client):
    response = client.get('/signup')
    assert b'<form method="POST" action="/signup" class="form">' in response.data
    assert response.status_code == 200

def test_predict_without_login(client):
	response = client.get('/predict')
	assert response.status_code == 302

def test_login(client):
    response = client.get('/login')
    assert b'<form method="POST" action="/login" class="form">' in response.data
    assert response.status_code == 200
 
def test_with_login(client):
    good_email = 'user@example.com'
    good_password = '123456'
    client.post('/login', data={'email' : good_email, 'password' : good_password})
    response = client.get('/predict')
    assert response.status_code == 200
    
def test_with_login_bad(client):
    bad_email = 'user1@example.com'
    good_password = '123456'
    client.post('/login', data={'email' : bad_email, 'password' : good_password})
    response = client.get('/predict')
    assert response.status_code == 302
    
def test_logout_logged_in(client):
    email = 'user@example.com'
    password = '123456'
    client.post('/login', data={'email' : email, 'password' : password})
    with client.get('/logout') as response:
        assert response.status_code == 302
        #assert len(response.history) == 1
        #assert response.request.path == "/"

def test_logout_logged_out(client):
    response = client.get('/logout')
    assert response.status_code == 302
    
def test_predict_not_logged_in(client):
    response = client.get('/predict')
    assert response.status_code == 302