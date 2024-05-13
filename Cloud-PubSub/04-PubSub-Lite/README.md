# Cloud Pub/Sub Lite

## Step-01: Introduction
1. Create Lite Reservation
2. Create Lite Topic
3. Create Lite Subscription
4. Publish a message using gcloud
5. Receive and Acknowledge a message using gcloud
6. Delete Lite Topic, Lite Subscription and Lite Reservation

## Step-02: Create Lite Reservations
- Go to Cloud Pub/Sub -> Pub/Sub Lite -> Lite Reservations -> CREATE LITE RESERVATION
- **Location:** Region: us-central1
- **ID:** litereservation1
- **Throughput:** 5
- Click on **REVIEW**  

## Step-03: Create Lite Topic1
- Go to Cloud Pub/Sub -> Pub/Sub Lite -> Lite Topics -> CREATE LITE TOPIC
- **Location:**
  - **Region Lite Topic:** us-central1
- **ID:** litetopic1
- **Throughput:**
  - **Select a Lite resource:** projects/470832909724/locations/us-central1/reservations/litereservation1
  - REST ALL LEAVE TO DEFAULTS   
- **Message Storage:** LEAVE TO DEFAULTS
- Click on **CREATE**  

## Step-04: Create Lite Subscription1
- Go to Cloud Pub/Sub -> Pub/Sub Lite -> Lite Subscriptions -> CREATE LITE SUBSCRIPTION
- Lite Subscription ID: litesubscription1
- Select a Lite resource: projects/470832909724/locations/us-central1/topics/litetopic1
- REST ALL LEAVE TO DEFAULTS
- Click on **CREATE**


## Step-05: Publish Message and 
```t
# Set Project
gcloud config set project PROJECT_ID
gcloud config set project gcplearn9

# List Lite Topics
gcloud pubsub lite-topics list --location=us-central1

# Publish Message
gcloud pubsub lite-topics publish litetopic1 --location=us-central1 --message="Hello Message 1"

# List Lite Subscriptions
gcloud pubsub lite-subscriptions list --location=us-central1

# Receive and Acknowledge Messages
# https://cloud.google.com/pubsub/lite/docs/subscribing#receiving_messages
gcloud pubsub lite-subscriptions subscribe litesubscription1 --location=us-central1 --auto-ack                
```

## Step-06: Delete Lite Topic, Subscription and Reservation
```t
# Delete Lite Subscription
gcloud pubsub lite-subscriptions delete litesubscription1 --location=us-central1

# Delete Lite Topic
gcloud pubsub lite-topics delete litetopic1 --location=us-central1

# List and Delete Lite Reservations
gcloud pubsub lite-reservations list --location=us-central1
gcloud pubsub lite-reservations delete literes1 --location=us-central1
```

## Additional References
- https://cloud.google.com/pubsub/docs/choosing-pubsub-or-lite