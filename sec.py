#!/usr/bin/python3
"""Script designed to automate SSH connecting to network devices."""

import sys
import os
import configparser
import pexpect
import subprocess


def do_ssh(host, config):

    targ = "%s@%s" % (config["ini"][0], host)
    sess = pexpect.spawn("/usr/bin/ssh", [targ])
    idx = sess.expect(["continue connecting", pexpect.EOF, pexpect.TIMEOUT], timeout=4)

    if idx == 0:
        print("Accepting new host SSH Key...")
        sess.sendline("yes")

    try:
        sess.expect("word:", timeout=4)
        sess.sendline(config["ini"][1])

        en = sess.expect([">", "#"], timeout=2)

        if en == 1:
            print("Enable Mode Granted. Press Enter to continue...")

        elif en == 0:
            sess.sendline("en")
            sess.expect("word:")
            sess.sendline(config["ini"][2])

        sess.interact()

        return 0

    except:
        print("\nError: Unable to connect to %s via SSH\n" % host)

        if input("Do you wish to remove the old SSH key and try again? (y/n):") == "y":
            remove_known_host_entry(host)
            return 1

        else:
            sys.exit("\nError: Unable to connect.\n")


def remove_known_host_entry(host):

    print("Attempting to remove ssh key and try again...")

    known_hosts_path = os.path.expanduser("~/.ssh/known_hosts")

    with open(known_hosts_path, "r") as file:
        lines = file.readlines()

    with open(known_hosts_path, "w") as file:
        for line in lines:
            if not line.startswith(host):
                file.write(line)

    print("Old ssh key removed, trying again....\n")


def ping(host):

    print(f"Pinging {host}...")
    command = ['ping', "-c", "2", host]

    return subprocess.call(command, stdout=open(os.devnull, 'w')) == 0



def init(host):

    config = configparser.ConfigParser()
    config.read("info.ini")

    config_v = {
        "ini" : [
            str(config["net"]["username"]),
            str(config["net"]["password"]),
            str(config["net"]["secret"])
            ]}

    if ping(host):
        print("Ping Successfull, connecting....")
        con = do_ssh(host, config_v)

        if con == 1:
            con = do_ssh(host, config_v)

    else:
        print("Ping Unsuccessfull, please check spelling of hostname.")



def main():

    if len(sys.argv) == 2:
        host = sys.argv[1]

    else:
        sys.exit("\nError: Please enter a valid switch ip addr or hostname\n")

    init(host)



if __name__ == '__main__':
    main()
