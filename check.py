import paramiko, time

client=paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('72.62.244.186',username='root',password='Mcn12345678@',timeout=10)

def run(cmd, wait=4):
    _,o,e=client.exec_command(cmd, timeout=20)
    time.sleep(wait)
    out=(o.read()+e.read()).decode()
    print(f"[{cmd[:70]}]\n{out[-1000:]}\n")

# Send a test comment then check logs
run('curl -s -X POST http://127.0.0.1:5100/ailivechat/live_comment -H "Content-Type: application/json" -d \'{"username":"Test","text":"halo kak"}\'', 6)
run('journalctl -u ailivechat --no-pager -n 30', 3)

client.close()
