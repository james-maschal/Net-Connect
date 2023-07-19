#!/usr/bin/python3
import sys
import os
import configparser
import pexpect


def do_ssh(host, config):

    targ = "%s@%s" % (config["ini"][0], host)
    sess = pexpect.spawn("/usr/bin/ssh", [targ])
    idx = sess.expect(["continue connecting", pexpect.EOF, pexpect.TIMEOUT], timeout=1)

    if idx == 1:
        print("Unable to connect, please ensure hostname spelling is correct.")
        sys.exit()

    if idx == 0:
        print("Accepting new host SSH Key...")
        sess.sendline("yes")

    try:
        sess.expect("word:")
        sess.sendline(config["ini"][1])

        en = sess.expect([">", "#"])

        if en == 1:
            sess.sendline("\b")
            print("\nConnected.")

        elif en == 0:
            sess.sendline("en")
            sess.expect("word:")
            sess.sendline(config["ini"][2])

        sess.interact()

        return 0

    except:
        print("\nError: Unable to connect to %s via SSH\n" % host)

        if input("Do you wish to remove the old SSH key and try again? (y/n):") == "y":

            known_hosts_path = os.path.expanduser("~/.ssh/known_hosts")
            remove_known_host_entry(known_hosts_path, host)
            return 1

        else:
            sys.exit("\nError: Unable to connect.\n")


def remove_known_host_entry(known_hosts_path, host):

    print("Attempting to remove ssh key and try again...")

    with open(known_hosts_path, "r") as file:
        lines = file.readlines()

    with open(known_hosts_path, "w") as file:
        for line in lines:
            if not line.startswith(host):
                file.write(line)

    print("Old ssh key removed, trying again....\n")



def init(host):

    config = configparser.ConfigParser()
    config.read("info.ini")

    config_v = {
        "ini" : [
            str(config["net"]["username"]),
            str(config["net"]["password"]),
            str(config["net"]["secret"])
            ]}

    con = do_ssh(host, config_v)

    if con == 1:
        con = do_ssh(host, config_v)



def main():

    if len(sys.argv) == 2:
        host = sys.argv[1]

    else:
        sys.exit("\nError: Please enter a valid switch ip addr or hostname\n")

    init(host)



if __name__ == '__main__':
    main()
