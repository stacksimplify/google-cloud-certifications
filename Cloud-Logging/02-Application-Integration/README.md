---
title: GCP Google Cloud Platform - Application Logging and Monitoring
description: Learn to create Cloud Logging Queries 
---

## Step-01: Introduction
- **Pre-requisite-1:** Create VM Instance with webserver installed
- **Pre-requisite-2:** Instal Ops Agent
### Logging
- Enable nginx_status
- Configure the Ops Agent for nginx
- Verify Nginx logs in Cloud Logging - Logs Explorer
### Metrics
- Metrics Explorer: Fetch Metrics
### Dashboard
- View Nginx Dashboard
### Alerting
- Create Alerting Policies for nginx

## Step-02: GCP Cloud Logging and Monitoring NGINX Integration
- Go to Cloud Logging -> Configure -> Integrations -> Search for **Nginx**
- Review
  - Metrics Tab
  - Logs Tab
  - Dashboard Tab
  - Alerts Tab

## Step-03: Enable Nginx Status - status.conf
```t
# Connect to VM Instance
gcloud compute ssh --zone "us-central1-a" "myvm1" --project "gcplearn9"

# Create status.conf in Nginx
sudo tee /etc/nginx/conf.d/status.conf > /dev/null << EOF
server {
   listen 80;
   server_name 127.0.0.1;
   location /nginx_status {
       stub_status on;
       access_log off;
       allow 127.0.0.1;
       deny all;
   }
   location / {
       root /dev/null;
   }
}
EOF

# Nginx reload
sudo service nginx reload

# Curl Test
curl http://127.0.0.1:80/nginx_status
curl http://104.154.43.173:80/nginx_status
```


## Step-04: Configure the Ops Agent for nginx
- Configures Ops Agent to collect telemetry from the app and restart Ops Agent.
```t
# Create a back up of the existing file so existing configurations are not lost.
sudo cp /etc/google-cloud-ops-agent/config.yaml /etc/google-cloud-ops-agent/config.yaml.bak

# Configure the Ops Agent.
sudo tee /etc/google-cloud-ops-agent/config.yaml > /dev/null << EOF
metrics:
  receivers:
    nginx:
      type: nginx
      stub_status_url: http://127.0.0.1:80/nginx_status
  service:
    pipelines:
      nginx:
        receivers:
          - nginx
logging:
  receivers:
    nginx_access:
      type: nginx_access
    nginx_error:
      type: nginx_error
  service:
    pipelines:
      nginx:
        receivers:
          - nginx_access
          - nginx_error
EOF

# Verify file
ls /etc/google-cloud-ops-agent/config.yaml
cat /etc/google-cloud-ops-agent/config.yaml

# Restart Cloud Ops Agent
sudo service google-cloud-ops-agent restart
sleep 60
```

## Step-05: Logging Explorer: Verify Nginx logs
- Go to Cloud Logging -> Logs Explorer
```t
# Query-1: Verify Nginx Logs
resource.type="gce_instance"
(log_id("nginx_access") OR log_id("nginx_error"))

# Query-2: Verify Nginx Logs with Instance ID
resource.type="gce_instance"
(log_id("nginx_access") OR log_id("nginx_error"))
resource.labels.instance_id="1493921793379482560"

# Observation
1. Should see Nginx access logs from Cloud Monitoring Agent
```

## Step-06: Logging Explorer: Hide similar entries
```t
# Generate Traffic in a while loop in Cloud shell
while true; do curl http://EXTERNAL-IP; sleep 1; done
while true; do curl http://34.29.5.200; sleep 1; done

# Hide similar entries query
resource.type="gce_instance"
(log_id("nginx_access") OR log_id("nginx_error"))
--Hide similar entries
-(httpRequest.requestUrl="/index.html")
--End of hide similar entries
```

## Step-07: Metrics Explorer: Fetch Metrics
- Go to Cloud Logging / Monitoring -> Metrics Explorer
```t
# Types of Nginx Metrics
workload.googleapis.com/nginx.connections_accepted
workload.googleapis.com/nginx.connections_current
workload.googleapis.com/nginx.connections_handled
workload.googleapis.com/nginx.requests

# Fetch Metrics
fetch gce_instance
| metric 'workload.googleapis.com/nginx.requests'
| every 1m

fetch gce_instance
| metric 'workload.googleapis.com/nginx.connections_accepted'
| every 1m

fetch gce_instance
| metric 'workload.googleapis.com/nginx.connections_current'
| every 1m

fetch gce_instance
| metric 'workload.googleapis.com/nginx.connections_handled'
| every 1m
```
## Step-08: Cloud Monitoring /Logging: Nginx Dashboard
- Go to Cloud Logging / Monitoring -> Dashboards -> Nginx Dashboard
- Review graphs
  - Requests Rate
  - Current Connections
  - Connection Rate
  - CPU % Top 5 VMs
  - Memory % Top 5 VMs
  - NGINX VMs by Region
  - NGINX Access Logs
  - NGINX Error Logs

## Step-09: Create Alerting Policies for nginx
- Go to Cloud Logging or Monitoring -> Configure -> Integrations -> Search for **Nginx**
- Go to
  - Alerts Tab
- Select and create alerts for the below
  - Nginx - low request rate
  - Nginx - high request rate
  - Nginx - connections dropped

## Step-10: Review 
- Review Nginx Alert Policies
- Review Nginx Incidents (if any)


## Additional References
- https://cloud.google.com/stackdriver/docs/solutions/agents/ops-agent/third-party/nginx

