import paramiko, time

HOST,USER,PASS="72.62.244.186","root","Mcn12345678@"

print("Connecting...")
client=paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST,username=USER,password=PASS,timeout=10)
print("Connected!")

print("Uploading via SFTP...")
sftp=client.open_sftp()
sftp.put("templates/index.html","/var/www/ailivechat/templates/index.html")
sftp.close()
print("Upload done!")

print("Restarting service...")
_,o,e=client.exec_command("systemctl restart ailivechat && sleep 2 && systemctl is-active ailivechat",timeout=10)
time.sleep(5)
print(o.read().decode().strip() or e.read().decode().strip())

client.close()
print("Done!")
