#!/bin/bash

COMMAND="$1"

case "$COMMAND" in
        yarn)
            yarn ${@:2}
            docker-compose -f ../docker-compose.yml exec ui yarn ${@:2}
            ;;

        *)
            echo "Unrecognized command: $COMMAND"
            exit 1

esac
