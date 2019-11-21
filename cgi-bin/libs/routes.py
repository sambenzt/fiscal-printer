import json
from libs.printer import Printer

class Routes:
    
    def __init__(self,http,body,response):
        self.http     = http
        self.body     = body
        self.response = response
 
        
    def res(self,param,code):
        
        self.http.send_response(code)
        self.http.send_header('Content-type', 'application/json')
        self.http.end_headers()

        if type(param) is dict:
           output = json.dumps(param)
        else:
            output = param

        return  self.response.write(bytes((str(output)).replace("'",'"')))
        
    def parse(self,string):
        s       = str(string)
        strJson = ((s.replace("b'{\\n\\t",'{')).replace("\\n}'","}").replace('\\n\\t\\t','')).replace('\\n\\t','')
        j       = json.loads(strJson)
        return j
       
    def init(self):
        jsonData = self.parse(self.body)
        printer  = Printer(self.res)

        if jsonData['tipo'] == 'z':
            return printer.Z()

        elif jsonData['tipo'] == 'info':
            return printer.infoImpresora()

        elif jsonData['tipo'] == 'Tique':
           return printer.TiqueFiscal(jsonData)
            
        elif jsonData['tipo'] == 'Tique nota de credito':
           return printer.TiqueNotaCredito(jsonData)

        elif jsonData['tipo'] == 'Factura A':
            print "Route Factura A"
            return printer.FacturaA(jsonData)
            
        elif jsonData['tipo'] == 'Factura B':
            print "Route Factura B"
            return printer.FacturaB(jsonData)
            
        elif jsonData['tipo'] == 'Factura A nota de credito':
            return printer.FacturaANotaCredito(jsonData)
            
        elif jsonData['tipo'] == 'Factura B nota de credito':
            return printer.FacturaBNotaCredito(jsonData)

        elif jsonData['tipo'] == 'Archivos AFIP':
            return printer.Informe_afip(jsonData)

        elif jsonData['tipo'] == 'Auditoria':
            return printer.Auditoria(jsonData)

        else:
            return res('no se encontro el tipo',404)
            
  
            

        
        
    