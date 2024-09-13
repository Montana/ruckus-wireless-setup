import paramiko
import time

def ruckus(hostname, username, password, commands):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname, username=username, password=password, look_for_keys=False, allow_agent=False)
        print(f"Connected to {hostname}")

        shell = client.invoke_shell()
        time.sleep(1)

        for command in commands:
            shell.send(command + '\n')
            time.sleep(2)

        output = shell.recv(65535).decode('utf-8')
        print(output)

    finally:
        client.close()
        print("Connection closed")

hostname = '192.168.1.1'
username = 'admin'
password = 'admin'

commands = [
    'enable',
    'configure terminal',

    'interface wlan 1',
    'ssid MyNetwork1',
    'passphrase securepassword1',
    'vlan 100',
    'encryption wpa2',

    'interface wlan 2',
    'ssid GuestNetwork',
    'passphrase guestpassword',
    'vlan 200',
    'encryption wpa2',
    'guest-access enable',
    'no dhcp server',

    'interface wlan 3',
    'ssid IoTNetwork',
    'passphrase iotpassword',
    'vlan 300',
    'encryption wpa2',
    'max-clients 50',
    'no-broadcast-ssid',  

    'interface radio 1',
    'channel 6',
    'power 75',
    'bandwidth 20',

    'interface radio 2',
    'channel 36',
    'power 100',
    'bandwidth 40',

    'interface vlan 100',
    'ip address 192.168.100.1 255.255.255.0',
    'interface vlan 200',
    'ip address 192.168.200.1 255.255.255.0',
    'interface vlan 300',
    'ip address 192.168.300.1 255.255.255.0',

    'traffic-policy guest',
    'rate-limit 5mbps',
    'block-peer-traffic',
    'traffic-policy iot',
    'rate-limit 2mbps',

    'qos trust dscp',  
    'qos profile video priority high', 

    'enable-mac-authentication', 
    'deny-unlisted-macs',        

    'end',
    'write memory',
]

# Call the RUCKUS function with provided credentials and commands
ruckus(hostname, username, password, commands)
