import time
import logging
import sys
from data import DATABASE
from nectconfclient import NETCONFCLIENT
import json


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


class ESrapp():
    def __init__(self):
        """
        Initialize the rApp runtime, data sources, and policy manager.
        """

        #super().__init__()
        self.db = DATABASE()
        self.db.connect()
        self.threshold = 50
        self.netconf=NETCONFCLIENT()
        self.index = 1

    def entry(self):
        """
        Start the loop that periodically runs inference.
        """
        while True:
            self.inference()
            time.sleep(60)

    # Send data to ML rApp
    def inference(self):
        """
        Evaluate KPI data and trigger NETCONF updates for target cells.
        """
        try:
            action_cells = []
            cell_map = self.db.get_cell_ID_map()
            if cell_map is None:
                logger.error("get_cell_ID_map returned None")
                return
            if not cell_map:
                logger.warning("No cell ID mapping found, skipping inference.")
                return
            for cell_name, cell_id in cell_map.items():
                data = self.db.get_mean_metric_value([cell_name])
                if not data:
                    logger.debug("No KPI data returned for %s", cell_name)
                    continue
                if data.get("RRU.PrbUsedUl", float("inf")) < self.threshold:
                    logger.info(
                        "Cell %s has RRU.PrbUsedUl value %s below threshold %s.",
                        cell_name,
                        data["RRU.PrbUsedUl"],
                        self.threshold,
                    )
                    cell_number = cell_name.split("S")[-1].split("/")[0]
                    logger.info("Extracted cell number: %s", cell_number)
                    action_cells.append(cell_number)
                    time.sleep(3)
                    self.netconf.network_config_update_netconf(action_cells)
        except Exception:
            logger.exception("Inference cycle failed")


if __name__ == "__main__":
    rapp = ESrapp()
    logger.debug("ES xApp starting")
    rapp.entry()
