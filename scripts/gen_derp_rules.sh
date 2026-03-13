#!/usr/bin/env bash
set -e

DERP_URL="https://login.tailscale.com/derpmap/default"
OUTPUT_FILE="ruleset/tailscale_derp.yaml"

# 获取 JSON 并解析生成 domain-suffix 规则
curl -s $DERP_URL | jq -r '
  .Regions[]?.Nodes[]? | 
  "  - " + .HostName
' | sort -u > $OUTPUT_FILE

echo "DERP rules saved to $OUTPUT_FILE"
