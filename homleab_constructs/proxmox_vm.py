from constructs import Construct

from homleab_constructs.vault_secrets import VaultSecrets

from imports.proxmox.vm_qemu import VmQemu
from imports.proxmox.provider import ProxmoxProvider
from defaults.vm import vm_defaults


class ProxmoxVm(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        vm_config: dict,
        secrets: VaultSecrets,
    ):
        super().__init__(scope, id)

        self.vm = VmQemu(
            self,
            id_="RunnerVm",
            # Required Vars
            name=vm_config["name"],
            target_node=vm_config["target_node"],
            desc=vm_config["desc"],
            # Secrets
            ssh_private_key=secrets.values["ssh_private_key"],
            # Optional Vars
            clone=vm_config.get("clone", vm_defaults["clone"]),
            full_clone=vm_config.get("full_clone", vm_defaults["full_clone"]),
            onboot=vm_config.get("onboot", vm_defaults["onboot"]),
            startup=vm_config.get("startup", vm_defaults["startup"]),
            cores=vm_config.get("cores", vm_defaults["cores"]),
            cpu=vm_config.get("cpu", vm_defaults["cpu"]),
            memory=vm_config.get("memory", vm_defaults["memory"]),
            ssh_user=vm_config.get("ssh_user", vm_defaults["ssh_user"]),
            ipconfig0=vm_config.get("ipconfig0", vm_defaults["ipconfig0"]),
            ipconfig1=vm_config.get("ipconfig1"),
            ipconfig2=vm_config.get("ipconfig2"),
            ipconfig3=vm_config.get("ipconfig3"),
            ipconfig4=vm_config.get("ipconfig4"),
            ipconfig5=vm_config.get("ipconfig5"),
            network=vm_config.get("network", vm_defaults["network"]),
            nameserver=vm_config.get("nameserver", vm_defaults["nameserver"]),
            os_type=vm_config.get("os_type", vm_defaults["os_type"]),
            disk=vm_config.get("disk", vm_defaults["disk"]),
            bootdisk=vm_config.get("bootdisk", vm_defaults["bootdisk"]),
            scsihw=vm_config.get("scsihw", vm_defaults["scsihw"]),
            agent=vm_config.get("agent", vm_defaults["agent"]),
        )
