import json
import requests
import logging

logger = logging.getLogger(__name__)

class PolicyManager:
    def __init__(self, base_url, policy_type_id):
        self.base_url = base_url
        self.policy_type_id = policy_type_id

    def create_policy_type(self):
        policy_type_data = {
            "name": "tspolicy",
            "description": "tsa parameters",
            "policy_type_id": self.policy_type_id,
            "create_schema": {
                "$schema": "http://json-schema.org/draft-07/schema#",
                "title": "TS Policy",
                "description": "TS policy type",
                "type": "object",
                "properties": {
                    "threshold": {
                        "type": "integer",
                        "default": 0
                    }
                },
                "additionalProperties": False
            }
        }
        url = f"{self.base_url}/policytypes/{self.policy_type_id}"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.put(url, headers=headers, data=json.dumps(policy_type_data))
        if response.status_code == 200:
            logger.info("Policy type created successfully.")
        else:
            logger.error(f"Failed to create policy type. Status code: {response.status_code}")
            logger.error(response.text)

    def create_policy_instance(self, threshold_value):
        policy_instance_id = f"policy_{threshold_value}"
        url = f"{self.base_url}/policytypes/{self.policy_type_id}/policies/{policy_instance_id}"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "threshold": threshold_value
        }
        response = requests.put(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            logger.info(f"Policy instance with threshold {threshold_value} created successfully.")
        else:
            logger.error(f"Failed to create policy instance. Status code: {response.status_code}")
            logger.error(response.text)
