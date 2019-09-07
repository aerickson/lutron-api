import getpass
import sys
import telnetlib

HOST = "lutron"
user = "lutron"
password = "integration"

tn = telnetlib.Telnet(HOST)

tn.read_until("login: ")
tn.write(user + "\n")
if password:
    tn.read_until("password: ")
    tn.write(password + "\n")

# tn.write("ls\n")
# tn.write("exit\n")

# print tn.read_all()

while True:
    line = tn.read_until("\n")  # Read one line
    print(line.strip())
