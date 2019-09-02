from ctypes import byref, c_int, c_char, c_long, c_short, create_string_buffer
import binascii
import sys
from ctypes import windll

PUERTO = "0"
ID_TIPO_DOCUMENTO_CUIT                       = 3
ID_RESPONSABILIDAD_IVA_RESPONSABLE_INSCRIPTO = 1
ID_TIPO_COMPROBANTE_TIQUE_FACTURA            = 2   # "81"  Tique Factura A, "82" Tique Factura B, "111" Tique Factura C, "118" Tique Factura M
ID_MODIFICADOR_AGREGAR                       = 200
ID_CODIGO_INTERNO                            = 1
AFIP_CODIGO_UNIDAD_MEDIDA_KILOGRAMO          = 1 
ID_TASA_IVA                                  = 0 #funciona con 1 - 5 -
ID_IMPUESTO_NINGUNO                          = 0
ID_MODIFICADOR_DESCUENTO                     = 400

#todos los campos son obligatorios

def ticket_invoice_A(nombreComprador,direccion,descuento,documento,items):


  #title 
  print "*** TICKET INVOICE 'A' ***"

  # get handle from DLL
  Handle_HL = windll.LoadLibrary("EpsonFiscalInterface.dll")

  # connect
  Handle_HL.ConfigurarVelocidad( 9600 )
  Handle_HL.ConfigurarPuerto( "0" )
  error = Handle_HL.Conectar()
  print "Connect               : ",
  print error

  # cancel
  error = Handle_HL.Cancelar()
  print "Cancel                : ",
  print error

  # load customer data
  error = Handle_HL.CargarDatosCliente( str(nombreComprador), "",str(direccion), "", "", ID_TIPO_DOCUMENTO_CUIT, str(documento), ID_RESPONSABILIDAD_IVA_RESPONSABLE_INSCRIPTO )
  print "Customer Data         : ",
  print error

  # open
  error = Handle_HL.AbrirComprobante( ID_TIPO_COMPROBANTE_TIQUE_FACTURA )
  print "Open                  : ",
  print error

  # fixed info
  send_fixed_invoice_body( Handle_HL , items )

  error = Handle_HL.CargarAjuste( ID_MODIFICADOR_DESCUENTO, "Descuento", str(descuento), 0, "CodigoInterno4567890123456789012345678901234567890"  )
  print "Discount              : ",
  print error

  # close
  error = Handle_HL.CerrarComprobante()
  print "Close                 : ",
  print error

  # disconect
  error = Handle_HL.Desconectar()
  print "Disconect             : ",
  print error

# -----------------------------------------------------------------------------
# Function: send_fixed_invoice_body para facturar
# -----------------------------------------------------------------------------
def send_fixed_invoice_body( Handle_HL , items ):

  # get document number
  str_doc_number_max_len = 20
  str_doc_number = create_string_buffer( b'\000' * str_doc_number_max_len )
  error = Handle_HL.ConsultarNumeroComprobanteActual( str_doc_number, str_doc_number_max_len )
  print "Get Doc. Number Error : ",
  print printError(error)
  print "Doc Number            : ",
  print str_doc_number.value

  # get document type
  str_doc_type_max_len = 20
  str_doc_type = create_string_buffer( b'\000' * str_doc_type_max_len )
  error = Handle_HL.ConsultarTipoComprobanteActual( str_doc_type, str_doc_type_max_len )
  print "Get Type Doc. Error   : ",
  print printError(error)
  print "Doc Type              : ",
  print str_doc_type.value 

  for i in range(0, len(items)):      
    producto = str(items[i]['producto'])
    peso     = str(items[i]['peso'])
    precio   = str(items[i]['precio_sin_iva'])
    iva      = int((items[i]['codigo_iva']))
    error    = Handle_HL.ImprimirItem( ID_MODIFICADOR_AGREGAR, producto, peso, precio, iva , ID_IMPUESTO_NINGUNO, "", ID_CODIGO_INTERNO, "CodigoInterno4567890123456789012345678901234567890", "", AFIP_CODIGO_UNIDAD_MEDIDA_KILOGRAMO )
    print "Item                  : ",
    print printError(error)
    #print "producto: " + producto + " - peso: " + peso + " - precio: " + precio

  # subtotal
  error = Handle_HL.ImprimirSubtotal()
  print "Subtotal              : ",
  print printError(error)

  # get subtotal gross amount
  str_subtotal_max_len = 20
  str_subtotal = create_string_buffer( b'\000' * str_subtotal_max_len )
  error = Handle_HL.ConsultarSubTotalBrutoComprobanteActual( str_subtotal, str_subtotal_max_len )
  print "Get Subtotal Gross    : ",
  print printError(error)
  print "Subtotal Gross Amount : ",
  print str_subtotal.value

  # get subtotal gross amount
  str_subtotal_max_len = 20
  str_subtotal = create_string_buffer( b'\000' * str_subtotal_max_len )
  error = Handle_HL.ConsultarSubTotalNetoComprobanteActual( str_subtotal, str_subtotal_max_len )
  print "Get Subtotal Net      : ",
  print printError(error)
  print "Subtotal Net Amount   : ",
  print str_subtotal.value


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

