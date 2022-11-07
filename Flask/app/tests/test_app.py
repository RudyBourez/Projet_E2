import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client   

def test_index(client):
    response = client.get('/')
    assert b'<h1> Welcome </h1>' in response.data
    assert response.status_code == 200
 
def test_signup(client):
    response = client.get('/signup')
    assert b'<form method="POST" action="/signup">' in response.data
    assert response.status_code == 200

def test_profile_without_login(client):
	response = client.get('/predict')
	assert response.status_code == 302

def test_login(client):
    response = client.get('/login')
    assert b'<form method="POST" action="/login">' in response.data
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
    response = client.post('/predict', data={'Year_Built':2000, 'Total_Bsmt_SF':50, '1st_Flr_SF':50,
                                             'Gr_Liv_Area':50,'Garage_Area':20, 'Overall_Qual':5,
                                             'Full_Bath':2, 'Exter_Qual':"TA",'Kitchen_Qual': "TA",
                                             'Neighborhood': "NWAmes"})
    assert b'<p> La maison vaut: 46534</p>' in response.data