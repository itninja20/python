# setup_vault_ssh.py
import hvac
import os

# Vault configurations
VAULT_ADDRESS = "http://192.168.1.1:8200"
VAULT_TOKEN = "your_vault_token"  # Replace with your Vault token

# SSH key configurations
SSH_KEY_PATH = "/path/to/ssh/key"  # Replace with the path to your SSH key
VAULT_SSH_ROLE = "ssh_role"  # Vault role name for SSH authentication

def main():
    # Connect to Vault
    client = hvac.Client(url=VAULT_ADDRESS, token=VAULT_TOKEN)

    # Enable the SSH secrets engine in Vault
    client.sys.enable_secrets_engine(backend_type="ssh")

    # Load the SSH key from the file
    with open(SSH_KEY_PATH, "r") as f:
        ssh_private_key = f.read()

    # Store the SSH key as a Vault role
    client.secrets.ssh.create_or_update_role(
        name=VAULT_SSH_ROLE,
        key_type="otp",
        default_user="vault",
        cidr_list="0.0.0.0/0",
        allowed_users="*",
        key=ssh_private_key,
    )

    print("Vault SSH setup completed.")

if __name__ == "__main__":
    main()
