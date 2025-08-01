# Implementation of Ian Joseph Chandra

Requirements:

- Rictest  run &  generate data
- SMO influxdb store the data

Step:

- deploy ML rapp <https://hackmd.io/@Jerry0714/HJmhjj-kT#3-Rrepare-standalone-Influx-DB-as-data-source-for-AIMLFW-to-prediction>
- deploy es rapp <https://github.com/bmw-ece-ntust/nonrtric-rapp-energysaving/tree/master/ES%20rApp/src>
- deploy RC,XP, HO xapp <https://github.com/o-ran-sc/ric-app-ts>

## Table of Contents



- [Implementation of Ian Joseph Chandra](#implementation-of-ian-joseph-chandra)
  - [Table of Contents](#table-of-contents)
  - [Deploy OSC xAPPS on Near-RT RIC](#deploy-osc-xapps-on-near-rt-ric)
    - [Deploy ES rAPP](#deploy-es-rapp)
    - [Deploy KPIMON-GO xAPP](#deploy-kpimon-go-xapp)
    - [Deploy HO xAPPs](#deploy-ho-xapps)

## Deploy OSC xAPPS on Near-RT RIC

### Deploy ES rAPP
1. 

### Deploy KPIMON-GO xAPP

1. Clone the repository:
  
    > [!NOTE]
    > Execute from the root folder `<YOUR_PATH>/ES_Use_Case/`

    ```bash
    git clone https://github.com/bmw-ece-ntust/kpimon-go-xapp.git
    ```

    **Output**

    ```
    Cloning into 'kpimon-go-xapp'...
    remote: Enumerating objects: 2904, done.
    remote: Counting objects: 100% (2904/2904), done.
    remote: Compressing objects: 100% (614/614), done.
    remote: Total 2904 (delta 2305), reused 2833 (delta 2289), pack-reused 0 (from 0)
    Receiving objects: 100% (2904/2904), 6.11 MiB | 13.32 MiB/s, done.
    Resolving deltas: 100% (2305/2305), done.
    ```

2. Build the container of KPIMON-GO xAPP:

    ```bash
    cd ES_Use_Case/kpimon-go-xapp/
    sudo nerdctl -n k8s.io build -t nexus3.o-ran-sc.org:10004/o-ran-sc/ric-app-kpimon-go:1.0.1 .
    sudo -E dms_cli onboard deploy/config.json deploy/schema.json
    sudo -E dms_cli install kpimon-go 2.0.1 ricxapp
    ```

    **Output**:

    ```shell
    ...
    => exporting to docker image format                                                           104.1s
    => => exporting layers                                                                         42.0s
    => => exporting manifest sha256:8daa5bac9dfbe4613986701aa47d38600e9eea48a4a5fbfee1a1f2ccf418a9  0.0s
    => => exporting config sha256:a59e6b004f5f23e8979d98a15e7830ee2d77b0e2650af5649293c77ee6f1121c  0.0s
    => => sending tarball                                                                          61.6s
    Loaded image: nexus3.o-ran-sc.org:10004/o-ran-sc/ric-app-kpimon-go:1.0.1
    ```

3. Verify the KPIMON-GO xAPP is running:

    ```bash
    sudo -E dms_cli onboard deploy/config.json deploy/schema.json
    ```

    **Output**:

    ```shell
    httpGet:
    path: '{{ index .Values "readinessProbe" "httpGet" "path" | toJson }}'
    port: '{{ index .Values "readinessProbe" "httpGet" "port" | toJson }}'
    initialDelaySeconds: '{{ index .Values "readinessProbe" "initialDelaySeconds" | toJson }}'
    periodSeconds: '{{ index .Values "readinessProbe" "periodSeconds" | toJson }}'

    httpGet:
    path: '{{ index .Values "livenessProbe" "httpGet" "path" | toJson }}'
    port: '{{ index .Values "livenessProbe" "httpGet" "port" | toJson }}'
    initialDelaySeconds: '{{ index .Values "livenessProbe" "initialDelaySeconds" | toJson }}'
    periodSeconds: '{{ index .Values "livenessProbe" "periodSeconds" | toJson }}'

    {
        "status": "Created"
    }
    ```

### Deploy HO xAPPs

> [!NOTE]
> This step will deploy two types of HO xAPPs: `HO-xAPP` by OSC and our custom `HO-assist-xAPP`.

1. Clone the repository for HO xAPPs:
  
    > [!NOTE]
    > Execute from the root folder `<YOUR_PATH>/ES_Use_Case/`

    ```bash
    git clone https://github.com/bmw-ece-ntust/ho-xapp.git
    ```

    **Output**

    ```shell
    Cloning into 'HO-xApp'...
    remote: Enumerating objects: 114, done.
    remote: Counting objects: 100% (114/114), done.
    remote: Compressing objects: 100% (106/106), done.
    remote: Total 114 (delta 25), reused 0 (delta 0), pack-reused 0 (from 0)
    Receiving objects: 100% (114/114), 8.69 MiB | 8.38 MiB/s, done.
    Resolving deltas: 100% (25/25), done.
    ```

2. Build HO-xAPP docker image

    ```bash
    cd HO-xApp
    sudo nerdctl -n k8s.io build -t ianjoseph/ho-xapp:0.0.1 .
    ```

    **Output**:

    ```shell
    => exporting to docker image format                                                             4.3s
    => => exporting layers                                                                          0.6s
    => => exporting manifest sha256:27a2a51ccdc6211f2b36e6801f890433080cefd2fca922c0ccd2aa756bcc84  0.0s
    => => exporting config sha256:c6352d13e370bd4a71b31263c9f554927792208f3cef920cb2b72d9daef89473  0.0s
    => => sending tarball                                                                           3.7s
    Loaded image: docker.io/ianjoseph/ho-xapp:0.0.1
    ```

3. Build HO-assist-xAPP docker image

    ```bash
    cd ../HO-assist-xApp
    sudo nerdctl -n k8s.io build -t ianjoseph/ho-assist-xapp:0.0.1 .
    ```

    **Output**:

    ```shell
    => exporting to docker image format                                                                                                                      59.1s
    => => exporting layers                                                                                                                                   41.0s
    => => exporting manifest sha256:846f3295658c0ab1e7e713754db41cda379eea3a0c58ffcf8cf8ee89aae55373                                                          0.0s
    => => exporting config sha256:fae3e057d0dfa8f252d3317714b9d86eae03485249d8b866dec43e72e9c40ba0                                                            0.0s
    => => sending tarball                                                                                                                                    18.0s
    Loaded image: docker.io/ianjoseph/ho-assist-xapp:0.0.1
    ```

4. Verify the built xAPPs in docker:

    ```bash
    sudo docker images | grep ho
    ```
