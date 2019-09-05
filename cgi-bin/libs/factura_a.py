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

def ticket_invoice_A(nombreComprador,direccion,descuento,documento,items,formaPago,cuotas):


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

  str_doc_number_max_len = 20
  punto_venta = create_string_buffer( b'\000' * str_doc_number_max_len )
  error = Handle_HL.ConsultarNumeroPuntoDeVenta( punto_venta, str_doc_number_max_len )
  print "Punto de venta Error : ",
  print printError(error)
  print "Punto de venta       : ",
  print punto_venta.value

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

  # get document number
  str_doc_number_max_len = 20
  str_doc_number = create_string_buffer( b'\000' * str_doc_number_max_len )
  error = Handle_HL.ConsultarNumeroComprobanteActual( str_doc_number, str_doc_number_max_len )
  print "Get Doc. Number Error : ",
  print printError(error)
  print "Doc Number            : ",
  print str_doc_number.value

  alic = alicuotas(items,descuento,True)
 
  ID_MODIFICADOR      = 200
  CODIGO_FORMA_PAGO   = int(formaPago)
  CANTIDAD_CUOTAS     = int(cuotas)
  MONTO               = str(alic['total'])
  DESCRIPCION_CUPONES = ""
  DESCRIPCION         = "", 
  DESCRIPCION_EXTRA1  = ""
  DESCRIPCION_EXTRA2  = ""

  if CODIGO_FORMA_PAGO != 20:
    CANTIDAD_CUOTAS = 0


  # cargar pago
  error = Handle_HL.CargarPago( ID_MODIFICADOR , CODIGO_FORMA_PAGO , CANTIDAD_CUOTAS, MONTO , DESCRIPCION_CUPONES , "" , "" , "" )
  print "Discount              : ",
  print printError(error)

  # close
  error = Handle_HL.CerrarComprobante()
  print "Close                 : ",
  print error

  # disconect
  error = Handle_HL.Desconectar()
  print "Disconect             : ",
  print error

  return { "status" : True, "punto_venta" : punto_venta.value , "comprobante" : str_doc_number.value , "codigo_pago" : CODIGO_FORMA_PAGO,  "cuotas" : CANTIDAD_CUOTAS , "descuento" : descuento,  "alicuotas" : alic }

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
# Function: alicuotas
# -----------------------------------------------------------------------------

def alicuotas(items,descuento,consola):
   
    importe_1050 = 0 
    importe_2100 = 0 
    importe_0000 = 0

    for i in range(0, len(items)):      
        producto       = str(items[i]['producto'])
        peso           = str(items[i]['peso'])
        precio         = str(items[i]['precio_sin_iva'])
        precio_con_iva = round(float(precio) * (1 + float(items[i]['iva']) / 100),2)
        iva            = float((items[i]['iva']))
        importe        = round(float(peso) * float(precio),2)

        if(iva == 10.50):
            importe_1050 = importe_1050 + importe
        elif(iva == 21):
            importe_2100 = importe_2100 + importe
        elif(iva == 0):
            importe_0000 = importe_0000 + importe
        #print "Item                  : " + producto + " importe " + str(importe)
 
    subtotal         = importe_0000 + importe_1050 + importe_2100
    descuento_0000   = round(descuento * importe_0000 / subtotal,2)
    descuento_1050   = round(descuento * importe_1050 / subtotal,2)
    descuento_2100   = round(descuento * importe_2100 / subtotal,2)
    gravado_0000_dto = importe_0000 - descuento_0000
    gravado_1050_dto = importe_1050 - descuento_1050
    gravado_2100_dto = importe_2100 - descuento_2100
    alicuota_0000    = round((importe_0000 - descuento_0000) * 0/100,2)
    alicuota_2100    = round((importe_2100 - descuento_2100) * 21/100,2)
    alicuota_1050    = round((importe_1050 - descuento_1050) * 10.5/100,2)
    subtotal_neto    = gravado_1050_dto + gravado_2100_dto
    total            = round(gravado_0000_dto,2) +  round(gravado_1050_dto,2) + round(gravado_2100_dto,2) + round(alicuota_0000,2) + round(alicuota_1050,2) + round(alicuota_2100,2)

    if consola:
        print ""
        print "*****************************************************"
        print "DESCUENTO:........................." + str(descuento)
        print ""
        print "GRAVADO (0.00):...................." + str(importe_0000)
        print "GRAVADO (21.00):..................." + str(importe_2100)
        print "GRAVADO (10.50):..................." + str(importe_1050)
        print ""
        print "SUBTOTAL:.........................." + str(subtotal)
        print ""
        print "DTO (0.00):........................-" + str(descuento_0000)
        print "DTO (21.00):.......................-" + str(descuento_2100)
        print "DTO (10.50):.......................-" + str(descuento_1050)
        print ""
        print "GRAVADO - DTO (0.00):..............." + str(gravado_0000_dto)
        print "GRAVADO - DTO (21.00):.............." + str(gravado_2100_dto)
        print "GRAVADO - DTO (10.50):.............." + str(gravado_1050_dto)
        print ""
        print "SUBTOTAL EXENTO:...................." + str(gravado_0000_dto)
        print "SUBTOTAL NETO GRAVADO:.............." + str(subtotal_neto)
        print "ALICUOTA (0.00):...................." + str(alicuota_0000)
        print "ALICUOTA (21.00):..................." + str(alicuota_2100)
        print "ALICUOTA (10.50):..................." + str(alicuota_1050)
        print "TOTAL:.............................." + str(total)
        print "*****************************************************"
        print ""

    return {"gravado_0000" : round(gravado_0000_dto,2) , "gravado_1050" : round(gravado_1050_dto,2) , "gravado_2100" : round(gravado_2100_dto,2), "alicuota_0000" : round(alicuota_0000,2) ,"alicuota_1050" : round(alicuota_1050,2) , "alicuota_2100" : round(alicuota_2100,2) , "total" : total}
    
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




