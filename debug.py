import paramiko

HOST = "72.62.244.186"
USER = "root"
PASS = "Mcn12345678@"

def run(client, cmd):
    print(f"$ {cmd[:100]}")
    _, stdout, stderr = client.exec_command(cmd, timeout=30)
    out = stdout.read().decode()
    err = stderr.read().decode()
    if out: print(out[-2000:])
    if err: print("[ERR]", err[-500:])
    return out

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, username=USER, password=PASS, timeout=15)

# Test actual endpoints
run(client, "curl -s -o /dev/null -w 'chat: %{http_code}' -X POST http://127.0.0.1:5100/ailivechat/chat/space/default -H 'Content-Type: application/json' -d '{\"messages\":[]}'")
run(client, "curl -s -o /dev/null -w 'talk: %{http_code}' -X POST http://127.0.0.1:5100/ailivechat/talk -H 'Content-Type: application/json' -d '{\"text\":\"test\"}'")
run(client, "curl -s -o /dev/null -w 'static: %{http_code}' http://127.0.0.1:5100/ailivechat/static/auto1.mp3")
run(client, "curl -s -o /dev/null -w 'admin: %{http_code}' http://127.0.0.1:5100/ailivechat/admin/spaces")

# Check what nginx actually passes
run(client, "curl -v http://72.62.244.186/ailivechat/static/auto1.mp3 2>&1 | grep -E 'HTTP|Location|< '")

client.close()
