# OSC Non-RT RIC Energy Saving rAPP

## Outline

- [Energy Saving (ES) rApp Documentation](https://github.com/bmw-ece-ntust/energy-saving-simple-usecase/edit/master/README.md)
  - Energy Saving (ES) rApp
- [RIC Test](https://github.com/bmw-ece-ntust/energy-saving-simple-usecase/edit/master/README.md#ric-test)
  - RIC Test & [I]SMO Integration (O1-Ves)
  - RIC Test Netconf Test
  - Cell on/off Scenario
- [Compal gNB](https://github.com/bmw-ece-ntust/energy-saving-simple-usecase/edit/master/README.md#compal-gnb)
  - Compal gNB - O1 VES Test
  - Compal gNB - O1 Netconf Test
- [Installation Guide](https://github.com/bmw-ece-ntust/energy-saving-simple-usecase/edit/master/README.md#installation-guide)
  - [I release] SMO Deployment
  - [I release] Install Non-RT RIC
  - rApp Manager Introduction
- [ML rApp](https://github.com/bmw-ece-ntust/energy-saving-simple-usecase/edit/master/README.md#ml-rapp)
  - ML rApp Overview
  - rApp Manager User Guide
- [Architecture](https://github.com/bmw-ece-ntust/energy-saving-simple-usecase/edit/master/README.md#architecture)
- [I/O Parameters Table](https://github.com/bmw-ece-ntust/energy-saving-simple-usecase/edit/master/README.md#io-parameters-table)
  - ES rApp I/O Parameters
    - Input Parameters
    - Output Parameters
  - ML rApp I/O Parameters
    - Input Parameters
    - Output Parameters
  - Summary

## Energy Saving (ES) rApp

- [ES rApp](https://github.com/bmw-ece-ntust/energy-saving-simple-usecase/tree/master/ES%20rApp)

## RIC Test

- [RIC Test & [I]SMO Integration(O1-Ves)](https://hackmd.io/@Winnie27/r1uReJjxp)
- [RIC Test Netconf test](https://hackmd.io/@Winnie27/r1BajOitT)
- [Cell on/off Scenario](https://hackmd.io/@Winnie27/rkltXnp1T)

## Compal gNB

- [Compal gNB - O1 VES test](https://hackmd.io/@Winnie27/rJZXQBxmC)
- [Compal gNB - O1 Netconf test](https://hackmd.io/@Winnie27/rJu88bff0)

## Installation guide

- [[I release] SMO Deployment](https://hackmd.io/@H131413/ByOoZCmDa)
- [[I release] Install Non-RT RIC](https://hackmd.io/@Winnie27/B1hE7bwBp)
- [rApp Manager introduction](https://hackmd.io/@Winnie27/Bk6xb7EBT)

## ML rApp

- [ML rApp](https://github.com/bmw-ece-ntust/energy-saving-simple-usecase/tree/master/ML%20rApp)
- [rApp Manager user guide](https://hackmd.io/@Winnie27/rJjXkxatp)

## Architecture

![image](https://github.com/user-attachments/assets/865db5d3-8217-42a7-af6f-0d34578d9ccc)

## [I/O Parameters Table](https://hackmd.io/EOb2BReXTpeOQ6wXwflPFA?view#IO-Parameters-Table)

### ES rApp I/O Parameters

**Desrciption:** These parameters are used to run the ES algorithm and output the target cell ID for shutting down the selected cell.

- Input

| Description                                                                                    | Target Entity | [3GPP TS 28.552 v17.6.0](https://portal.3gpp.org/desktopmodules/Specifications/SpecificationDetails.aspx?specificationId=3413) index | 3GPP         | [VIAVI](https://drive.google.com/file/d/1-1XJGd6pl0W2EnxBbraI_mbzAObB0C1n/view?usp=sharing) | ns-3       | OSC O1            |
| ---------------------------------------------------------------------------------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ------------ | ------------------------------------------------------------------------------------------- | ---------- | ----------------- |
| Average downlink throughput (in Gbp)                                                           | Cell, UE, QoS | 5.1.1.3.1                                                                                                                            | DRB_UEThpDl  |                                                                                             | throughput | DL_throughput     |
| Average power consumed over the measurement period (in watts, W)                               | Cell          | 5.1.1.19.2.1                                                                                                                         | PEE.AvgPower |                                                                                             | (TBD.)     | pmPowerConsumed   |
| Total usage (in percentage) of Physical Resource Blocks (PRBs) on the downlink for any purpose | Cell, mMIMO   | 5.1.1.2.1                                                                                                                            | RRU_PrbTotDl |                                                                                             | (TBD.)     | pmPdschPrbUsageDL |
| Cell's or UE serving cell's "localCellId"                                                      | UE            |                                                                                                                                      | -            | Viavi_Cell_id                                                                               | ap_id      | gNBDUId           |

- Output

| KPI/Measurement Name | Target Entity | Description                               | Defined by (3GPP TS 28.552 v17.6.0 / VIAVI) |
| -------------------- | ------------- | ----------------------------------------- | ------------------------------------------- |
| Viavi_Cell_id        | UE            | Cell's or UE serving cell's "localCellId" | VIAVI proprietary                           |

### ML rApp I/O Parameters

**Desrciption:** The ML rApp utilizes input parameters to predict future cell throughput. Its outputs include both the target cell ID and the predicted throughput value, enabling informed decisions for network optimization.

- Input
  
| KPI/Measurement Name | Target Entity | Description                                                                                    | Defined by (3GPP TS 28.552 v17.6.0 / VIAVI) |
| -------------------- | ------------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------- |
| DRB_UEThpDl          | Cell, UE, QoS | Average downlink throughput (in Gbp)                                                           | 3GPP TS 28.552 v17.6.0 5.1.1.3.1            |
| Viavi_Cell_id        | UE            | Cell's or UE serving cell's "localCellId"                                                      | VIAVI proprietary                           |
| PEE.AvgPower         | Cell          | Average power consumed over the measurement period (in watts, W)                               | 3GPP TS 28.552 v17.6.0 5.1.1.19.2.1         |
| RRU_PrbTotDl         | Cell, mMIMO   | Total usage (in percentage) of Physical Resource Blocks (PRBs) on the downlink for any purpose | 3GPP TS 28.552 v17.6.0 5.1.1.2.1            |

- Output

| KPI/Measurement Name | Target Entity | Description                               | Defined by (3GPP TS 28.552 v17.6.0 / VIAVI) |
| -------------------- | ------------- | ----------------------------------------- | ------------------------------------------- |
| Viavi_Cell_id        | UE            | Cell's or UE serving cell's "localCellId" | VIAVI proprietary                           |
| DRB_UEThpDl          | Cell, UE, QoS | Average downlink throughput (in Gbp)      | 3GPP TS 28.552 v17.6.0 5.1.1.3.1            |

### Summary

The ES rApp runs an energy-saving algorithm based on input parameters and outputs a cell ID to turn off cells with low load, achieving energy savings. In contrast, the ML rApp uses input parameters to predict the future cell throughput, with the output including the cell ID and the predicted throughput value.
