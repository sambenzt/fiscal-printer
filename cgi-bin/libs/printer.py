from ctypes import byref, c_int, c_char, c_long, c_short, create_string_buffer
from ctypes import windll
import binascii

from libs.factura_a import *
from libs.factura_b import *
from libs.tique import *
from libs.cierre_z import *

class Printer:

    #  parametro: comprobante
    #  Descripcion del comprobante.
    #  Formato: "ddd:ppppp:nnnnnnnn"
    #  Siendo:
    #  ddd: el tipo de comprobante. (ejemplo: "081")
    #  "83" Tique
    #  "81" Tique Factura A
    #  "82" Tique Factura B, 
    #  "111" Tique Factura C
    #  "118" Tique Factura M
    #  "110" Tique Nota de Credito
    #  "112" Tique Nota de Credito A
    #  "113" Tique Nota de Credito B
    #  "114" Tique Nota de Credito C
    #  "119" Tique Nota de Credito M
    #  "115" Tique Nota de Debito A
    #  "116" Tique Nota de Debito B
    #  "117" Tique Nota de Debito C
    #  "120" Tique Nota de Debito M
    # ppppp: numero de caja. (ejemplo: "00001")
    # nnnnnnnn: numero de comprobante. (ejemplo: "00000027")
    # Los equipos Hera (v.:22.00) y Demeter (v.:22.01) pueden prescindir del
    # formato indicado. Teniendo la posibilidad de cargar un texto libre.

    # parametro: tipoComprobante
    #Identificador del tipo de comprobante:
    # 1 : Tique.
    # 2 : Tique factura A/B/C/M
    # 3 : Tique nota de credito, tique nota credito A/B/C/M.
    # 4 : Tique nota de debito A/B/C/M.
    # 21 : documento no fiscal homologado generico.
    # 22 : documento no fiscal homologado de uso interno.

    # parametro: tipoDocumento
    # 0 : Ningun documento.
    # 1 : D.N.I.
    # 2 : C.U.I.L.
    # 3 : C.U.I.T.
    # 4 : Cedula de identidad.
    # 5 : Pasaporte.
    # 6 : Libreta civica.
    # 7 : Libreta de enrolamiento.

    # parametro: tipoResponsable 
    # 0 : Ninguno.
    # 1 : I.V.A responsable inscripto.
    # 3 : I.V.A no responsable.
    # 4 : I.V.A monotributista.
    # 5 : I.V.A consumidor final.
    # 6 : I.V.A exento.
    # 7 : I.V.A no categorizado.
    # 8 : I.V.A monotributista social.
    # 9 : I.V.A monotributista eventual.
    # 10 : I.V.A monotributista eventual social.
    # 11 : I.V.A monotributo independiente promovido.

    def __init__(self,response):
        self.response = response

    def res(self,param,code):
        return self.response(param,code)

    def set_header(self):
        return set_and_get_header_trailer()

    def Z(self):
        return self.res(print_Z(),200)

    def Error(self):
        return self.res(printError(83886127),200)
        
    def tipoResponsableIva(self):
        tipoResponsable()

    def TiqueFiscal(self,jsonData):
       
        items     = jsonData['items']
        descuento = jsonData['descuento']
        pagaCon   = jsonData['paga_con']
        recargo   = jsonData['recargo']
        formaPago = jsonData['codigo_pago']
        cuotas    = jsonData['cuotas']

        return self.res({"printer" : ticket(items,descuento,pagaCon,recargo,formaPago,cuotas)},201)

    def TiqueNotaCredito(self,jsonData):

        comprobante     = "110-00001-" + str(jsonData['comprobante'])
        tipoComprobante = 3 #integer
        items     = jsonData['items']

        print "Tique Nota de Credito"
        print "Comprobante:" + comprobante 
        print "Tipo comprobante:" + str(tipoComprobante)
        return self.res({"printer":ticket_credit_note(comprobante,tipoComprobante,items)},200)

    def FacturaA(self,jsonData):
        
        items             = jsonData['items']
        descuento         = jsonData['descuento']
        recargo           = jsonData['recargo']
        nombreComprador   = jsonData['nombre_comprador']
        codigoResponsable = jsonData['codigo_responsable']
        direccion         = jsonData['direccion']
        documento         = jsonData['documento']
        formaPago         = jsonData['codigo_pago']
        cuotas            = jsonData['cuotas']


        return self.res({"printer":ticket_invoice_A(nombreComprador,direccion,descuento,documento,items,formaPago,cuotas)},200)
    
    def FacturaB(self,jsonData):
        
        # SOLO ADMITE CUIT!

        items             = jsonData['items']
        descuento         = jsonData['descuento']
        recargo           = jsonData['recargo']
        nombreComprador   = jsonData['nombre_comprador']
        codigoResponsable = jsonData['codigo_responsable']
        direccion         = jsonData['direccion']
        documento         = jsonData['documento']
        formaPago         = jsonData['codigo_pago']
        cuotas            = jsonData['cuotas']

        return self.res({"printer":ticket_invoice_B(nombreComprador,codigoResponsable,direccion,descuento,documento,items,formaPago,cuotas)},200)

    def infoImpresora(self):
        equipment_machine_version()
        return self.res({"status": 1 , "info": "info impresora"},200)

    def cancelarTodo(self):
        cancel_all()
        return self.res({"status": 1 , "info": "Cancelar todo"},200)
    
    