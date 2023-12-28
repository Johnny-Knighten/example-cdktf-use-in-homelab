import pytest
from cdktf import Testing as CDKTFTesting


from imports.proxmox.vm_qemu import VmQemu
from imports.awx.host import Host
from imports.powerdns.record import Record

from stacks.single_vm_stack import SingleVMStack

from defaults.vm import vm_defaults


class TestSingleVMStack:
    pve_config = {
        "address": "https://pve.test.com/",
        "nodes": ["node1"],
        "pm_tls_insecure": True,
    }

    vault_config = {
        "address": "http://vault.test.com/",
        "skip_tls_verify": True,
    }

    pdns_config = {
        "address": "http://dns.test.com/",
        "zone": "test.com",
    }

    awx_config = {
        "address": "http://awx.test.com/",
        "org": "Test",
        "inventory": "Test",
    }

    vm_config = {
        "vm": {
            "name": "Test",
            "target_node": "node1",
            "desc": "Test VM",
        },
        "awx": {
            "name": "Test",
            "desc": "Test VM",
            "awx_groups": [
                "proxmox-hosts",
                "ipa_managed_clients",
            ],
            "fqdn": "test.test.com",
        },
        "dns": {"name": "test"},
    }

    stack_id = "TestStack"

    app = CDKTFTesting.app()

    stack = SingleVMStack(
        app,
        stack_id,
        pve_config,
        pdns_config,
        awx_config,
        vm_config,
        vault_config,
    )

    synthesized = CDKTFTesting.synth(stack)

    def test_check_validity(self):
        assert CDKTFTesting.to_be_valid_terraform(CDKTFTesting.full_synth(self.stack))

    #############
    # PVE Tests #
    #############

    def test_should_contain_proxmox_vm(self):
        assert CDKTFTesting.to_have_resource(self.synthesized, VmQemu.TF_RESOURCE_TYPE)

    def test_proxmox_vm_should_have_assigned_values_and_defaults(self):
        assert CDKTFTesting.to_have_resource_with_properties(
            self.synthesized,
            VmQemu.TF_RESOURCE_TYPE,
            {
                "name": self.vm_config["vm"]["name"],
                "target_node": self.vm_config["vm"]["target_node"],
                "desc": self.vm_config["vm"]["desc"],
                "clone": vm_defaults["clone"],
                "cores": vm_defaults["cores"],
                "cpu": vm_defaults["cpu"],
                "memory": vm_defaults["memory"],
                "ssh_user": vm_defaults["ssh_user"],
                "agent": vm_defaults["agent"],
                "os_type": vm_defaults["os_type"],
                "startup": vm_defaults["startup"],
                "onboot": vm_defaults["onboot"],
                "full_clone": vm_defaults["full_clone"],
                "scsihw": vm_defaults["scsihw"],
                "bootdisk": vm_defaults["bootdisk"],
                "disk": vm_defaults["disk"],
                "ipconfig0": vm_defaults["ipconfig0"],
                "nameserver": vm_defaults["nameserver"],
                "network": vm_defaults["network"],
            },
        )

    #############
    # AWX Tests #
    #############

    def test_should_contain_awx_host(self):
        assert CDKTFTesting.to_have_resource(self.synthesized, Host.TF_RESOURCE_TYPE)

    def test_awx_host_should_have_assigned_values(self):
        assert CDKTFTesting.to_have_resource_with_properties(
            self.synthesized,
            Host.TF_RESOURCE_TYPE,
            {
                "description": self.vm_config["awx"]["desc"],
                "enabled": True,
                "name": self.vm_config["awx"]["name"],
            },
        )

    ##############
    # PDNS Tests #
    ##############

    def test_should_contain_pdns_record(self):
        assert CDKTFTesting.to_have_resource(self.synthesized, Record.TF_RESOURCE_TYPE)

    def test_pdns_record_should_have_assigned_values(self):
        assert CDKTFTesting.to_have_resource_with_properties(
            self.synthesized,
            Record.TF_RESOURCE_TYPE,
            {
                "name": f"{self.vm_config['dns']['name']}.{self.pdns_config['zone']}.",
                "ttl": 60,
                "type": "A",
                "zone": f"{self.pdns_config['zone']}.",
            },
        )
