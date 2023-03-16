#!/usr/bin/env sh
set -eu

if ! [ $(id -u) = 0 ]; then
    echo "The script need to be run as root." >&2
    exit 1
fi

# Service name / aka filename
SERVICE_NAME="adsb_logger.service"
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"


printf "Adsb Logger service initializer \n"
printf "Current service name: %s\n" "$SERVICE_NAME"

printf "Check service status \n"
if systemctl is-active "$SERVICE_NAME" > /dev/null 2>&1
then
    printf "Service already exists. \n"
    printf "Remove Adsb Logger service \n"
    systemctl stop "$SERVICE_NAME"
    systemctl disable "$SERVICE_NAME"
    rm -f /etc/systemd/system/"$SERVICE_NAME"
    rm -f /usr/lib/systemd/system/"$SERVICE_NAME" 
    systemctl daemon-reload
    systemctl reset-failed
    printf "Remove succesfull \n"
fi

printf "Service doesn't exist yet. \n"

printf "Copy service file from: $PWD \n"
cp "$SCRIPTPATH/$SERVICE_NAME"  "/etc/systemd/system/$SERVICE_NAME"
chmod 644 "/etc/systemd/system/$SERVICE_NAME" 

printf "Start and Enable service  \n"
systemctl start --quiet "$SERVICE_NAME"
systemctl status --quiet "$SERVICE_NAME"
systemctl enable --quiet "$SERVICE_NAME"

if systemctl is-active "$SERVICE_NAME" > /dev/null 2>&1
then
    printf "Service is up and running... \n"
    printf "Exiting \n"
else
    printf "Service is down... \n"
fi
