---
title: Google Cloud Managed Instance Groups Stateless
description: Learn to Create Managed Instance Groups Stateless on Google Cloud Platform GCP
---

## Step-01: Introduction
1. **Instance Group:** An instance group is a collection of virtual machine (VM) instances that you can manage as a single entity.
2. **Managed Instance Group (Stateless)**
   1. Autoscaling
   2. Autohealing
   3. Auto-updating
   4. Multi-Zone Deployment
   5. Load Balancing
3. In this demo, we are going to focus on **Managed Instance Groups - Stateless**

## Step-02: Create Instance Template
- Go to Compute Enginer -> Virtual Machines -> Instance Templates -> Create Instance Template -> Provide required details
- **Name:** mig-it-stateless-v1
- **Location:** Regional
- **Region:** us-central1
- **Machine Configuration:** 
  - **Series:** E2
  - **Machine Type:** e2-micro
- **Availability Policies:**
  - **VM Provisioning Model:** Standard    
- **Display Device:** unchecked (leave to default)
- **Confidential VM Service:** unchecked (leave to default)
- **Container:** unchecked (leave to default)
- **Boot Disk:** Leave to defaults
- **Identity and API Access:**
  - **Service Account:** Compute Engine default Service Account
  - **Access Scopes:** Allow default Access
- **Firewall**
  - Allow HTTP Traffic
- **Advanced Options**
  - **Management:**
    - **Description:** demo4-vm-startupscript
    - **Reservations:** Automatically use created reservation (leave to default)
    - **Automation:**
      - **Startup Script:** Copy paste content from `v1-webserver-install.sh` file
- Click on **Create**
```t
# Set Project
gcloud config set project PROJECT_ID
gcloud config set project gcplearn9

# Create Instance Template - V1
gcloud compute instance-templates create mig-it-stateless-v1 \
  --machine-type=e2-micro \
  --network-interface=network=default,network-tier=PREMIUM \
  --instance-template-region=us-central1 \
  --tags=http-server \
  --metadata-from-file=startup-script=v1-webserver-install.sh 
```

## Step-03: Create Health Check 
- **What is Health Check?**
    1. A health check determines whether a VM instance is healthy by sending requests to the instance. 
    2. An instance is considered healthy if it returns consecutive responses within a specified time. 
    3. Health checks are used for load balancing and autoscaling managed instance groups
- Go to Compute Engine -> Instance Groups -> Health Checks -> **CREATE HEALTH CHECK**
- **Name:** app1-health-check
- **Description:** 
- **Scope:** Regional 
- **Region:** us-central-1 (IOWA)
- **Protocol:** HTTP
- **Port:** 80
- **Proxy Protocol:** None
- **Request Path:** /app1/status.html
- **Response:** App1
- **Host HTTP Header:** leave empty (leave to defaults)
- **Logs:** Off (leave to defaults) If enabled Cloud Logging cost is going to be high
- **Health Criteria:** Leave to defaults
```t
# Create Health Check
gcloud compute health-checks create http app1-health-check \
   --project=gcplearn9 \
   --port=80 \
   --request-path=/index.html \
   --proxy-header=NONE \
   --response=App1 \
   --region=us-central1 \
   --no-enable-logging \
   --check-interval=10 \
   --timeout=5 \
   --unhealthy-threshold=3 \
   --healthy-threshold=2
```
- Click on **CREATE**

## Step-04: Create a firewall rule to allow health check probes to connect to your app 
- Health check probes come from addresses in the ranges 130.211.0.0/22 and 35.191.0.0/16, so make sure your firewall rules allow the health check to connect. For this example, the MIG uses the default network, and its VMs listen on port 80. If port 80 isn't already open on the default network, create a firewall rule.
```t
# Create Firewall rule
gcloud compute firewall-rules create allow-health-check \
    --allow tcp:80 \
    --source-ranges 130.211.0.0/22,35.191.0.0/16 \
    --network default
```

