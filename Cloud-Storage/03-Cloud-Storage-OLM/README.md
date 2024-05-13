# Cloud Storage - Object Lifecycle Management

## Step-01: Introduction
- Create Object Lifecycle Management Rules (OLM Rules)
- **Rule-1:** Delete Object OLM Rule
- **Rule-2:** Set storage class to Archive

## Step-02: Create Object Lifecycle Management Rules (OLM Rules)
### Step-02-01: Rule-1: Delete Object OLM Rule
- Upload a folder, that will get deleted using delete object OLM rule.
```t
# Set Project
gcloud config set project PROJECT_ID
gcloud config set project gcplearn9

# Create Copy of myapp2 as myapp3
gcloud storage cp gs://mybucket1032/myapp2/*.html gs://mybucket1032/myapp3/
```
- **Important Note:** After you add or edit a rule, it may take up to 24 hours to take effect.
- Go to Cloud Storage -> mybucket1032 -> LIFECYCLE -> Click on **ADD A RULE**
- **Select an action:** Delete Object
- **Select object conditions**
  - **Set Rule Scopes**
    - **Object name matches prefix:** myapp2
- Click on **CREATE**  

### Step-02-02: Rule-2: Set storage class to Archive
- Go to Cloud Storage -> mybucket1032 -> LIFECYCLE -> Click on **ADD A RULE**
- **Select an action:** Set storage class to Archive
- **Select object conditions**
  - **Set Rule Scopes**
    - **Object name matches prefix:** myapp3
  - **Set Conditions:**
    - **Age:** 10 days    
- Click on **CREATE**  
