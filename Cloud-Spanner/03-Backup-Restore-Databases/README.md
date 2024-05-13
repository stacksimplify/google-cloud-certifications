# Cloud Spanner - Backup and Restore Databases

## Step-01: Introduction
- Create Database backup for mywebappdb in mycsinstance1
- Restore Database backup to database myrestoredb

## Step-02: Backup mywebappdb from mycsinstance1
- Go to Cloud Spanner -> mycsinstance1 -> Backup / Restore -> CREATE BACKUP
- Database name: mywebappdb
- Backup name: mywebadddb-backup1
- Set an expiration date: 1 year
- Click on **CREATE**

## Step-03: Restore mywebappdb in mycsinstance1 to mywebadddb-backup1
- Go to  Cloud Spanner -> mycsinstance1 -> mywebappdb -> Backup / Restore -> mywebadddb-backup1 -> ACTIONS -> RESTORE
- **Choose a compatible instance:** mycsinstance1
- **Name the restored database for mywebadddb-backup1:** myrestoreddb
- Click on **RESTORE**

## Step-04: Review and Query new restored Database: myrestoreddb
- Go to  Cloud Spanner -> mycsinstance1 -> myrestoreddb -> Spanner Studio
```t
# Query Table
select * from myusers;    
```

## Step-05: Clean-up
- Delete Databases in mycsinstance1
- Delete mycsinstance1
- Delete Databases in mycsinstance2
- Delete mycsinstance2
```t
# Set Project
gcloud config set project PROJECT_ID
gcloud config set project gcplearn9

# Cloud Spanner Instance: mycsinstance1
gcloud spanner databases delete mywebappdb --instance=mycsinstance1
gcloud spanner databases delete myrestoreddb --instance=mycsinstance1
gcloud spanner backups delete mywebadddb-backup1 --instance=mycsinstance1
gcloud spanner instances delete mycsinstance1

# Cloud Spanner Instance: mycsinstance2
gcloud spanner databases delete myappdb --instance=mycsinstance2
gcloud spanner databases delete mywebappdb --instance=mycsinstance2
gcloud spanner instances delete mycsinstance2

# List Cloud Spanner Instances
gcloud spanner instances list
```
