# install_vault_on_kali.py
import os
import requests
import subprocess

def setup_vault_apt_repo():
    # Fetch the HashiCorp Vault apt repository URL from the HashiCorp API
    api_url = "https://releases.hashicorp.com/index.json"
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()

    # Get the latest version of Vault from the API response
    latest_version = data.get("vault", {}).get("versions", [])[0].get("version")
    if not latest_version:
        raise RuntimeError("Unable to fetch the latest version of Vault from the HashiCorp API.")

    # Construct the Vault apt repository URL for Kali Linux
    repo_url = f"https://releases.hashicorp.com/vault/{latest_version}/vault_{latest_version}_linux_arm64.deb"

    # Add the Vault apt repository to the sources list
    with open("/etc/apt/sources.list", "a") as sources_list:
        sources_list.write(f"deb {repo_url} /")

    print("Vault apt repository added to sources list.")

def install_vault():
    subprocess.run(["sudo", "apt", "update"])
    subprocess.run(["sudo", "apt", "install", "vault"])

def main():
    try:
        setup_vault_apt_repo()
        install_vault()
        print("Vault installation completed.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
