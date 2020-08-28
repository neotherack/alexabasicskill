from flask import Flask
from flask_ask import Ask, statement, question, session
from wakeonlan import send_magic_packet
import logging

logging.getLogger('flask_ask').setLevel(logging.DEBUG)

app = Flask(__name__)
ask = Ask(app, "/")

sitios_fran = {'oficina', 'de fran', 'habitación'}
id_fran  = "amzn1.ask.account.AFINAOB5SJS7H4ZIU4WMAPU3WARKM62SJH2WAS6KBZBGRD4SE3NVDHT67IJOAZDLRUTHYFU3D5GDIQQLK27C4KZAYKSMXBAIEDPWCTXGF5TD5ZRRM7IYP3PVAC4X33OEZ4V7PZ2GIZB446CP4QDZBC3XAMQQVZD2S3XERWQWTZJIUIAJHYXYLAGDQTFVXGJNITJYBRNIYH7V2UY"
sitios_ester = {'salón', 'de ester'}
id_ester = "amzn1.ask.account.AHJWELXVQRIEFFKDTMDOHFIRCF6I3IMKWHVPMLT43U3MVFCHAC2V4JBJK5JXHJI47IQBAVTSP2Z2I2Y665FUNBIOY6X3UHLS63V7EBJ6K3SMFZ7K5MFUU2NVBOCPSM6YLTJRX4PK7YFKSWL3FUD5UKRSB3MJ6SVHJUVF7EMBNZWW2MOJOCSHFBSTUKDZE2BZURFPW7IAH4P5L6Y"


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

  print("sitio: %s" % sitio)
  print("usuario: %s" % usuario)

  if (sitio in sitios_fran):
    return fran_wol()

  elif (sitio in sitios_ester):
    return ester_wol()

  else:
    return question('¡Caquita fresca! he entendido %s y %s' % (usuario, sitio))


@ask.intent("MyWOLIntent", mapping={'verbo':'verbo', 'cosa':'cosa'})
def mywol(verbo, cosa):
  usuario = user_name(session.user.userId)
  print("usuario: %s" % usuario)

  if (usuario == "Fran"):
    return fran_wol()

  elif (usuario == "Ester"):
    return ester_wol()

  else:
    return statement('¡Putísimo Coque! He entendido %s' % usuario)

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5443)