## Step-05: Create Managed Instance Group Stateless Single Zone
- **Name:** mig-stateless
- **Description:** mig-stateless
- **Instance Template:** mig-it-stateless-v1
- **Location:** Single Zone
- **Region:** us-central1
- **Zone:** us-central1-a
- **Autoscaling:**
   - **Autoscaling Mode:** On: add and remove instances to the group (Discuss 3 autoscaling modes)
   - **Minimum Number of Instances:** 2
   - **Maximum Number of Instances:** 6
   - **Autoscaling Signals:** CPU utilization 60% 
      - Discuss other two Autoscaling Signals
         - HTTP Load Balancer Utilization 
         - Cloud Pub/Sub Queue
         - Cloud Monitoring Metric
   - **Predictive Autoscaling:** On
   - **Initialization period:** 60 seconds
   - **Scale in Controls**
      - **Enable Scale In Controls:** Checked (Enabled)
      - **Don't scale in by more than:** Number of Instances: 1 VMs
      - **Over the course of:** 10 Minutes
- **VM instance lifecycle:**
   - **Default action on failure:** Repair Instance (leave to defaults)
- **Autohealing:**
   - **Health check:** app1-health-check   
   - **Initial Delay:** 180 seconds
   - **Updates during VM instance repair:** Keep the same instance configuration (leave to defaults)
- **Specify Port Name Mapping:** 
   - **Port Name:** webserver-port
   - **Port Numbers:** 80
- **Advanced creation options:** leave to defaults and discuss
- Click on **CREATE**
```t
# Create Managed Instance Group
gcloud compute instance-groups managed create mig-stateless \
   --size=2 \
   --template=projects/gcplearn9/regions/us-central1/instanceTemplates/mig-it-stateless-v1 \
   --zone=us-central1-c \
   --health-check=projects/gcplearn9/regions/us-central1/healthChecks/app1-health-check \

# Set Named Ports
gcloud compute instance-groups set-named-ports mig-stateless \
   --zone=us-central1-c \
   --named-ports=webserver-port:80

# Set Autoscaling
gcloud compute instance-groups managed set-autoscaling mig-stateless \
   --project=gcplearn9 \
   --zone=us-central1-c \
   --cool-down-period=60 \
   --max-num-replicas=6 \
   --min-num-replicas=2 \
   --mode=on \
   --target-cpu-utilization=0.6 \
   --scale-in-control=max-scaled-in-replicas=1,time-window=600
```
## Step-06: Review Managed Instance Group Properties
- Go to Compute Engine -> Instance Groups -> Click on **mig-stateless**
- Review the following Tabs
   - Overview
   - Details
   - Monitoring
   - Errors 
- Go to Compute Engine -> VM Instances -> Verify VM created by Instance Group

## Step-07: Create a Load Balancer
- Go to Network Services -> Load Balancing -> Create Load Balancer -> HTTP(S) Load Balancing -> START CONFIGURATION
- **Internet facing or internal only:** From internet to my VMs
- Click on **Continue**
- **Name:** lb-for-mig-stateless
### Frontend Configuration
- **New Frontend IP and port**
- **Name:** fip-lb-mig-stateless
- **Protocol:** HTTP
- **Network Service Tier:** Premium
- **IP Version:** IPV4
- **IP Address:** Click on **CREATE IP ADDRESS** 
   - **NAME:** sip-lb-mig-stateless
   - **DESCRIPTION:** sip-lb-mig-stateless
- **Port:** 80
- Click on **DONE** 
### CREATE A BACKEND SERVICE
- Click on **CREATE A BACKEND SERVICE**
   - **Name:** lb-backend-for-mig-stateless
   - **Description:** lb-backend-for-mig-stateless
   - **Backend Type:** Instance Group
   - **Protocol:** HTTP
   - **Naed Port:** http
   - **Timeout:** 30
   - **New backend:** managed-instance-group-stateless
   - **Port Numbers:** 80 (select webserver-port named port from that instance group)
   - **Balancing mode:** Utilization 
   - **Maximum backend utilization:** 80
   - **Maximum RPS:** leave empty (leave to defaults)
   - **Scope:** per instance (leave to defaults)
   - **Capacity:** 100
   - Click on **DONE**
   - Click on **CREATE**
