import requests
import json
import Settings

api_key = Settings.get_setting("KEY")
logger_id = Settings.get_setting("LOGGERID")

def post_http_single(log):
    
    try:
        url = "https://westeurope.azure.data.mongodb-api.com/app/data-mgxzs/endpoint/data/v1/action/insertOne"
        payload = json.dumps({

                "collection": "motion_data",
                "database": "VMLog",
                "dataSource": "VMLog",

                "document": {
                    "logger_id": logger_id,
                    "timestamp": log["timestamp"],

                    "pitch": log["pitch"],
                    "roll": log["roll"],
                    "yaw": log[yaw],

                    "acc_x": log["acc_x"],
                    "acc_y": log["acc_y"],
                    "acc_z": log["acc_z"],

                    "gyr_x": log["gyr_x"],
                    "gyr_y": log["gyr_y"],
                    "gyr_z": log["gyr_z"],
                }
            })
        
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Request-Headers': '*',
            'api-key': api_key,
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        return response.ok
    except Exception as err:
        print(str(err))
        return False

