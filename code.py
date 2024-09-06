# from sqlalchemy import MetaData  # type: ignore
# from sqlalchemy import Table, Column, Integer, String
# import json
# from collections import defaultdict
# from functools import reduce
# from itertools import groupby
# import random
# from datetime import datetime, timedelta
# metadata_obj = MetaData()
# user_table = Table(
#     "user_account",
#     metadata_obj,
#     Column("id", Integer, primary_key=True),
#     Column("name", String(30)),
#     Column("fullname", String),
# )

# print(user_table.c)

# user_table.c.keys()


# """
# imported 
# filter
# sort, sorted 
# map => transform the data
# reduce
# group
# """

# # Use print("messages...") to debug your solution.

# show_expected_result = True
# show_hints = False


# weather = [{
#        "data": "02-02-2007",
#        "tmin": 0.02,
#        "tmax": 23,
#        "prcp": 0.8,
#        "snow": 0.3,
#        "snwd": 10.2,
#        "awnd": 10
#     },
    
#     {
#        "data": "02-03-209",
#        "tmin": 0.08,
#        "tmax": 23,
#        "prcp": 0.8,
#        "snow": 0.3,
#        "snwd": 10.2,
#        "awnd": 10
#     }]
# def get_cold_windy_rainy_days():
    
#     with open("C:\\Users\\Adeyori\\alx-project\\backend\\weathe.json") as file:
#         weather = json.load(file)
#         data = list(filter(lambda x: x['snow'] > 0.7 and x['tmax'] < 45
#                            and x['awnd'] > 10, weather))
#         data2 = list(map(lambda x1, x2: (x1['snow'] + x2['snow']) / 2, weather[1::2], weather[::2]))
#         """
#         weather[1::2], weather[::2]
#         weather[1::2] seleect every odd element
#         weather[::2] select every every element

#         """
#         data3 = reduce(lambda acc, cur: acc + cur['snow'],
#                             weather, 0.0)
#     return [weather, data, data2, data3]

# fun = lambda x, y: print(x + y)
# fun(12, 34)
# # data2 = list(map(lambda x1, x2: (x1['snow'] + x2['snow']) / 2, weather))
# # print(get_cold_windy_rainy_days())
# def group():
#     data = get_cold_windy_rainy_days()[0]
#     grp = {}
#     for i in data:
#         snow_value = i['snow']
#         if snow_value not in grp:
#             grp[snow_value] = []
#         grp[snow_value].append(i)
#     return grp

# # Example usage
# grouped_data = group()
# # print(grouped_data)
# for i in range(10):
#     print(i)
# #print(help(datetime))
# #print(group())
# print(defaultdict(list))


# def generate_random_weather_data(start_date, num_days):
#     weather_data = []
#     current_date = start_date
#     for _ in range(num_days):
#         entry = {
#             "date": current_date.strftime("%d-%m-%Y"),
#             "tmin": round(random.uniform(-10, 10), 2),  # Min temperature in Celsius _ mean loop variable is not important
#             "tmax": round(random.uniform(10, 35), 2),  # Max temperature in Celsius
#             "prcp": round(random.uniform(0, 50), 2),  # Precipitation in mm
#             "snow": round(random.uniform(0, 20), 2),  # Snowfall in cm
#             "snwd": round(random.uniform(0, 50), 2),  # Snow depth in cm
#             "awnd": round(random.uniform(0, 30), 2)  # Average wind speed in km/h
#         }
#         weather_data.append(entry)
#         current_date += timedelta(days=1)
    
#     return weather_data

# # Generate weather data for 10 days starting from 1st January 2024
# # start_date = datetime.strptime("01-01-2002", "%d-%m-%Y")
# # weather_data = generate_random_weather_data(start_date, 500)

# # with open("weathe.json", "w+") as f:
# #     f.write(json.dumps(weather_data))
# # Print the generated weather data

# user_data = {
#     'first_name': 'John',
#     'last_name': 'Doe',
#     'email': 'john.doe@example.com',
#     'password': 'hashed_password',
#     'user_id': '12345',
#     'profile_pix': 'profile.jpg',
#     'middle_name': 'Middle',
#     'gender': 'Male',
#     'date_of_birth': '1990-01-01'
# }

# print("First Name: {first_name}, Last Name: {last_name}, Email: {email}".format(**user_data))

import bcrypt
import base64


def hash_password(plain_text_password: str) -> str:
    """Encrypt a plain text password."""
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(plain_text_password.encode('utf-8'), salt)
    # Encode the hashed password with base64
    return base64.b64encode(hashed_password).decode('utf-8')


def check_password(plain_text_password: str, hashed_password: str) -> bool:
    """Check if the provided plain text password matches the hashed password."""
    # Decode the base64 encoded hashed password
    decoded_hashed_password = base64.b64decode(hashed_password)
    # Check if the provided password matches the hashed password
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), decoded_hashed_password)


# Example usage
if __name__ == "__main__":
    original_password = "my_secure_password"
    hashed_pw = hash_password(original_password)
    
    print("Hashed password:", hashed_pw)

    # Now check if the password is correct
    is_correct = check_password(original_password, hashed_pw)
    print("Password is correct:", is_correct)

    # Check with an incorrect password
    is_correct = check_password("wrong_password", hashed_pw)
    print("Password is correct:", is_correct)

