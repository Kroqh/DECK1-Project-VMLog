# libraries for base functionality
import requests
import json
import pandas as pd
# our own scripts
import Settings
import LogHandler

# settings
api_key = Settings.get_setting("KEY")
logger_id = Settings.get_setting("LOGGERID")

# FUNCTIONS

def post_http_single(log_df):
    document_from_df = log_df.to_dict()
    try:
        url = "https://westeurope.azure.data.mongodb-api.com/app/data-mgxzs/endpoint/data/v1/action/insertOne"
        payload = json.dumps(
            {
            "collection": "motion_data",
            "database": "VMLog",
            "dataSource": "VMLog",

            "document": document_from_df,
            }
        )
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Request-Headers': '*',
            'api-key': api_key,
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        """
        LogHandler.write_to_system_log
        if response.ok:
            LogHandler.write_to_system_log("Log succesfully uploaded with id: " + response.text)
            return True
        else:
            LogHandler.write_to_system_log("Log upload failed, error message: " + response.text)
            return False
        """
        print(response)
        
    except Exception as err:
        #LogHandler.write_to_system_log("Upload failed, exception: " + str(err))
        print("Upload failed, exception: " + str(err))
        return False



"""
def post_http_single(log_df):
    
    try:
        url = "https://westeurope.azure.data.mongodb-api.com/app/data-mgxzs/endpoint/data/v1/action/insertOne"
        payload = json.dumps(
            {
            "collection": "motion_data",
            "database": "VMLog",
            "dataSource": "VMLog",

            "document":
                {
                "logger_id": logger_id,
                "timestamp": log_df["timestamp"],
                "roll": log_df["roll"],
                "pitch": log_df["pitch"],
                "yaw": log_df["yaw"],
                "acc_x": log_df["acc_x"],
                "acc_y": log_df["acc_y"],
                "acc_z": log_df["acc_z"],
                "gyr_x": log_df["gyr_x"],
                "gyr_y": log_df["gyr_y"],
                "gyr_z": log_df["gyr_z"]
                }
            }
        )
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
        
        print(response)
        
    except Exception as err:
        #LogHandler.write_to_system_log("Upload failed, exception: " + str(err))
        print("Upload failed, exception: " + str(err))
        return False
"""
