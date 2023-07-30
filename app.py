import numpy as np
import pandas as pd
import pickle
from flask import Flask, request, render_template, jsonify
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import GradientBoostingRegressor


# app
app = Flask(__name__, template_folder='templates')

load_model = pickle.load(open('gbr_model_v1.pkl', 'rb'))
le_region = pickle.load(open('region_label_encoder.pkl', 'rb'))
std_scaler = pickle.load(open('std_scaler.pkl', 'rb'))

with open('gbr_model_v1.pkl', 'rb') as f:
    loaded_model = pickle.load(f)

print('loaded')

# welcome page
# работает на фронте
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('main.html')

    if request.method == 'POST':

        sex = str.lower(request.form['sex'])
        if sex == 'male':
            sex = 1
        elif sex == 'female':
            sex = 0
        else:
            raise ValueError('sex must be male or female')
        age = int(request.form['age'])
        bmi = float(request.form['bmi'])
        smoker = str.lower(request.form['smoker'])
        if smoker == 'yes':
            smoker = 1
        elif smoker == 'no':
            smoker = 0
        else:
            raise ValueError('must be no or yes')
        children = int(request.form['children'])
        region = request.form['region']

        df = pd.DataFrame([age, sex, bmi, children, smoker, region]).T
        df.columns=['age', 'sex', 'bmi', 'children', 'smoker', 'region']

        df['region'] = le_region.transform(df['region'])

        df = std_scaler.transform(df.values)
        y_pred = round(loaded_model.predict(df)[0], 2)

        return render_template('main.html', result=y_pred)
    return render_template('main.html')

# на фронте не работает (только на бэке происходит)
# создаем маршрут
# uuid - какое-то сообщение
@app.route('/api/add_message/<uuid>', methods=['GET', 'POST'])
def add_message(uuid):
    content = request.json
    print(content['mytext'])
    df = std_scaler.transform(np.array(content['mytext']).reshape(1, -1))
    y_pred = str(round(loaded_model.predict(df)[0], 2))
    # return y_pred
    return jsonify({"uuid":str(y_pred)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
