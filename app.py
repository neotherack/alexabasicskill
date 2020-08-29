from flask import Flask
from flask_ask import Ask, statement, question, session

from lib.conf import *
from lib.ssh import *
from lib.wol import *

app = Flask(__name__)
ask = Ask(app, "/")

config = load_config('settings.conf')

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

def iniciar_servidor():
  return enviar_cmd(sshconn, sshcom['cmdStartMC'])

def parar_servidor():
  return enviar_cmd(sshconn, sshcom['cmdStopMC'])

def revisar_servidor():
  return enviar_cmd(sshconn, sshcom['cmdStatusMC'])

def pid_servidor():
  return enviar_cmd(sshconn, sshcom['cmdGetPIDMC'])

@ask.intent("WOLIntent", mapping={'verbo':'verbo', 'cosa':'cosa', 'sitio':'sitio'})
def wol(verbo, cosa, sitio):
  usuario = user_name(session.user.userId)

  if (sitio in places['fran_places'].split(',')):
    return statement(fran_wol(macs))

  elif (sitio in places['ester_places'].split(',')):
    return statement(ester_wol(macs))

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

  pid, err = pid_servidor()

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
  info, err = revisar_servidor()

  if (info is not None): #si está arrancado
    return statement('El servidor de Minecraft está arrancado: %s' % info)

  else: #si está parado
    return statement('El servidor de Minecraft está parado')

if __name__ == '__main__':
  app.run(debug=True, host=serv['host'], port=serv['port'])
