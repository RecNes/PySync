PySync
=========

File Synchronizator for Linux


Prerequisites & Installation
============================

Before everything, you must have the permission to access to the remote host by ssh. OpenSSH server is preinstalled on Mac OsX and you don't need to install any additional package. Just need to do some system settings. To enable the OpenSSH server on Mac OS X, open System Preferences and click to Sharing. And than, check the Remote Login box to enable SSH, then select the radio button labeled All Users from the Allow Access For section.

You can now access to the remote host by ssh.

Now, you must create a public access key for passwordless access from local guest machine to remote host over ssh. For that you must get your hand dirty a little bit. :)

First, determine if you already have authentication keys. In the Terminal, run:

sudo ls -la /var/root/.ssh

If you see "id_dsa" and id_dsa.pub, then you can skip the rest of this section.

On the client machine, run the following in the Terminal:

sudo ssh-keygen -t dsa -f /private/var/root/.ssh/id_dsa -C "comment about this key"

AFter created access key in local guest machine, you need to copy the guest's public key to the host's authorized_keys file. You can do this with a simple Terminal command that appends the public key to the list of authorized keys:

sudo cat /private/var/root/.ssh/id_dsa.pub | ssh root@remote_host_address 'cat - >> ~/.ssh/authorized_keys'

The command below that will perform an incremental backup of your root filesystem in local guest machine on to your remote host:

/usr/local/bin/rsync -aNHAXx --protect-args --fileflags --force-change --rsync-path="/usr/local/bin/rsync" / root@remote_host_address:/Volumes/Backup/GuestMachine

You can change parameters of rsync for change synchronization behaviors. If you add this command into crontab, synchronization can be run in any time cycles. For example:

sudo crontab -e

append line below to crontab:

*/30 * * * * /usr/local/bin/rsync -aNHAXx --protect-args --fileflags --force-change --rsync-path="/usr/local/bin/rsync" / root@remote_host_address:/Volumes/Backup/GuestMachine

This will be run synchronization in every half hour.
