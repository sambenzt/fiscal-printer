def ticket_invoice_B(nombreComprador,descuento,tipoDocumento,documento,tipoResponsable,items):
 
  #title 
  print "*** TICKET INVOICE 'B' ***"

  # get handle from DLL
  Handle_HL = windll.LoadLibrary("EpsonFiscalInterface.dll")

  # connect
  Handle_HL.ConfigurarVelocidad( 9600 )
  Handle_HL.ConfigurarPuerto( "0" )
  error = Handle_HL.Conectar()
  print "Connect               : ",
  print printError(error)

  # cancel
  error = Handle_HL.Cancelar()
  print "Cancel                : ",
  print printError(error)

  # load customer data
  error = Handle_HL.CargarDatosCliente( str(nombreComprador), " ", " ", " ", " ", int(tipoDocumento), str(documento), ID_RESPONSABILIDAD_IVA_MONOTRIBUTISTA )
  print "Customer Data         : ",
  print printError(error)

  # open
  error = Handle_HL.AbrirComprobante( ID_TIPO_COMPROBANTE_TIQUE_FACTURA )
  print "Open                  : ",
  print printError(error)

  # fixed info
  send_fixed_invoice_body( Handle_HL,items )

  # global discount
  error = Handle_HL.CargarAjuste( ID_MODIFICADOR_DESCUENTO, "Descuento", str(descuento), 0, "CodigoInterno4567890123456789012345678901234567890"  )
  print "Discount              : ",
  print printError(error)



  # close
  error = Handle_HL.CerrarComprobante()
  print "Close                 : ",
  print printError(error)

  # disconect
  error = Handle_HL.Desconectar()
  print "Disconect             : ",
  print printError(error)