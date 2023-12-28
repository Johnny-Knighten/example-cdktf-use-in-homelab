from constructs import Construct
from cdktf import TerraformResource

from imports.awx.data_awx_organization import DataAwxOrganization
from imports.awx.data_awx_inventory import DataAwxInventory
from imports.awx.data_awx_inventory_group import DataAwxInventoryGroup

from imports.awx.host import Host as AWXHost

from imports.proxmox.vm_qemu import VmQemu


class AWXRegistration(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        vm_config: dict,
        awx_config: dict,
        vm: VmQemu,
    ):
        super().__init__(scope, id)

        awx_org = DataAwxOrganization(self, "awx-org", name=awx_config["org"])
        awx_inv = DataAwxInventory(
            self, "awx-inv", name=awx_config["inventory"], organization_id=awx_org.id
        )

        group_ids = []
        for index, group_name in enumerate(vm_config["awx_groups"]):
            awx_inv_group = DataAwxInventoryGroup(
                self,
                f"awx_inv_group_{index}",
                name=group_name,
                inventory_id=awx_inv.id,
            )
            group_ids.append(awx_inv_group.id)

        AWXHost(
            self,
            "awx-host",
            name=vm_config["name"],
            description=vm_config["desc"],
            inventory_id=awx_inv.id,
            group_ids=group_ids,
            enabled=True,
            variables=f"""---
ansible_host: {vm.default_ipv4_address}
hostname: {vm_config["fqdn"]}
""",
        )
