vm_config = {
    "name": "github-runner",
    "target_node": "alpha",
    "ssh_user": "service-account",
    "desc": "GitHub Runner",
    "cores": 8,
    "memory": 16384,
    "nameserver": "192.168.2.1",
    "disk": [
        {
            "type": "scsi",
            "storage": "local-zfs",
            "size": "100G",
        }
    ],
    "ipconfig0": "ip=192.168.2.100/24,gw=192.168.2.1",
    "network": [
        {
            "model": "virtio",
            "bridge": "vmbr0",
            "tag": 2,
            "queues": 4,
        }
    ],
}

dns_config = {
    "name": "ghrunner",
}

awx_config = {
    "name": vm_config["name"],
    "desc": vm_config["desc"],
    "awx_groups": [
        "proxmox-hosts",
        "docker-hosts",
    ],
    "fqdn": f'{dns_config["name"]}.homelab.lan',
}

config = {
    "vm": vm_config,
    "awx": awx_config,
    "dns": dns_config,
}
