import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer

from sklearn.preprocessing import OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

def transformation_X(X,all_col):
       X = X[all_col]
    #    X.columns = ['Year_Built', 'Total_Bsmt_SF', '1st_Flr_SF', 'Gr_Liv_Area','Garage_Area', 'Overall_Qual', 'Full_Bath', 'Exter_Qual',
    #           'Kitchen_Qual', 'Neighborhood']
       return X

# numeric_features = ["Year Built", "Total Bsmt SF", "1st Flr SF", "Gr Liv Area", "Garage Area", "Overall Qual", "Full Bath"]
# ordinal_features = [ "Exter Qual",  "Kitchen Qual"],
# cat_feature = ["Neighborhood"]):
    

def regression(y_train ="default", y_test ="default", X_train ="default", X_test ="default", numeric_features = "default",ordinal_features =  "default",cat_feature =  "default"):
    
    if not isinstance(y_train, pd.Series):
        y_train = pd.read_csv("data/y_train.csv")
    
    if not isinstance(y_test, pd.Series):
        y_test = pd.read_csv("data/y_test.csv")

    if not isinstance(X_train, pd.DataFrame):
        X_train = pd.read_csv("data/X_train.csv")
    
    if not isinstance(X_test, pd.DataFrame):
        X_test = pd.read_csv("data/X_test.csv")

    if numeric_features == "default":
        numeric_features = ["Year Built", "Total Bsmt SF", "1st Flr SF", "Gr Liv Area", "Garage Area", "Overall Qual", "Full Bath"]

    if ordinal_features == "default":
        ordinal_features = [ "Exter Qual",  "Kitchen Qual"]

    if cat_feature == "default":
        cat_feature = ["Neighborhood"]

    all_col = numeric_features.copy()
    all_col.extend(ordinal_features)
    all_col.extend(cat_feature)
    
    X_train = transformation_X(X_train,all_col)
    X_test = transformation_X(X_test, all_col)

    numeric_transformer = SimpleImputer()

    exter_cat = [ 'Po', 'Fa','TA', 'Gd','Ex']
    kitchen_cat = [ 'Po', 'Fa','TA', 'Gd',"Ex"]

    ordinal_transformer = OrdinalEncoder(categories=[exter_cat, kitchen_cat])

    categorical_transformer = OneHotEncoder()



    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('ord', ordinal_transformer, ordinal_features),
            ('cat', categorical_transformer, cat_feature)
        ]
    )
    
    reg = LinearRegression()

    from sklearn.metrics import mean_absolute_error

    pipe = Pipeline([
        ('preprocessor', preprocessor),
        ('reg', reg)
    ])


    pipe.fit(X_train, y_train) 

    
    pipe.score(X_test,y_test)

    predict_train  = pipe.predict(X_train)
    predict_test  = pipe.predict(X_test)

    # Root Mean Squared Error on train and test date
    mae_train = mean_absolute_error(y_train, predict_train)
    mae_test = mean_absolute_error(y_test, predict_test)
    print('MAE on train data: ', mae_train)
    print('MAE on test data: ', mae_test)
    return (mae_train,mae_test)


if __name__ == "__main__":
    regression()


