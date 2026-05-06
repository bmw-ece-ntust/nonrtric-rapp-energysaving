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

1. Clone the reposiotry:

    > [!NOTE]
    > Execute from the root folder `<YOUR_PATH>/ES_Use_Case/`

    ```bash
    git clone https://github.com/bmw-ece-ntust/nonrtric-rapp-energysaving.git
    ```

2. Build the image

```bash
sudo nerdctl build -t ianjoseph/es-rapp:noML
# ...
# => exporting to docker image format                                                35.1s
# => => exporting layers                                                             12.7s
# => => exporting manifest sha256:ed412f6d55fa356f9fc034ba1bc4a5cd05a45fa41bb00a4762  0.0s
# => => exporting config sha256:148e0331f9c7757be95f9ea5985ad145fe7e7cb766f272805960  0.1s
# => => sending tarball                                                              22.2s
# Loaded image: docker.io/ianjoseph/es-rapp:noML
```

3. Verify the image is built:

```bash
sudo nerdctl images | grep es-rapp
# REPOSITORY                                              TAG      IMAGE ID        CREATED               PLATFORM       SIZE        BLOB SIZE
# ianjoseph/es-rapp                                       noMl     ed412f6d55fa    4 minutes ago         linux/amd64    1.2 GiB     454.6 MiB
```

4. Create K8s namespace:

    ```bash
    sudo kubectl create ns es-rapp

    # Output:
    # namespace/es-rapp created
    ```

5. Deploy the ES rAPP:

    > [!NOTE]
    > Execute from the root folder of the cloned repository.

    ```bash
    sudo helm package ./ES\rApp/

    # OUTPUT:
    # Successfully packaged chart and saved it to: /home/kric/ian/ES_Use_Case/nonrtric-rapp-energysaving/energy-saving-rapp-0.1.0.tgz

    sudo helm install es-rapp-noml ./energy-saving-rapp-0.1.0.tgz --namespace=es-rapp

    # OUTPUT:
    # Successfully packaged chart and saved it to: /home/kric/ian/ES_Use_Case/nonrtric-rapp-energysaving/energy-saving-rapp-0.1.0.tgz

    sudo helm install es-rapp-noml ./energy-saving-rapp-0.1.0.tgz --namespace=es-rapp

    # OUTPUT:
    # Release "es-rapp-noml" has been installed.
    # NAMESPACE: es-rapp
    # NAME: es-rapp-noml
    # LAST DEPLOYED: Fri Aug  1 23:44:42 2025
    # NAMESPACE: es-rapp
    # STATUS: deployed
    # REVISION: 1
    # NOTES:
    # 1. Get the application URL by running these commands:
    #     export POD_NAME=$(kubectl get pods --namespace es-rapp -l "app.kubernetes.io/name=energysaving,app.kubernetes.io/instance=es-rapp-noml" -o jsonpath="{.items[0].metadata.name}")
    #     export CONTAINER_PORT=$(kubectl get pod --namespace es-rapp $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
    #     echo "Visit http://127.0.0.1:8080 to use your application"
    #     kubectl --namespace es-rapp port-forward $POD_NAME 8080:$CONTAINER_PORT
    ```

6. Verify the ES rAPP pods status:

    ```bash
    sudo kubectl get pods -n es-rapp

    # OUTPUT:
    # NAME                            READY   STATUS              RESTARTS   AGE
    # energysaving-865bcff57b-dcczm   0/1     ContainerCreating   0          20s
    ```

> [!CAUTION]
> Error found where executing this command:
>
> ```bash
> sudo kubectl logs -f -n <namespace> <pod Name> $(sudo kubectl get pods -A | grep es-rapp-noml | awk '{print $1 " " $2}')
> 
> # ERROR:
> # Traceback (most recent call last):
> #   File "main2.py", line 8, in <module>
> #     from nectconfclient import NETCONFCLIENT
> #   File "/app/nectconfclient.py", line 42, in <module>
> #     netconf_client.perform_action(6)
> #   File "/app/nectconfclient.py", line 34, in perform_action
> #     with manager.connect(host="192.168.8.28", port=30619, username="root", password="viavi", hostkey_verify=False) as m:
> #   File "/usr/local/lib/python3.8/site-packages/ncclient/manager.py", line 187, in connect
> #     return connect_ssh(*args, **kwds)
> #   File "/usr/local/lib/python3.8/site-packages/ncclient/manager.py", line 139, in connect_ssh
> #     session.connect(*args, **kwds)
> #   File "/usr/local/lib/python3.8/site-packages/ncclient/transport/ssh.py", line 288, in connect
> #     raise SSHError("Could not open socket to %s:%s" % (host, port))
> # ncclient.transport.errors.SSHError: Could not open socket to 192.168.8.28:30619
> ```

### Deploy KPIMON-GO xAPP

1. Clone the repository:
  
    > [!NOTE]
    > Execute from the root folder `<YOUR_PATH>/ES_Use_Case/`

    ```bash
    git clone https://github.com/bmw-ece-ntust/kpimon-go-xapp.git
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
