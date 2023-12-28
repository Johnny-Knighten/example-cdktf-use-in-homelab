#!/usr/bin/env python
from cdktf import App

from config.awx import awx_config
from config.pdns import pdns_config
from config.pve import pve_config
from config.vault import vault_config
from config.vm.github_runner import config as github_runner_config

from stacks.single_vm_stack import SingleVMStack

app = App()
SingleVMStack(
    app,
    "GithubRunner",
    pve_config,
    pdns_config,
    awx_config,
    github_runner_config,
    vault_config,
)

app.synth()
