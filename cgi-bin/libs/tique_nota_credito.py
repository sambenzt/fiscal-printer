from ctypes import byref, c_int, c_char, c_long, c_short, create_string_buffer
import binascii
import sys
from ctypes import windll

PUERTO = "0"
ID_TIPO_DOCUMENTO_NINGUNO                    = 0
ID_RESPONSABILIDAD_IVA_CONSUMIDOR_FINAL      = 5
ID_MODIFICADOR_ANULAR                        = 201
ID_MODIFICADOR_AGREGAR                       = 200
ID_CODIGO_INTERNO                            = 1
AFIP_CODIGO_UNIDAD_MEDIDA_KILOGRAMO          = 1 
ID_TASA_IVA                                  = 0 #funciona con 1 - 5 -
ID_IMPUESTO_NINGUNO                          = 0
ID_MODIFICADOR_DESCUENTO                     = 400
ID_TIPO_COMPROBANTE_TIQUE_NOTA_DE_CREDITO    = 3 


# 083 Tique.
# 081 Tique factura A.
# 082 Tique factura B.
# 110 Tique nota de credito.
# 112 Tique nota de credito A.
# 113 Tique nota de credito B.




# -----------------------------------------------------------------------------
# Function: ticket_credit_note
# -----------------------------------------------------------------------------
def ticket_credit_note(punto_venta,comprobanteAsociado,descuento,items):

  #title 
  print "*** TICKET CREDIT NOTE ***"
  
  # get handle from DLL
  Handle_HL = windll.LoadLibrary("EpsonFiscalInterface.dll")

  # connect
  Handle_HL.ConfigurarVelocidad( 9600 )
  Handle_HL.ConfigurarPuerto( PUERTO )
  error = Handle_HL.Conectar()
  print "Connect               : ",
  print printError(error)

  # try cancel
  error = Handle_HL.Cancelar()
  print "Cancel                : ",
  print printError(error)

  str_date_len = 20
  fecha = create_string_buffer( b'\000' * str_date_len )
  error = Handle_HL.ConsultarFechaHora( fecha, str_date_len )
  print "Fecha Impresora       : ",
  print printError(error)
  print "Fecha                 : ",
  print parse_date(fecha.value)

  # load customer data
  error = Handle_HL.CargarDatosCliente( "CONSUMIDOR FINAL", " ", " ", " ", " ", ID_TIPO_DOCUMENTO_NINGUNO, "0", ID_RESPONSABILIDAD_IVA_CONSUMIDOR_FINAL )
  print "Customer Data         : ",
  print printError(error)

  # load customer data
  print "Comprobante asociado  :" +  "110-" + str(punto_venta) + "-" + str(comprobanteAsociado)
  error = Handle_HL.CargarComprobanteAsociado( "110-" + str(punto_venta) + "-" + str(comprobanteAsociado) )
  print "main source voucher   : ",
  print printError(error)

  # open
  error = Handle_HL.AbrirComprobante( ID_TIPO_COMPROBANTE_TIQUE_NOTA_DE_CREDITO )
  print "Open                  : ",
  print printError(error)

  # fixed info
  send_fixed_invoice_body_note( Handle_HL , items )

  # global discount
  error = Handle_HL.CargarAjuste( ID_MODIFICADOR_DESCUENTO, "APLICADO", str(descuento), 0, "CodigoInterno4567890123456789012345678901234567890"  )
  print "Discount              : ",
  print printError(error)

  # get document number
  str_doc_number_max_len = 20
  str_doc_number = create_string_buffer( b'\000' * str_doc_number_max_len )
  error = Handle_HL.ConsultarNumeroComprobanteActual( str_doc_number, str_doc_number_max_len )
  print "Get Doc. Number Error : ",
  print printError(error)
  print "Doc Number            : ",
  print str_doc_number.value

  # close
  error = Handle_HL.CerrarComprobante()
  print "Close                 : ",
  print printError(error)

  # disconect
  error = Handle_HL.Desconectar()
  print "Disconect             : ",
  print printError(error)

  return { "status" : True, "fecha" : parse_date(fecha.value),  "tipo" : "tique nota de credito" , "punto_venta" : punto_venta , "comprobante" : str_doc_number.value  }
 

# -----------------------------------------------------------------------------
# Function: send_fixed_invoice_body para nota de credito - debito
# -----------------------------------------------------------------------------
def send_fixed_invoice_body_note( Handle_HL , items ):

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
    precio_con_iva = str(round(float(precio) * (1 + float(items[i]['iva']) / 100),2))
    error    = Handle_HL.ImprimirItem( ID_MODIFICADOR_AGREGAR, producto, peso, precio_con_iva, iva , ID_IMPUESTO_NINGUNO, "", ID_CODIGO_INTERNO, "CodigoInterno4567890123456789012345678901234567890", "", AFIP_CODIGO_UNIDAD_MEDIDA_KILOGRAMO )
    print "Item                  : ",
    print printError(error)
 
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

def parse_date(fecha):
    lfecha = list(fecha)
    dia    = str(lfecha[0]) + str(lfecha[1])
    mes    = str(lfecha[2]) + str(lfecha[3])
    hora   = str(lfecha[7]) + str(lfecha[8]) + ':' + str(lfecha[9]) + str(lfecha[10]) + ':' + str(lfecha[11]) + str(lfecha[12])
    return  '20' + str(lfecha[4]) + str(lfecha[5]) + '-' + mes + '-' + dia + ' ' + hora


