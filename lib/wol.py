from wakeonlan import send_magic_packet

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

