import os
import sys
import logging
from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.core.exception import AzureError

logging.basicConfig(level=logging.INFO, format=%(asctime)s - %(levelname)s - %(message)s')

TENANT_ID = os.getenv("AZURE_TENANT_ID")
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")

def authenticate_azure():
    """Authenticate with Azure using a service principal."""
    try:
        credential = ClientSecretCredential(
            tenant_id=TENANT_ID,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET
        )
        logging.info("Authentication Successful")
        return credential
    except AzureError as e:
        logging.error(f"Authentication failed: {str(e)}")
        sys.exit(1)

def list_vm_instances(compute_client):
    """List all VM instances"""
    try:
        vms = compute_client.virtual_machines.list_all()
        vm_list = [(vm.name,vm.location) for vm in vms]
        return vm_list
    except AzureError as 0:
        logging.error(f"Failed to list VMs: {str(e)}")
        sys.exit(1)

def start_stop_vm_instances(compute_client, action):
    """Start or stop all VM instances based on user input"""
    vms = list_vm_instances(compute_client)       
    for vm in vms:
        vm_name = vm[0]
        vm_location = vm[1]
        logging.info(f"Processing VM: {vm_name} in {vm_location}")

        if action.lower() == 'start':
           logging.info(f"Starting VM: {vm_name}")
           compute_client.virtual_machines.begin_start(vm_location, vm_name)
        elif action.lower() == 'stop':
            logging.info(f"Stopping VM: {vm_name}")
           compute_client.virtual_machines.begin_power_off(vm_location, vm_name)
        else:
            logging.error("Invalid action. Please choose 'start' or 'stop'.")
            sys.exit(1)
    logging.info(f"All VMs have been {action}ed.")

def main(action):
    credential = authenticate_azure()
    compute_client = ComputeManagementClient(credential, SUBSCRIPTION_ID)
    start_stop_vm_instances(compute_client, action)

if __name__ == " __main__ ":
    if len(sys.argv) !=2:
        logging.error("Usage: python Myfile1.py <start/stop>")
        sys.exit(1)
    action = sys.argv[1]
    main(action)            
