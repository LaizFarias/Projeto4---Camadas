#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import numpy as np
import random

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)


def main():
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com3 = enlace(serialName)
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação serial 
        com3.enable()
        print("esperando 1 byte de sacrifício") 
        rxBuffer, nRx = com3.getData(1)
        com3.rx.clearBuffer()
        time.sleep(.1)
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")
        
           
                  
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são um array bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Essa sempre irá armazenar os dados a serem enviados.
#################################################################################




        #txBuffer = imagem em bytes!
        #txBuffer = b'\x12\x13\xAA'  #isso é um array de bytes

        #endereço da imagem a ser transmitida
        #imageR = "img\linha.png"

        #endereço da imagem a ser salva
        #imageW = "img\linhaCopia.png"

        #carregando imagem
        print("carregando imagem para transmissão")
        #print("- {}".format(imageR))
        print("----------------")
        #txBuffer = open(imageR, "rb").read()
        #print("meu array de bytes tem tamanho {}" .format(len(txBuffer)))
        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
        #print(f'Esse é o tamanho do txBuffer = {len(txBuffer)}')
#################################################################################3

#PROJETO 2 ------- CLIENTE
     

        dic_comandos = {'comando 1': b'\x00\x00\x00\x00', 'comando 2':b'\x00\x00\xAA\x00' , 'comando 3': b'\xAA\x00\x00', 'comando 4': b'\x00\xAA\x00', 'comando 5':b'\x00\x00\xAA' , 'comando 6': b'\x00\xAA' , 'comando 7': b'\xAA\x00', 'comando 8':b'\x00' ,'comando 9': b'\xFF'}
        list_comandos = ['comando 1', 'comando 2', 'comando 3', 'comando 4', 'comando 5', 'comando 6', 'comando 7','comando 8','comando 9']
    
        contagem = b'\xcc'
        qtd_comandos = random.randint(10,30)
        i = 0

        print(f'comandos{qtd_comandos}')
        mensagem = b''
        while i < qtd_comandos-1:
            a = random.randint(0,8)
            txBuffer = dic_comandos[list_comandos[a]]
            contagem = (len(txBuffer)).to_bytes(1, byteorder='big') #transofrmando para 1 byte 
            mensagem = mensagem + contagem + txBuffer
            i+=1
        tamanho = (len(mensagem)).to_bytes(1,byteorder='big' )    
        mensagem = tamanho + mensagem
        com3.sendData(mensagem)
        
        #recebendo o envio do servidor
        rxBuffer = com3.getData(1)
        for i in range(len(rxBuffer)):
            print("recebeu {}" .format(rxBuffer[i]))

       
        
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com3.disable()

        
        
        #finalmente vamos transmitir os dados. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmita arrays de bytes!
               
        print('trasmissão de dados irá começar')

          #as array apenas como boa pratica para casos de ter uma outra forma de dados
          
        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # O método não deve estar funcionando quando usado como abaixo. deve estar retornando zero. Tente entender como esse método funciona e faça-o funcionar.
        txSize = com3.tx.getStatus()
        print('enviou = {}' .format(txSize))
        
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.
        print("recepção dos dados começou")

        


#PROJETO 2 ------- SERVIDOR
        
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen
      
        #acesso aos bytes recebidos
        #txLen = len(txBuffer)
        #rxBuffer, nRx = com3.getData(txLen)
        #print("recebeu {} bytes" .format(len(rxBuffer)))

        #primeiro get
        
        
        p_by = com3.getData(1)
        tam_p_by = p_by[0]
        
        rxBuffer = com3.getData(tam_p_by) #agroa ele tem o tamanho do comando completo
        lista_comandos = rxBuffer.split(b'\xcc')
        qtd_c = len(lista_comandos)
        envio = (qtd_c).to_bytes(1, byteorder='big')
        com3.sendData(envio)
        

       


    
        for i in range(len(rxBuffer)):
            print("recebeu {}" .format(rxBuffer[i]))

       
        
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com3.disable()

         #print(f'- {imageW}')
        #f = open(imageW, 'wb')
        #f.write(rxBuffer)
        #f.close()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com3.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
