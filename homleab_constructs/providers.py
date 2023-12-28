from constructs import Construct

from homleab_constructs.vault_secrets import VaultSecrets

from imports.proxmox.vm_qemu import VmQemu
from imports.proxmox.provider import ProxmoxProvider
from imports.awx.provider import AwxProvider

from imports.powerdns.provider import PowerdnsProvider


class HomelabProviders(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        pve_config: dict,
        pdns_config: dict,
        awx_config: dict,
        secrets: VaultSecrets,
    ):
        super().__init__(scope, id)

        PowerdnsProvider(
            self,
            id="PDNSProvider",
            server_url=pdns_config["address"],
            api_key=secrets.values["pdns_api_key"],
        )

        ProxmoxProvider(
            self,
            id="PVEProviderr",
            pm_api_url=pve_config["address"],
            pm_user=secrets.values["pm_user"],
            pm_password=secrets.values["pm_password"],
            pm_tls_insecure=pve_config["pm_tls_insecure"],
        )

        AwxProvider(
            self,
            id="AWXProvider",
            hostname=awx_config["address"],
            username=secrets.values["awx_user"],
            password=secrets.values["awx_password"],
            insecure=True,
        )
