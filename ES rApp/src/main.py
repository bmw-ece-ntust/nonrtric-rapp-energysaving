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
        """
        Initialize the rApp runtime, data sources, and policy manager.
        """

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
        """
        Start the scheduler loop that periodically runs inference.
        """
        schedule.every(1).minute.do(self.inference)

        while True:
            schedule.run_pending()

    # Send data to ML rApp
    def inference(self):
        """
        Evaluate KPI data and trigger NETCONF updates for target cells.
        """
        action_cells = []
        self.db.get_cell_ID_map()
        for cell_name, cell_id in self.db.cell_name_ID_map.items():
            data = self.db.read_data([cell_name])
            if data["RRU.PrbUsedUl"] < self.threshold:
                logger.info(f"Cell {cell_name} has RRU.PrbUsedUl value {data['RRU.PrbUsedUl']} below threshold {self.threshold}.")
                cell_number = cell_name.split("S")[-1].split("/")[0]
                logger.info(f"Extracted cell number: {cell_number}")
                action_cells.append(cell_number)
                time.sleep(3)
                self.netconf.network_config_update_netconf(action_cells)


if __name__ == "__main__":
    rapp = ESrapp()
    logger.debug("ES xApp starting")
    rapp.entry()
