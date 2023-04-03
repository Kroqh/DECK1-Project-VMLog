import requests
import json
import Settings
import LogHandler
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
        LogHandler.write_to_system_log
        if response.ok:
            LogHandler.write_to_system_log("Log succesfully uploaded with id: " + response.text)
            return True
        else:
            LogHandler.write_to_system_log("Log upload failed, error message: " + response.text)
            return False
        
        print()
        
    except Exception as err:
        LogHandler.write_to_system_log("Upload failed, exception: " + str(err))
        return False

