from app import db, app
from app.models import User, Prediction
from werkzeug.security import generate_password_hash

app.app_context().push()
db.create_all()


if not User.query.filter(User.email == 'admin@example.com').first():
    admin = User(
        email='admin@example.com',
        password=generate_password_hash('1234'),
        first_name='Rudy',
        last_name='Bourez'
    )
    db.session.add(admin)
    db.session.commit()

if not User.query.filter(User.email == 'user@example.com').first():       
    user = User(
        email="user@example.com",
        password=generate_password_hash('123456'),
        first_name="User",
        last_name="User"
    )
    db.session.add(user)
    db.session.commit()
        
prediction = Prediction(
    id_user=1,
    neighborhood="Crawford",
    garage_area=30,
    garage_cars=2,
    age_house=20,
    fst_flr_sf=50,
    total_bsmt_sf=50,
    gr_liv_area=120,
    overall_qual=5,
    bath=2,
    bsmt_qual="Good",
    kitchen_qual="Excellent",
    estimated_price=69011
    )

db.session.add(prediction)
db.session.commit()