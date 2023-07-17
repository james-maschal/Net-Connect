#!/usr/bin/python3
"""Conencts to host via SSH, and outputs all CLI output to a txt file."""

import os
import sys
import subprocess


def init(host):

    ssh_command = f"ssh {host} | tee {host}_output.txt"
    subprocess.run(ssh_command, shell=True)



def ping(host):

    print(f"Pinging {host}...")
    ping_command = ['ping', "-c", "2", host]

    return subprocess.call(ping_command, stdout=open(os.devnull, 'w')) == 0



def main():

    if len(sys.argv) == 2:
        host = sys.argv[1]

        if ping(host):
            print("Ping Successfull, connecting....")
            init(host)

        else:
            print("Ping Unsuccessfull, please check spelling of hostname.")

    else:
        sys.exit("\nError: Provide valid switch ip addr or hostname\n")



if __name__ == '__main__':
    main()
