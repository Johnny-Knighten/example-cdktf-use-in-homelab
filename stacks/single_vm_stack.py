from constructs import Construct

from homleab_constructs.proxmox_vm import ProxmoxVm
from homleab_constructs.powerdns_a_record import PDNSARecord
from homleab_constructs.awx_registration import AWXRegistration
from homleab_constructs.vault_secrets import VaultSecrets
from homleab_constructs.providers import HomelabProviders


from cdktf import TerraformStack

from homleab_constructs.proxmox_vm import ProxmoxVm
from homleab_constructs.powerdns_a_record import PDNSARecord
from homleab_constructs.awx_registration import AWXRegistration
from homleab_constructs.vault_secrets import VaultSecrets
from homleab_constructs.providers import HomelabProviders



class SingleVMStack(TerraformStack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        pve_config: dict,
        pdns_config: dict,
        awx_config: dict,
        vm_config: dict,
        vault_config: dict,
    ):
        super().__init__(scope, id)

        secrets = VaultSecrets(self, "VaultSecrets", vault_config)

        HomelabProviders(
            self, "HomelabProviders", pve_config, pdns_config, awx_config, secrets
        )

        pve_vm = ProxmoxVm(self, "PVEVM", vm_config["vm"], secrets)

        PDNSARecord(self, "PDNSARecord", pdns_config, vm_config["dns"], pve_vm.vm)

        AWXRegistration(
            self,
            "AWXRegistration",
            vm_config["awx"],
            awx_config,
            pve_vm.vm,
        )
