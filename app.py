from flask import Flask
from flask_ask import Ask, statement, question, session
from wakeonlan import send_magic_packet
import logging

logging.getLogger('flask_ask').setLevel(logging.DEBUG)

app = Flask(__name__)
ask = Ask(app, "/")

sitios_fran = {'oficina', 'de fran', 'habitación'}
id_fran = "amzn1.ask.account.AHJWELXVQRIEFFKDTMDOHFIRCF6I3IMKWHVPMLT43U3MVFCHAC2V4JBJK5JXHJI47IQBAVTSP2Z2I2Y665FUNBIOY6X3UHLS63V7EBJ6K3SMFZ7K5MFUU2NVBOCPSM6YLTJRX4PK7YFKSWL3FUD5UKRSB3MJ6SVHJUVF7EMBNZWW2MOJOCSHFBSTUKDZE2BZURFPW7IAH4P5L6Y"
sitios_ester = {'salón', 'de ester'}
id_ester = "amzn1.ask.account.AHJWELXVQRIEFFKDTMDOHFIRCF6I3IMKWHVPMLT43U3MVFCHAC2V4JBJK5JXHJI47IQBAVTSP2Z2I2Y665FUNBIOY6X3UHLS63V7EBJ6K3SMFZ7K5MFUU2NVBOCPSM6YLTJRX4PK7YFKSWL3FUD5UKRSB3MJ6SVHJUVF7EMBNZWW2MOJOCSHFBSTUKDZE2BZURFPW7IAH4P5L6Y"

arranque = {'arranca', 'inicia'}
parada = {'detén', 'para'}

@ask.launch
def start_skill():
  return question('¡Hola {}! ¿qué quieres que haga?'.format(user_name(session.user.userId))).reprompt('No te he entendido bien, ¿me lo podrías repetir?')

def user_name(id):
  if (id == id_fran):
    return "Fran"
  else:
    return "Ester"


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
def mywol(instruccion):
  usuario = user_name(session.user.userId)
#  print("usuario: %s" % usuario)
  if (instrucion in arranque):

    return statement('Arrancando el servidor de minecraft')
  elif (instruccion in parada):

    return statement('Deteniendo el servidor de minecraft')
  else:
    return question('%s, no he entendido si quieres parar o arrancar el servidor' % usuario)

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5443)
