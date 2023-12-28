vm_defaults = {
    "clone": "packer-built-image",
    "cores": 2,
    "cpu": "host",
    "memory": 4096,
    "ssh_user": "service-account",
    "agent": 1,
    "os_type": "cloud-init",
    "startup": "",
    "onboot": False,
    "full_clone": True,
    "scsihw": "virtio-scsi-pci",
    "bootdisk": "scsi0",
    "disk": [
        {
            "type": "scsi",
            "storage": "local-zfs",
            "size": "40G",
        }
    ],
    "ipconfig0": "ip=dhcp",
    "nameserver": "192.168.1.1",
    "network": [
        {
            "model": "virtio",
            "bridge": "vmbr0",
            "tag": -1,
            "queues": 0,
        }
    ],
}
