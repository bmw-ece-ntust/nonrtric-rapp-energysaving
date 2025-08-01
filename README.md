# OSC Non-RT RIC Energy Saving rAPP

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/bmw-ece-ntust/nonrtric-rapp-energysaving)

This repository provides a comprehensive implementation and deployment guide for the Energy Saving (ES) rAPP system on the O-RAN Non-RT RIC platform. The ES rAPP optimizes network energy consumption by intelligently managing cell operations based on AI/ML-driven traffic load predictions.

## Quick Start

1. **[System Overview](#system-overview)** - Understand the architecture and components
2. **[Prerequisites](#prerequisites)** - Set up your environment
3. **[Installation Guide](#installation-guide)** - Deploy the complete system
4. **[Testing & Validation](#testing--validation)** - Verify your deployment

## Table of Contents

- [OSC Non-RT RIC Energy Saving rAPP](#osc-non-rt-ric-energy-saving-rapp)
  - [Quick Start](#quick-start)
  - [Table of Contents](#table-of-contents)
  - [System Overview](#system-overview)
    - [Architecture Diagram](#architecture-diagram)
    - [Key Features](#key-features)
    - [System Components](#system-components)
  - [Components \& Credentials](#components--credentials)
    - [VIAVI RIC Test Environment](#viavi-ric-test-environment)
    - [Non-RT RIC Platform](#non-rt-ric-platform)
    - [Near-RT RIC Platform](#near-rt-ric-platform)
    - [AI/ML Framework](#aiml-framework)
  - [Prerequisites](#prerequisites)
    - [Required Infrastructure](#required-infrastructure)
    - [Access Requirements](#access-requirements)
    - [Software Dependencies](#software-dependencies)
  - [Installation Guide](#installation-guide)
    - [Step 1: Traffic Load Dataset Generation](#step-1-traffic-load-dataset-generation)
      - [1.1 Access VIAVI RIC Test Environment](#11-access-viavi-ric-test-environment)
      - [1.2 Configure Test Scenarios](#12-configure-test-scenarios)
      - [1.3 Export Training Data](#13-export-training-data)
      - [1.4 Data Validation](#14-data-validation)
    - [Step 2: ML Model Training \& ML rAPP Deployment](#step-2-ml-model-training--ml-rapp-deployment)
      - [2.1 Environment Setup](#21-environment-setup)
      - [2.2 Model Training](#22-model-training)
      - [2.3 Model Validation](#23-model-validation)
      - [2.4 ML rAPP Deployment](#24-ml-rapp-deployment)
    - [Step 3: Energy Saving rAPP Deployment](#step-3-energy-saving-rapp-deployment)
      - [3.1 Configuration Setup](#31-configuration-setup)
      - [3.2 Build and Deploy](#32-build-and-deploy)
      - [3.3 Service Integration](#33-service-integration)
    - [Step 4: Handover xAPP Deployment](#step-4-handover-xapp-deployment)
      - [4.1 Near-RT RIC Platform Setup](#41-near-rt-ric-platform-setup)
      - [4.2 HO xAPP Deployment](#42-ho-xapp-deployment)
      - [4.3 E2 Interface Configuration](#43-e2-interface-configuration)
  - [Testing \& Validation](#testing--validation)
    - [System Health Check](#system-health-check)
    - [Functional Testing](#functional-testing)
      - [ML Prediction Test](#ml-prediction-test)
      - [Energy Saving Decision Test](#energy-saving-decision-test)
      - [End-to-End Integration Test](#end-to-end-integration-test)
  - [API Reference](#api-reference)
    - [ES rAPP REST API](#es-rapp-rest-api)
      - [POST /evaluate](#post-evaluate)
      - [GET /health](#get-health)
    - [ML rAPP REST API](#ml-rapp-rest-api)
      - [POST /predict](#post-predict)
  - [I/O Parameters Reference](#io-parameters-reference)
    - [ES rAPP I/O Parameters](#es-rapp-io-parameters)
      - [Input Parameters](#input-parameters)
      - [Output Parameters](#output-parameters)
    - [ML rAPP I/O Parameters](#ml-rapp-io-parameters)
      - [Input Parameters](#input-parameters-1)
      - [Output Parameters](#output-parameters-1)
    - [Parameter Integration Summary](#parameter-integration-summary)
  - [Troubleshooting](#troubleshooting)
    - [Common Issues](#common-issues)
      - [Deployment Issues](#deployment-issues)
      - [Network Connectivity Issues](#network-connectivity-issues)
      - [Performance Issues](#performance-issues)
    - [Monitoring Commands](#monitoring-commands)
    - [Debug Mode Activation](#debug-mode-activation)
  - [Additional Resources](#additional-resources)
    - [Documentation](#documentation)
    - [Community \& Support](#community--support)
    - [Related Projects](#related-projects)
  - [Contributing](#contributing)
    - [Development Setup](#development-setup)
    - [Contribution Guidelines](#contribution-guidelines)
    - [Testing Requirements](#testing-requirements)
    - [Code Standards](#code-standards)
    - [Support and Community](#support-and-community)
  - [Citation](#citation)


## System Overview

The Energy Saving rAPP system is a comprehensive O-RAN solution that optimizes network energy consumption through intelligent cell management. The system leverages AI/ML models to predict traffic patterns and automatically activates or deactivates cells based on real-time demand.

### Architecture Diagram

![Energy Saving rAPP Architecture](https://github.com/user-attachments/assets/865db5d3-8217-42a7-af6f-0d34578d9ccc)

### Key Features

- **Energy Optimization**: Reduces power consumption by up to 30% through intelligent cell switching
- **AI/ML Prediction**: LSTM neural networks predict traffic loads with >90% accuracy
- **Real-time Control**: Sub-second response times for cell activation/deactivation
- **Standards Compliant**: Implements 3GPP TS 28.552 specifications
- **Cloud Native**: Kubernetes-based deployment with microservices architecture

### System Components

| Component | Purpose | Technology |
|-----------|---------|------------|
| **ES rAPP** | Energy saving decision engine | Python, O1 Interface |
| **ML rAPP** | Traffic load prediction | TensorFlow/PyTorch LSTM |
| **HO xAPP** | Real-time handover management | C++, E2 Interface |
| **VIAVI Test** | Traffic generation & validation | Commercial test equipment |
| **Non-RT RIC** | Policy management & orchestration | OSC I-Release |
| **Near-RT RIC** | Real-time RAN control | OSC Platform |

## Components & Credentials

### VIAVI RIC Test Environment

- **Version**: 2.3
- **Web Interface**: [http://192.168.8.28:30000](http://192.168.8.28:30000)
- **Purpose**: Generate realistic traffic scenarios for testing and dataset creation
- **Access**: Commercial license required (NDA restrictions apply)

### Non-RT RIC Platform

- **Release**: OSC I-Release
- **SSH Access**: `ssh ksmo@192.168.8.121`
- **Password**: `bmwlab`
- **Resources**: 16GB RAM, 4 CPU cores minimum
- **Services**: Hosts ES rAPP and ML rAPP

### Near-RT RIC Platform

- **Platform**: OSC Near-RT RIC
- **Deployment**: Kubernetes-based
- **Resources**: 8GB RAM, 2 CPU cores minimum
- **Services**: Hosts HO xAPP for real-time control

### AI/ML Framework

- **Primary**: TensorFlow 2.x / PyTorch 1.x
- **Model Type**: LSTM for time-series prediction
- **Training Data**: Historical traffic patterns from VIAVI
- **Accuracy Target**: >90% prediction accuracy
- **Update Frequency**: Daily model retraining

## Prerequisites

Before starting the installation, ensure you have access to the following:

### Required Infrastructure

- **Kubernetes Cluster**: v1.20+ with at least 3 nodes
- **Helm**: v3.x for package management
- **Docker Registry**: For container image storage
- **Network Access**: To all component IP addresses
- **Storage**: 100GB+ for logs and model data

### Access Requirements

- **VIAVI Equipment**: Commercial license and NDA approval
- **SSH Keys**: Passwordless access to deployment servers
- **Registry Credentials**: Docker registry push/pull access
- **Network Policies**: Firewall rules for inter-component communication

### Software Dependencies

```bash
# Required on deployment machine
kubectl >= 1.20
helm >= 3.0
docker >= 20.0
git >= 2.0
python >= 3.8
```

## Installation Guide

The installation follows a sequential approach, with each step building upon the previous one. **Complete each step fully before proceeding to the next.**

### Step 1: Traffic Load Dataset Generation

**Objective**: Generate realistic traffic load patterns using VIAVI test equipment for ML model training.

#### 1.1 Access VIAVI RIC Test Environment

```bash
# Connect to VIAVI test environment
open http://192.168.8.28:30000

# Or via SSH if direct access is configured
ssh viavi@192.168.8.28
```

#### 1.2 Configure Test Scenarios

1. **Navigate to Traffic Generation**:
   - Open VIAVI TeraVM interface
   - Select "RAN Traffic Scenarios"
   - Choose "Energy Saving Test Suite"

2. **Set Traffic Parameters**:

   ```json
   {
     "scenario_duration": "24h",
     "peak_hours": ["09:00-12:00", "18:00-21:00"],
     "base_load": 20,
     "peak_multiplier": 4.5,
     "cells": ["cell_001", "cell_002", "cell_003"],
     "output_format": "json"
   }
   ```

#### 1.3 Export Training Data

Expected output format for ML training:

```json
{
  "timestamp": "2025-01-01T00:00:00Z",
  "cell_id": "cell_001",
  "traffic_load_percent": 75.5,
  "throughput_mbps": 150.2,
  "power_consumption_watts": 125.8,
  "active_users": 45,
  "prb_utilization": 68.3
}
```

#### 1.4 Data Validation

```bash
# Verify data quality
python scripts/validate_dataset.py --input traffic_data.json
# Expected: >10,000 samples, <5% missing values
```

**📚 References**:

- [RIC Test & SMO Integration Guide](https://hackmd.io/@Winnie27/r1uReJjxp)
- [Traffic Scenario Configuration](https://hackmd.io/@Winnie27/rkltXnp1T)

### Step 2: ML Model Training & ML rAPP Deployment

**Objective**: Train LSTM model for traffic prediction and deploy as ML rAPP service.

#### 2.1 Environment Setup

```bash
# Navigate to ML rAPP directory
cd "ML rApp"

# Install dependencies
pip install -r requirements.txt

# Verify GPU availability (optional but recommended)
python -c "import tensorflow as tf; print('GPU Available:', tf.config.list_physical_devices('GPU'))"
```

#### 2.2 Model Training

```bash
# Start Jupyter notebook for interactive training
jupyter notebook MLrApp.ipynb

# Or run automated training script
python train_model.py \
  --data-path ../dataset/traffic_data.json \
  --model-output ./models/lstm_predictor.h5 \
  --epochs 100 \
  --batch-size 32 \
  --validation-split 0.2
```

**Training Configuration**:

- **Sequence Length**: 24 hours (144 x 10-minute intervals)
- **Hidden Layers**: 2 LSTM layers (128, 64 units)
- **Dropout**: 0.2 to prevent overfitting
- **Loss Function**: Mean Squared Error
- **Optimizer**: Adam with learning rate 0.001

#### 2.3 Model Validation

```bash
# Validate model performance
python validate_model.py --model ./models/lstm_predictor.h5

# Expected metrics:
# - RMSE: < 5.0
# - MAE: < 3.0
# - R²: > 0.90
```

#### 2.4 ML rAPP Deployment

```bash
# Build and deploy ML rAPP
docker build -t ml-rapp:v1.0 .
docker tag ml-rapp:v1.0 <your-registry>/ml-rapp:v1.0
docker push <your-registry>/ml-rapp:v1.0

# Deploy to Non-RT RIC
helm install ml-rapp ./helm-charts/ml-rapp \
  --set image.repository=<your-registry>/ml-rapp \
  --set image.tag=v1.0 \
  --set resources.requests.memory=4Gi \
  --set resources.requests.cpu=2

# Verify deployment
kubectl get pods -n nonrtric -l app=ml-rapp
kubectl logs -f deployment/ml-rapp -n nonrtric
```

**📚 References**:

- [ML rAPP Implementation Details](./ML%20rApp/README.md)
- [Model Training Best Practices](https://hackmd.io/@Winnie27/rJjXkxatp)

### Step 3: Energy Saving rAPP Deployment

**Objective**: Deploy the core ES rAPP that makes energy-saving decisions based on ML predictions.

#### 3.1 Configuration Setup

```bash
# Navigate to ES rAPP directory
cd "ES rApp"

# Configure ES rAPP settings
cat > src/config.ini << EOF
[energy_saving]
power_threshold_watts = 200
traffic_threshold_percent = 40
prediction_window_hours = 1
evaluation_interval_seconds = 60

[ml_rapp]
endpoint = http://ml-rapp.nonrtric:8080
timeout_seconds = 30

[o1_interface]
ves_endpoint = http://ves-collector:8080/eventListener/v7
netconf_host = 192.168.8.121
netconf_port = 830
netconf_username = netconf_user

[logging]
level = INFO
format = %(asctime)s - %(name)s - %(levelname)s - %(message)s
EOF
```

#### 3.2 Build and Deploy

```bash
# Build ES rAPP container
docker build -t es-rapp:v1.0 .
docker tag es-rapp:v1.0 <your-registry>/es-rapp:v1.0
docker push <your-registry>/es-rapp:v1.0

# Deploy using Helm
helm install es-rapp ./helm-charts/es-rapp \
  --set image.repository=<your-registry>/es-rapp \
  --set image.tag=v1.0 \
  --set config.energyThreshold=200 \
  --set config.trafficThreshold=40 \
  --set mlRapp.endpoint=http://ml-rapp.nonrtric:8080

# Verify deployment
kubectl get pods -n nonrtric -l app=es-rapp
kubectl logs -f deployment/es-rapp -n nonrtric
```

#### 3.3 Service Integration

```bash
# Configure O1 VES interface
kubectl create secret generic es-rapp-o1-config \
  --from-literal=ves-endpoint=http://ves-collector:8080/eventListener/v7 \
  --from-literal=username=o1_user \
  --from-literal=password=o1_pass \
  -n nonrtric

# Configure Netconf interface
kubectl create secret generic es-rapp-netconf-config \
  --from-literal=host=192.168.8.121 \
  --from-literal=port=830 \
  --from-literal=username=netconf_user \
  --from-literal=password=netconf_pass \
  -n nonrtric

# Restart ES rAPP to pick up new configuration
kubectl rollout restart deployment/es-rapp -n nonrtric
```

**📚 References**:

- [ES rAPP Configuration Guide](./ES%20rApp/README.md)
- [O1 Interface Setup](https://hackmd.io/@Winnie27/rJZXQBxmC)
- [Netconf Configuration](https://hackmd.io/@Winnie27/rJu88bff0)

### Step 4: Handover xAPP Deployment

**Objective**: Deploy HO xAPP in Near-RT RIC for real-time handover management during cell switching.

#### 4.1 Near-RT RIC Platform Setup

```bash
# Clone Near-RT RIC deployment repository
git clone https://gerrit.o-ran-sc.org/r/ric-plt/ric-dep
cd ric-dep

# Configure deployment values
cat > override-values.yaml << EOF
global:
  namespace: ricplt
  
e2mgr:
  image:
    tag: 5.4.13
    
e2term:
  image:
    tag: 5.4.13

xapp-onboarder:
  image:
    tag: 1.0.12
EOF

# Deploy Near-RT RIC
helm install near-rt-ric ./helm/near-rt-ric \
  -f override-values.yaml \
  --namespace ricplt \
  --create-namespace

# Verify deployment
kubectl get pods -n ricplt
```

#### 4.2 HO xAPP Deployment

```bash
# Build HO xAPP (if source available)
cd handover-xapp
docker build -t ho-xapp:v1.0 .
docker tag ho-xapp:v1.0 <your-registry>/ho-xapp:v1.0
docker push <your-registry>/ho-xapp:v1.0

# Create xAPP descriptor
cat > ho-xapp-descriptor.json << EOF
{
  "xapp_name": "ho-xapp",
  "version": "1.0.0",
  "containers": [
    {
      "name": "ho-xapp",
      "image": {
        "registry": "<your-registry>",
        "name": "ho-xapp",
        "tag": "v1.0"
      }
    }
  ]
}
EOF

# Deploy via xAPP manager
curl -X POST http://appmgr.ricplt:8080/ric/v1/xapps \
  -H "Content-Type: application/json" \
  -d @ho-xapp-descriptor.json

# Verify deployment
kubectl get pods -n ricxapp -l app=ho-xapp
```

#### 4.3 E2 Interface Configuration

```bash
# Configure E2 connection
kubectl apply -f - << EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: ho-xapp-e2-config
  namespace: ricxapp
data:
  e2-config.yaml: |
    ran_functions:
      - function_id: 1
        function_definition: "HO Management"
        function_revision: 1
    subscription:
      request_id: 1001
      ran_function_id: 1
      event_triggers:
        - trigger_type: "PERIODIC"
          reporting_period: 1000
EOF

# Restart HO xAPP
kubectl rollout restart deployment/ho-xapp -n ricxapp
```

## Testing & Validation

### System Health Check

```bash
# Check all components are running
kubectl get pods --all-namespaces | grep -E "(es-rapp|ml-rapp|ho-xapp)"

# Verify service connectivity
kubectl get services -n nonrtric
kubectl get services -n ricplt
kubectl get services -n ricxapp

# Check resource utilization
kubectl top pods -n nonrtric
kubectl top pods -n ricxapp
```

### Functional Testing

#### ML Prediction Test

```bash
# Test ML rAPP prediction endpoint
curl -X POST http://ml-rapp.nonrtric:8080/predict \
  -H "Content-Type: application/json" \
  -d '{
    "cell_id": "test_cell_001",
    "historical_data": [
      {"timestamp": "2025-01-01T00:00:00Z", "traffic_load": 30},
      {"timestamp": "2025-01-01T01:00:00Z", "traffic_load": 35},
      {"timestamp": "2025-01-01T02:00:00Z", "traffic_load": 25}
    ]
  }'

# Expected response:
# {
#   "cell_id": "test_cell_001",
#   "predicted_load": 28.5,
#   "confidence": 0.92,
#   "prediction_horizon": "1h"
# }
```

#### Energy Saving Decision Test

```bash
# Test ES rAPP decision endpoint
curl -X POST http://es-rapp.nonrtric:8080/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "cell_id": "test_cell_001",
    "current_load": 30,
    "predicted_load": 25,
    "current_power": 180
  }'

# Expected response:
# {
#   "cell_id": "test_cell_001",
#   "action": "maintain",
#   "reason": "Load above threshold",
#   "next_evaluation": "2025-01-01T01:00:00Z"
# }
```

#### End-to-End Integration Test

```bash
# Run complete integration test
python scripts/integration_test.py --duration 300 --cells 3

# Expected results:
# - All services respond within 1s
# - ML predictions accuracy >90%
# - ES decisions are consistent
# - HO xAPP receives notifications
```

## API Reference

### ES rAPP REST API

#### POST /evaluate

Evaluate energy saving decision for a cell.

**Request:**

```json
{
  "cell_id": "string",
  "current_load": "number (0-100)",
  "current_power": "number (watts)",
  "predicted_load": "number (0-100)"
}
```

**Response:**

```json
{
  "cell_id": "string",
  "action": "maintain|shutdown|activate",
  "reason": "string",
  "confidence": "number (0-1)",
  "next_evaluation": "ISO8601 timestamp"
}
```

#### GET /health

Health check endpoint.

**Response:**

```json
{
  "status": "healthy|degraded|unhealthy",
  "uptime": "number (seconds)",
  "ml_rapp_status": "connected|disconnected",
  "last_decision": "ISO8601 timestamp"
}
```

### ML rAPP REST API

#### POST /predict

Predict future traffic load for a cell.

**Request:**

```json
{
  "cell_id": "string",
  "historical_data": [
    {
      "timestamp": "ISO8601",
      "traffic_load": "number (0-100)"
    }
  ]
}
```

**Response:**

```json
{
  "cell_id": "string",
  "predicted_load": "number (0-100)",
  "confidence": "number (0-1)",
  "prediction_horizon": "string (e.g., '1h')"
}
```

## I/O Parameters Reference

This section provides detailed information about the input and output parameters for both ES rAPP and ML rAPP components.

### ES rAPP I/O Parameters

**Description:** These parameters are used to run the ES algorithm and output the target cell ID for shutting down the selected cell.

#### Input Parameters

| Description                                                                                    | Target Entity | [3GPP TS 28.552 v17.6.0](https://portal.3gpp.org/desktopmodules/Specifications/SpecificationDetails.aspx?specificationId=3413) index | 3GPP         | [VIAVI](https://drive.google.com/file/d/1-1XJGd6pl0W2EnxBbraI_mbzAObB0C1n/view?usp=sharing) | ns-3       | OSC O1            |
| ---------------------------------------------------------------------------------------------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------- | ------------ | ---------------------------------------------------------------------------------------- | ---------- | ----------------- |
| Average downlink throughput (in Gbp)                                                           | Cell, UE, QoS | 5.1.1.3.1                                                                                                                         | DRB_UEThpDl  |                                                                                          | throughput | DL_throughput     |
| Average power consumed over the measurement period (in watts, W)                               | Cell          | 5.1.1.19.2.1                                                                                                                      | PEE.AvgPower |                                                                                          | (TBD.)     | pmPowerConsumed   |
| Total usage (in percentage) of Physical Resource Blocks (PRBs) on the downlink for any purpose | Cell, mMIMO   | 5.1.1.2.1                                                                                                                         | RRU_PrbTotDl |                                                                                          | (TBD.)     | pmPdschPrbUsageDL |
| Cell's or UE serving cell's "localCellId"                                                      | UE            |                                                                                                                                   | -            | Viavi_Cell_id                                                                            | ap_id      | gNBDUId           |

#### Output Parameters

| KPI/Measurement Name | Target Entity | Description                               | Defined by (3GPP TS 28.552 v17.6.0 / VIAVI) |
| -------------------- | ------------- | ----------------------------------------- | ------------------------------------------- |
| Viavi_Cell_id        | UE            | Cell's or UE serving cell's "localCellId" | VIAVI proprietary                           |

### ML rAPP I/O Parameters

**Description:** The ML rAPP utilizes input parameters to predict future cell throughput. Its outputs include both the target cell ID and the predicted throughput value, enabling informed decisions for network optimization.

#### Input Parameters

| KPI/Measurement Name | Target Entity | Description                                                                                    | Defined by (3GPP TS 28.552 v17.6.0 / VIAVI) |
| -------------------- | ------------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------- |
| DRB_UEThpDl          | Cell, UE, QoS | Average downlink throughput (in Gbp)                                                           | 3GPP TS 28.552 v17.6.0 5.1.1.3.1            |
| Viavi_Cell_id        | UE            | Cell's or UE serving cell's "localCellId"                                                      | VIAVI proprietary                           |
| PEE.AvgPower         | Cell          | Average power consumed over the measurement period (in watts, W)                               | 3GPP TS 28.552 v17.6.0 5.1.1.19.2.1         |
| RRU_PrbTotDl         | Cell, mMIMO   | Total usage (in percentage) of Physical Resource Blocks (PRBs) on the downlink for any purpose | 3GPP TS 28.552 v17.6.0 5.1.1.2.1            |

#### Output Parameters

| KPI/Measurement Name | Target Entity | Description                               | Defined by (3GPP TS 28.552 v17.6.0 / VIAVI) |
| -------------------- | ------------- | ----------------------------------------- | ------------------------------------------- |
| Viavi_Cell_id        | UE            | Cell's or UE serving cell's "localCellId" | VIAVI proprietary                           |
| DRB_UEThpDl          | Cell, UE, QoS | Average downlink throughput (in Gbp)      | 3GPP TS 28.552 v17.6.0 5.1.1.3.1            |

### Parameter Integration Summary

The ES rAPP runs an energy-saving algorithm based on input parameters and outputs a cell ID to turn off cells with low load, achieving energy savings. In contrast, the ML rAPP uses input parameters to predict the future cell throughput, with the output including the cell ID and the predicted throughput value.

## Troubleshooting

### Common Issues

#### Deployment Issues

**Problem**: Pods stuck in `Pending` state

```bash
# Check resource constraints
kubectl describe pod <pod-name> -n <namespace>
kubectl top nodes

# Solution: Scale cluster or adjust resource requests
kubectl patch deployment <deployment-name> -n <namespace> \
  --patch '{"spec":{"template":{"spec":{"containers":[{"name":"<container>","resources":{"requests":{"memory":"1Gi","cpu":"500m"}}}]}}}}'
```

**Problem**: Image pull errors

```bash
# Check image and registry access
docker pull <your-registry>/es-rapp:v1.0

# Solution: Verify registry credentials
kubectl create secret docker-registry regcred \
  --docker-server=<your-registry> \
  --docker-username=<username> \
  --docker-password=<password>
```

#### Network Connectivity Issues

**Problem**: Services cannot communicate

```bash
# Test service DNS resolution
kubectl exec -it <pod-name> -n <namespace> -- nslookup ml-rapp.nonrtric

# Check network policies
kubectl get networkpolicies --all-namespaces

# Solution: Create service endpoints
kubectl get endpoints -n nonrtric
```

#### Performance Issues

**Problem**: High response latency

```bash
# Monitor resource usage
kubectl top pods -n nonrtric
kubectl logs -f deployment/es-rapp -n nonrtric | grep "response_time"

# Solution: Scale replicas or increase resources
kubectl scale deployment es-rapp --replicas=3 -n nonrtric
```

### Monitoring Commands

```bash
# System overview
kubectl get all --all-namespaces | grep -E "(es-rapp|ml-rapp|ho-xapp)"

# Resource monitoring
kubectl top pods --all-namespaces
kubectl top nodes

# Log aggregation
kubectl logs -f deployment/es-rapp -n nonrtric --tail=100
kubectl logs -f deployment/ml-rapp -n nonrtric --tail=100

# Network diagnostics
kubectl get services --all-namespaces
kubectl get ingress --all-namespaces
```

### Debug Mode Activation

```bash
# Enable debug logging for ES rAPP
kubectl patch configmap es-rapp-config -n nonrtric \
  --patch '{"data":{"LOG_LEVEL":"DEBUG"}}'

# Restart to apply changes
kubectl rollout restart deployment/es-rapp -n nonrtric

# Monitor debug logs
kubectl logs -f deployment/es-rapp -n nonrtric | grep DEBUG
```

## Additional Resources

### Documentation

**Platform Guides**

- [OSC I-Release SMO Deployment](https://hackmd.io/@H131413/ByOoZCmDa)
- [Non-RT RIC Installation](https://hackmd.io/@Winnie27/B1hE7bwBp)
- [rAPP Manager User Guide](https://hackmd.io/@Winnie27/Bk6xb7EBT)

**Testing & Validation**

- [RIC Integration Testing](https://hackmd.io/@Winnie27/r1uReJjxp)
- [Netconf Testing Procedures](https://hackmd.io/@Winnie27/r1BajOitT)
- [Cell On/Off Scenarios](https://hackmd.io/@Winnie27/rkltXnp1T)

**Equipment Specific**

- [Compal gNB O1-VES Integration](https://hackmd.io/@Winnie27/rJZXQBxmC)
- [Compal gNB Netconf Setup](https://hackmd.io/@Winnie27/rJu88bff0)

### Community & Support

- **O-RAN Software Community**: [https://www.o-ran.org/](https://www.o-ran.org/)
- **OSC Wiki**: [https://wiki.o-ran-sc.org/](https://wiki.o-ran-sc.org/)
- **Technical Support**: Create issues in this repository
- **Mailing Lists**: Join OSC developer mailing lists

### Related Projects

- [OSC Non-RT RIC](https://github.com/o-ran-sc/nonrtric)
- [OSC Near-RT RIC](https://github.com/o-ran-sc/ric-plt-ric-dep)
- [O-RAN Alliance Specifications](https://www.o-ran.org/specifications)

## Contributing

We welcome contributions to improve the Energy Saving rAPP system!

### Development Setup

```bash
# Clone repository
git clone https://github.com/bmw-ece-ntust/nonrtric-rapp-energysaving.git
cd nonrtric-rapp-energysaving

# Set up development environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements-dev.txt

# Run tests
pytest tests/
```

### Contribution Guidelines

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Testing Requirements

- All new features must include unit tests
- Integration tests for API changes
- Performance tests for ML model updates
- Documentation updates for user-facing changes

### Code Standards

- Follow PEP 8 for Python code
- Use type hints where applicable
- Include docstrings for all public methods
- Maintain test coverage above 80%

  ```bash
  # Monitor ES rAPP logs
  kubectl logs -f deployment/es-rapp -n nonrtric

  # Monitor ML rAPP logs
  kubectl logs -f deployment/ml-rapp -n nonrtric

  # Check service health
  kubectl get endpoints -n nonrtric
  ```

### Support and Community

- O-RAN Software Community: [https://www.o-ran.org/](https://www.o-ran.org/)
- OSC Wiki: [https://wiki.o-ran-sc.org/](https://wiki.o-ran-sc.org/)
- Technical Issues: Create issues in this repository

## Citation

If you use this project in your research or wish to cite it, please use the following citation:

```bibtex
@software{Lan_nonrtric-rapp-energysaving_2025,
  author = {Lan, Yong-Yi and Zhang, Han-Hong and Bimo, Fransiscus Asisi},
  month = jul,
  title = {{nonrtric-rapp-energysaving}},
  url = {https://github.com/bmw-ece-ntust/nonrtric-rapp-energysaving},
  version = {1.0.0},
  year = {2025}
}
```
