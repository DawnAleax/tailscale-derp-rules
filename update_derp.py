import requests
import yaml
import sys

DERP_SOURCE_URL = "https://controlplane.tailscale.com/derpmap/default"

def fetch_derp_map():
    """
    拉取 Tailscale DERP map
    """
    r = requests.get(DERP_SOURCE_URL, timeout=30)
    r.raise_for_status()
    return r.json()

def normalize(data):
    """
    统一输出结构：
    Regions -> Nodes
    """
    regions_out = {}

    regions = data.get("Regions", {})

    for region_id, region in regions.items():
        nodes = region.get("Nodes", [])

        norm_nodes = []
        for n in nodes:
            norm_nodes.append({
                "HostName": n.get("HostName", ""),
                "IPv4": n.get("IPv4"),
                "IPv6": n.get("IPv6"),
                "RegionID": region_id,
                "RegionCode": region.get("RegionCode"),
                "RegionName": region.get("RegionName"),
            })

        regions_out[region_id] = {
            "RegionCode": region.get("RegionCode"),
            "RegionName": region.get("RegionName"),
            "Nodes": norm_nodes
        }

    return {"Regions": regions_out}

def main():
    try:
        raw = fetch_derp_map()
    except Exception as e:
        print(f"[ERROR] fetch failed: {e}")
        sys.exit(1)

    # 兼容：有些返回结构是 derpMap 包裹
    if "Regions" not in raw:
        print("[ERROR] invalid derp format (no Regions)")
        sys.exit(1)

    cleaned = normalize(raw)

    # 写文件
    with open("tailscale_derp.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(cleaned, f, allow_unicode=True, sort_keys=False)

    print(f"rules: {sum(len(r['Nodes']) for r in cleaned['Regions'].values())}")

if __name__ == "__main__":
    main()
