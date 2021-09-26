#!/usr/bin/bash

# Exit if any of the commands fails.
set -o errexit
# Exit if one of pipe command fails.
set -o pipefail
# Exit if any of the variables is not set.
set -o nounset

# Execute corresponding command.
exec "$@"
