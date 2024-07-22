#!/bin/bash
# This script will create and mount a swapfile to boost your memory in case you need to use memory demanding software (i.e. Bakta) and there is no SCE boost available. change the SWAPFILE path with your folder. If no swapfile is already present the script will create one for you (it will need sudo rights).
#use: ./swapdrive.sh mount. To unmount ./swapdrive.sh unmount.
# Warning: it will take the amount of space on your SCE hard drive according to the dimension you asked when creating the swapfile, and it will stay there even if not mounted. If you want to free up space from the hard drive unmount it and just delete the swapfile (rm swapfile). 

SWAPFILE="/home/guidocordoni/Desktop/tmp/swapfile" #insert your path here

function create_swap {
    read -p "Swap file $SWAPFILE does not exist. Do you want to create it? (yes/no) " choice
    if [ "$choice" == "yes" ]; then
        read -p "Enter the size of the swap file in megabytes (e.g., 2048 for 2GB): " size
        sudo dd if=/dev/zero of="$SWAPFILE" bs=1M count="$size"
        sudo chmod 600 "$SWAPFILE"
        sudo mkswap "$SWAPFILE"
        echo "Swap file $SWAPFILE created successfully."
    else
        echo "Swap file creation aborted."
        exit 1
    fi
}

function mount_swap {
    if [ ! -f "$SWAPFILE" ]; then
        create_swap
    fi

    if sudo swapon --show | grep -q "$SWAPFILE"; then
        echo "Swap file $SWAPFILE is already enabled."
    else
        echo "Enabling swap file $SWAPFILE..."
        sudo swapon "$SWAPFILE"
        if [ $? -eq 0 ]; then
            echo "Swap file $SWAPFILE enabled successfully."
        else
            echo "Failed to enable swap file $SWAPFILE."
        fi
    fi
}

function unmount_swap {
    if sudo swapon --show | grep -q "$SWAPFILE"; then
        echo "Disabling swap file $SWAPFILE..."
        sudo swapoff "$SWAPFILE"
        if [ $? -eq 0 ]; then
            echo "Swap file $SWAPFILE disabled successfully."
        else
            echo "Failed to disable swap file $SWAPFILE."
        fi
    else
        echo "Swap file $SWAPFILE is not currently enabled."
    fi
}

if [ "$1" == "mount" ]; then
    mount_swap
elif [ "$1" == "unmount" ]; then
    unmount_swap
else
    echo "Usage: $0 {mount|unmount}"
fi

