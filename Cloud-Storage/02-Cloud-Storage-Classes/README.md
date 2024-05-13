# Cloud Storage - Storage Classes

## Step-01: Introduction
- Discuss and understand Cloud Storage - Storage Classess
- Standard Class
- Nearline Class
- Coldline Class
- Archive Class
- Autoclass

## Step-02: Review Storage classes with Set a default class option
- Nearline Class
- Coldline Class
- Archive Class
- Autoclass

## Step-03: Autoclass with Standard and Nearline
### Step-03-01: Create Bucket with Autosclass enabled
- Goto Cloud Storage -> CREATE BUCKET
- **Bucket name:** mybucket1033
- Goto section `Choose a storage class for your data` and discuss about Autocalss
- **Autoclass:** checked
- Click on **CREATE**
### Step-03-02: Review the Bucket configuration
- Goto Cloud Storage -> mybucket1033 -> CONFIGURATION
- **Observation:** we should see the below
  - Default storage class: Managed by Autoclass
  - Included classes: Standard, Nearline

## Step-04: Autoclass with Standard, Nearline, Coldline and Archive
### Step-04-01: Create Bucket with Autosclass enabled
- Goto Cloud Storage -> CREATE BUCKET
- **Bucket name:** mybucket1034
- Goto section `Choose a storage class for your data` and discuss about Autocalss
- **Autoclass:** checked
- **Opt-in to allow object transitions to Coldline and Archive classes:** checked
- Click on **CREATE**

### Step-04-02: Review the Bucket configuration
- Goto Cloud Storage -> mybucket1034 -> CONFIGURATION
- **Observation:** we should see the below
  - Default storage class: Managed by Autoclass
  - Included classes: Standard, Nearline, Coldline, Archive
