# Cloud SQL - Backup and Restore Operations

## Step-01: Introduction
- Backup and Restore Cloud SQL Instances

## Step-02: Backup Databases
- Backup Database Instance: mydb1
- Restore Database Instance: mydb2
```t
# List Backups
gcloud sql backups list --instance=mydb1

# mydb1: Create Database Instance Backup 
gcloud sql backups create --instance=mydb1 --description=mydb1backup101
gcloud sql backups list --instance=mydb1

# Verify mydb2 BEFORE restore from mydb1
# List Databases from the Database Instance
gcloud sql databases list --instance=INSTANCE_NAME
gcloud sql databases list --instance=mydb1

## Get BACKUP_ID: RUN the command to get 
gcloud sql backups list --instance=mydb1
```

## Step-02: Restore Databases
- Restore to Database Instance: mydb2
```t
# mydb2: Restore to mydb2
gcloud sql backups restore BACKUP_ID --restore-instance=RESTORE_INSTANCE --backup-instance=BACKUP_INSTANCE
gcloud sql backups restore 1705141309136 --restore-instance=mydb2 --backup-instance=mydb1

# Verify mydb2 AFTER restore from mydb1
# List Databases from the Database Instance
gcloud sql databases list --instance=INSTANCE_NAME
gcloud sql databases list --instance=mydb1

# Important Option
--async: Return immediately, without waiting for the operation in progress to complete.
```

