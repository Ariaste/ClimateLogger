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
    pass


def main():
    print(log_climate_data("192.168.2.119", "192.168.2.119", "database_test.json"))


if __name__ == '__main__':
    main()
