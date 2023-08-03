# configure_ssh_server.py
import os
import subprocess

# SSH server configurations
SSH_SERVER_CONFIG_PATH = "/etc/ssh/sshd_config"  # Replace with your SSH server config path
VAULT_SSH_ROLE = "ssh_role"  # Vault role name for SSH authentication

def configure_ssh_server():
    with open(SSH_SERVER_CONFIG_PATH, "a") as f:
        f.write(f"\nTrustedUserCAKeys /etc/ssh/trusted-user-ca-keys.pem\n")
        f.write(f"AuthorizedPrincipalsFile /etc/ssh/authorized_principals/%u\n")

def main():
    configure_ssh_server()
    subprocess.run(["systemctl", "restart", "sshd"])

if __name__ == "__main__":
    main()