- **Logging:** leave unchecked (leave to defaults)
- **Security:** leave unselected (leave to defaults)   
- Click on **CREATE**
### Host and Path Rules
- **Mode:** Simple host and path rule

### Review and Finalize
1. Front End
2. Backend
- Click on **CREATE**
- It will take 3 to 5 minutes to create the load balancer. 

## Step-08: Verify Load Balancer Properties after creation
- Go to Network Services -> Load Balancing -> lb-for-unmanaged-instance-group
- Verify if Instances are Healthy

## Step-09: Access Sample Application using LB IP 
```t
# Access Sample App
http:/;<LB-IP-ADDRESS>
http://34.149.43.103
Observation: 
1. Keep refreshing to see the output from both Virtual Machines
2. You will see output from both VMs switching

# Curl with while loop runs every 1 second
while true; do curl http://35.209.128.93/; sleep 1; done
```

## Step-10: Discuss about MANAGE SCHEDULES
- Go to Compute Engine -> Instance Groups -> Click on **mig-stateless** 
- Click on **DETAILS TAB**
- Click on **MANAGE SCHEDULES** -> **CREATE SCHEDULE**
- **Name:** high-traffic-tuesday
- **Description:** high-traffic-tuesday
- **Minimum Required Instances:** 3 (Usually minimum is 2 but on tuesday we will have 3)
- **Start Time:** 7:00 AM
- **Time Zone:** India Standard Time (IST)
- **Duration:** 10 hours
- **Recurrence:** Every Week
- **Day(s) of week:** Tuesday
- Click on **SAVE**
- Click on **REFRESH** and Review
- Click on **DONE**
```t
# Create Autoscaling Schedules
gcloud compute instance-groups managed update-autoscaling mig-stateless \
   --project=gcplearn9 \
   --zone=us-central1-c \
   --set-schedule=high-traffic-tuesday \
   --schedule-cron='0 7 * * Tue' \
   --schedule-duration-sec=36000 \
   --schedule-time-zone='Asia/Calcutta' \
   --schedule-min-required-replicas=3 \
   --schedule-description='high-traffic-tuesday'
```

## Step-11: Predictive autoscaling and Auto-healing
### Step-11-01: Discuss about Predictive autoscaling
- Go to Compute Engine -> Instance Groups -> Click on **mig-stateless** 
- Click on **Edit**
- Go to **Predictive Autoscaling** -> Click on **See if predictive autoscaling can optimize your availability**

### Step-11-02: Auto-healing
```t
# Connect to one VM Instane
gcloud compute ssh --zone "us-central1-c" "mig-stateless-2ztq" --project "gcplearn9"

# Delete index.html
cd /var/www/html
sudo rm index.html
sudo rm index.nginx-debian.html

# Access App from Browser using VM public IP
http://EXTERNAL-IP
Observation:
1. HTTP 403 forbidden error from ngnix

## Auto-healing observation
1. A new vm instance should be re-created with same name
```

## Step-12: Discuss about UPDATE VMs
### Step-12-01: Create a new Instance Template
- Here we are going to create a new Instance Template by cloning existing template named `mig-it-stateless-v1` 
   - **Change-1:** change the `machine type` to `e2-small`
   - **Change-2:** change the Startup script to `v2-webserver-install.sh`
- Go to Compute Engine -> VM Instances -> Instance Template -> mig-it-stateless-v1 -> **CREATE SIMILAR**
- **Name:** mig-it-stateless-v2
- **Machine Type:** e2-small
- Click on **CREATE**
```t
# Create Instance Template - V2
gcloud compute instance-templates create mig-it-stateless-v1 \
  --machine-type=e2-small \
  --network-interface=network=default,network-tier=PREMIUM \
  --instance-template-region=us-central1 \
  --tags=http-server \
  --metadata-from-file=startup-script=v2-webserver-install.sh 
```

