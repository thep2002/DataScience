import pandas as pd 
from sklearn.model_selection import train_test_split 
import os 
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression   
from sklearn.neighbors import KNeighborsRegressor
from flask_cors import CORS, cross_origin
from flask import Flask, render_template, request


df = pd.read_csv('dataset/convert_number_data_17.csv') 
# load pickle file
categorical_dict = pd.read_pickle('dataset/categorical_dict.pkl')

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
        return render_template('index.html', file ='') 
    
    if request.method == 'POST':
        # get data from form
        print(request.form)
        
        data = request.form
        # extract keys from data 
        print(data)
        
        keys = list(data.keys())
        keys.append('price')
        
        # select only keys from df 
        df_train = df[keys] 
        
        X = df.drop('price', axis=1)
        # price column
        y = np.log(df['price'])
        
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
        
        rf = RandomForestRegressor(random_state = 123 , max_depth = 45 , n_estimators = 600)
        rf.fit(X_train,y_train)   
        
        # convert data to dataframe
        df_test = pd.DataFrame(data, index=[0])
        
        for col in df_test.columns:
            if col in categorical_dict:
                convert_to_int(col, df_test, categorical_dict[col])
        
        X_test = norm.transform(df_test)
        linear_pred = np.exp(linear.predict(X_test))
        knn_pred = np.exp(knn.predict(X_test))
        rf_pred = np.exp(rf.predict(X_test))
        
        
        
        
        # return render_template('index.html', linear_pred=linear_pred, knn_pred=knn_pred, rf_pred=rf_pred, dtr_pred=dtr_pred)
        
        
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 9910))
    app.run(debug=False, host="0.0.0.0", port=port)

        