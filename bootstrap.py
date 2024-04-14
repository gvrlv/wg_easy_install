#!/usr/bin/env python3

import argparse
import subprocess


def run_command(command):
    '''
    Run a command using subprocess.run and raise an exception
     if the command fails.

    Args:
        command (list): List containing the command and its arguments.
    '''
    try:
        subprocess.run(command, check=True)
    except Exception as err:
        raise ValueError(f'Can\'t run command: {err}')


def run_ansible_playbook(variables):
    '''
    Run an Ansible playbook with the specified variables.

    Args:
        variables (str): String containing the variables to pass to
         the Ansible playbook.
    '''
    command = [
        'ansible-playbook',
        'main.yml',
        '--extra-vars',
        f'{variables}',
    ]
    run_command(command)


def set_variables(
    username,
    wg_server_ip,
    wg_password,
    data_dir,
    tcp_port,
    udp_port,
    ssh_key_path,
):
    '''
    Set variables for the Ansible playbook.

    Args:
        username (str): Username for the playbook.
        wg_server_ip (str): Server IP address for the playbook.
        wg_password (str): WireGuard password for the playbook.
        data_dir (str): Data directory for the playbook.
        tcp_port (int): TCP port for the playbook.
        udp_port (int): UDP port for the playbook.
        ssh_key_path (str): SSH key path for the playbook.

    Returns:
        str: String containing the formatted variables.
    '''
    variables = {
        'USERNAME': username,
        'WG_SERVER_IP_ADDRESS': wg_server_ip,
        'WG_PASSWORD': wg_password,
        'DATA_DIR': data_dir,
        'WG_WEB_TCP_PORT': tcp_port,
        'WG_WEB_UDP_PORT': udp_port,
        'WG_SERVER_SSH_KEY_PATH': ssh_key_path,
    }

    return ' '.join(f"{key}='{value}'" for key, value in variables.items())


def parse_args():
    '''
    Parse command-line arguments using argparse.

    Returns:
        argparse.Namespace: Parsed arguments.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', type=str, default='root')
    parser.add_argument('--server-ip', type=str, required=True)
    parser.add_argument('--ssh-key-path', type=str, required=True)
    parser.add_argument('--data-dir', type=str, default='data')
    parser.add_argument('--wg-password', type=str, required=True)
    parser.add_argument('--tcp-port', type=int, default=80)
    parser.add_argument('--udp-port', type=int, default=51820)
    return parser.parse_args()


def main():
    '''
    Main function to parse arguments, set variables, and run the Ansible playbook.
    '''
    args = parse_args()

    variables = set_variables(
        args.username,
        args.server_ip,
        args.wg_password,
        args.data_dir,
        args.tcp_port,
        args.udp_port,
        args.ssh_key_path,
    )

    run_ansible_playbook(variables)


if __name__ == '__main__':
    main()
