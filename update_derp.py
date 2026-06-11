import requests
import yaml

URL = "https://controlplane.tailscale.com/derpmap/default"

def fetch():
    r = requests.get(URL, timeout=20)
    r.raise_for_status()
    return r.json()

def normalize(data):
    regions = data.get("Regions", {})
    out = {"Regions": {}}

    for rid, region in regions.items():
        nodes = []
        for n in region.get("Nodes", []):
            nodes.append({
                "HostName": n.get("HostName"),
                "IPv4": n.get("IPv4"),
                "IPv6": n.get("IPv6"),
            })

        out["Regions"][rid] = {
            "RegionID": region.get("RegionID"),
            "RegionCode": region.get("RegionCode"),
            "Nodes": nodes
        }

    return out

def main():
    data = fetch()
    out = normalize(data)

    with open("tailscale_derp.yaml", "w") as f:
        yaml.safe_dump(out, f, sort_keys=False, allow_unicode=True)

    print("rules:", sum(len(r["Nodes"]) for r in out["Regions"].values()))

if __name__ == "__main__":
    main()
