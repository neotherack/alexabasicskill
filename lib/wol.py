from wakeonlan import send_magic_packet

def fran_wol(macs):
  try:
    send_magic_packet(macs['fran_laptop'])
    return 'Se ha enviado la orden al PC de la oficina'
  except:
    return 'No he podido arrancar el ordenador de la oficina'

def ester_wol(macs):
  try:
    send_magic_packet(macs['ester_laptop'])
    return 'Se ha enviado la orden al portátil de Ester'
  except:
    return 'No he podido arrancar el portátil de Ester'

