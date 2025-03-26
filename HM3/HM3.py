from faker import Faker
import csv
from flask import Flask, request, jsonify
import requests


fake = Faker()
app = Flask(__name__)


@app.route('/generate_students')
def generate_students():
    # count should be as input GET parameter
    # first_name, last_name, email, password, birthday (18-60)
    # save to csv and show on web page
    # set limit as 1000
    count_of_students = request.args.get('count', default=10, type=int)
    if count_of_students > 1000:
        return "Error: Count cannot exceed 1000"
    
    filename = "students.csv"
    students: dict = {}

    for i in range(count_of_students):
        
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        password = fake.password(length=12)
        birthday = fake.date_of_birth(minimum_age=18, maximum_age=60)

        i += 1
        students[f"student {i}"] = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
            "birthday": birthday.strftime("%Y-%m-%d")
        }

    fieldnames = ["student_id", "first_name", "last_name", "email", "password", "birthday"]

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for student_id, data_dict in students.items():
            row = {"student_id": student_id}
            row.update(data_dict)
            writer.writerow(row)

    return jsonify(students)


@app.route("/get_bitcoin_value")
def get_bitcoin_value():
    # https://bitpay.com/api/rates
    # /bitcoin_rate?currency=UAH&convert=100
    # input parameter currency code
    # default is USD
    # default count is 1
    # return value currency of bitcoin
    # add one more input parameter count and multiply by currency (int)
    # * https://bitpay.com/api/
    # * Example: $, €, ₴
    # * return symbol of input currency code

    try:
        currency = request.args.get("currency", default="USD", type=str)
        count = request.args.get("convert", default=1, type=float)

        rate_url = f"https://bitpay.com/api/rates/{currency}"
        rate_response = requests.get(rate_url)
        rate_json = rate_response.json()

        symbols_url = "https://bitpay.com/currencies"
        symbols_response = requests.get(symbols_url)
        symbols_json = symbols_response.json()

        rate_ok = rate_response.status_code == 200 and rate_json
        symbols_ok = symbols_response.status_code == 200 and symbols_json

        if rate_ok and symbols_ok:
            for i in symbols_json["data"]:
                if i["code"] == "BTC":
                    btc_symbol = i["symbol"]
                
                if i["code"] == currency:
                    currency_symbol = i["symbol"]

            rate = rate_json.get("rate")
            return_str = f"BTC({btc_symbol}) is {rate} {currency}({currency_symbol})"

            if count != 1:
                final_value = round(rate * count, 3)
                return_str += f"<br>----------"
                return_str += f"<br>{count} BTC({btc_symbol}) is {final_value} {currency}({currency_symbol})"

            return return_str

        else:
            return "ERROR: Error fetching data from API"
    
    except requests.exceptions.RequestException as e:
        return f"ERROR: {e}"


if __name__ == '__main__':

    app.run(debug=True)
