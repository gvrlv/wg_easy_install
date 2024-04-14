# WireGuard easy install

Ansible playbooks to quickly setup a WireGuard via python `bootstrap.py` script.
Playbooks are designed to be run on a fresh install of Ubuntu.
The playbooks will update the system, install Docker, and then deploy the Docker WireGuard container.

# Requirements
- Ansible
- Python 3.x

# Bootstrap script

To use the `bootstrap.py` script, simply run it with the required command-line arguments:

```shell
python3 bootstrap.py \
    --server-ip <server IP address> \
    --ssh-key-path <SSH key path> \
    --wg-password <WireGuard password> \
    --username <username> \
    --data-dir <data directory> \
    --tcp-port <TCP port> \
    --udp-port <UDP port>
```

- `--username`: The username to use when connecting to the server via SSH. The default value is `root`.
- `--server-ip`: The IP address of the server to connect to via SSH. This argument is required.
- `--ssh-key-path`: The path to the SSH key to use when connecting to the server. This argument is required.
- `--data-dir`: The directory where data will be stored. The default value is `data`.
- `--wg-password`: The password to use for the WireGuard configuration. This argument is required.
- `--tcp-port`: The TCP port to use for the WireGuard connection. The default value is `80`.
- `--udp-port`: The UDP port to use for the WireGuard connection. The default value is `51820`.
