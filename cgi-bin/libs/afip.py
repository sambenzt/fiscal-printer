from ctypes import byref, c_int, c_char, c_long, c_short, create_string_buffer
from ctypes import windll
import binascii
import subprocess
import os

PUERTO = '0'

CARPETA_DESTINO = os.getcwd() + "\libs\downloads"

def descarga(desde,hasta):

  #title 
  print "*** DESCARGANDO ARCHIVOS AFIP ***"

  abrirCarpeta()

  return { "status" : True , "desde" : desde , "hasta" : hasta, }

  # get handle from DLL
  Handle_HL = windll.LoadLibrary("EpsonFiscalInterface.dll")

  # connect
  Handle_HL.ConfigurarVelocidad( 9600 )
  Handle_HL.ConfigurarPuerto( PUERTO )
  error = Handle_HL.Conectar()
  print "Connect               : ",
  print printError(error)

  # try cancel vouchers
  error = Handle_HL.Cancelar()
  print "Cancel voucher        : ",
  print printError(error)

  # download 
  carpeta_de_descarga = "donwloads"

  error = Handle_HL.Descargar(str(desde), str(hasta),CARPETA_DESTINO)
  print "Download              : ",
  print printError(error)

  # disconect
  error = Handle_HL.Desconectar()
  print "Disconect             : ",
  print printError(error)

  return { "status" : True , "desde" : desde , "hasta" : hasta }

# -----------------------------------------------------------------------------
# Function: audit
# -----------------------------------------------------------------------------

def auditoria(TipoDetalle,desde,hasta):

  ID_MODIFICADOR_AUDITORIA_DETALLADA  = 500
  ID_MODIFICADOR_AUDITORIA_RESUMIDA   = 501

  #title 
  print "*** AUDIT ***"

  return { "status" : True , "desde" : desde , "hasta" : hasta, "tipo_detalle" : TipoDetalle}

  # get handle from DLL
  Handle_HL = windll.LoadLibrary("EpsonFiscalInterface.dll")

  # connect
  Handle_HL.ConfigurarVelocidad( 9600 )
  Handle_HL.ConfigurarPuerto( PUERTO )
  error = Handle_HL.Conectar()
  print "Connect               : ",
  print printError(error)

  # try cancel all
  error = Handle_HL.Cancelar()
  print "Cancel voucher        : ",
  print printError(error)

  # audit 
  error = Handle_HL.ImprimirAuditoria( int(TipoDetalle),str(desde),str(hasta))
  print "Audit Detail         : ",
  print printError(error)

  # disconect
  error = Handle_HL.Desconectar()
  print "Disconect             : ",
  print printError(error)


# -----------------------------------------------------------------------------
# Function: printError
# -----------------------------------------------------------------------------

def printError(codigo):
  # get handle from DLL
  Handle_HL = windll.LoadLibrary("EpsonFiscalInterface.dll")
  # connect
  Handle_HL.ConfigurarVelocidad( 9600 )
  Handle_HL.ConfigurarPuerto( PUERTO )
  error = Handle_HL.Conectar()
  response = create_string_buffer( b'\000' * 200 )
  error = Handle_HL.ConsultarDescripcionDeError(int(codigo),response,200)
  return str(response.value)


def abrirCarpeta():

  string_path = 'explorer "' + CARPETA_DESTINO + '"'
  print "abriendo carpeta " + string_path
  subprocess.Popen(string_path)