import paramiko

def ssh_command(hostname='localhost', port='22', username='pi', password='NaN', command='dir /'):
  try:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy)

    client.connect(hostname, port=port, username=username, password=password)

    stdin, stdout, stderr = client.exec_command(command)
    ret = stdout.read().decode('utf-8')
    print(ret)

  except Exception as e:
    print('error en la conexión ssh %s' % str(e))
  finally:
    client.close()


ssh_command(hostname='www.example.com', port='x', username='xxxxxxx', password='xxxxxxxxx', command='ps -fea | grep -i python')
