description = """
# Loan Approval API with Monitoring and Load Testing
<p style="text-align:center">
<img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" width="200" > 
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Prometheus_software_logo.svg/1200px-Prometheus_software_logo.svg.png" width="100">
<img src="https://www.skedler.com/blog/wp-content/uploads/2021/08/grafana-logo-300x150.png" width="200" >
<img src="https://devnot.com/wp-content/uploads/2017/09/docker-compose.jpg" width="200" >

</p>
<br>

# Table of Contents
- [Installation](#Installation)
- [Usage](#Usage)
- [API-Endpoints](#API-Endpoints)
- [Monitoring](#Monitoring)
- [Folder Structure](#Folder-Structure)
- [Screenshots](#Screenshots)


## Installation  <a name="Installation"></a>

There are only two prerequisites:

* [Docker](https://docs.docker.com/get-docker/)
* [Docker-compose](https://docs.docker.com/compose/install/)

## Usage <a name="Usage"></a>
### Start 

``` bash
docker-compose up --build -d
``` 

### Stopping containers

``` bash
docker-compose down
```

### Container Logs
When running containers with detached mode (`-d`) they work in the background thus you can't see the flowing logs. If you want to check compose logs with cli you can use `logs`.

``` bash
docker-compose logs --tail 50
```
## API Endpoints <a name="API-Endpoints"></a>
### Predict-API
There is a single endpoint for the prediction. You can find the endpoint in the `endpoints.py` file. It takes a json input and returns a prediction as a json response.

## Monitoring
### Prometheus 
Prometheus is used for monitoring. You can find the prometheus config in the `monitoring/prometheus.yml` file. It scrapes the metrics from the API container.

### Grafana 
Grafana is used for visualization. You can find the dashboard in the `provisioning/dashboards/dashboard.json` file. It visualizes the metrics from the prometheus.
> Graphana login credentials:
> user: admin
> password: pass


* FastAPI: http://localhost:8000
* Prometheus: http://localhost:9090
* Grafana: http://localhost:3000

### Folder Structure <a name="Folder-Structure"></a>

<details>
    <summary>Click to hide/unhide the folder structure.</summary>

``` bash

├── api.py
├── data
│   └── loan_approval_dataset.csv
├── docker-compose.yml
├── load_test
│   ├── data.py
│   └── locustfile.py
├── ml_engineer_case.pdf
├── model
│   └── model.txt
├── monitoring
│   ├── config.monitoring
│   └── prometheus.yml
├── notebooks
│   ├── eda.ipynb
│   ├── modelling.ipynb
│   └── test.ipynb
├── provisioning
│   ├── dashboards
│   │   ├── dashboard.json
│   │   └── dashboard.yaml
│   └── datasources
│       └── datasource.yml
├── readme.md
├── requirements.txt
├── src
│   ├── Dockerfile.app
│   ├── config.py
│   ├── datamodel.py
│   ├── endpoints.py
│   └── utils.py
└── tests
    ├── __init__.py
    ├── pytest.ini
    └── test_main.py
```
</details>

## Screenshots <a name="Screenshots"></a>

### Grafana Dashboard
<p align="center">
  <img src="assets/Loan_Approval_Dashboard.png"  width="800">
  <img src="assets/Loan_Approval_Dashboard_2.png" width="800">
</p>

### pytest (Unit Test)
<p align="center">
  <img src="assets/pytest.PNG"  width="800">
</p>



### Locust (Load Test)
<p align="center">
  <img src="assets/Locust_1.png"  width="800">
  <img src="assets/Locust_2.png" width="800">
</p>

"""