#!/bin/bash

URL="https://login.tailscale.com/derpmap/default"
OUT="ruleset/tailscale_derp.yaml"

mkdir -p ruleset

curl -s $URL | jq -r '

[
"payload:",
"",
"# DERP hostnames",
(.Regions[].Nodes[].HostName | "  - DOMAIN," + .),
"",
"# DERP IPv4",
(.Regions[].Nodes[].IPv4 | "  - IP-CIDR," + . + "/32,no-resolve")
] | .[]
' > $OUT
