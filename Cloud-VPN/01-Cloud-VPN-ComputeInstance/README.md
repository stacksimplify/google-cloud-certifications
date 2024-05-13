# Cloud VPN - Compute Instances

## Step-01: Introduction
- https://blog.thecloudside.com/configure-site-to-site-vpn-azure-vnet-to-gcp-vpc-4a727ca10726
- BGP SESSION FAILING

## Step-02: AZURE CLOUD: Create Resource Group
- **Subscription:** StackSimplify-Paid-Subscription
- **Resource group:** azure-gcp-vpn
- **Resource details:** East US
- Click on **Review + Create**

## Step-03: AZURE CLOUD: Create Virtual Network Gateway
- Goto Virtual Network Gateways -> Create
### Basics Tabs
- **Project details**
  - **Subscription:** StackSimplify-Paid-Subscription
  - **Resoruce Group:** Select a virtual network to get resource group
- **Instance details**
  - **Name:** azure-vnet-gateway
  - **Region:** East US
  - **Gateway type:** VPN
  - **SKU:** VpnGw2AZ
  - **Generation:** Generation2
  - **Virtual Network:** azurevnet1
    - **Name:** azurevnet1
    - **Resoruce Group:** azure-gcp-vpn
    - **Address space:** 10.0.0.0/16
    - **default subnet:** 10.0.0.0/24
    - REST ALL DEFAULTS and Click **OK**
  - **Gateway subnet address range:** 10.0.1.0/24 (Auto-created and auto-populated)
- **Public IP address**
  - Public IP address: Create new
  - Public IP address name: azure-gcp-vpn-pip1
  - Public IP address SKU: standard
  - Assignment: Static
  - Availability Zone: Zone-Redundant
  - Enable active-active mode: Enabled
- **Second Public IP address**
  - Second Public IP address: Create new
  - Public IP address name: azure-gcp-vpn-pip1
  - Public IP address SKU: standard
  - Assignment: Static
  - Availability Zone: Zone-Redundant
  - Enable active-active mode: Enabled
- **Configure BGP:** Enabled
  - **Autonomous system number (ASN):** 65515
  - **Custom Azure APIPA BGP IP address:** 169.254.21.5
  - **Second Custom Azure APIPA BGP IP address:** 169.254.22.5
- Click on **REVIEW + CREATE**
- Click on **CREATE**  
- **IMPORTANT NOTE:** It will take 15 to 20 minutes to creat the Azure Virtual Network Gateway

## Step-04: GOOGLE CLOUD: VPN Setup
- **Pre-requisite-1:** Create Cloud VPC and Subnet (We will use VPC: vpc2-custom and Subnet: mysubnet1-10.225.0.0/20)
- **Pre-requisite-2:** Make a note of Azure Public IPs used for Azure Virtual Network Gateway
  - **Azure VPN Public IP 1:** 4.156.106.42 
  - **Azure VPN Public IP 2:** 4.156.106.56 
- Goto Network Connectivity -> VPN -> **CREATE VPN CONNECTION**
- **VPN Options:** High-availability (HA) VPN 
- Click on **CONTINUE**
### Create Cloud HA VPN gateway
- **VPN Gateway name:** gcpvpn1
- **Network:** vpc2-custom
- **Region:** us-central1
- **VPN tunnel inner IP stack type:** IPv4(single stack)
- Click on **CREATE AND CONTINUE**
### Add VPN tunnels
- **Peer VPN gateway:** On-prem or Non Google Cloud
- **Create new PEER VPN Gateway**
  - **Name:** gcp-azure-peer-vpn1
  - **Interfaces:** two interfaces
  - **Interface 0 IP Address:** 4.156.106.42  (Get VPN Azure Public IP 1)
  - **Interface 1 IP Address:** 4.156.106.56 (Get VPN Azure Public IP 2)
  - Click on **CREATE**
- **High Availability**
  - **Create a pair of VPN tunnels:** Enabled
- **Routing options**
  - Click on **CREATE NEW CLOUD ROUTER**
  - **Name:** gcp-azure-vpn-cloud-router1
  - **Description:** gcp-azure-vpn-cloud-router1
  - **Google ASN:** 64512
  - **BGP keepalive interval:** 20 (which will be 20 seconds as default)
  - **Advertised routes: Advertise all subnets visible to the Cloud Router (Default)
  - Click on **CREATE**
- **VPN tunnels** 
  - **TUNNEL-1 Configs**
    - **Name:** vpn-tunnel1
    - **IKE Version:** IKEv2
    - **IKE Preshared Key:** kalyanreddydaida
    - Click on **DONE**
  - **TUNNEL-2 Configs**
    - **Name:** vpn-tunnel2
    - **IKE Version:** IKEv2
    - **IKE Preshared Key:** kalyanreddydaida
    - Click on **DONE**
  - Click **CREATE AND CONTINUE**  
### Configure BGP Sessions
- **CONFIGURE BGP SESSION-1**
  - **Name:** bgp-session-1
  - **PEER ASN:** 65515
  - **Allocate BGP IPv4 address:** Manually
    - **Cloud Router BGP IPv4 address:** 169.254.21.5
    - **BGP peer IPv4 address:** 169.254.21.6
    - **BGP peer:** Enabled
    - **MD5 Authentication:** Disabled
  - Click on **SAVE AND CONTINUE**
