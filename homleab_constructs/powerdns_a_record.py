from constructs import Construct
from imports.powerdns.record import Record

from imports.proxmox.vm_qemu import VmQemu
from imports.powerdns.provider import PowerdnsProvider

from homleab_constructs.vault_secrets import VaultSecrets


class PDNSARecord(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        pdns_config: dict,
        vm_config: dict,
        vm: VmQemu,
    ):
        super().__init__(scope, id)

        Record(
            self,
            "ARecord",
            zone=f'{pdns_config["zone"]}.',
            name=f'{vm_config["name"]}.{pdns_config["zone"]}.',
            type="A",
            ttl=60,
            records=[vm.default_ipv4_address],
        )
