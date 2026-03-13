import requests
import yaml
import os

def fetch_and_convert():
    url = "https://login.tailscale.com/derpmap/default"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    payload = []

    # 遍历所有区域和节点
    for region_id, region in data.get("Regions", {}).items():
        for node in region.get("Nodes", []):
            # 添加域名
            host = node.get("HostName")
            if host:
                payload.append(f"DOMAIN,{host}")
            
            # 添加 IPv4
            ipv4 = node.get("IPv4")
            if ipv4:
                payload.append(f"IP-CIDR,{ipv4}/32")
            
            # 添加 IPv6 (如果需要)
            ipv6 = node.get("IPv6")
            if ipv6:
                payload.append(f"IP-CIDR6,{ipv6}/128")

    # 构建 Clash Rule-set 格式
    rule_set = {
        "payload": payload
    }

    # 写入文件
    output_file = "tailscale_derp.yaml"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Tailscale DERP Servers Rule-set\n")
        f.write("# Generated automatically\n")
        yaml.dump(rule_set, f, default_flow_style=False, allow_unicode=True)
    
    print(f"Successfully generated {output_file} with {len(payload)} rules.")

if __name__ == "__main__":
    fetch_and_convert()
