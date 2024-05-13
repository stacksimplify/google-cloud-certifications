# Cloud BigTable - using gcloud

## Step-01: Introduction
- Create BigTable tasks using gcloud
  - Create BigTable Instance
  - Create Table in BigTable
- Implement backup and restore operations
- Clean-up: Delete BigTable instances

## Step-02: gcloud: Create BigTable Instance 
```t
# Set Project
gcloud config set project PROJECT_ID
gcloud config set project gcplearn9

# Create BigTable Instance
gcloud bigtable instances create mybigtableins2 \
    --display-name=mybigtableins2 \
    --cluster-config=id=mybigtableins2-c1,zone=europe-west10-c,autoscaling-min-nodes=1,autoscaling-max-nodes=3,autoscaling-cpu-target=60,autoscaling-storage-target=2560

# List Instances
gcloud bigtable instances list    

# Describe Instances
gcloud bigtable instances describe mybigtableins2

# List Clusters
gcloud bigtable clusters list

# Describe Clusters
gcloud bigtable clusters describe mybigtableins2-c1 --instance=mybigtableins2
```

## Step-03: gcloud: Create Tables using gcloud cli
```t
# Create Table
gcloud bigtable instances tables create mytable1 \
    --instance=mybigtableins2 \
    --column-families="mycf1:maxage=2d,mycf2:maxage=3d"

# List Tables 
gcloud bigtable instances tables list --instances="mybigtableins2"

# Describe Tables
gcloud bigtable instances tables describe mytable1 --instance=mybigtableins2
```

## Step-04: Backup mytable1 in mybigtableins1
- Goto mybigtableins1 -> Backups -> **CREATE BACKUP**
- Table ID: mytable1
- Cluster ID: mybigtableins1-c1
- Backup ID: mybackup101
- Set an expiration date: 7 days
- Click on **CREATE**

## Step-05: Restore data to mybigtableins2
- Goto mybigtableins1 -> Backups -> mybackup101 -> RESTORE
- Select an instance to restore to: mybigtableins2
- Name the restored table for mybackup101: mytable101
- Click on **RESTORE**

## Step-06: Verify restore operation successfull or not in mybigtableins2 
- Goto mybigtableins1 -> Tables
- Goto mybigtableins1 -> Bigtable Studio -> RUN 
- Verify the data records

## Step-07: Clean-Up
```t
# Delete mybigtableins1
gcloud bigtable backups delete mybackup101 --instance=mybigtableins1 --cluster=mybigtableins1-c1
gcloud bigtable instances delete mybigtableins1

# Delete mybigtableins2
gcloud bigtable instances delete mybigtableins2
```
