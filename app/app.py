from flask import Flask, request, jsonify
from sklearn.ensemble import GradientBoostingClassifier
import pickle
import numpy as np
import pymysql
import cryptography

# Загрузка модели
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

app = Flask(__name__)

# Настройки базы данных
db_config = {
    'host': 'db',            # Используем название сервиса из docker-compose.yml
    'user': 'user',
    'password': 'password',
    'database': 'predictions_db'
}

# Эндпоинт для получения предсказаний
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    features = np.array(data['features']).reshape(1, -1)
    prediction = model.predict(features)[0]

    # Сохраняем предсказание в базу данных
    save_prediction_to_db(features.tolist(), prediction)

    return jsonify({'prediction': int(prediction)})

# Функция для сохранения предсказаний в базу данных
def save_prediction_to_db(features, prediction):
    connection = pymysql.connect(**db_config)
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO predictions (features, prediction) VALUES (%s, %s)",
                       (str(features), int(prediction)))
    connection.commit()
    connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
