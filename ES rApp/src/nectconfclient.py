import requests
import logging
from ncclient import manager
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)

class NETCONFCLIENT():

    def convert_to_xml(self, index):
        root = ET.Element("config", xmlns="urn:ietf:params:xml:ns:netconf:base:1.0")
        managed_element = ET.SubElement(root, "ManagedElement", xmlns="urn:3gpp:sa5:_3gpp-common-managed-element")
        id_element = ET.SubElement(managed_element, "id")
        id_element.text = "1193046"
        gnb_ucp_function = ET.SubElement(managed_element, "GNBCUCPFunction", xmlns="urn:3gpp:sa5:_3gpp-nr-nrm-gnbcucpfunction")
        id_element = ET.SubElement(gnb_ucp_function, "id")
        id_element.text = "1"
        nr_cell_cu = ET.SubElement(gnb_ucp_function, "NRCellCU", xmlns="urn:3gpp:sa5:_3gpp-nr-nrm-nrcellcu")
        id_element = ET.SubElement(nr_cell_cu, "id")
        id_element.text = str(index)
        ces_management_function = ET.SubElement(nr_cell_cu, "CESManagementFunction", xmlns="urn:3gpp:sa5:_3gpp-nr-nrm-cesmanagementfunction")
        id_element = ET.SubElement(ces_management_function, "id")
        id_element.text = str(index)
        attributes = ET.SubElement(ces_management_function, "attributes")
        energy_saving_control = ET.SubElement(attributes, "energySavingControl")
        energy_saving_control.text = "toBeEnergySaving"
        energy_saving_state = ET.SubElement(attributes, "energySavingState")
        energy_saving_state.text = "isNotEnergySaving"
        return ET.tostring(root, encoding="unicode")

    def perform_action(self, index):
        xml_data = self.convert_to_xml(index)
        with manager.connect(host="192.168.8.28", port=31383, username="root", password="viavi", hostkey_verify=False) as m:
            try:
                edit_response = m.edit_config(target="running", config=xml_data)
                logger.info(f"Successfully turn off the cell")
            except Exception as e:
                logger.error(f"Failed to turn off the cell: {str(e)}")

    def convert_to_xml_1(self, index):
        root = ET.Element("config", xmlns="urn:ietf:params:xml:ns:netconf:base:1.0")
        managed_element = ET.SubElement(root, "ManagedElement", xmlns="urn:3gpp:sa5:_3gpp-common-managed-element")
        id_element = ET.SubElement(managed_element, "id")
        id_element.text = "1193046"
        gnb_ucp_function = ET.SubElement(managed_element, "GNBCUCPFunction", xmlns="urn:3gpp:sa5:_3gpp-nr-nrm-gnbcucpfunction")
        id_element = ET.SubElement(gnb_ucp_function, "id")
        id_element.text = "1"
        nr_cell_cu = ET.SubElement(gnb_ucp_function, "NRCellCU", xmlns="urn:3gpp:sa5:_3gpp-nr-nrm-nrcellcu")
        id_element = ET.SubElement(nr_cell_cu, "id")
        id_element.text = str(index)
        ces_management_function = ET.SubElement(nr_cell_cu, "CESManagementFunction", xmlns="urn:3gpp:sa5:_3gpp-nr-nrm-cesmanagementfunction")
        id_element = ET.SubElement(ces_management_function, "id")
        id_element.text = str(index)
        attributes = ET.SubElement(ces_management_function, "attributes")
        energy_saving_control = ET.SubElement(attributes, "energySavingControl")
        energy_saving_control.text = "toBeNotEnergySaving"
        energy_saving_state = ET.SubElement(attributes, "energySavingState")
        energy_saving_state.text = "isNotEnergySaving"
        return ET.tostring(root, encoding="unicode")

    def perform_action_1(self, index):
        xml_data = self.convert_to_xml_1(index)
        with manager.connect(host="192.168.8.28", port=31383, username="root", password="viavi", hostkey_verify=False) as m:
            try:
                edit_response = m.edit_config(target="running", config=xml_data)
                logger.info(f"Successfully turn on the cell")
            except Exception as e:
                logger.error(f"Failed to turn on the cell: {str(e)}")