import paramiko

def ssh_command(hostname='localhost', port='22', username='user', password='NaN', command='dir /'):

  ret = ""
  err = ""

  try:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy)

    client.connect(hostname, port=port, username=username, password=password)

    stdin, stdout, stderr = client.exec_command(command)
    ret = stdout.read().decode('utf-8')
    err = stderr.read().decode('utf-8')

    return [ret,err]

  except Exception as e:
    return ["",str(e)]
  finally:
    client.close()


def enviar_cmd(cmd):
  try:
    stdout, stderr = ssh_command(hostname=sshconn['hostname'], port=sshconn['port'], username=sshconn['username'], password=sshconn['password'], command=cmd)

    return [stdout.strip(), stderr.strip()]
  except Exception as e:
    return ["", str(e)]

