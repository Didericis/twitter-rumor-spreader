#!/bin/bash

COMMAND="$1"

case "$COMMAND" in
        ui)
            cd ui && ./run.sh ${@:2}
            ;;

        *)
            echo "Unrecognized command: $COMMAND"
            exit 1

esac
