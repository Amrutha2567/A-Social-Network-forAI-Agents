import json,re,shutil,subprocess
ALLOW_LIST={
 "get_cpu_info":["lscpu"],
 "get_block_devices":["lsblk","-J","-o","NAME,SIZE,TYPE,MOUNTPOINT,MODEL,ROTA,TRAN"],
 "get_memory_summary":["free","-b"],
 "get_dmi_memory":["dmidecode","-t","memory"],
 "get_pci_devices":["lspci"]}
def available_tools(): return {k:shutil.which(v[0]) is not None for k,v in ALLOW_LIST.items()}
def run_fixed(command):
    binary=shutil.which(command[0])
    if not binary: raise RuntimeError("Missing utility: "+command[0])
    result=subprocess.run([binary,*command[1:]],capture_output=True,text=True,check=True,timeout=5,shell=False)
    return result.stdout
def parse_cpu(raw):
    out={}
    for line in raw.splitlines():
        if ":" in line:
            k,v=line.split(":",1); out[k.strip()]=v.strip()
    return out
def parse_memory(raw):
    for row in (x.split() for x in raw.splitlines() if x.strip()):
        if row[0].lower().startswith("mem"):
            vals=list(map(int,row[1:]))
            keys=["total_bytes","used_bytes","free_bytes","shared_bytes","buff_cache_bytes","available_bytes"]
            return dict(zip(keys,vals))
    return {"error":"Unable to parse free output"}
def parse_dmi(raw):
    cap=re.search(r"Maximum Capacity:\s*(.+)",raw)
    slots=re.findall(r"^\s*Size:\s*(.+)$",raw,re.M)
    used=[x.strip() for x in slots if "No Module Installed" not in x]
    return {"maximum_capacity":cap.group(1).strip() if cap else None,"total_slots":len(slots),"used_slots":len(used),"free_slots":len(slots)-len(used),"installed_modules":used}
def execute_tool(name):
    if name not in ALLOW_LIST: raise ValueError("Tool is not allow-listed")
    try:
        raw=run_fixed(ALLOW_LIST[name])
        if name=="get_cpu_info": return parse_cpu(raw)
        if name=="get_block_devices": return json.loads(raw)
        if name=="get_memory_summary": return parse_memory(raw)
        if name=="get_dmi_memory": return parse_dmi(raw)
        return {"devices":raw.splitlines()}
    except subprocess.TimeoutExpired: return {"error":"Command timed out"}
    except subprocess.CalledProcessError as e: return {"error":(e.stderr or str(e)).strip()}
    except (RuntimeError,json.JSONDecodeError) as e: return {"error":str(e)}
def collect_hardware(): return {name:execute_tool(name) if ok else {"error":"Utility unavailable"} for name,ok in available_tools().items()}
