from flask import Flask
import random
import string
import csv  
import re


app = Flask(__name__)


@app.route("/generate_password")
def generate_password():
    """
    from 10 to 20 chars
    upper and lower case
    """
    # string
    # ascii_lowercase
    # ascii_uppercase
    # int
    # special symbols
    # return password
    
    letters = list(string.ascii_letters)
    special_symbols = [symbol for symbol in string.punctuation if symbol not in ("\\", "<", ">")] 
    print(special_symbols)
    numbers = [str(num) for num in range(10)]
    all_symbols = letters + special_symbols + numbers

    min_count_symbols = 10
    max_count_symbols = 20

    while True:
        genered_pasword = random.choices(all_symbols, k=random.randint(min_count_symbols, max_count_symbols))

        has_letter = any(symb_pswrd in letters for symb_pswrd in genered_pasword)
        has_special_symbol = any(symb_pswrd in special_symbols for symb_pswrd in genered_pasword)
        has_number = any(symb_pswrd in numbers for symb_pswrd in genered_pasword)

        if all([has_letter, has_special_symbol, has_number]):
            return_pasword_string = "".join(genered_pasword)
            return return_pasword_string


@app.route("/calculate_average")
def calculate_average():
    """
    csv file with students
    1.calculate average high
    2.calculate average weight
    csv - use lib
    *pandas - use pandas for calculating
    """
    with open("hw.csv", "r") as file:
        reader = csv.reader(file)

        heights_list = []
        weight_list = []

        for row in reader:
            height = row[1]
            weight = row[2]
            if re.match(r"^[\d.]+$", height.strip()):
                heights_list.append(float(height))
            if re.match(r"^[\d.]+$", weight.strip()):
                weight_list.append(float(weight))

    print(weight_list[-1])

    average_high = sum(heights_list) / len(heights_list)
    average_high = round(average_high, 5)
    average_weight = sum(weight_list) / len(weight_list)
    average_weight = round(average_weight, 4)

    # return_dict = {"average high": average_high, "average weight": average_weight}

    return_str = f"Average high: {average_high} inch | Average weight: {average_weight} pound"
    return return_str


if __name__ == "__main__":
    app.run(debug=True)
