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
                    "timestamp": log.get("time"),
                    "pitch": log.get("pitch"),
                    "roll": log.get("roll"),
                    "g_force_x": log.get("g_force_x"),
                    "g_force_y": log.get("g_force_y"),
                    "g_force_z": log.get("g_force_z")
            }})
        
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

