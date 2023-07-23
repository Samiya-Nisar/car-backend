from flask import Flask, render_template, jsonify
import psycopg2
import requests
import calendar
import os
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

db_config = {
    "host": "dpg-ciufiip5rnuhcntlo74g-a",
    "database": "car_6jjt",
    "user": "samiya",
    "password": "qhs1lxvHtLbQTq3BhuSBjUTRyRDyxNRP"
}


@app.route('/')
def index():
    file_path = os.path.join(os.path.dirname(__file__), 'data', 'data.json')
    with open(file_path, 'r') as file:
        cars_data = json.load(file)

    save_cars_to_database(cars_data)

    cars_from_db = fetch_cars_from_database()

    return render_template('index.html', cars=cars_from_db)


def save_cars_to_database(cars_data):
    try:
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS cars (
            id INT NOT NULL PRIMARY KEY,
            make VARCHAR(2000),
            model VARCHAR(2000),
            fuelType VARCHAR(3000),
            accelaration VARCHAR(3000),
            topSpeed VARCHAR(3000),
            engine VARCHAR(3000),
            price VARCHAR(4000),
            year VARCHAR(100),
            image VARCHAR(10000),
            seatingCapacity VARCHAR(100),
            colors VARCHAR(10000),
            variants VARCHAR(10000),
            summary VARCHAR(20000),
            pros VARCHAR(20000),
            cons VARCHAR(20000)
        );
        """
        cursor.execute(create_table_query)

        for car in cars_data:
            id = car.get('id', 0)
            make = car.get('make', '')
            model = car.get('model', '')
            fuelType = car.get('fuelType', '')
            accelaration = car.get('accelaration', '')
            topSpeed = car.get('topSpeed', '')           
            engine = car.get('engine', '')           
            price = car.get('price', '')           
            year = car.get('year', '')           
            image = car.get('image', '')            
            seatingCapacity = car.get('seatingCapacity', '')           
            colors = car.get('colors', '')            
            variants = car.get('variants', '')            
            summary = car.get('summary', '')
            pros = car.get('pros', '')
            cons = car.get('cons', '')

            insert_query = """
            INSERT INTO cars (id, make, model, fuelType, accelaration, topSpeed, engine, price, year, image, seatingCapacity, colors, variants, summary, pros, cons)
            VALUES (%s, %s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s) ON CONFLICT (id) DO NOTHING;
            """
            cursor.execute(insert_query, (id, make, model, fuelType, accelaration, topSpeed, engine, price, year, image, seatingCapacity, colors, variants, summary, pros, cons))

        connection.commit()
        connection.close()

    except psycopg2.Error as e:
        print("Error saving data to the database:", e)


def fetch_cars_from_database():
    try:
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()

        select_query = "SELECT id, make, model, fuelType, accelaration, topSpeed, engine, price, year, image, seatingCapacity, colors, variants, summary, pros, cons FROM cars;"
        cursor.execute(select_query)
        cars_data = cursor.fetchall()
        connection.close()

        cars_list = []
        for car in cars_data:
            car_dict = {
                'id': car[0],
                'make': car[1],
                'model': car[2],
                'fuelType': car[3],
                'accelaration': car[4],
                'topSpeed': car[5],
                'engine': car[6],
                'price': car[7],
                'year': car[8],
                'image': car[9],
                'seatingCapacity': car[10],
                'colors': car[11],
                'variants': car[12],
                'summary': car[13],
                'pros': car[14],
                'cons': car[15]
            }
            cars_list.append(car_dict)
        return cars_list

    except psycopg2.Error as e:
        print("Error fetching data from the database:", e)

@app.route('/cars')
def cars():
    try:
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()

        select_query = "SELECT id, make, model, fuelType, accelaration, topSpeed, engine, price, year, image, seatingCapacity, colors, variants, summary, pros, cons FROM cars;"
        cursor.execute(select_query)
        cars_data = cursor.fetchall()
        connection.close()

        cars_list = []
        for car in cars_data:
            car_dict = {
                'id': car[0],
                'make': car[1],
                'model': car[2],
                'fuelType': car[3],
                'accelaration': car[4],
                'topSpeed': car[5],
                'engine': car[6],
                'price': car[7],
                'year': car[8],
                'image': car[9],
                'seatingCapacity': car[10],
                'colors': car[11],
                'variants': car[12],
                'summary': car[13],
                'pros': car[14],
                'cons': car[15]
            }
            cars_list.append(car_dict)
        return jsonify(cars_list)

    except psycopg2.Error as e:
        print("Error fetching data from the database:", e)
        return jsonify([])

@app.route('/news')
def news():
    json_api_url = "https://newsapi.org/v2/everything?q=mercedes&pageSize=5&apiKey=8172fa01de234f44ac520b0d970114cc"
    response = requests.get(json_api_url)
    news_data = response.json()

    try:
        news_list = []
        for news in news_data['articles']:
            newsDate = news['publishedAt'][:10]
            year = newsDate[:4]
            monthStr = int(newsDate[5:7])
            month = calendar.month_name[monthStr]
            day = newsDate[8:10]
            publish = month + ' ' + day + ', ' + year

            news_dict = {
                'id': news['source']['id'],
                'name': news['source']['name'],
                'title': news['title'],
                'url': news['url'],
                'urlToImage': news['urlToImage'],
                'publishedAt': publish,
                'date': news['publishedAt'],
            }
            news_list.append(news_dict)
        return jsonify(news_list)

    except psycopg2.Error as e:
        print("Error fetching data from the api:", e)
        return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)
