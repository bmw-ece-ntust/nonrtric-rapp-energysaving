import json
import requests
import logging
from mdclogpy import Logger

logger = Logger(name=__name__)

class ASSIST(object):

    def send_request_to_server(self, json_data):
        with open('input.json', 'w') as f:
            json.dump(json_data, f)

        url = 'http://10.233.9.173:80/v1/models/qoe-model:predict'
        headers = {'Host': 'qoe-model.kserve-test.example.com'}

        with open('input.json', 'rb') as f:
            response = requests.post(url, headers=headers, data=f)
        logger.info("Prediction result")
        logger.info(response.text)
        return response.status_code, response.text
