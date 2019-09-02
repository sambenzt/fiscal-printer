from ctypes import byref, c_int, c_char, c_long, c_short, create_string_buffer
from ctypes import windll
import binascii

PUERTO = '0'

def print_Z():

  # get handle from DLL
  Handle_HL = windll.LoadLibrary("EpsonFiscalInterface.dll")

  # connect
  Handle_HL.ConfigurarVelocidad( 9600 )
  Handle_HL.ConfigurarPuerto( PUERTO )
  error = Handle_HL.Conectar()
  print "Connect               : ",
  print printError(error)

  # print Z
  error = Handle_HL.ImprimirCierreZ()
  print "Closure Day           : ",
  print printError(error)

  # close port
  error = Handle_HL.Desconectar()
  print "Disconect             : ",
  print printError(error)

  return { "status" : True }

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

