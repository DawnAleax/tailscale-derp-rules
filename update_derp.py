import requests
import yaml

URL = "https://controlplane.tailscale.com/derpmap/default"

def fetch():
    r = requests.get(URL, timeout=20)
    r.raise_for_status()
    return r.json()

def build_payload(data):
    payload = []

    regions = data.get("Regions", {})

    for _, region in regions.items():
        nodes = region.get("Nodes", [])

        for n in nodes:
            host = n.get("HostName")

            # DOMAIN
            if host:
                payload.append(f"DOMAIN,{host}")

            # IPv4
            ipv4 = n.get("IPv4")
            if ipv4:
                payload.append(f"IP-CIDR,{ipv4}/32")

            # IPv6
            ipv6 = n.get("IPv6")
            if ipv6:
                payload.append(f"IP-CIDR6,{ipv6}/128")

    return payload

def main():
    data = fetch()

    payload = build_payload(data)

    out = {
        "payload": payload
    }

    with open("tailscale_derp.yaml", "w") as f:
        yaml.safe_dump(out, f, sort_keys=False, allow_unicode=True)

    print("rules:", len(payload))

if __name__ == "__main__":
    main()
