# Cloud Pub/Sub - Write to Cloud Storage

## Step-01: Introduction
- Create Pub/Sub Topic
- Create Pub/Sub Subscription with Delivery Type as **Write to Cloud Storage**
- Publish Messages
- Messages should be automatically pushed to Cloud Storage Bucket


## Step-02: Create Pub/Sub Topic
- Go to Cloud Pub/Sub -> Topics -> CREATE TOPIC
- **Topic ID:** mytopic3
- REST ALL LEAVE TO DEFAULTS
- Click on **CREATE**
- Review the Topic Tabs
  - SUBSCRIPTIONS
  - SNAPSHOTS
  - METRICS
  - DETAILS
  - MESSAGES

## Step-03: Create Pub/Sub Subscription
- Go to Cloud Pub/Sub -> Subscriptions -> CREATE SUBSCRIPTION
- **Subscription ID:** mysubscription3
- **Select Cloud/Pub Topic:** mytopic3
- **Delivery type:** Write to Cloud Storage
- **Cloud Bucket:** mybucket1099
- **File format:** text
- **Filename prefix:** mydemo
- **Storage Batch max duration:** 1
- REST ALL LEAVE TO DEFAULTS
- Click on **CREATE**

## Step-04: Publish Messages and Verify Cloud Storage Bucket
- Go to Cloud Pub/Sub -> Topics -> mytopic3 -> MESSAGES
- **PUBLISH MESSAGE**
- **Number of Messages:** 10
- **Message Body:** Hi Kalyan
- Click on **PUBLISH**
- Verify 


## Step-05: Clean-up
```t
# List and Delete Pubsub Subscriptions
gcloud pubsub subscriptions list
gcloud pubsub subscriptions delete projects/gcplearn9/subscriptions/mysubscription3
gcloud pubsub subscriptions delete projects/gcplearn9/subscriptions/mysubscription2
gcloud pubsub subscriptions delete projects/gcplearn9/subscriptions/mysubscription1

# List and Delete Pubsub Topics
gcloud pubsub topics list
gcloud pubsub topics delete projects/gcplearn9/topics/mytopic1
gcloud pubsub topics delete projects/gcplearn9/topics/mytopic2
gcloud pubsub topics delete projects/gcplearn9/topics/mytopic3
```
