import requests
import json
import datetime
import time


def get_climate_data(ip):
    return json.loads(requests.get("http://" + ip).text)


def get_database():
    with open("database.json") as database:
        return json.loads(database.read())


def log_climate_data(ip_inside, ip_outside):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    try:
        data_inside = get_climate_data(ip_inside)
    except:
        print("Inside sensor not available.")
    try:
        data_outside = get_climate_data(ip_outside)
    except:
        print("Outside sensor not available.")
    database = get_database()
    climate_json = {
        "inside": {
            "temperature": round(data_inside["temperature"], 2),
            "humidity": round(data_inside["humidity"], 2)
        },
        "outside": {
            "temperature": round(data_outside["temperature"], 2),
            "humidity": round(data_outside["humidity"], 2)
        }
    }
    database["logs"][timestamp] = climate_json
    with open("database.json", "w") as file:
        file.seek(0)
        file.write(json.dumps(database))
    print(climate_json)

def calculate_average():
    current_month = str(datetime.datetime.now().month)
    database = get_database()
    average = database["calculations"]
    logs = database["logs"]
    accumulator = {
        "inside": {
            "temperature": {
                "general": 0,
                "month": 0
            },
            "humidity": {
                "general": 0,
                "month": 0
            },
        },
        "outside": {
            "temperature": {
                "general": 0,
                "month": 0
            },
            "humidity": {
                "general": 0,
                "month": 0
            }
        }
    }
    amount_of_monthly_logs = 0
    for log in logs:
        accumulator["inside"]["temperature"]["general"] += database["logs"][log]["inside"]["temperature"]
        accumulator["inside"]["humidity"]["general"] += database["logs"][log]["inside"]["humidity"]
        accumulator["outside"]["temperature"]["general"] += database["logs"][log]["outside"]["temperature"]
        accumulator["outside"]["humidity"]["general"] += database["logs"][log]["outside"]["humidity"]
        if current_month == log.split("-")[1]:
            amount_of_monthly_logs += 1
            accumulator["inside"]["temperature"]["month"] += database["logs"][log]["inside"]["temperature"]
            accumulator["inside"]["humidity"]["month"] += database["logs"][log]["inside"]["humidity"]
            accumulator["outside"]["temperature"]["month"] += database["logs"][log]["outside"]["temperature"]
            accumulator["outside"]["humidity"]["month"] += database["logs"][log]["outside"]["humidity"]
    database["calculations"]["inside"]["temperature"]["average"] = round(accumulator["inside"]["temperature"]["general"] / len(logs), 2)
    database["calculations"]["inside"]["humidity"]["average"] = round(accumulator["inside"]["humidity"]["general"] / len(logs), 2)
    database["calculations"]["outside"]["temperature"]["average"] = round(accumulator["outside"]["temperature"]["general"] / len(logs), 2)
    database["calculations"]["outside"]["humidity"]["average"] = round(accumulator["outside"]["humidity"]["general"] / len(logs), 2)
    if not amount_of_monthly_logs == 0:
        database["calculations"]["inside"]["temperature"]["average_current_month"] = round(accumulator["inside"]["temperature"]["month"] / amount_of_monthly_logs, 2)
        database["calculations"]["inside"]["humidity"]["average_current_month"] = round(accumulator["inside"]["humidity"]["month"] / amount_of_monthly_logs, 2)
        database["calculations"]["outside"]["temperature"]["average_current_month"] = round(accumulator["outside"]["temperature"]["month"] / amount_of_monthly_logs, 2)
        database["calculations"]["outside"]["humidity"]["average_current_month"] = round(accumulator["outside"]["humidity"]["month"] / amount_of_monthly_logs, 2)
    with open("database.json", "w") as file:
        file.seek(0)
        file.write(json.dumps(database))

def main():
    while True:
        log_climate_data("192.168.2.119", "192.168.2.120")
        calculate_average()
        time.sleep(600)


if __name__ == '__main__':
    main()
