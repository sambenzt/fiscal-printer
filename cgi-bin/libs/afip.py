from ctypes import byref, c_int, c_char, c_long, c_short, create_string_buffer
from ctypes import windll
import binascii
import subprocess
import os

PUERTO = '0'

CARPETA_DESTINO = "C:\downloads" 

def descarga(desde,hasta):

  #title 
  print "*** DESCARGANDO ARCHIVOS AFIP ***"

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

  error = Handle_HL.Descargar(str(desde), str(hasta),CARPETA_DESTINO.replace("\\","/"))

  print "Download              : ",
  resultado = printError(error)
  print resultado
  print error

  mensaje = ""
  if error == 2055:
    mensaje = "PERIODO AUDITADO SIN DATOS. VERIFIQUE EL RANGO DE FECHAS"
  
  elif error == 2071:
    mensaje = "FALTA DESCARGAR JORNADAS PREVIAS. REALICE UNA DESCARGAGA PENDIENTE"

  else:
    mensaje = "REPORTES DESCARGADOS"
    abrirCarpeta()


  # disconect
  error = Handle_HL.Desconectar()
  print "Disconect             : ",
  print printError(error)

  return { "resultado" : mensaje }


# -----------------------------------------------------------------------------
# Function: audit
# -----------------------------------------------------------------------------

def descarga_periodo_pendiente():
   #title 
  print "*** DESCARGANDO ARCHIVOS AFIP DEL PERIODO PENDIENTE ***"

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

  error = Handle_HL.DescargarPeriodoPendiente(CARPETA_DESTINO.replace("\\","/"))
  print "Download              : ",
  resultado = printError(error)
  print resultado
  print error

  mensaje = ""
  if error == 83886161:
    mensaje = "NO EXISTE RANGO DE PERIODO DISPONIBLE PARA DESCARGAR"
  else:
    abrirCarpeta()
    mensaje = "REPORTES DESCARGADOS"

  # disconect
  error = Handle_HL.Desconectar()
  print "Disconect             : ",
  print printError(error)

  return { "resultado" : mensaje }

def auditoria(TipoDetalle,desde,hasta):

  ID_MODIFICADOR_AUDITORIA_DETALLADA  = 500
  ID_MODIFICADOR_AUDITORIA_RESUMIDA   = 501

  #title 
  print "*** AUDIT ***"

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
  print "Audit Detail          : ",
  print printError(error)

  # disconect
  error = Handle_HL.Desconectar()
  print "Disconect             : ",
  print printError(error)

  return { "status" : True , "desde" : desde , "hasta" : hasta, "tipo_detalle" : TipoDetalle}

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