# Google Cloud Firestore Fundamentals

## Step-01: Introduction
- Create a Firestore database using web console 
- Create the following
  - Collection
  - Documents

## Step-02: Web Console: Create Cloud Firestore Instance
- **Important Note:** 
  - Each project may have a single database named “(default)” which qualifies it for free-tier quota. 
  - Once you've exhausted this quota, you're billed based on operations, storage, and network usage
- Go to Cloud Firestore -> **Create Database**
- **Select your Firestore mode:** Native(recommended)
- **Database ID:** (default) or myfirestore1
- **Location:** us-east-1
- **Secure rules:** Test rules
- **SHOW DETAILS:** Review pricing
- Click on **CREATE DATABASE**

## Step-03: Create Collection and Documents
- Go to firstore -> myfirstore1 (or) default -> Data
- **Collection ID:** apps
- Documents
- **Document ID:** myapp1
  - appname: myapp1 (String)
  - apptype: web (String)
  - appversion: 1 (number)
  - appenabled: true  (boolean)
  - appmap: (map)
    - fied1: myfield1value
    - fied2: myfield2value
- Add Similar Document: myapp2


## Step-04: Query Builder
- Query1: WHERE Document name == myapp1
- Query2: WHERE apptype == web
