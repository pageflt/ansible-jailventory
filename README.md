# jailventory

Ansible dynamic inventory provider for FreeBSD jails.

## Usage

- Make sure `jailventory.py` is executable:

```
$ chmod +x jailventory.py
```

- Add the following directive to your `ansible.cfg`:

```
inventory = /path/to/jailventory.py
```

- Ansible should now automatically detect any active jails and add them to the `jails` group:

```
$ jls
   JID  IP Address      Hostname                      Path
    16  192.168.1.1     www                           /home/jails/www
    17  192.168.1.2     dns                           /home/jails/dns
$ ansible jails -m ping -o
dns | SUCCESS => {"changed": false, "ping": "pong"}
www | SUCCESS => {"changed": false, "ping": "pong"}
$ sudo service jail start mail
Starting jails: mail.
$ ansible jails -m ping -o
dns | SUCCESS => {"changed": false, "ping": "pong"}
www | SUCCESS => {"changed": false, "ping": "pong"}
mail | SUCCESS => {"changed": false, "ping": "pong"}
```

