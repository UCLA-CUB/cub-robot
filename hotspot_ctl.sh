#!/bin/bash

interface=wlan0

if [[ $EUID -ne 0 ]]
then
	echo "Script must be run as root!"
	exit
fi

for i in $@
do
	if [[ $i == '-d' ]]
	then
		update-rc.d hostapd disable
		update-rc.d udhcpd disable
		echo "Disabled hostapd on boot"
		exit
	fi

    if [[ $i == '-c' ]]
    then
        echo "Configuring for connect mode"
        service hostapd stop
        service udhcpd stop
        
    fi

	if [[ $i == '-r' ]]
	then
		echo "Disabling hostapd, udhcpd"
		service hostapd stop
		service udhcpd stop

		echo "Resetting $interface"
		ifdown $interface
		ifup $interface

		sleep 1

		echo "Enabling hostapd, udhcpd"
		service hostapd start
		service udhcpd start

		exit
	fi
done		

update-rc.d hostapd enable
update-rc.d udhcpd enable
echo "Enabled hostapd on boot"
