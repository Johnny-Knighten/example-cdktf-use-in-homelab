from constructs import Construct

from cdktf_cdktf_provider_vault.provider import VaultProvider
from cdktf_cdktf_provider_vault.data_vault_generic_secret import DataVaultGenericSecret


class VaultSecrets(Construct):
    def __init__(self, scope: Construct, id: str, vault_config: dict):
        super().__init__(scope, id)

        VaultProvider(
            scope,
            "VaultProvider",
            address=vault_config["address"],
            skip_tls_verify=vault_config["skip_tls_verify"],
        )

        pve_credentials = DataVaultGenericSecret(
            self, "PVECredSecrets", path="kv/homelab-pve-terraform-agent"
        )

        pve_template_ssh_key = DataVaultGenericSecret(
            self, "PVESSHSecrets", path="kv/homelab-packer-ansible-sa"
        )

        pdns_api_key = DataVaultGenericSecret(self, "PDNSCredSecrets", path="kv/pdns")

        awx_credentials = DataVaultGenericSecret(self, "AWXCredSecrets", path="kv/awx")

        self.values = {
            "pm_user": pve_credentials.data.lookup("username"),
            "pm_password": pve_credentials.data.lookup("password"),
            "ssh_private_key": pve_template_ssh_key.data.lookup("ssh-key"),
            "pdns_api_key": pdns_api_key.data.lookup("terraform_api_key"),
            "awx_user": awx_credentials.data.lookup("terraform-user"),
            "awx_password": awx_credentials.data.lookup("terraform-password"),
        }
