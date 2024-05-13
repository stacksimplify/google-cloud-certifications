# Cloud BigTable - Basics

## Step-01: Introduction
- Web Console
  - Create Big Table Instance
  - Create Table
- cbt cli  

## Step-02: Create BigTable Instance
- Go to BigTable -> CREATE INSTANCE
- Name your Instance
  - Instance Name: mybigtableins1
  - Instance ID: mybigtableins1
- Select your Storage type: SSD
- Configure your first cluster
  - Select a cluster ID: mybigtableins1-c1
  - Select Location: europe-west10(Berlin) 
  - Zone: Any
- Choose node scaling mode
  - Autoscaling Minimun: 1
  - Autoscaling Maximum: 3
  - CPU utilization target: 60%
  - Storage utilization target: 2.5%
- REST ALL LEAVE TO DEFAULTS  

## Step-03: Create Table in BigTable Instance
- Go to BigTable -> mybigtableins1 -> Instance -> Tables -> CREATE TABLE
- Table ID: mytable1
- Add Column Family
  - Column Family Name: cf1
- Click on **CREATE**

## Step-04: cbt cli: Create BigTable Instance, Table using cbt cli
- [cbt reference](https://cloud.google.com/bigtable/docs/cbt-reference)
```t
# Set Project
gcloud config set project PROJECT_ID
gcloud config set project gcplearn9

# Install cbt cli
gcloud components install cbt
[or]
sudo apt-get install google-cloud-sdk-cbt

# List Instances
cbt listinstances

# Setup Project and BigTable Instance for cbt cli
echo project = PROJECT_ID >> ~/.cbtrc && echo instance = INSTANCE_NAME >> ~/.cbtrc
echo project = gcplearn9 >> ~/.cbtrc && echo instance = mybigtableins1 >> ~/.cbtrc
cat $HOME/.cbtrc

# Create Table (Optional)
cbt createtable mytable1

# List Tables
cbt ls

# Add one column family (Optional)
cbt createfamily mytable1 cf1

# List colum families
cbt ls mytable1

# Write the values test-value1 and test-value2 to the row r1, using the column family cf1 and the column qualifier c1:
cbt set mytable1 r1 cf1:c1=test-value1
cbt set mytable1 r1 cf1:c1=test-value2
cbt set mytable1 r1 cf1:c1=test-value3

# Read the data you added to the table
cbt read mytable1
Important Note: In this demo you set only three cells, but Bigtable lets you set up to 10,000 cells in a single write request.

# Delete Table (DONT DELETE)
cbt deletetable mytable1

# Delete BigTable Instance (DONT DELETE)
cbt deleteinstance mybigtableins1
```


## Additional References
- https://cloud.google.com/bigtable/docs/cbt-reference
- https://cloud.google.com/bigtable/docs/create-instance-write-data-cbt-cli


