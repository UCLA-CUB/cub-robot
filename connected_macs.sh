#!/bin/bash

iw dev wlan0 station dump | sed -n "s/^Station\ \([0-9a-fA-F:]*\).*$/\1/p"
