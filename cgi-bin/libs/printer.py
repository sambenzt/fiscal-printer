from ctypes import byref, c_int, c_char, c_long, c_short, create_string_buffer
from ctypes import windll
import binascii

from libs.factura_a import *
from libs.factura_b import *
from libs.tique import *
from libs.tique_nota_credito import *
from libs.factura_a_nota_credito import *
from libs.factura_b_nota_credito import *
from libs.cierre_z import *
from libs.afip import *

class Printer:

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

        punto_venta     = jsonData['punto_venta']
        comprobante     = jsonData['comprobante']
        descuento       = jsonData['descuento']
        items           = jsonData['items']

        print "Tique Nota de Credito"
        print "Comprobante: 110-" + punto_venta + "-" + comprobante 

        return self.res({"printer":ticket_credit_note(punto_venta,comprobante,descuento,items)},200)

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
    
    def FacturaANotaCredito(self,jsonData):

        punto_venta     = jsonData['punto_venta']
        comprobante     = jsonData['comprobante']
        nombreComprador = jsonData['nombre_comprador']
        direccion       = jsonData['direccion']
        documento       = jsonData['documento']
        descuento       = jsonData['descuento']
        items           = jsonData['items']

        return self.res({"printer":invoice_A_credit_note(punto_venta,comprobante,nombreComprador,direccion,documento,descuento,items)},200)

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

    def FacturaBNotaCredito(self,jsonData):
        
        punto_venta     = jsonData['punto_venta']
        comprobante     = jsonData['comprobante']
        nombreComprador = jsonData['nombre_comprador']
        direccion       = jsonData['direccion']
        documento       = jsonData['documento']
        descuento       = jsonData['descuento']
        tipoResponsable = jsonData['codigo_responsable']
        items           = jsonData['items']

        return self.res({"printer":invoice_B_credit_note(punto_venta,comprobante,nombreComprador,direccion,documento,descuento,items,tipoResponsable)},200)


    def infoImpresora(self):
        equipment_machine_version()
        return self.res({"status": 1 , "info": "info impresora"},200)

    def cancelarTodo(self):
        cancel_all()
        return self.res({"status": 1 , "info": "Cancelar todo"},200)

    def Informe_afip(self,jsonData):

        desde = jsonData['desde']
        hasta = jsonData['hasta']

        return self.res({"printer":descarga(desde,hasta)},200)

    def Auditoria(self,jsonData):

        tipoDetalle = jsonData['tipo_detalle']
        desde       = jsonData['desde']
        hasta       = jsonData['hasta']

        return self.res({"printer":auditoria(tipoDetalle,desde,hasta)},200)

    