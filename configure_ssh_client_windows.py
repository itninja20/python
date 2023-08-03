# configure_ssh_client_windows.py
import os
import platform
import subprocess
import paramiko

# SSH client configurations
SSH_CLIENT_CONFIG_PATH = "/c/Users/jan/.ssh/config"  # Replace with your SSH client config path
VAULT_SSH_ROLE = "ssh_role"  # Vault role name for SSH authentication

def configure_ssh_client_windows():
    client_os = platform.system()
    if client_os != "Windows":
        raise RuntimeError("This script is intended for Windows clients only.")

    # Generate an SSH keypair for Windows clients using paramiko
    private_key_file = "id_rsa"
    public_key_file = "id_rsa.pub"

    key = paramiko.RSAKey.generate(2048)
    key.write_private_key_file(private_key_file)
    with open(public_key_file, "w") as f:
        f.write(f"{key.get_name()} {key.get_base64()}")

    # Set up SSH client to use Vault for SSH authentication
    with open(SSH_CLIENT_CONFIG_PATH, "a") as f:
        f.write(f"\nHost *\n")
        f.write(f"    IdentityFile {os.path.abspath(private_key_file)}\n")
        f.write(f"    ProxyCommand vault-ssh-helper -role={VAULT_SSH_ROLE} -endpoint=http://localhost:8200 %%h")

def main():
    configure_ssh_client_windows()

if __name__ == "__main__":
    main()
