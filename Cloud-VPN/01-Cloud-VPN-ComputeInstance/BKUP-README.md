# Cloud VPN - Compute Instances

## Step-01: Introduction

## Step-02: 
kalyanreddydaida

## DELETE
- https://blog.thecloudside.com/configure-site-to-site-vpn-azure-vnet-to-gcp-vpc-4a727ca10726


## Azure Steps
- Create Resource Group: az-gcp-vpn
- Create Virtual Network Gateway: azure-vnet-gateway
  - Create Virtual Network: azurevnet1
    - Add Subnets: 
    - azuresubnet1: 10.0.1.0/24
    - azuresubnet2: 10.0.2.0/24
  - Gateway subnet address range: 10.0.3.0/24
  - Public IP address name: az-vnet-gateway-pip1
  - Availability Zone: zone-redundant
  - Public IP address name: az-vnet-gateway-pip2
  - Availability Zone: zone-redundant
  - ASN: 65515
- **Important Note:** It will take 10 to 20 mins to create azure-vnet-gateway

## GCP VPN Setup
- Create VPC and Subnet (We will use vpc2-custom)
### Create Cloud HA VPN gateway
- VPN Gateway name: gcpvpn
- Network: vpc2-custom
- Region: us-central1
- Click on Create 
### Add VPN tunnels
- Peer VPN gateway: On-prem or Non Google Cloud
- **Create new PEER VPN Gateway**
  - Name: gcp-azure-peer-vpn
  - Interfaces: two interfaces
  - Interface 0 IP Address: 4.255.73.40  (Azure Public IP 1)
  - Interface 1 IP Address: 4.255.73.116 (Azure Public IP 2)
- **High Availability**
  - Create a pair of VPN tunnels
- **Routing options**
  - CREATE NEW CLOUD ROUTER
  - Name: gcp-azure-vpn-cloud-router
  - Description: gcp-azure-vpn-cloud-router
  - Google ASN: 64512
  - BGP keepalive interval: leave empty (which will be 20 seconds as default)
  - Advertised routes: Advertise all subnets visible to the Cloud Router (Default)
  - Click on **CREATE**
- **VPN tunnels** 
- TUNNEL-1 Configs
  - Name: vpn-tunnel1
  - IKE Version: IKEv2
  - IKE Preshared Key: kalyanreddydaida
  - Click on **DONE**
- TUNNEL-2 Configs  
  - Name: vpn-tunnel2
  - IKE Version: IKEv2
  - IKE Preshared Key: kalyanreddydaida
  - Click on **DONE**
- Click **CREATE AND CONTINUE**  
### Configure BGP Sessions
- **CONFIGURE BGP SESSION-1**
  - Name: bgp-session-1
  - PEER ASN: 65515
  - Allocate BGP IPv4 address: Manually
    - Cloud Router BGP IPv4 address: 169.254.21.5
    - BGP peer IPv4 address: 169.254.21.6
    - BGP peer: Enabled
    - MD5 Authentication: Disabled
  - Click on **SAVE AND CONTINUE**
- **CONFIGURE BGP SESSION-2**
  - Name: bgp-session-2
  - PEER ASN: 65515
  - Allocate BGP IPv4 address: Manually
    - Cloud Router BGP IPv4 address: 169.254.22.5
    - BGP peer IPv4 address: 169.254.22.6
    - BGP peer: Enabled
    - MD5 Authentication: Disabled
  - Click on **SAVE AND CONTINUE**    
- Click on **BGP CONFIGURATION**

## Azure: Update Peer IP Address in Azure Virtual Network Gateway
- Goto Virtual Network Gateway -> azure-vnet-gateway -> Configuration
- Custom Azure APIPA BGP IP address: 169.254.21.5
- Second Custom Azure APIPA BGP IP address: 169.254.22.5

## Create Azure Local Network Gateways
### Create Azure Local Network Gateway-1
- **Basics Tab**
  - Resource Group: azure-gcp-vpn
  - Name: az-gcp-lng1
  - IP Address: 34.157.104.44 (GCP VPN Public IP 1)
  - Address Space(s): 10.225.0.0/20 (GCP Subnet address range)
- **Advanced Tab**
  - **Configure BGP settings:** Yes
  - **Autonomous system number (ASN):** 64512 (GCP cloud router BGP ASN)
  - **BGP peer IP address:** 169.254.21.5  (GCP BGP IP1)
- Click on **REVIEW + CREATE**
### Create Azure Local Network Gateway-2
- **Basics Tab**
  - Resource Group: azure-gcp-vpn
  - Name: az-gcp-lng2
  - IP Address: 35.220.84.98 (GCP VPN Public IP 2)
  - Address Space(s): 10.225.0.0/20 (GCP Subnet address range)
- **Advanced Tab**
  - **Configure BGP settings:** Yes
  - **Autonomous system number (ASN):** 64512 (GCP cloud router BGP ASN)
  - **BGP peer IP address:** 169.254.22.5  (GCP BGP IP2)  
- Click on **REVIEW + CREATE**

## Create Connections on Azure Virtual Network Gateway
### Create Connection-1
- **Basics Tab**
  - Resource Group: azure-gcp-vpn
  - Connection type: Site-to-Site(IPSec)
  - Name: azure-gcp-vpn-connection1
  - Region: East US
- **Settings Tab**
  - Virtual network gateway: azure-vnet-gateway
  - Local network gateway: az-gcp-lng1
  - Shared Key (PSK): kalyanreddydaida
  - IKE Protocol: IKEv2
  - Enable BGP: Enabled
- Click on **REVIEW + CREATE**
### Create Connection-2
- **Basics Tab**
  - Resource Group: azure-gcp-vpn
  - Connection type: Site-to-Site(IPSec)
  - Name: azure-gcp-vpn-connection2
  - Region: East US
- **Settings Tab**
  - Virtual network gateway: azure-vnet-gateway
  - Local network gateway: az-gcp-lng2
  - Shared Key (PSK): kalyanreddydaida
  - IKE Protocol: IKEv2
  - Enable BGP: Enabled
- Click on **REVIEW + CREATE**

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