### Step-12-02: How to UPDATE VMs setting in Instance Groups ? - UPDATE VMs
- Go to Compute Engine -> Instance Groups -> Click on **mig-stateless** 
#### Instance template & overrides
- **Instance Template:** mig-it-stateless-v2
#### Update Type: Selective 
- Existing VMs are not updated automatically when instance configuration changes. 
- Changes will apply once existing VMs are replaced or restarted. (API name: OPPORTUNISTIC)
- Update VMs in this group when they are replaced, refreshed, or restarted, except during auto-healing. 
```t
Updater will not actively replace instances, but when new instances are created by other means, you will deploy template "mig-it-stateless-v1" to 50% of instances and template "mig-it-stateless-v2" to 50% of instances in instance group "mig-stateless".
```     
#### Update Type: Automatic 
- When instance configuration changes, updates to existing VMs will be applied automatically by MIG. (API name: PROACTIVE)
```t
1. You are deploying template "mig-it-stateless-v1" to 50% of instances and template "mig-it-stateless-v2" to 50% of instances in instance group "mig-stateless".
2. 1 instance will be taken offline at a time and 1 instance will be temporarily added to support the update.
```
- **Actions allowed to update VMs:** only replace (Discuss all options)
- **When replacing keep VM names same:** leave empty (leave to defaults - NOT CHECKED)
- **Temporary additional instances:** 1
- **Maximum unavailable instances:** 1
- **Minimum wait time:** 0 seconds
- Click on **SAVE**
```t
# Update VMs: Selective (opportunistic)
gcloud compute instance-groups managed rolling-action start-update mig-stateless \
   --project=gcplearn9 \
   --type='opportunistic' \
   --max-surge=1 \
   --max-unavailable=1 \
   --min-ready=0 \
   --minimal-action='replace' \
   --most-disruptive-allowed-action='' \
   --replacement-method='substitute' \
   --version=template=projects/gcplearn9/regions/us-central1/instanceTemplates/mig-it-stateless-v2 \
   --zone=us-central1-c

# Update VMs: Automatic (proactive)
gcloud compute instance-groups managed rolling-action start-update mig-stateless \
   --project=gcplearn9 \
   --type='proactive' \
   --max-surge=1 \
   --max-unavailable=1 \
   --min-ready=0 \
   --minimal-action='replace' \
   --most-disruptive-allowed-action='replace' \
   --replacement-method='substitute' \
   --version=template=projects/gcplearn9/regions/us-central1/instanceTemplates/mig-it-stateless-v2 \
   --zone=us-central1-c     
```

### Step-12-03: Verify the VM Instances
- Go to Compute Engine -> VM Instances 
- We should observe one VM created with `e2-small`
- We should see finally we end up with 2 VMs
   - 2VMs with e2-small
- We should see V2 version of application deployed   
- **Observation:** It will take few minutes (approximately 10 minutes) to complete the overall process and reach desired state   
```t
# Access Application using Load balancer
curl http://35.209.128.93/
http://35.209.128.93/

# In a while loop
while true; do curl http://35.209.128.93/; sleep 1; done
```

## Step-13: Explore DELETE INSTANCE setting 
- Go to Compute Engine -> Instance Groups -> Click on **mig-stateless**
- Select one instance and DELETE the instance
- Wait for couple of minutes
- New instance will be recreated in few minutes

## Step-14: Explore REMOVE FROM GROUP setting
- Go to Compute Engine -> Instance Groups -> Click on **mig-stateless**
- REMOVE Instance from group
- Wait for couple of minutes
- New instance will be created in few minutes
- Go to Compute Engine -> VM Instances -> Delete the instance which was removed from Instance Group (WAIT FOR DELETE OPTION TO BE ENABLED)

