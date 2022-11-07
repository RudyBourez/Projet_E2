from flask import Blueprint, render_template, request
import pandas as pd
from flask_login import login_required, current_user
from app import model

main =  Blueprint("main", __name__)

@main.route('/')
def index():
    return render_template("index.html")

@main.route('/predict')
@login_required
def predict():
    return render_template("predict.html")

@main.route('/predict', methods=["POST"])
@login_required
def predict_post():
    X_predict = {}
    for var in ['Year_Built', 'Total_Bsmt_SF', '1st_Flr_SF', 'Gr_Liv_Area','Garage_Area', 'Overall_Qual', 'Full_Bath', 'Exter_Qual',
              'Kitchen_Qual', 'Neighborhood']:
        if var in ['Exter_Qual','Kitchen_Qual', 'Neighborhood']:
            X_predict[var]= request.form[var]
        else:
            X_predict[var]= int(request.form[var])

    pred = model.predict(pd.DataFrame(X_predict, index=[0]))
    return render_template('predict.html', data=int(pred))