# Dataproc Serverless - Batch Jobs

## Step-01: Introduction
- Create a Dataproc Serverless Batch Job

## Step-02: Pre-requisite-1: Enable Private Google Access in VPC Subnet
- Goto VPC Networks -> default -> SUBNETS -> PICK us-central1 region SUBNET 
- Edit Subnet
- Private Google Access: ON
- Click on **SAVE**

## Step-03: Pre-requisite-2: Verify firewall rule default-allow-internal	
- Goto VPC Networks -> default -> FIREWALLS
- Verify if **default-allow-interna** is present

## Step-04: Create Dataproc Serverless Batch Job
- Goto Dataproc -> Serverless -> Batches -> Create
### Batch Info
- Batch ID: sort-words-101
- Region: us-central1
### Container
- Batch Type: PySpark
- Runtime version: USE LATEST  **2.1 (Spark 3.4, Java 17, Scala 2.13)**
- Main Python file: gs://mybucket1071/sort-words.py
### Network Configuration
- Networks in this project: select
- Primary network: default
- Subnetwork: default
- REST ALL LEAVE TO DEFAULTS
- Click on **SUBMIT**

## Step-04: Verify Job logs
- Goto Dataproc -> Serverless -> Batches -> sort-words-101

## Step-05: Delete the Batch Job after completion
- Goto Dataproc -> Serverless -> Batches -> sort-words-101 -> DELETE
