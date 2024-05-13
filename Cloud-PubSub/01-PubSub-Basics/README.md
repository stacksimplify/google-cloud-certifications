# Cloud Pub/Sub Basics

## Step-01: Introduction
- Create Pub/Sub Topic
- Create Pub/Sub Subscription
- Publish Messages
- Pull Messages in Subscription and Acknowledge

## Step-02: Create Pub/Sub Topic
- Go to Cloud Pub/Sub -> Topics -> CREATE TOPIC
- **Topic ID:** mytopic1
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
- **Subscription ID:** mysubscription1
- **Select Cloud/Pub Topic:** mytopic1
- **Delivery type:** pull
- REST ALL LEAVE TO DEFAULTS
- Click on **CREATE**

## Step-04: Publish Messages
- Go to Cloud Pub/Sub -> Topics -> mytopic1 -> MESSAGES
- **PUBLISH MESSAGE**
- **Number of Messages:** 10
- **Message Body:** Hi Kalyan
- Click on **PUBLISH**

## Step-05: Pull Messages in Subscription and Acknowledge
- Go to Cloud Pub/Sub -> Topics -> mytopic1 -> MESSAGES
### Pull without checking Enable ack messages
- **Select a Cloud Pub/Sub subscription to pull messages from:** projects/gcplearn9/subscriptions/mysubscription1
- Click on **PULL**
### Pull with checking Enable ack messages
- **Select a Cloud Pub/Sub subscription to pull messages from:** projects/gcplearn9/subscriptions/mysubscription1
- Click on **PULL** with CHECKING `Enable ack messages`
- Click on **ACK** for each message



