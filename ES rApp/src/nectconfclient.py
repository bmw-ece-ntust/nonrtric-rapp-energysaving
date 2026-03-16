import logging
import os
from ncclient import manager
import xml.etree.ElementTree as ET
import yaml
from configparser import ConfigParser


logger = logging.getLogger(__name__)

class NETCONFCLIENT():
    def __init__(self):
        """
        Initialize the O1Netconf connection details.

        Args:
            host (str): The device IP address or hostname.
            port (int): The NETCONF port.
            username (str): The username for authentication.
            password (str): The password for authentication.
            timeout (int): The connection timeout in seconds.
            hostkey_verify (bool): Whether to verify the host key.
        """
        self.host = None
        self.port = None
        self.username = None
        self.password = None
        self.timeout = None
        self.hostkey_verify = None
        self.session = None
        self.config()
        self.connect()

    def connect(self):
        """
        Establish the NETCONF connection to the device.
        Returns:
            bool: True if connection is successful, False otherwise.
        """
        if self.session and self.session.connected:
            logger.info("Already connected.")
            return True
        try:
            logger.info(f"Connecting to {self.host}:{self.port}...")
            self.session = manager.connect(
                host=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                timeout=self.timeout,
                hostkey_verify=self.hostkey_verify,
                allow_agent=False,
                look_for_keys=False
            )
            logger.info(f"Connection successful. Session ID: {self.session.session_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to {self.host}:{self.port}. Error: {e}")
            self.session = None
            return False

    def network_config_update_netconf(self, cell_list):
        """
        Update the network configuration based on the provided action data.
        Args:
            action_data (dict): The action data containing configuration updates.
            netconf_handler: The NETCONF interface handler.
        """
        for cell in cell_list:
            energy_saving_xml = ""
            control_xml = f"""
<config xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
    <ManagedElement xmlns="urn:3gpp:sa5:_3gpp-common-managed-element">
    <id>1193046</id>
    <GNBCUCPFunction xmlns="urn:3gpp:sa5:_3gpp-nr-nrm-gnbcucpfunction">
        <id>1</id>
{{}}    </GNBCUCPFunction>
    </ManagedElement>
</config>
"""
            energy_saving_xml = energy_saving_xml + f"""        <NRCellCU xmlns="urn:3gpp:sa5:_3gpp-nr-nrm-nrcellcu">
            <id>{cell}</id>
            <CESManagementFunction xmlns="urn:3gpp:sa5:_3gpp-nr-nrm-cesmanagementfunction">
                <id>{cell}</id>
                <attributes>
                    <energySavingControl>toBeEnergySaving</energySavingControl>
                </attributes>
            </CESManagementFunction>
        </NRCellCU>
"""
            logger.info(f"Network configuration updated for Cell {cell} off")
            logger.debug(f"Generated NETCONF XML:\n{control_xml.format(energy_saving_xml)}")
            self.edit_config(control_xml.format(energy_saving_xml))

    def edit_config(self, config_data, target="running", default_operation="merge"):
        """
        Edit the configuration on the device.

        Args:
            config_data (str): The configuration to apply, in XML format.
            target (str): The target configuration datastore (e.g., "running").
            default_operation (str): The default operation (e.g., "merge", "replace").

        Returns:
            The result of the edit operation, or None on failure.
        """
        if not self.session or not self.session.connected:
            logger.error("Not connected. Please call connect() first.")
            return None
        try:
            logger.info(f"Applying configuration to '{target}' datastore...")
            return self.session.edit_config(target=target, config=config_data, default_operation=default_operation)
        except Exception as e:
            logger.error(f"Failed to edit configuration: {e}")
            return None

    def config(self):
        """
        Load NETCONF connection settings from config.yaml or config.ini.
        """
        if os.path.exists("config.yaml"):
            with open("config.yaml", "r", encoding="utf-8") as file_handle:
                data = yaml.safe_load(file_handle) or {}
            netconf_cfg = data.get("netconf", {})
            self.host = netconf_cfg.get("host", self.host)
            self.port = netconf_cfg.get("port", self.port)
            self.username = netconf_cfg.get("user", self.username)
            self.password = netconf_cfg.get("password", self.password)
            self.timeout = netconf_cfg.get("timeout", self.timeout)
            self.hostkey_verify = netconf_cfg.get("hostkey_verify", self.hostkey_verify)
            return
        
        logger.warning("config.yaml not found, falling back to config.ini")
        cfg = ConfigParser()
        cfg.read("config.ini")
        for section in cfg.sections():
            if section == "netconf":
                self.host = cfg.get(section, "host")
                self.port = cfg.get(section, "port")
                self.username = cfg.get(section, "user")
                self.password = cfg.get(section, "password")
                self.timeout = cfg.get(section, "timeout")
                self.hostkey_verify = cfg.get(section, "hostkey_verify")