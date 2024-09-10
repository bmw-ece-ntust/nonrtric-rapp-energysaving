import time
import pandas as pd
import schedule
import logging
from mdclogpy import Logger
from data import DATABASE
from assist import ASSIST
from nectconfclient import NETCONFCLIENT
from policy_manager import PolicyManager  
import json


logger = Logger(name=__name__)


class ESrapp():
    def __init__(self):

        #super().__init__()
        self.db = DATABASE()
        self.assist=ASSIST()
        self.db.connect()
        self.threshold = 50
        self.netconf=NETCONFCLIENT()
        self.index = 1

        # Create Policy Manager instance
        self.policy_manager = PolicyManager(base_url="http://192.168.8.111:32080/a1mediator/A1-P/v2", policy_type_id=20008)
        
        # Create policy type and policy instance
        self.policy_manager.create_policy_type()

    def entry(self):
        schedule.every(1).minute.do(self.inference)

        while True:
            schedule.run_pending()

    # Send data to ML rApp
    def inference(self):
        data = self.db.read_data()
        data_mapping = self.mapping(data)
        groups = data_mapping.groupby("CellID")
        for group_name, group_data in groups:
            json_data = self.generate_json_data(group_data)
            logger.info(f"Send data to ML rApp {group_name}: {json_data}")
            status_code, response_text = self.assist.send_request_to_server(json_data)
            if self.check_and_perform_action(response_text):
                cell_id_number = group_data['cellidnumber'].iloc[0] 
                logger.inf(f"Turn off the {group_name}")
                # Create policy instance with the cell_id_number before performing action
                self.policy_manager.create_policy_instance(cell_id_number)
                # Wait for 3 seconds before performing the action
                time.sleep(3)
                self.netconf.perform_action(cell_id_number)

    # Generate the input data for ML rApp
    def generate_json_data(self, data):
        rrc_conn_mean_values = data["RRC.ConnMean"].tolist()
        drb_ue_thp_ul_values = data["DRB.UEThpUl"].tolist()
        rru_prb_used_ul_values = data["RRU.PrbUsedUl"].tolist()
        pee_avg_power_values = data["PEE.AvgPower"].tolist()

        instances = [
            [
                [rrc, drb, rru, pee] 
                for rrc, drb, rru, pee in zip(
                    rrc_conn_mean_values, 
                    drb_ue_thp_ul_values, 
                    rru_prb_used_ul_values, 
                    pee_avg_power_values
                )
            ]
        ]

        json_data = {"signature_name": "serving_default", "instances": instances}
        logger.info(f'Generated JSON data: {json_data}')
        return json_data
    # Mapping CellID and Cell name
    def mapping(self, data):
        data[['S', 'B', 'C']] = data['CellID'].str.extract(r'S(\d+)/[BN](\d+)/C(\d+)')
        data[['S', 'B', 'C']] = data[['S', 'B', 'C']].astype(int)
        data = data.sort_values(by=['B', 'S', 'C'])
        data['cellidnumber'] = data.groupby(['B', 'S', 'C']).ngroup().add(1)
        data = data.drop(['S', 'B', 'C'], axis=1)
        return data


    def check_and_perform_action(self, data):
        response_obj = json.loads(data)
        predictions = response_obj.get('predictions')
        if predictions:
            for prediction in predictions:
                if all(pred < 0.04 for pred in prediction):
                    return True
            return False


if __name__ == "__main__":
    rapp = ESrapp()

    logger.debug("ES xApp starting")


    rapp.entry()
