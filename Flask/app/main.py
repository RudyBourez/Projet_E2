from flask import Blueprint, render_template, request
import pandas as pd
from flask_login import login_required, current_user
from app import model, cat_neighborhood, db
from app.models import Prediction

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
    # Génére les données pour les insérer dans le modèle de prédiction
    dict_qual = {"Excellent": "Ex", "Good": "Gd", "Average": "TA", "Fair": "Fa", "Poor": "Fa"}
    dict_neighborhood = {"Bloomington Heights": "Blmngtn", "Bluestem": "Blueste", "Briardale": "BrDale", "Brookside": "BrkSide",
                         "Clear Creek": "ClearCr", "College Creek": "CollgCr", "Crawford": "Crawfor", "Edwards": "Edwards",
                         "Gilbert": "Gilbert", "Iowa DOT and Rail Road": "IDOTRR", "Meadow Village": "MeadowV", "Mitchell": "Mitchel",
                         "North Ames": "Names", "Northridge": "NoRidge", "Northpark Villa": "NPkVill", "Northridge Heights": "NridgHt",
                         "Northwest Ames": "NWAmes", "Old Town": "OldTown", "South & West of Iowa State University": "SWISU",
                         "Sawyer": "Sawyer", "Sawyer West": "SawyerW", "Somerset": "Somerst", "Stone Brook": "StoneBr",
                         "Timberland": "Timber", "Veenker": "Veenker"}
    X_predict = {}
    for var in ['Age_house', 'Total Bsmt SF', '1st Flr SF', 'Gr Liv Area','SF_Cars', 'Overall Qual', 'Bath', 'Bsmt Qual',
              'Kitchen Qual', 'Cat_neighborhood']:
        if var in ['Bsmt Qual','Kitchen Qual']:
            X_predict[var] = dict_qual[request.form[var]]
        elif var=="SF_Cars":
            if request.form["Garage Cars"]==0:
                 X_predict[var] = 0
            else:
                X_predict[var] = int(request.form["Garage Area"])/int(request.form["Garage Cars"])
        elif var=="Cat_neighborhood":
            X_predict[var] = int(cat_neighborhood[dict_neighborhood[request.form["Neighborhood"]]])
        else:
            if var=="Overall Qual":
                X_predict[var]=int(request.form["Overall_Qual"])
            else:
                X_predict[var]=int(request.form[var])

    pred = model.predict(pd.DataFrame(X_predict, index=[0]))
    
    # Génére les données pour les introduire dans la Table Prediction
    pred_dict = {}
    pred_dict["neighborhood"] = request.form["Neighborhood"]
    pred_dict["garage_area"] = int(request.form["Garage Area"])
    pred_dict["garage_cars"] = int(request.form["Garage Cars"])
    pred_dict["fst_flr_sf"] = int(request.form["1st Flr SF"])
    pred_dict["total_bsmt_sf"] = int(request.form["Total Bsmt SF"])
    pred_dict["gr_liv_area"] = int(request.form["Gr Liv Area"])
    pred_dict["overall_qual"] = int(request.form["Overall_Qual"])
    pred_dict["kitchen_qual"] = request.form["Kitchen Qual"]
    pred_dict["bsmt_qual"] = request.form["Bsmt Qual"]
    pred_dict["age_house"] = int(request.form["Age_house"])
    pred_dict["bath"] = int(request.form["Bath"])
    pred_dict["estimated_price"] = pred[0]
    print(pred_dict)
    Prediction.add_prediction(pred_dict)
    
    return render_template('predict.html', data=int(pred))

@main.route('/profile', methods=["GET","POST"])
@login_required
def profile():
    conn = db.session()
    cursor = conn.execute(f'''SELECT b.neighborhood, b.garage_area, b.garage_cars, b.fst_flr_sf, b.total_bsmt_sf,
                          b.gr_liv_area, b.overall_qual, b.kitchen_qual, b.bsmt_qual, b.age_house, b.bath, b.estimated_price
                          FROM Users AS a JOIN Predictions AS b ON a.id=b.id_user WHERE a.id={current_user.id}''').cursor
    data = cursor.fetchall()
    return render_template('profile.html', data=data)