## Step-15: Explore RESTART / REPLACE VMs setting
- Go to Compute Engine -> Instance Groups -> Click on **mig-stateless**
### Step-15-01: Restart Option
- **Maximum unavailable:** 1 Instance
- **Minimum wait time:** 0 seconds
- Click on **RESTART**

### Step-15-02: Replace Option
- **Maximum surge:** 1 instnace   (Maximum number (or percentage) of temporary instances to add while replacing.)
- **Maximum unavailable:** 1 Instance
- **Minimum wait time:** 0 seconds
- Click on **REPLACE**

## Step-16: Review Monitoring Tab
- Go to Compute Engine -> Instance Groups -> Click on **mig-stateless**
- Click on **MONITORING** Tab
- Primarily review `Instances` graph - How instances scaled-out and scaled-in

## Step-17: Clean-Up - Delete Load Balancer
- Go to Network Services -> Load Balancing -> lb-for-managed-instance-group
- Click on **DELETE**
- Select **Backend services:lb-backend-for-mig-stateless** for deletion
- Leave **Health Checks: lb-health-check-http** unchecked to not to delete
- Click on **DELETE LOAD BALANCER AND SELECTED RESOURCES**

## Step-18: Clean-Up - Release External IP Address used for LB
- Go to VPC Networks -> External IP Addresses
- Select **sip-lb-mig-stateless** 
- click on **RELEASE STATIC IP ADDRESS**

## Step-19: Clean-Up - Delete Instance Group
- Go to Compute Engine -> Instance Groups -> Click on **mig-stateless**
- Click on **DELETE GROUP**
```t
# Delete Instance Group - Managed
gcloud compute instance-groups managed delete mig-stateless \
   --project=gcplearn9 \
   --zone=us-central1-a
```

## Step-20: Create Managed Instance Group Stateless Multiple Zones
- **Name:** mig-stateless-multiple-zones
- **Description:** mig-stateless-multiple-zones
- **Location:** Multiple Zones
- **Region:** us-central1
- **Zones:** us-central1-a, us-central1-a, us-central1-b, us-central1-c, us-central1-f
- **Target distribution shape:** Even (Distribute managed instances evenly across zones)
- **Specify Port Name Mapping:** 
   - **Port Name:** webserver-port
   - **Port Numbers:** 80
- **Instance Template:** demo3-instance-template-externalip-none
- **Number of Instances:** Based on autoscaling configuration (leave to default)
- **Autoscaling:**
   - **Autoscaling Mode:** Autoscale (Discuss 3 autoscaling modes)
   - **Autoscaling Policy:** CPU utilization 60% (Discuss other two Autoscaling Policies - HTTP Load Balancer Metrics and StackDriver or Cloud Monitoring Metric)
   - **Predictive Autoscaling:** Off
   - **Cool down period:** 60 seconds
   - **Minimum Number of Instances:** 3
   - **Maximum Number of Instances:** 9
   - **Scale in Controls**
      - **Enable Scale In Controls:** Checked (Enabled)
      - **Don't scale in by more than:** Number of Instances: 1 VMs
      - **Over the course of:** custom (5 minutes)
- **Autohealing:** 
- **Health check:** No Health Check
- **Advanced creation options:** leave to defaults and discuss
- Click on **CREATE**

## Step-21: Review Managed Instance Group Properties
- Go to Compute Engine -> Instance Groups -> Click on **mig-stateless-multiple-zones**
- Review the following Tabs
   - Overview
   - Details
   - Monitoring
   - Errors 
- Go to Compute Engine -> VM Instances -> Verify VM created by Instance Group and Verify its Zones

## Step-22: Delete Managed Instance Group
- Go to Compute Engine -> Instance Groups -> Click on **mig-stateless-multiple-zones**
- Click on **DELETE GROUP**


## References 
- [Instance Groups](https://cloud.google.com/compute/docs/instance-groups)