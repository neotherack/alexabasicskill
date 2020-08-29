from flask import Flask
from flask_ask import Ask, statement, question, session
from wakeonlan import send_magic_packet
import paramiko
import logging

logging.getLogger('flask_ask').setLevel(logging.DEBUG)

app = Flask(__name__)
ask = Ask(app, "/")

sitios_fran = {'oficina', 'de fran', 'habitación'}
id_fran = "amzn1.ask.account.AHJWELXVQRIEFFKDTMDOHFIRCF6I3IMKWHVPMLT43U3MVFCHAC2V4JBJK5JXHJI47IQBAVTSP2Z2I2Y665FUNBIOY6X3UHLS63V7EBJ6K3SMFZ7K5MFUU2NVBOCPSM6YLTJRX4PK7YFKSWL3FUD5UKRSB3MJ6SVHJUVF7EMBNZWW2MOJOCSHFBSTUKDZE2BZURFPW7IAH4P5L6Y"
sitios_ester = {'salón', 'de ester'}
id_ester = "amzn1.ask.account.AHJWELXVQRIEFFKDTMDOHFIRCF6I3IMKWHVPMLT43U3MVFCHAC2V4JBJK5JXHJI47IQBAVTSP2Z2I2Y665FUNBIOY6X3UHLS63V7EBJ6K3SMFZ7K5MFUU2NVBOCPSM6YLTJRX4PK7YFKSWL3FUD5UKRSB3MJ6SVHJUVF7EMBNZWW2MOJOCSHFBSTUKDZE2BZURFPW7IAH4P5L6Y"

arranque = {'arranca', 'inicia', 'lanza'}
parada = {'detén', 'para', 'mata'}

cmdArrancarMC = "/opt/minecraft/minecraft_server/launch.sh"
cmdGetPIDMC = "ps -fea | grep mine | grep java | grep -v grep | awk '{print $2}'"
cmdPararMC = "kill -9 $(%s)" % cmdGetPIDMC

@ask.launch
def start_skill():
  return question('¡Hola {}! ¿qué quieres que haga?'.format(user_name(session.user.userId))).reprompt('No te he entendido bien, ¿me lo podrías repetir?')

def user_name(id):
  if (id == id_fran):
    return "Fran"
  else:
    return "Ester"

def ssh_command(hostname='localhost', port='22', username='user', password='NaN', command='dir /'):

  ret = ""
  err = ""

  try:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy)

    print("debug: %s %s %s %s" % (hostname, port, username, password))
    client.connect(hostname, port=port, username=username, password=password)
    print("command: %s" % command)

    stdin, stdout, stderr = client.exec_command(command)
    ret = stdout.read().decode('utf-8')
    err = stderr.read().decode('utf-8')

    return [ret,err]

  except Exception as e:
    return ["",str(e)]
    #print('error en la conexión ssh %s' % str(e))
  finally:
    client.close()

def fran_wol():
  try:
    send_magic_packet('00.e0.4c.68.0d.4c')
    return statement('Se ha enviado la orden al PC de la oficina')
  except:
    return statement('No he podido arrancar el ordenador de la oficina')

def ester_wol():
  try:
    send_magic_packet('70.8b.cd.27.e1.dd')
    return statement('Se ha enviado la orden al portátil de Ester')
  except:
    return statement('No he podido arrancar el portátil de Ester')

def enviar_cmd(cmd):
  try:
    stdout, stderr = ssh_command(hostname='putisimocoque.tk', port='1986', username='fran', password='matrix05', command=cmd)

    print("stdout: %s" % stdout.strip())
    print("stderr: %s" % stderr.strip())

    return [stdout.strip(), stderr.strip()]
#    return ['1999','']
  except Exception as e:
    return ["", str(e)]

def iniciar_servidor():
    return enviar_cmd(cmdArrancarMC)

def parar_servidor():
    return enviar_cmd(cmdPararMC)

def revisar_servidor():
    return enviar_cmd(cmdGetPIDMC)


@ask.intent("WOLIntent", mapping={'verbo':'verbo', 'cosa':'cosa', 'sitio':'sitio'})
def wol(verbo, cosa, sitio):
  usuario = user_name(session.user.userId)

#  print("sitio: %s" % sitio)
#  print("usuario: %s" % usuario)

  if (sitio in sitios_fran):
    return fran_wol()

  elif (sitio in sitios_ester):
    return ester_wol()

  else:
    return question('%s, por favor, repite el comando relacionado con %s' % (usuario, sitio))


@ask.intent("MyWOLIntent", mapping={'verbo':'verbo', 'cosa':'cosa'})
def mywol(verbo, cosa):
  usuario = user_name(session.user.userId)
#  print("usuario: %s" % usuario)

  if (usuario == "Fran"):
    return fran_wol()

  elif (usuario == "Ester"):
    return ester_wol()

  else:
    return statement('%s, por favor, repite el comando' % usuario)


@ask.intent("MCStartStopIntent", mapping={'instruccion':'instruccion'})
def mcstartstop(instruccion):
  usuario = user_name(session.user.userId)
#  print("usuario: %s" % usuario)

  pid, err = revisar_servidor()

  if (pid is not None): #si está arrancado
    if (instruccion in arranque):
      return statement('El servidor de Minecraft ya estaba activo, se ejecuta ahora mismo con el PID: %s' % pid)
    else:
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
#  print("usuario: %s" % usuario)

  pid, err = revisar_servidor()

  print("pid %s" % pid)
  print("err %s" % err)

  if (pid is not None): #si está arrancado
    return statement('El servidor de Minecraft está arrancado con el PID: %s' % pid)

  else: #si está parado
    return statement('El servidor de Minecraft está parado')

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5443)
