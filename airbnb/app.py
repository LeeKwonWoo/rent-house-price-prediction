from flask import Flask, render_template, request
from pandas import DataFrame
import joblib
from sklearn.preprocessing import StandardScaler

seoul_model = joblib.load('/home/leekwonwoo/previous/PycharmProjects/pythonProject/costPredictionProject/seoul/RandomForestRegressor_model.pkl')
tokyo_model = joblib.load('/home/leekwonwoo/previous/PycharmProjects/pythonProject/costPredictionProject/tokyo/RandomForestRegressor_model.pkl')

app = Flask(__name__, static_url_path='/static')

@app.route('/', methods=['GET'])
def index():
    return render_template("button.html")

@app.route('/seoul', methods=['GET'])
def seoul():
    return render_template("seoul.html")

@app.route('/tokyo', methods=['GET'])
def tokyo():
    return render_template("tokyo.html")

@app.route('/calculate', methods=['GET'])
def calculate(num=None):
    ## 어떤 http method를 이용해서 전달받았는지를 아는 것이 필요함
    ## 아래에서 보는 바와 같이 어떤 방식으로 넘어왔느냐에 따라서 읽어들이는 방식이 달라짐
    if request.method == 'POST':
        #temp = request.form['num']
        pass
    elif request.method == 'GET':
        ## 넘겨받은 숫자 
        
        temp0 = request.args.get('seoul')
        
        temp = request.args.get('num')
        temp2 = request.args.get('bed')
        temp3 = request.args.get('bath')
        temp4 = request.args.get('min')
        temp5 = request.args.get('lat')
        temp6 = request.args.get('long')
              
        
        if request.args.get('ss1'):
            temp7 = 1
            temp8 = 0
            temp9 = 0
        elif request.args.get('ss2'):
            temp7 = 0
            temp8 = 1
            temp9 = 0
        elif request.args.get('ss3'):
            temp7 = 0
            temp8 = 0
            temp9 = 1

        data_df = [[temp,temp2,temp3,temp4,temp5,temp6,temp7,temp8,temp9]]
        arr = DataFrame(data_df)
        scaler = StandardScaler().fit(arr)
        arr = scaler.transform(arr)
        arr = DataFrame(arr)
        
        q = arr.iloc[:, 0:9].values
        
        if temp0 in 'seoul':
            loaded_model = seoul_model
        elif temp0 in 'tokyo':
            loaded_model = tokyo_model

        answer = f'{loaded_model.predict(q)[0]*1256.11:.0f}'
        print(str(answer))
        ## 넘겨받은 값을 원래 페이지로 리다이렉트
        return render_template('result.html', answer=answer)
    ## else 로 하지 않은 것은 POST, GET 이외에 다른 method로 넘어왔을 때를 구분하기 위함


if __name__ == '__main__':
    app.run(debug=True)