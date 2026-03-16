import time
import pandas as pd
from configparser import ConfigParser
import logging
import os
import influxdb_client
import yaml

from influxdb import DataFrameClient
from influxdb.exceptions import InfluxDBClientError, InfluxDBServerError
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.warnings import MissingPivotFunction
from requests.exceptions import RequestException, ConnectionError

logger = logging.getLogger(__name__)

class DATABASE(object):
    
    def __init__(self):
        """
        Initialize database settings and load configuration.
        """
        self.meas = None
        self.org = None
        self.bucket = None
        self.address = None
        self.cell_name_ID_map = {}
        self.config()

    # Connect with influxdb
    def connect(self):
        """
        Connect to InfluxDB using the configured endpoint and token.
        Returns:
            bool: True when connected successfully, otherwise False.
        """
        if self.client is not None:
            self.client.close()
        try:
            self.client = influxdb_client.InfluxDBClient(url=self.address, org=self.org, token=self.token)
            version = self.client.version()
            logger.info("Connected to Influx Database, InfluxDB version : {}".format(version))
            return True

        except (RequestException, InfluxDBClientError, InfluxDBServerError, ConnectionError):
            logger.error("Failed to establish a new connection with InflulxDB, Please check your url/hostname")
            time.sleep(120)

    def get_cell_ID_map(self):
        """
        Retrieve the mapping of cell names to cell IDs from InfluxDB.
        Returns:
            timestamp: The timestamp of the newest data point.
        """
        query = f"""
        from(bucket: "O1PM")
        |> range(start: start: -1m)
        |> filter(fn: (r) => r["_measurement"] == "CellReports")
        |> filter(fn: (r) => r["_field"] == "Viavi.Cell.Name")
        |> last()
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
        """
        result = self.read_data(self.org, query)
        # print(result)
        global cell_name_ID_map
        cell_name_ID_map = {}
        timestamp = None
        if isinstance(result, pd.DataFrame) and not result.empty:
            if isinstance(result, pd.DataFrame):
                # Get data's timestamp
                result['_time'] = pd.to_datetime(result['_time'])
                query_time = result['_time'].iloc[0]
                timestamp = int(query_time.timestamp()) if query_time is not None else None
                logger.debug("Newest Data Timestamp:", query_time.strftime('%Y-%m-%dT%H:%M:%SZ'), "timestamp:", timestamp)

                # Filter rows where 'CellID' contains 'NrCellDu'
                filtered = result[result['CellID'].str.contains('NrCellDu', na=False)]
                # print(filtered)
                for _, row in filtered.iterrows():
                    cell_name = row['Viavi.Cell.Name']
                    cell_id = row['CellID']
                    cell_name_ID_map[cell_name] = cell_id
                # print(cell_name_ID_map)
            # logger.info(f"Retrieved {cell_name_ID_map} cell name-ID mappings from InfluxDB.")
        return timestamp

    # Query information
    def read_data(self, cell_list):
        """
        Query mean KPI values for the provided cell list.

        Args:
            cell_list (list[str]): Cell names to query.

        Returns:
            dict: KPI name to aggregated value mapping.
        """
        self.data = None
        cell_ids = [cell_name_ID_map[cell] for cell in cell_list if cell in cell_name_ID_map]
        cell_ids_filter = " or ".join([f'r["CellID"] == "{cell_id}"' for cell_id in cell_ids])
        # Retrieve mean KPI values for specified cells from InfluxDB.
        query = f"""
            from(bucket: "{self.bucket}")
                |> range(start: -1m)
                |> filter(fn: (r) => r["_measurement"] == "{self.meas}")
                |> filter(fn: (r) => {cell_ids_filter})
                |> filter(fn: (r) => r["_field"] == "DRB.UEThpUl" or r["_field"] == "RRU.PrbUsedUl" or r["_field"] == "PEE.AvgPower") '
                |> mean()
                |> group(columns: ["_field"])
                |> sum()
        """
        result = self.read_data(self.org, query)
        return{row['_field']: row['_value'] for _, row in result.iterrows()}

    def config(self):
        """
        Load configuration from config.yaml or fall back to config.ini.
        """
        if os.path.exists("config.yaml"):
            with open("config.yaml", "r", encoding="utf-8") as file_handle:
                data = yaml.safe_load(file_handle) or {}
            influx_cfg = data.get("influxdb", {})
            self.host = influx_cfg.get("host", self.host)
            self.port = str(influx_cfg.get("port", self.port))
            self.user = influx_cfg.get("user", self.user)
            self.password = influx_cfg.get("password", self.password)
            self.ssl = self._parse_bool(influx_cfg.get("ssl"), self.ssl)
            self.dbname = influx_cfg.get("database", self.dbname)
            self.meas = influx_cfg.get("measurement", self.meas)
            self.token = influx_cfg.get("token", self.token)
            self.org = influx_cfg.get("org", self.org)
            self.bucket = influx_cfg.get("bucket", self.bucket)
            self.address = influx_cfg.get("address", self.address)
            return
        logger.warning("config.yaml not found, falling back to config.ini")
        cfg = ConfigParser()
        cfg.read("config.ini")
        for section in cfg.sections():
            if section == "influxdb":
                self.host = cfg.get(section, "host")
                self.port = cfg.get(section, "port")
                self.user = cfg.get(section, "user")
                self.password = cfg.get(section, "password")
                self.ssl = cfg.get(section, "ssl")
                self.dbname = cfg.get(section, "database")
                self.meas = cfg.get(section, "measurement")
                self.token = cfg.get(section, "token")
                self.org = cfg.get(section, "org")
                self.bucket = cfg.get(section, "bucket")
                self.address = cfg.get(section, "address")

    def _parse_bool(self, value, default):
        """
        Parse a boolean-like value with a fallback default.

        Args:
            value: The input value to parse.
            default (bool): Value to return when parsing fails.

        Returns:
            bool: Parsed boolean value.
        """
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.strip().lower() in ("true", "1", "yes", "y")
        return default

