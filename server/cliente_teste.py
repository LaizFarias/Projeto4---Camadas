from enlace import *
import time
import numpy as np
import random
import datetime as dt


serialName = "COM3"

def main():
    try:
        print("Iniciou o main")
        com3 = enlace(serialName)
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação serial 
        com3.enable()
        time.sleep(.2)
        com3.sendData(b'00')
        time.sleep(1)
        #começa aqui


        #------------------------------------------------------------------
        #processo de transformação da imagem em bytes para ser transmitida
        #------------------------------------------------------------------

        imagem = "./img/imgs.jpg"
        img_bytes = open(imagem, 'rb').read()

        '''Contabilizar quantos pacotes serão necessários para enviar a imagem'''
        if len(img_bytes) % 144 == 0:
            n_pacotes = len(img_bytes)//144
        else:
            n_pacotes = len(img_bytes)//144 + 1

        print('tamanho da imagem{}'.format(n_pacotes))


        inicia = False
        # 01 =  Tipo de mensagem. 
        # 23 = Se tipo for 1: número do servidor. Qualquer outro tipo: livre
        # 00 =  quando é nada
        # 3ds = Se tipo for handshake: id do arquivo (crie um para cada arquivo).
        
        while inicia is False:
            head1 = b'\x01\x17\x00' + (n_pacotes).to_bytes(1, byteorder='big') + b'\x00\x3c\x00\x00\x00\x00' 
            eop = (1).to_bytes(4,byteorder='big')

            handshake = (head1+eop)
            print(f'Esse é o handshake: {handshake}')
            print('quero falar com vc')
            com3.sendData(bytearray(handshake))

            t0 = time.time()
            while com3.rx.getBufferLen() is True:
                tf = time.time()
                if t0-tf >= 5:

                    print('---------------------------')
                    print(       'Deu ruim!'  ':('     )
                    print('---------------------------')
                    com3.sendData(bytearray(handshake))
                    t0 = time.time()
            else:
                rxBuffer, nRx = com3.getData(10)
                print(rxBuffer)
                if rxBuffer[0]== 2:
                    print('---------------------------------')
                    print("Conexão estabelecida com sucesso!")
                    print('---------------------------------')
                    inicia = True
                    com3.rx.clearBuffer()   



        #------------------------------------------------------------------
        #Criando Pacotes
        #------------------------------------------------------------------

        pacotes = []

        while len(img_bytes) > 144: 
            print('entrou no cria pacotes')
            payload = img_bytes[:144]
            img_bytes = img_bytes[144:]
            
            eop = (1).to_bytes(4,byteorder='big')

            if len(pacotes) -1 == -1:
                head1 = b'\x03\x00\x00' + (n_pacotes).to_bytes(1, byteorder='big') + (len(pacotes)+1).to_bytes(1, byteorder='big') + (len(payload)).to_bytes(1, byteorder='big') + (0).to_bytes(1, byteorder='big') + b'\x00\x00\x00' 
                pacotes.append(head1 + payload + eop)
                
            else:
                head1 = b'\x03\x00\x00' + (n_pacotes).to_bytes(1, byteorder='big') + (len(pacotes)+1).to_bytes(1, byteorder='big') + (len(payload)).to_bytes(1, byteorder='big') + (len(pacotes)).to_bytes(1, byteorder='big') + b'\x00\x00\x00' 
                pacotes.append(head1 + payload + eop)


        '''guardando o resto da imagem na lista de pacoetes'''

        head2 = b'\x03\x00\x00' + (n_pacotes).to_bytes(1, byteorder='big') + (len(pacotes)+1).to_bytes(1, byteorder='big') + (len(img_bytes)).to_bytes(1, byteorder='big') + (len(pacotes)).to_bytes(1, byteorder='big') + b'\x00\x00\x00' 
        pacotes.append(head2 + img_bytes + (1).to_bytes(4,byteorder='big'))
        print('tamanho da lista de pacotes: {}'.format(pacotes))
        
        #-------------------------------------
        #processo de envio da mensagem/imagem
        #-------------------------------------
        n_envio = 0

        while n_envio < len(pacotes):
            print('enviando pacote tipo 3')

            t_envio = dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            com3.sendData(bytearray(pacotes[n_envio]))

            t1 = time.time() #set timer 1
            t2 = time.time() #set timer 2

            verifica_envio, nRx = com3.getData(10) #pegando o head
            verifica_envio = verifica_envio[0]

            if verifica_envio == 4:
                print(f'pacote {n_envio} foi recebido com sucesso')
                with open("registros\client1.txt", "a") as arquivo:
                    arquivo.write(t_envio + "/ENVIO/" + str(3) + "/" + str(n_envio) + "\n")
                with open("registros\client1.txt", "a") as arquivo:
                    arquivo.write(dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "/RECEBIDO/" + str(4) +  "\n")

                if com3.getData(-1) == 1: 
                    print('fudeuuuuu, envia dnv')
                    n_envio = n_envio

                n_envio += 1
            else:
                if t1 > 5:
                    com3.sendData(bytearray(pacotes[n_envio]))
                    t1 = time.time() #reset do timer 1
                    print(f'pacote {n_envio} não foi enviado, reenviando')
                    with open("registros\client4.txt", "a") as arquivo:
                        arquivo.write(t_envio + "/ENVIO/" + str(3) + "/" + str(n_envio) + "\n")
                    n_envio = n_envio
                if t2 > 20:
                    head5 = b'\x05\x00\x00' + (n_pacotes).to_bytes(1, byteorder='big') + (len(pacotes)+1).to_bytes(1, byteorder='big') + b'\x01' + (len(pacotes)-1).to_bytes(1, byteorder='big') + b'\x00\x00\x00' 
                    payload = b'\x01'
                    eop = (1).to_bytes(4, byteorder='big')
                    msg5 = (head5 + payload + eop)
                    print('enviando emnsagem tipo 5')
                    com3.sendData(bytearray(msg5))
                    print("encerrando comunicação")
                    with open("registros\client3.txt", "a") as arquivo:
                        arquivo.write(t_envio + "/ENVIO/" + str(3) + "/" + str(n_envio) + "\n")
                    with open("registros\client3.txt", "a") as arquivo:
                        arquivo.write(dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "/RECEBIDO/" + str(5) + "\n")
                    break
                else:
                    com3.rx.clearBuffer()
                    head6, nRx = com3.getData(10)
                    tipo = head6[0]
                    if tipo == 6:
                        print('msg tipo 6 recebida')
                        with open("registros\client2.txt", "a") as arquivo:
                            arquivo.write(t_envio + "/ENVIO/" + str(3) + "/" + str(n_envio) + "\n")
                        with open("registros\client2.txt", "a") as arquivo:
                            arquivo.write(dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "/RECEBIDO/" + str(6) + "/" + str(n_envio) + "\n")
                        n_envio = head6[6]
                        com3.sendData(bytearray(pacotes[n_envio]))
                        t1 = time.time() #set timer 1
                        t2 = time.time() #set timer 2





            com3.rx.clearBuffer()
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com3.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com3.disable()
            


if __name__ == "__main__":
    main()    