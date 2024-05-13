# Google Cloud - Zonal Managed Instance Groups

## Step-01: Introduction
1. Create Regional Health check
2. Create Firewall rule
3. Create Instance Template
4. Create Zonal Managed Instance Group

## Step-02: Create Regional Health Check - TCP
```t
# Create Regional Health Check
gcloud compute health-checks create tcp regional-tcp-health-check \
  --port=80 \
  --region=us-central1 
```

## Step-03: Create Firewwall Rules
- This firewall rule is already created as part of demo-1, just for reference only
```t
# Firewall Rule-1: Ingress rule that allows traffic from the Google Cloud health checking systems (130.211.0.0/22 and 35.191.0.0/16).
gcloud compute firewall-rules create vpc3-custom-allow-health-check \
  --network=vpc3-custom \
  --description=Allows\ traffic\ from\ Google\ Cloud\ health\ checking\ systems \
  --direction=ingress \
  --source-ranges=130.211.0.0/22,35.191.0.0/16 \
  --action=allow \
  --rules=tcp:80   
```

## Step-04: Create Instance Template
```t
# us-central1: Create Instance Template
gcloud compute instance-templates create it-rlbdemo-us-central1 \
   --region=us-central1 \
   --network=vpc3-custom \
   --subnet=us-central1-subnet \
   --tags=lb-tag \
   --machine-type=e2-micro \
   --metadata-from-file=startup-script=nginx-webserver.sh
```

## Step-05: Create Zonal Managed Instance Groups 
```t
# Zone: us-central1-a: Create Managed Instance Groups in the Zone
gcloud compute instance-groups managed create zmig-us-1 \
    --zone us-central1-a \
    --size 2 \
    --template it-rlbdemo-us-central1 

# Zone: us-central1-c: Create Managed Instance Groups in the Zone
gcloud compute instance-groups managed create zmig-us-2 \
    --zone us-central1-c \
    --size 2 \
    --template it-rlbdemo-us-central1
```
