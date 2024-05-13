# AlloyDB for PostgreSQL - Basics

## Step-01: Introduction
- Create AlloyDB Cluster
- Create GCE VM instance to connect to AlloyDB Cluster using Private Service Connection with psql client
- Review Backup options
- Delete GCE VM and AlloyDB Cluster

## Step-02: Create AlloyDB Cluster
- Goto -> AlloyDB -> CREATE CLUSTER
### Choose a cluster configuration to start with: 
- Select Option: Highly available with read pool(s)
### Configure your cluster
- Basic info
  - Cluster ID: myalloydb1
  - Password: mypassword11
  - Database version: PostgreSQL 15 compatible
  - Location: us-central1
  - Networking: default
  - **Important Note:** Private services access connection for network default has been successfully created. You will now be able to use the same network across all your project's managed services
  - Data Protection: 
    - Google-managed continuous data protection: ON
    - Recovery Window: 14 days
  - Encryption Options: Google managed encryption key or CMEK    
### Configure your cluster
- Basic info: myprimaryinstance1
- Machine: 2vCPU, 16GB
### Add Read Pool Instances (OPTIONAL)
- Read pool Instance ID: myreadpool1
- Node count: 1
- Machine: 2vCPU, 16GB
- Click on ***ADD READ POOL**
- Click on **CREATE CLUSTER**

## Step-03: Create GCE VM Instance
- Create a VM Instance in default VPC and default subnet

## Step-04: Install psql client
```t
# Install psql client
sudo apt-get update
sudo apt-get install postgresql-client
```

## Step-05: Connect to AlloyDB Cluster and Execute DB Commands
```t
# Connect to AlloyDB Cluster
psql -h IP_ADDRESS -U USERNAME
psql -h 10.80.1.2 -U postgres

# Create Database
CREATE DATABASE mydatabase;

# Connect to Database
\c mydatabase

# Create Table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL
);

# Insert Data in to Table
INSERT INTO users (username, email) VALUES ('myuser1', 'myuser1@example.com');
INSERT INTO users (username, email) VALUES ('myuser2', 'myuser2@example.com');

# Query Data
SELECT * FROM users;

# Update Data
UPDATE users SET email = 'john.doe@example.com' WHERE username = 'myuser1';

# Delete Data
DELETE FROM users WHERE username = 'myuser1';

# Quit PostgreSQL
\q
```

## Step-06: Data Protection Tab
- Review Continuous Backups
- Review about Create Backup options

## Step-07: Clean-Up
- Delete GCE VM Instance
- Delete AlloyDB Primary Instance
- Delete AlloyDB Cluster


