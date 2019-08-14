from ctypes import byref, c_int, c_char, c_long, c_short, create_string_buffer
from ctypes import windll
import binascii
from libs.app_client_using_dll import *

class Printer:

    def __init__(self,response):
        self.response = response

    def res(self,param,code):
        return self.response(param,code)

    def TiqueFiscal(self,jsonData):
       
        items     = jsonData['items']
        descuento = jsonData['descuento']
        pagaCon   = jsonData['paga_con']
        recargo   = jsonData['recargo']
        
        #return self.res({"printer" : self.yeison() },201)
        return self.res({"printer" : ticket(items,descuento,pagaCon,recargo)},201)

    def TiqueNotaDebito(self,jsonData):
        ticket_debit_note()

    
    