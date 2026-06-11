import requests
import yaml

URL = "https://login.tailscale.com/derpmap/default"

def main():
    data = requests.get(URL, timeout=15).json()

    regions = data.get("Regions", {})
    payload = []

    for _, region in regions.items():
        for node in region.get("Nodes", []):
            host = node["HostName"]
            ipv4 = node.get("IPv4")
            ipv6 = node.get("IPv6")

            payload.append(f"DOMAIN,{host}")
            if ipv4:
                payload.append(f"IP-CIDR,{ipv4}/32")
            if ipv6:
                payload.append(f"IP-CIDR6,{ipv6}/128")

    payload = sorted(set(payload))

    out = {"payload": payload}

    with open("tailscale_derp.yaml", "w", encoding="utf-8") as f:
        yaml.dump(out, f, sort_keys=False, allow_unicode=True)

    print(f"rules: {len(payload)}")

if __name__ == "__main__":
    main()
