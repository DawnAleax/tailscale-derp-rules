import yaml

def load(p):
    try:
        with open(p, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except:
        return {}

old = load("old.yaml")
new = load("tailscale_derp.yaml")

def extract(d):
    s = set()
    for r in d.get("Regions", {}).values():
        for n in r.get("Nodes", []):
            s.add((n["HostName"], n.get("IPv4"), n.get("IPv6")))
    return s

old_nodes = extract(old)
new_nodes = extract(new)

added = sorted(new_nodes - old_nodes)
removed = sorted(old_nodes - new_nodes)

def fmt(items):
    if not items:
        return "- None"
    return "\n".join([f"- {a} | {b} | {c}" for a,b,c in items])

with open("CHANGELOG.md", "w", encoding="utf-8") as f:
    f.write("# DERP Change Log\n\n")

    f.write("## ➕ Added\n")
    f.write(fmt(added))
    f.write("\n\n")

    f.write("## ➖ Removed\n")
    f.write(fmt(removed))
    f.write("\n")
