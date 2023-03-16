# Useful to know 
This document contains all the collected information that is needed to use the included `systemd` service. The atached `update_service.sh` file also based on these commands.

## Basic commands
These commands can be copy pasted to achive the described behaviour of the service. In any case the name change that should be changed.

* Status of service
    ```bash  
    $ systemctl status adsb_logger.service
    ```
* Starts the service
    ```bash
    $ systemctl start adsb_logger.service
    ```
* Stops the service
    ```bash
    $ systemctl stop adsb_logger.service
    ```
* Enable the service
    ```bash
    $ systemctl enable adsb_logger.service
    ```
* disable the service
    ```bash
    $ systemctl disable adsb_logger.service
    ```

System wide `systemctl` related commands.
* Reload the `systemctl` daemon of the system
    ```bash
    $ systemctl daemon-reload
    ```
* Resets the failed `systemctl` services
    ```bash
    $ systemctl reset-failed
    ```

## How to use `update_service.sh`
To run the included update service bash file use this command:
```bash
$ sudo bash update_service.sh
```