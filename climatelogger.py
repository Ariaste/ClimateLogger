import requests
import json
import datetime


def get_climate_data(ip):
    return json.loads(requests.get("http://" + ip).text)


def get_data_base():
    with open("database.json") as database:
        return database.readlines()


def log_climate_data(ip_inside, ip_outside, database_file):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    data_inside = get_climate_data(ip_inside)
    data_outside = get_climate_data(ip_outside)
    database = get_data_base()
    data_json = """         \"{t}\" : {{
            \"inside\": {{
                \"temperature\": {it:.2f},
                \"humidity\": {ih:.2f}
            }},
            \"outside\": {{
                \"temperature\": {ot:.2f},
                \"humidity\": {oh:.2f}
            }}
        }}\n""".format(t=timestamp, it=data_inside["temperature"], ih=data_inside["humidity"], ot=data_outside["temperature"], oh=data_outside["humidity"])
    if database[len(database) - 3].__contains__("logs"):
        database = database[0:len(database)-3] + [data_json] + database[len(database)-2:]
    else:
        database = database[0:len(database)-3] + ["\t\t},\n",  data_json] + database[len(database)-2:]
    with open(database_file, "w") as file:
        file.seek(0)
        for line in database:
            file.write(str(line))


def calculate_average():
    database = json.loads("".join(get_data_base()))
    logs_keys = database["logs"].keys()
    average_temperature_inside = 0
    average_temperature_outside = 0
    average_temperature_inside_month = 0
    average_temperature_outside_month = 0
    for key in logs_keys:
        average_temperature_inside += database["logs"][key]["inside"]["temperature"]
        average_temperature_outside += database["logs"][key]["outside"]["temperature"]
    average_temperature_inside = round(average_temperature_inside / len(logs_keys), 2)
    average_temperature_outside = round(average_temperature_outside / len(logs_keys), 2)
    print(str(average_temperature_inside) + " " + str(average_temperature_outside))



def main():
    calculate_average()



if __name__ == '__main__':
    main()
