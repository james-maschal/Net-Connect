#!/usr/bin/python3
"""Telnet script to login to network devices. Designed to SSH to a
Bastion Host, and then Telnet to the actual device."""

import sys
import os
import configparser
import pexpect
import subprocess


def do_tel(host, config):

    bastion = config["ini"][3]
    targ = "%s@%s" % (config["ini"][0], bastion)
    sess = pexpect.spawn("/usr/bin/ssh", [targ])
    idx = sess.expect(["continue connecting", pexpect.EOF, pexpect.TIMEOUT], timeout=1)

    if idx == 0:
        sess.sendline("yes")
        sess.expect("word:")
        sess.sendline(config["ini"][1])
        sess.expect(bastion)
        print(f"Connected. Telnetting to {host}")
        sess.sendline(f"telnet {host}")
        sess.expect("sername:")
        sess.sendline(config["ini"][0])
        sess.expect("word:")
        sess.sendline(config["ini"][1])

    elif idx != 0:
        sess.expect("word:")
        sess.sendline(config["ini"][1])
        sess.expect(bastion)
        print(f"Connected. Telnetting to {host}")
        sess.sendline(f"telnet {host}")
        sess.expect("sername:")
        sess.sendline(config["ini"][0])
        sess.expect("word:")
        sess.sendline(config["ini"][1])

    else:
        print("\nError: Unable to connect to host %s via Telnet\n" % host)

    sess.interact()



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
            str(config["net"]["secret"]),
            str(config["net"]["bastion"])
            ]}

    if ping(host):
        print("Ping Successfull, connecting to Bastion Host...")
        do_tel(host, config_v)

    else:
        print("Ping Unsuccessfull, please check spelling of hostname.")
        sys.exit("\nError: Provide valid switch ip addr or hostname\n")



def main():

    if len(sys.argv) == 2:
        host = sys.argv[1]

    else:
        sys.exit("\nError: Provide valid switch ip addr or hostname\n")

    init(host)



if __name__ == '__main__':
    main()
