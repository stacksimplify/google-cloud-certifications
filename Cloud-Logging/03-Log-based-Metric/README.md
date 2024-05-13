---
title: GCP Google Cloud Platform - Create log-based metric
description: Learn to create log-based metrics in Cloud Monitoring or Cloud Logging
---

## Step-01: Introduction
- Create log-based metric
- Review the log-based metric in **Metrics Explorer**

## Step-02: Generate HTTP 404 Traffic
```t
# Generate Traffic in a while loop in Cloud shell
while true; do curl http://EXTERNAL-IP/abc.html; sleep 1; done
while true; do curl http://34.171.101.170/abc.html; sleep 1; done
```

## Step-03: Logs Explorer: Search for 404 logs
```t
# Search 404 logs
resource.type="gce_instance"
log_id("nginx_access") 
http_request.status="404"

# Search 404 logs with resource name
resource.type="gce_instance"
log_id("nginx_access") 
http_request.status="404"
labels."compute.googleapis.com/resource_name"="myvm1"
```

## Step-03: Create Log based metric
- Go to -> Cloud Logging / Cloud Monitoring -> Logs Explorer 
- Create Metric from Logs Explorer screen
- **[OR]
- Go to -> Cloud Logging / Cloud Monitoring -> Configure -> Log-based Metrics
- Click on **Create Metric**
- **Metric Type:** Counter
- **Log-based Metric name:** http404-metric
- **Description:** HTTP 404 metrics
- **Units:** leave empty
- **Select log scope:** Project logs
- **Build filter:** 
```t
# Search 404 logs with resource name
resource.type="gce_instance"
log_id("nginx_access")
http_request.status="404"
labels."compute.googleapis.com/resource_name"="myvm1"
```
- Click on **Create metric**


## Step-04: Metrics Explorer: Review the newly created Metric
- Go to Cloud Logging or Cloud Monitoring -> Explore -> Metrics Explorer
- **Metric:** http404-metric-for-myvm1
- Review the Chart
- Review **Line Chart**
- Review **Stacked bar chart**


## Step-05: Review the option to create Alert using Metric
- Review the Alert creation option from newly created Metric

## Step-06: Also review additional options from Metric
- View in Metrics Explorer
- View metric details
- View logs for metric
- Delete Metric
- Disable Metric

## Step-07: Create Alert Policy from Log-based Metric 
- Go to Cloud Logging or Cloud Monitoring -> Configure -> log-based-metrics -> http404-metric-for-myvm1 
- Click on **Create alert from metric**
### Alert Condition
#### NEW CONDITION
- Rolling Window: 1 minute
- REST ALL LEAVE TO DEFAULTS
- click on **NEXT**
#### CONFIGURE TRIGGER
- **Threshold value:** 20 (20 HTTP 404 errors in a minute)
- **Coniditon name:** http-404-per-minute-greater-than-20
- REST ALL LEAVE TO DEFAULTS
- Click on **NEXT**
### Configure notification channels
- **Notification channel:** gcpuser08
- **Name the alert policy:** http404-metric-alert-policy
- REST ALL LEAVE TO DEFAULTS
- Click on **CREATE POLICY**

## Step-08: Simulate HTTP 404 Traffic
```t
# Generate Traffic in a while loop in Cloud shell
while true; do curl http://EXTERNAL-IP/abc.html; sleep 1; done
while true; do curl http://34.171.101.170/abc.html; sleep 1; done
```

## Step-09: Verify Incidents
- Go to Cloud Monitoring -> Detect -> Alerting -> http404-metric-alert-policy -> INCIDENTS
- Verify email: gcpuser08 for incident email

