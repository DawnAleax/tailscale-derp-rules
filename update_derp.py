import requests
import yaml

URL = "https://login.tailscale.com/derpmap/default"

def main():
    data = requests.get(URL, timeout=10).json()

    regions = data.get("Regions", {})
    result = {"payload": []}

    for region_id, region in regions.items():
        nodes = region.get("Nodes", [])
        for node in nodes:
            hostname = node["HostName"]
            ipv4 = node.get("IPv4")
            ipv6 = node.get("IPv6")

            result["payload"].append(f"DOMAIN,{hostname}")
            if ipv4:
                result["payload"].append(f"IP-CIDR,{ipv4}/32")
            if ipv6:
                result["payload"].append(f"IP-CIDR6,{ipv6}/128")

    # 保证稳定输出（关键）
    result["payload"] = sorted(set(result["payload"]))

    with open("tailscale_derp.yaml", "w") as f:
        yaml.dump(result, f, sort_keys=False, allow_unicode=True)

    print(f"Generated {len(result['payload'])} rules")

if __name__ == "__main__":
    main()