- **CONFIGURE BGP SESSION-2**
  - **Name:** bgp-session-2
  - **PEER ASN:** 65515
  - **Allocate BGP IPv4 address:** Manually
    - **Cloud Router BGP IPv4 address:** 169.254.22.5
    - **BGP peer IPv4 address:** 169.254.22.6
    - **BGP peer:** Enabled
    - **MD5 Authentication:** Disabled
  - Click on **SAVE AND CONTINUE**    
### SUMMARY and Reminder  
- Click on **DOWNLOAD CONFIGURATION**
- **Vendor:** Other
```t
# Configure your peer-side device to access your VPC networks with the following information:

# vpn-tunnel1
Cloud Router BGP IP: 169.254.21.5
BGP peer IP: 169.254.21.6
Peer ASN: 64512

# vpn-tunnel2
Cloud Router BGP IP: 169.254.22.5
BGP peer IP: 169.254.22.6
Peer ASN: 64512
```
- Click on **OK**

## Step-05: AZURE CLOUD: Create Azure Local Network Gateways
- **Pre-requisite-2:** Make a note of Google Cloud Public IPs used for GCP VPN
  - **GCP VPN Public IP 1:** 34.157.104.44
  - **GCP VPN Public IP 2:** 35.220.84.98
### Create Azure Local Network Gateway-1
- **Basics Tab**
  - **Resource Group:** azure-gcp-vpn
  - **Region:** East US
  - **Name:** az-gcp-lng1
  - **IP Address:** 34.157.104.44 (Get GCP VPN Public IP 1)
  - **Address Space(s):** 10.225.0.0/20 (Get GCP Subnet mysubnet1 address range from VPC: vpc2-custom)
- **Advanced Tab**
  - **Configure BGP settings:** Yes
  - **Autonomous system number (ASN):** 64512 (GCP cloud router BGP ASN)
  - **BGP peer IP address:** 169.254.21.5  (GCP BGP IP1)
- Click on **REVIEW + CREATE**
### Create Azure Local Network Gateway-2
- **Basics Tab**
  - **Resource Group:** azure-gcp-vpn
  - **Region:** East US  
  - **Name:** az-gcp-lng2
  - **IP Address:** 35.220.84.98 (Get GCP VPN Public IP 2)
  - **Address Space(s):** 10.225.0.0/20 (Get GCP Subnet mysubnet1 address range from VPC: vpc2-custom)
- **Advanced Tab**
  - **Configure BGP settings:** Yes
  - **Autonomous system number (ASN):** 64512 (GCP cloud router BGP ASN)
  - **BGP peer IP address:** 169.254.22.5  (GCP BGP IP2)  
- Click on **REVIEW + CREATE**

## Step-06: AZURE CLOUD: Create Connections on Azure Virtual Network Gateway
### Create Connection-1
- **Basics Tab**
  - **Resource Group:** azure-gcp-vpn
  - **Connection type:** Site-to-Site(IPSec)
  - **Name:** azure-gcp-vpn-connection1
  - **Region:** East US
- **Settings Tab**
  - **Virtual network gateway:** azure-vnet-gateway
  - **Local network gateway:** az-gcp-lng1
  - **Shared Key (PSK):** kalyanreddydaida
  - **IKE Protocol: IKEv2
  - **Enable BGP:** Enabled
- Click on **REVIEW + CREATE**
### Create Connection-2
- **Basics Tab**
  - **Resource Group:** azure-gcp-vpn
  - **Connection type:** Site-to-Site(IPSec)
  - **Name:** azure-gcp-vpn-connection2
  - **Region:** East US
- **Settings Tab**
  - **Virtual network gateway:** azure-vnet-gateway
  - **Local network gateway:** az-gcp-lng2
  - **Shared Key (PSK):** kalyanreddydaida
  - **IKE Protocol:** IKEv2
  - **Enable BGP:** Enabled
- Click on **REVIEW + CREATE** and Click on **CREATE**

## Verify GCP VPN Tunnels
- Goto -> Network Connectivity -> VPN -> CLOUD VPN TUNNELS Tab
- Both VPN Tunnel Status should be enabled



## GCP VM: Create a VM Instance with Internal-Only IP Address
```t
# Set Project
gcloud config set project PROJECT_ID
gcloud config set project gcplearn9

# Create VM in mysubnet2pca without External IP Address
gcloud compute instances create mygcpvm1 \
    --zone=us-central1-a \
    --machine-type=e2-micro \
    --network-interface=subnet=mysubnet1,no-address
   
# Connect to VM using gcloud
gcloud compute ssh --zone "us-central1-a" "mygcpvm1" --tunnel-through-iap 

# Ping to any Internet URL
ping stacksimplify.com
ping google.com
Observation:
1. Should fail, because VM dont have internet access

# Try and Install any package
sudo apt install -y telnet
Observation:
1. Should fail, because VM dont have internet access to download and install package
```

## Azure VM: Create Azure VM Instance
- 