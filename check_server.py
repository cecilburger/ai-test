import paramiko

HOST = "72.62.244.186"
USER = "root"
PASS = "Mcn12345678@"

def run(client, cmd):
    print(f"\n$ {cmd}")
    _, stdout, stderr = client.exec_command(cmd, timeout=30)
    out = stdout.read().decode()
    err = stderr.read().decode()
    if out: print(out[-3000:])
    if err: print("[ERR]", err[-1000:])
    return out

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, username=USER, password=PASS, timeout=15)

# Test static file paths
run(client, "curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:5100/ailivechat/static/auto1.mp3")
run(client, "curl -s -o /dev/null -w '%{http_code}' http://72.62.244.186/ailivechat/static/auto1.mp3")
run(client, "curl -s -o /dev/null -w '%{http_code} %{url_effective}' http://72.62.244.186/ailivechat/chat -X POST -H 'Content-Type: application/json' -d '{\"messages\":[]}'")

client.close()
