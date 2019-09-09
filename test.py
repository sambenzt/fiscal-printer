import json


def parse(string):
    s       = str(string)
    strJson = ((s.replace("b'{\\n\\t",'{')).replace("\\n}'","}").replace('\\n\\t\\t','')).replace('\\n\\t','')
    j       = json.loads(strJson)
    return j

#main



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
        importe        = round(float(peso) * float(precio_con_iva),2)

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
    alicuota_0000    = round(gravado_0000_dto * 0/100,2)
    alicuota_2100    = round(gravado_2100_dto * 21/100,2)
    alicuota_1050    = round(gravado_1050_dto * 10.5/100,2)
    gravado_0000_dto = gravado_0000_dto - alicuota_0000
    gravado_1050_dto = gravado_1050_dto - alicuota_1050
    gravado_2100_dto = gravado_2100_dto - alicuota_2100
    subtotal_neto    = gravado_1050_dto + gravado_2100_dto
    total            = gravado_0000_dto + subtotal_neto + alicuota_0000 + alicuota_2100 + alicuota_1050

    if consola:
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
        print ""

    return {"gravado_0000" : round(gravado_0000_dto,2) , "gravado_1050" : round(gravado_1050_dto,2) , "gravado_2100" : round(gravado_2100_dto,2), "alicuota_0000" : round(alicuota_0000,2) ,"alicuota_1050" : round(alicuota_1050,2) , "alicuota_2100" : round(alicuota_2100,2) , "total" : total}
   
   



jsons = '[{"producto":"ASADO","precio_sin_iva":77.6,"peso":0.855,"codigo_iva":1,"iva":0},{"producto":"VACIO","precio_sin_iva":77.6,"peso":2.255,"codigo_iva":1,"iva":0},{"producto":"MILANESA","precio_sin_iva":77.6,"peso":2.555,"codigo_iva":5,"iva":21},{"producto":"PESCADO","precio_sin_iva":77.6,"peso":0.75,"codigo_iva":5,"iva":21},{"producto":"CUADRIL","precio_sin_iva":77.6,"peso":0.75,"codigo_iva":4,"iva":10.5},{"producto":"LOMO","precio_sin_iva":77.6,"peso":1.35,"codigo_iva":4,"iva":10.5}]'

items        = parse(jsons)
descuento    = 30
detalle = alicuotas(items,descuento,True)

