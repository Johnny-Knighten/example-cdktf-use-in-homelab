# Example of Using CDKTF To Manage Homelab Infrastructure

This is an example of using [CDKTF](https://developer.hashicorp.com/terraform/cdktf) to manage my homelab's infrastructure. It is a curated vertical slice snippet from the actual repoI use for my homelab; that is, this is a very limited and focused example.

There wasn't many examples of using CDKTF for homelab infrastructure purposes, so I decided to share a little about what I have created. I hope this helps others get started with CDKTF.

In this example I will be using Python, but this should be easily adapted to any language supported by CDKTF.

## Homelab Infrastructure Guidelines

The following guidelines are used to define our CDKTF automation scope:

1. [ProxMox](https://www.proxmox.com/en/) is used as the primary hypervisor,
   - More Specifically Qemu VMs are our core building blocks
2. Every VM is has an associated DNS A record
   - [Power DNS](https://www.powerdns.com/) will be our DNS technology of choice
3. Every VM is registered with [AWX](https://github.com/ansible/awx), to enable automation workflows using the VM
4. All secrets are stored in [Hashicorp Vault](https://www.vaultproject.io/)

## Terraform Providers Used

The following providers are used in this example:

- [telmate/proxmox](https://registry.terraform.io/providers/Telmate/proxmox/latest/docs)
- [pan-net/powerdns](https://registry.terraform.io/providers/pan-net/powerdns/latest)
- [denouche/awx](https://registry.terraform.io/providers/denouche/awx/latest)
- [hasicorp/vault](https://registry.terraform.io/providers/hashicorp/vault/latest)

**Remember - any existing terraform providdred can be used with CDKTF**

## Project Layout

Here are the core project directories and files:

```
config             - python dicts of configuration data
defaults           - python dicts of default values
homelab_constructs - modular/extendable classes used to make up CDKTF
stacks             - CDKTF stacks (i.e. collections of constructs that make up a single unit of infrastructure)
tests              - pytest tests that cover the CDKTF stacks and constructs
main.py            - main entry point for CDKTF
```

## How To Use

The primary goal of this repo is to be a reference for others to use, it was not intended to be directly used or executed. However, in the very unlikely coincidence that you are using the same set of technologies found in this repo, read below how to use it.

This example uses a `GithubRunner` stack as an example.

### Prerequisites

Have the following dependencies already installed:

- Terraform
- CDKTF
- Python
- Node
- Git

### Required Secrets

You most provide the Vault token via an environment variable:

```bash
export VAULT_TOKEN=ACCESS-TOKEN-HERE
```

### Execution

Assuming you are positioned in the project root directory:

```bash
cdktf get
pip install -r requirements.txt
cdktf plan GithubRunner
cdktf deploy GithubRunner
```

### Modifying/Extending This Example

To add more stacks based on `SingleVMStack`, then just implement the required config dict then add a new instances of `SingleVMStack` in `main.py` that uses your config. Look at `./config/vm/github_runner.py` for an example cofnig dict for a `SingleVMStack`.

To introduce more constructs, create a new class in `homelab_constructs` and then add it to the `SingleVMStack` class or a another stack class if desired. To add new providers use the `cdktf provider` to add them to the project; you then will need to inspect the imported provider code inside the `imports` directory to determine how to use them inside your stacks and constructs.

**Always remember that you can import any existing terraform provider and use it in your CDKTF code.**

## Local Development via Dev Container

In this repo is also a dev container configuration that can be used to develop locally. This is the same dev container I use to develop this repo. I highly recommend using it if you are going to be developing CDKTF code. Essentially, instead of cluttering your own system with all the configs/tools needed for development, you bake all that inside  a container and use it for development. This feature is provided by VSCode, and I think Jetbrains IDEs also support it.

## Integrating With Github Actions

The way I have my Github actions setup is opinionated. I prefer to make all executions of my workflows to be triggered manually. The main motivation for this is that my infrastructure code doesn't change frequently and there is very little chance of anything drifting. I want to always be in control when a infrastructure change occurs.

### Github Actions Secrets

Inject the `VAULT_TOKEN` secret into the Github Actions workflow. This is done by navigating to the repo's settings and then selecting `Secrets and variables` from the left menu and selecting the `Actions` menu item. Then create a new repository secret with the name `VAULT_TOKEN` and the value of the token.


### Local Github Runner

I have a local Github runner setup on my homelab. This is done by following the [official documentation](https://docs.github.com/en/actions/hosting-your-own-runners/adding-self-hosted-runners). I have the runner configured to run as a service and to start on boot. 

This setup allows me to run Github Actions locally, which allows it to interact with my local infrastructure and tools (ie. you will notice that I store by TF state in a protected NFS share). It is possible to use normal Github Runners, but you will need to expose your local infrastructure to the internet. I don't recommend this, but it is possible.

I also prefer to run all my steps in a container and try to keep the runner host itself as clean as I can. Below you will see that I use the `ghcr.io/catthehacker/ubuntu:act-22.04` image everywhere. This image was chosen because it is the same image used by [`netkos/act`](https://github.com/nektos/act) which is a tool I use to test Github Actions locally.

**In all the examples below if you introduce new stacks you will need it to the options array.**

### Lint, Test, and Plan Workflow

```yaml
---
name: Manaul Lint, Test, and Plan
run-name: Lint/Test/Plan for ${{ github.event.inputs.stackName }}

on:
  workflow_dispatch:
    inputs:
      stackName:
        type: choice
        required: true
        description: "Stack to Deploy"
        options:
          - GithubRunner

permissions:
  contents: read
  pull-requests: write

jobs:
  lint:
    runs-on: self-hosted
    container: ghcr.io/catthehacker/ubuntu:act-22.04
    steps:
      - name: Checkout Repo
        uses: actions/checkout@v3

      - name: Ensure Python 3.10 Is Installed For Linting
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Lint Python Files Using Black
        uses: psf/black@stable
        with:
          options: "--check --verbose"
          src: "./"
          version: "~= 23.0"

  test:
    runs-on: self-hosted
    container: ghcr.io/catthehacker/ubuntu:act-22.04
    needs:
      - lint
    steps:
      - name: Checkout Repo
        uses: actions/checkout@v3

      - name: Install Terraform
        uses: hashicorp/setup-terraform@v3

      - uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Generate module and provider bindings
        run: npx cdktf-cli get

      - name: Ensure Python 3.10 Is Installed For Testing
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Install Python Dependencies
        run: pip install -r requirements.txt

      - name: CDKTF Tests
        run: |
          pytest -v

  plan:
    runs-on: self-hosted
    container:
      image: ghcr.io/catthehacker/ubuntu:act-22.04
      volumes:
        - /nfs/nas/tf-state/homelab:/nfs/nas/tf-state/homelab
    needs:
      - test
    steps:
      - name: Checkout Repo
        uses: actions/checkout@v3

      - name: Install Terraform
        uses: hashicorp/setup-terraform@v3

      - uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Generate module and provider bindings
        run: npx cdktf-cli get

      - name: Ensure Python 3.10 Is Installed For Deployment
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Install Python Dependencies
        run: pip install -r requirements.txt

      - name: Generate Plan
        uses: hashicorp/terraform-cdk-action@v1
        env:
          VAULT_TOKEN: ${{ secrets.VAULT_TOKEN }}
        with:
          cdktfVersion: 0.19.2
          terraformVersion: 1.6.6
          mode: plan-only
          stackName: ${{ github.event.inputs.stackName }}
          githubToken: ${{ secrets.GITHUB_TOKEN }}
```

### Deploy Workflow

```yaml
---
name: Manual Deploy
run-name: Manual Deploy for ${{ github.event.inputs.stackName }}

on:
  workflow_dispatch:
    inputs:
      stackName:
        type: choice
        required: true
        description: "Stack to Deploy"
        options:
          - GithubRunner

permissions:
  contents: read
  pull-requests: write
  issues: read

jobs:
  deploy:
    runs-on: self-hosted
    container:
      image: ghcr.io/catthehacker/ubuntu:act-22.04
      volumes:
        - /nfs/nas/tf-state/homelab:/nfs/nas/tf-state/homelab
    steps:
      - name: Checkout Repo
        uses: actions/checkout@v3

      - name: Install Terraform
        uses: hashicorp/setup-terraform@v3

      - uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Generate module and provider bindings
        run: npx cdktf-cli get

      - name: Ensure Python 3.10 Is Installed For Deployment
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Install Python Dependencies
        run: pip install -r requirements.txt

      - name: Deploy with CDKTF
        uses: hashicorp/terraform-cdk-action@v1
        env:
          VAULT_TOKEN: ${{ secrets.VAULT_TOKEN }}
        with:
          cdktfVersion: 0.19.2
          terraformVersion: 1.6.6
          mode: auto-approve-apply
          stackName: ${{ github.event.inputs.stackName }}
          githubToken: ${{ secrets.GITHUB_TOKEN }}
```