import pandas as pd 
from sklearn.model_selection import train_test_split 
import os 
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression   
from sklearn.neighbors import KNeighborsRegressor
from flask_cors import CORS, cross_origin
from flask import Flask, render_template, request, jsonify
from sklearn.tree import DecisionTreeRegressor

df = pd.read_csv('dataset/convert_number_data_17.csv') 
# load pickle file
categorical_dict = pd.read_pickle('dataset/categorical_dict.pkl')

def convert_to_float(data):
    """Converts numerical string values in a dictionary to floats."""
    for key, value in data.items():
        try:
            # Attempt to convert each value to a float
            data[key] = float(value)
        except ValueError:
            # Keep the original value if it's not a numerical string
            continue
    return data

def convert_to_int( col, df, convert_list):
    for idx, value in enumerate(convert_list):
        df[col] = df[col].replace(value, idx)


# app = Flask(__name__)
app = Flask(__name__, template_folder='/mnt/disk3/tiennh/Cars-price-prediction-Data-Science/project/templates/')
app.secret_key = "super secret key"

cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
}) 


@app.route('/', methods=['GET', 'POST'])

def get_info(): 
    
    print(request)
    
    if request.method == 'GET':
        return render_template('index1.html', file ='') 
    
    if request.method == 'POST':
        # get data from form
        
        
        data = request.get_json()
        # extract keys from data 
        print(data)
        
        data = convert_to_float(data) 
        
        print(data)
        
        keys = list(data.keys())
        keys.append('price')
        
        # select only keys from df 
        df_train = df[keys] 
        
        X = df_train.drop('price', axis=1)
        # price column
        y = np.log(df_train['price'])
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=8)
        
        norm = StandardScaler().fit(X_train) 
        # transform training data
        X_train = norm.transform(X_train)

        # transform testing data
        X_test = norm.transform(X_test)
        
        linear = LinearRegression()
        linear.fit(X_train, y_train)
        
        knn = KNeighborsRegressor()
        knn.fit(X_train, y_train)
        
        dtr = DecisionTreeRegressor()
        dtr.fit(X_train, y_train)
        # rf = RandomForestRegressor(random_state = 123 , max_depth = 45 , n_estimators = 600)
        # rf.fit(X_train,y_train)   
        
        # convert data to dataframe
        df_test = pd.DataFrame(data, index=[0])
        
        print('df_test: ' ,df_test)
        
        for col in df_test.columns:
            if col in categorical_dict:
                convert_to_int(col, df_test, categorical_dict[col])
        
        print()
        print('df_test: ' ,df_test)
        
        X_test = norm.transform(df_test)
        
        print('X_test: ' ,X_test)
        
        linear_pred = np.exp(linear.predict(X_test))*1000
        knn_pred = np.exp(knn.predict(X_test))*1000
        # rf_pred = np.exp(rf.predict(X_test))
        dtr_pred = np.exp(dtr.predict(X_test))*1000
        data = {
            "linear_pred": round(linear_pred.tolist()[0]),
             "knn_pred": round(knn_pred.tolist()[0]),
             "dtr_pred":round(dtr_pred.tolist()[0])
        }
        
        return jsonify(data)
        # return render_template('index1.html', response=True ,linear_pred=linear_pred, knn_pred=knn_pred, dtr_pred=dtr_pred)
        
        
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 9090))
    app.run(debug=False, host="0.0.0.0", port=port)

        