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
import enlaceRx as rx
import datetime 
# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)

#projeto 1

# def main():
#     try:
#         print("Iniciou o main")
#         #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
#         #para declarar esse objeto é o nome da porta.
#         com3 = enlace(serialName)
        
    
#         # Ativa comunicacao. Inicia os threads e a comunicação seiral 
#         com3.enable()
#         #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
#         print("Abriu a comunicação")
        
           
                  
#         #aqui você deverá gerar os dados a serem transmitidos. 
#         imageR = "img/ponto.png"
#         imageW = "img/Recebidacopia.png"
#         #seus dados a serem transmitidos são um array bytes a serem transmitidos. Gere esta lista com o 
#         #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        
#         print("Carregando imagem para transmissão:")
#         print(" - {}".format(imageR))
#         print("-----------------")
#         txBuffer = open(imageR,'rb').read()

#         #txBuffer = imagem em bytes!
#         #txBuffer = b'\x12\x13\xAA'  #isso é um array de bytes
       
#         #print("meu array de bytes tem tamanho {}" .format(len(txBuffer)))
#         #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
       
            
#         #finalmente vamos transmitir os todos. Para isso usamos a funçao sendData que é um método da camada enlace.
#         #faça um print para avisar que a transmissão vai começar.
#         #tente entender como o método send funciona!
#         #Cuidado! Apenas trasmita arrays de bytes!
               
        
#         com3.sendData(np.asarray(txBuffer))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
          
#         # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
#         # O método não deve estar fincionando quando usado como abaixo. deve estar retornando zero. Tente entender como esse método funciona e faça-o funcionar.
#         txSize = com3.tx.getStatus()
#         print('enviou = {}' .format(txSize))
        
#         #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
#         #Observe o que faz a rotina dentro do thread RX
#         #print um aviso de que a recepção vai começar.
        
#         #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
#         #Veja o que faz a funcao do enlaceRX  getBufferLen
      
#         #acesso aos bytes recebidos
#         txLen = len(txBuffer)
#         rxBuffer, nRx = com3.getData(txLen)
#         print("recebeu {} bytes" .format(len(rxBuffer)))
        
#         for i in range(len(rxBuffer)):
#             print("recebeu {}" .format(rxBuffer[i]))
        

            
    
#         # Encerra comunicação
#         print("-------------------------")
#         print("Comunicação encerrada")
#         print("-------------------------")
#         com3.disable()

#         print("Salvando dados no arquivo:")
#         print(" - {}".format(imageW))
#         f = open(imageW,'wb')
#         f.write(rxBuffer)

#         f.close()
        
#     except Exception as erro:
#         print("ops! :-\\")
#         print(erro)
#         com3.disable()
        
def main():
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com3 = enlace(serialName)
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com3.enable()
        time.sleep(.2)
        com3.sendData(b'00')
        time.sleep(1)
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")
        
        lista_comandos = [b'\x00\x00\x00\x00',b'\x00\x00\xAA\x00',b'\xAA\x00\x00',b'\x00\xAA\x00',b'\x00\x00\xAA',b'\x00\xAA',b'\xAA\x00',b'\x00',b'\xFF']
        sortear_qtd_comandos = np.random.randint(10,30)
        print('A quantidade de comandos sorteados foram: {}' .format(sortear_qtd_comandos))


        #envia os dados
        envia_comandos = []
        for i in range(sortear_qtd_comandos):
            sortear_comandos = np.random.randint(0,8)
            comando = lista_comandos[sortear_comandos]
            comando_final = b'\xCC' + comando  
            envia_comandos.append(comando_final)
        
        envia_comandos= b''.join(envia_comandos)
        tamanho = len(envia_comandos).to_bytes(1, byteorder='big')
        envia_comandos = tamanho + envia_comandos
        com3.sendData(bytearray(envia_comandos))
        print(type(envia_comandos))

        print('A lista de comandos sorteados foram: {}' .format(bytearray(envia_comandos)))

        #calculo do tempo de resposta
        t0 = time.time()
        while com3.rx.getIsEmpty() is True: 
            ti = time.time()
            if ti - t0 > 5:
                print('Time Out')
                break
        # receber envio do servidor
        else:
            rxBuffer = com3.getData(1)[0]
            for i in range(len(rxBuffer)):
                print("recebeu {}" .format(rxBuffer[i]))





            

        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com3.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()


# imagina que tem um caracter 