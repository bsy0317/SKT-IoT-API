from flask import Flask, jsonify, request
import requests
import configparser
import os

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('settings.ini')

authorization = config['Credentials']['authorization']
widget_id = config['Device']['widgetId']

# API endpoint to control device and perform polling
@app.route('/controlDevice/<action>', methods=['GET'])
def control_device(action):
    remote_ip = request.remote_addr
    if not is_private_ip(remote_ip):
        return jsonify({"error": "Access denied."}), 403
        
    headers = {
        "host": "mobile.sktsmarthome.com:9002",
        "x-sh-os-type": "IOS",
        "accept": "application/json",
        "authorization": authorization,
        "smartmode": "true",
        "accept-language": "ko-KR,ko;q=0.9",
        "content-type": "application/json",
        "user-agent": "smarthome-ios",
    }

    if action == 'on' or action == 'off':
        data = {
            "commandType": "D03",
            "rtnDvcId": widget_id,
            "connStatCd": "001",
            "requestValue": action,
            "dvcKindCd": "013"
        }
        
        response = requests.post("https://mobile.sktsmarthome.com:9002/v1/device/controlDevice", json=data, headers=headers)
        if response.status_code == 200:
            response_data = response.json()

            if "commandId" in response_data:
                polling_response = perform_polling(response_data["commandId"])
                result_message = polling_response.get("pollingList", [{}])[0].get("message", "")
                result_cd = polling_response.get("resultCd", "")
                return jsonify({"message": result_message, "resultCd": result_cd})
            else:
                return jsonify({"error": "No commandId found in the response."}), 500
        else:
            return jsonify({"error": "Failed to send control device request."}), response.status_code
    elif action == 'status':
        data = {
            "widgetDvcList": [
                {
                    "svcType": "D",
                    "widgetId": widget_id
                }
            ]
        }
        response = requests.post("https://mobile.sktsmarthome.com:9002/v1/widget/set/villageUserDvcModelList", json=data, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            result_message = response_data.get("resultMsg", "")
            result_cd = response_data.get("dvcList", [{}])[0].get("widgetControlFncStauts", "")
            return jsonify({"message": result_message, "resultCd": result_cd})
        else:
            return jsonify({"error": "Failed to send status request."}), response.status_code
    else:
        return jsonify({"error": "Invalid action."}), 400

# Function to perform polling
def perform_polling(command_id):
    polling_url = f"https://mobile.sktsmarthome.com:9002/v1/device/commandPolling?commandId={command_id}"
    polling_response = requests.get(polling_url)
    if polling_response.status_code == 200:
        polling_data = polling_response.json()
        return polling_data
    else:
        return {"error": "Failed to perform polling."}

# Function to check if an IP address is in a private network range
def is_private_ip(ip):
    private_ranges = [
        ("10.0.0.0", "10.255.255.255"),
        ("172.16.0.0", "172.31.255.255"),
        ("192.168.0.0", "192.168.255.255"),
        ("127.0.0.0", "127.255.255.255"),
    ]
    ip_int = ip_to_int(ip)
    for start, end in private_ranges:
        if ip_int >= ip_to_int(start) and ip_int <= ip_to_int(end):
            return True
    return False

# Function to convert IP address to integer
def ip_to_int(ip):
    parts = ip.split('.')
    return (int(parts[0]) << 24) + (int(parts[1]) << 16) + (int(parts[2]) << 8) + int(parts[3])
    
if __name__ == '__main__':
    app.run(debug=True)
