from flask import Flask
from flask_ask import Ask, statement, question, session
from wakeonlan import send_magic_packet
import paramiko
import logging
import configparser
import json

logging.getLogger('flask_ask').setLevel(logging.DEBUG)

app = Flask(__name__)
ask = Ask(app, "/")

config = configparser.ConfigParser()
config.read('settings.conf')

serv = config['Main-Settings']
sshconn = config['SSH-Connection']
sshcom  = config['SSH-Commands']
places = config['PC-Places']
actions = config['MC-Actions']
amzids = config['IDs-Amazon']
macs = config['MAC']

@ask.launch
def start_skill():
  return question('¡Hola {}! ¿qué quieres que haga?'.format(user_name(session.user.userId))).reprompt('No te he entendido bien, ¿me lo podrías repetir?')

def user_name(id):
  if (id == amzids['id_fran']):
    return "Fran"
  else: #amzids['id_ester']
    return "Ester"

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

def fran_wol():
  try:
    send_magic_packet(macs['fran_laptop'])
    return statement('Se ha enviado la orden al PC de la oficina')
  except:
    return statement('No he podido arrancar el ordenador de la oficina')

def ester_wol():
  try:
    send_magic_packet(macs['ester_laptop'])
    return statement('Se ha enviado la orden al portátil de Ester')
  except:
    return statement('No he podido arrancar el portátil de Ester')

def enviar_cmd(cmd):
  try:
    stdout, stderr = ssh_command(hostname=sshconn['hostname'], port=sshconn['port'], username=sshconn['username'], password=sshconn['password'], command=cmd)

    return [stdout.strip(), stderr.strip()]
  except Exception as e:
    return ["", str(e)]

def iniciar_servidor():
    return enviar_cmd(sshcom['cmdStartMC'])

def parar_servidor():
    return enviar_cmd(sshcom['cmdStopMC'])

def revisar_servidor():
    return enviar_cmd(sshcom['cmdGetPIDMC'])


@ask.intent("WOLIntent", mapping={'verbo':'verbo', 'cosa':'cosa', 'sitio':'sitio'})
def wol(verbo, cosa, sitio):
  usuario = user_name(session.user.userId)

  if (sitio in places['fran_places'].split(',')):
    return fran_wol()

  elif (sitio in places['ester_places'].split(',')):
    return ester_wol()

  else:
    return question('%s, por favor, repite el comando relacionado con %s' % (usuario, sitio))


@ask.intent("MyWOLIntent", mapping={'verbo':'verbo', 'cosa':'cosa'})
def mywol(verbo, cosa):
  usuario = user_name(session.user.userId)

  if (usuario == "Fran"):
    return fran_wol()

  elif (usuario == "Ester"):
    return ester_wol()

  else:
    return statement('%s, por favor, repite el comando' % usuario)


@ask.intent("MCStartStopIntent", mapping={'instruccion':'instruccion'})
def mcstartstop(instruccion):
  usuario = user_name(session.user.userId)

  pid, err = revisar_servidor()

  if (pid is not None): #si está arrancado
    if (instruccion in actions['start'].split(',')):
      return statement('El servidor de Minecraft ya estaba activo, se ejecuta ahora mismo con el PID: %s' % pid)
    else: # actions['stop'].split(',')
      info, err = parar_servidor()
      return statement('Se ha enviado la orden de detener el servidor')


  else: #si está parado
    if (instruccion in arranque):
      info, err = iniciar_servidor()
      return statement('Se ha enviado la orden de arranque al servidor')
    else:
      return statement('El servidor ya estaba parado')


@ask.intent("MCStatusIntent")
def mcstatus():
  usuario = user_name(session.user.userId)

  pid, err = revisar_servidor()

  if (pid is not None): #si está arrancado
    return statement('El servidor de Minecraft está arrancado con el PID: %s' % pid)

  else: #si está parado
    return statement('El servidor de Minecraft está parado')

if __name__ == '__main__':
  app.run(debug=True, host=serv['host'], port=serv['port'])
