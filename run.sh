#!/usr/bin/env bash
set -e

export PYTHONPATH=$PYTHONPATH:$(pwd)


run_uvicorn() {
    set -x
    # Uvicorn (ASGI)
    exec uvicorn --host 0.0.0.0 --port $WEATHER_SRV_PORT  'src.main:create_app'
}

unittest() {
    set -x
    echo "Running unittests"
    pytest --cov=src/ tests -vvv
    rm -rf testing.sqlite
}

prodinit() {
    set -x
    echo "Production instance"
    run_uvicorn
}


SELF="$0"

USAGE="$SELF <command>

Main entrypoint for operations and processes inside docker
container.

Commands:
      Set up environment according to <profile>. Possible values for profile are:
        prod:
            - set environment variables
            - run app with production server
        test:
            - set environment variables
            - run unittests
"

CMD="$1"
if [ -n "$CMD" ]; then
    shift
fi

case "$CMD" in
    prod)
        prodinit
        ;;
    test)
        unittest
        ;;
    help|--help|-h)
        echo "$USAGE"
        ;;
    *)
        echo "$USAGE" >&2
        echo "Wrong invocation" >&2
        exit 1
        ;;
esac
