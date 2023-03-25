from enlace import *
import time
import numpy as np
import random
import datetime

serialName = "COM4"
#head = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
ocioso = True

def verifica_handShake(com):
    global ocioso
    handshake, nRx = com.getData(10) # Handshake agora tem apenas 10
    print(handshake)
    time.sleep(.1)

    tipo = handshake[0] #tipo da mensagem
    identificador = handshake[1] #identificador que diz se é para o servidor ou não
    total_pacotes = handshake[3]

    if tipo == 1: # handshake ok
        print('recebi mensagem tipo 1')
        if identificador == 23:
            print("mensagem é pra mim")
            com.rx.clearBuffer()
            ocioso = False
            return ocioso, total_pacotes, handshake
           
        else:
            print("mensagem não é para mim")
            time.sleep(.1)   
            ocioso = True
            return ocioso, total_pacotes, handshake
        
            
    
    else:
        print("o tipo não é 1")
        com.rx.clearBuffer()
        time.sleep(.1)
        ocioso = True
        return ocioso, total_pacotes, handshake
        
    
        
        
def envia_tipo2(com, h,t):
    print('envia pacote tipo 2')
    head = (2).to_bytes(1, byteorder='big') + b'\x00' + b'\x00' + (h[3]).to_bytes(1, byteorder = 'big') + b'\x00' + (t).to_bytes(1,byteorder = 'big') + b'\x01'+b'\x00\x00\x00'
    
    payload = b'\x01'
    eop = (1).to_bytes(4, byteorder='big')
    msg2 = head + payload + eop
    com.sendData(bytearray(msg2))
    print('pacote tipo 2 enviado')

#função de criar pacote para envio ao cliente
def cria_envia_pacote(com,h,p,tipo): #com, head, payload e tipo da mensagem
    print(f'envia pacote tipo {tipo}')
    if h[6] == 0:
        head = (tipo).to_bytes(1, byteorder='big') + b'\x00' + b'\x00' + (h[3]).to_bytes(1, byteorder = 'big') + (h[4]).to_bytes(1, byteorder = 'big') + (len(p)).to_bytes(1,byteorder = 'big') +(h[6]).to_bytes(1,byteorder = 'big')+b'\x00\x00\x00'
    
    else:
        head = (tipo).to_bytes(1, byteorder='big') + b'\x00' + b'\x00' + (h[3]).to_bytes(1, byteorder = 'big') + (h[4]).to_bytes(1, byteorder = 'big') + (len(p)).to_bytes(1,byteorder = 'big') + (h[6]-1).to_bytes(1,byteorder = 'big')+b'\x00\x00\x00'
    

    payload = b'\x01'
    eop = (1).to_bytes(4, byteorder='big')
    msg = head+payload+eop
    com.sendData(bytearray(msg))




#função de quebra do pacote
def pega_pacote(com,t1,t2):

    #time.sleep(5)
    
    while com.rx.getBufferLen() < 10  :
        tf = time.time()
        print('Ainda não')
    tempo = tf - t1

                
            
        
   #     tempo = time.time()
    #if tempo >2:
    #    deu time out
    head,nRx = com.getData(10)#pego o head, que são os 12 primeiros
    print(f'head: {head, nRx}')
    #tipo = head[0] #tipo da mensagem
    payload, nRx = com.getData(head[5]) #pedo o payload
    eop,nRx = com.getData(4) #verifico se os três últimos batem com o eop definido por nós
    return head, payload, eop, tempo

         


    
#def monta_imagem(p):
 #   imagem_final += p
        



def main():
    imagem_final = b''
    try:
        print("Iniciou o main")
        com3 = enlace(serialName)
        com3.enable()
        #byte de sacrifício
        print("esperando 1 byte de sacrifício") 
        rxBuffer, nRx = com3.getData(1)
        com3.rx.clearBuffer()
        time.sleep(.1)

        print("Esperando a conexão")
        ocioso, total_pacotes, head= verifica_handShake(com3) #deve fazer o primeiro bloco

        print(ocioso)
        while ocioso:
            #VF, n_pacotes = verifica_handShake(com3)
            continue
        print("Conexão bem-sucedida")


        envia_tipo2(com3,head,total_pacotes) #enviando mensagem tipo 2
        contagem_pacote = 1
       

        while contagem_pacote <= total_pacotes:
            
            t1 = time.time() #set timer 1
            t2 = time.time() #set timer 2
            
            com3.rx.clearBuffer() #talvez seja interessante
            head, payload,eop,tempo = pega_pacote(com3, t1,t2)
            tipo = head[0]

            
            if tipo == 3:
                print("checando número do pacote")
                n_pacote = head[4]
                print(f"numero do pacote é {n_pacote}")
                print(f'contagem_pacote é {contagem_pacote}')
                print(f'p eop é {eop}')
                with open('registros\servidor1.txt', 'a') as servidor1:
                        a = datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')
                        
                        servidor1.write(str(a) + ' ' + 'recebimento' + ' '+ '3' + '\n')
                if contagem_pacote == n_pacote and eop ==  b'\x00\x00\x00\x01': #talvez de erro nesse if
                    imagem_final += payload
                    cria_envia_pacote(com3,head,payload,4) #crio e envio pacote do tipo 4
                    contagem_pacote += 1
                    with open('registros\servidor1.txt', 'a') as servidor1:
                        a = datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')
                        
                        servidor1.write(str(a)  + ' ' + 'envio'+ ' ' + '4' + '\n')
                    
                else:
                    with open('registros\servidor2.txt', 'a') as servidor2:
                        a = datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')
                    
                        servidor2.write(str(a)  + ' ' + 'recebimento'+ ' ' + str(tipo) + '\n')
                    with open('registros\servidor2.txt', 'a') as servidor2:
                        a = datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')
                    
                        servidor2.write(str(a)  + ' ' + 'envio'+ ' ' + '6' + '\n')
                    cria_envia_pacote(com3, head, payload, 6)
                    
                    
            #se não for do tipo 3
            elif tipo == 5:
                ocioso = True
                print("deu time out no client")
                break
            
                    
            else:
                time.sleep(.1)
                if tempo > 20:
                    cria_envia_pacote(com3,head,payload,5)
                    with open('registros\servidor3.txt', 'a') as servidor3:
                        a = datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')
                        
                        servidor3.write(str(a)  + ' ' + 'recebimento'+ ' ' + str(tipo) + '\n')
                    with open('registros\servidor3.txt', 'a') as servidor3:
                        a = datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')
                
                        servidor3.write(str(a) + ' ' + 'envio'+ ' ' + '5' + '\n')
                    ocioso = True

                    print('encerrando comunicação')
                    break
                print("deu ruim pra caralho")
                if tempo > 2:
                    print("averiguando pacote 3")
                    cria_envia_pacote(com3,head,payload,4)
                    with open('registros\servidor4.txt', 'a') as servidor4:
                        a = datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')
                        
                        servidor4.write(str(a)  + ' ' + 'recebimento'+ ' ' + str(tipo) + '\n')
                    with open('registros\servidor4.txt', 'a') as servidor4:
                        a = datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')
                        
                        servidor4.write(str(a)  + ' ' + 'envio'+ ' ' + '4' + '\n')
                    t1 = time.time()
                else:
                    #pego novamente!!!!
                    com3.rx.clearBuffer() #talvez seja interessante
                    head, payload,eop = pega_pacote(com3)


        
        print('salvando imagem')
        imageW = 'img/linhaCopia.png'
        f = open(imageW, 'wb')
        f.write(imagem_final)
        f.close()

        com3.disable()

        


    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com3.disable()
            


if __name__ == "__main__":
    main()        