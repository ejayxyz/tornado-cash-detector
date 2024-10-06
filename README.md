# Tornado Cash Detector

Simple tornado cash detector by given  block number and tornado cash address. For the script to work, it is necessary that the given RPC Geth node has the debug namespace enabled, because the `debug_traceBlockByNumber` method is part of the debug API.

Manually tested blocks are `20031962`, `17475649`, `20877171` with the given `0x47ce0c6ed5b0ce3d3a51fdb1c52dc66a7c3c2936` tornado cash address.

With minor improvements, this script can be used to detect any ERC20 token transfer to or from a specific address.

## Prerequisites

Ensure you have the following tools installed on your system:

1. **`web3`**: A library for interacting with the Ethereum blockchain.
2. **`python-dotenv`**: A library to manage environment variables.

#### Optional
1. **`pipx`**: A tool to install and run Python applications in isolated environments.
2. **`virtualenv`**: A tool to create isolated Python environments for different projects.

## Installation

### 1. Install `pipx`
*If you skipped the Optional part you can jump ahead to [Install dependencies](#4-install-dependencies).*

[Pipx Docs](https://pypi.org/project/pipx/)

```bash
brew install pipx
pipx ensurepath
```

### 2. Install `virtualenv`

[Virtualenv Docs](https://virtualenv.pypa.io/en/latest/installation.html)



```bash
pipx install virtualenv
```

### 3. Create a virtual environment

```bash
virtualenv venv
```
Also activate the virtual environment

```bash
source venv/bin/activate
```

### 4. Install dependencies

Install `web3` and `python-dotenv`

```bash
pip install web3 python-dotenv
```

### 5. Set up environment variables


Create a `.env` file in the root directory of the project and add the following environment variables:

```bash 
RPC_URL=
TORNADO_CASH_ADDRESS=
```
*Make sure you use the correct env variables, for example try to check and unset the env variables if you have any issues.*


### 6. Run the script

```bash
python main.py
```

