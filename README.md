# Energysaver

## Sobre
Energysaver é uma plataforma IoT para monitoramento de sensores e dados implementada em Python com o micro-framework Flask. A plataforma possui uma página web de gerenciamento de usuarios e sensores, onde os dados de cada sensor podem ser visualizados ou baixados em um arquivo `.csv` para uma futura análise em softwares exeternos. Atualmente a plataforma está em desenvolvimento, mas já possui uma fase de teste que está em andamento nas dependências da Universidade Federal do Oeste do Pará.

A plataforma é conectada a um banco de dados (MongoDB) do tipo não-relacional orientado a documentos (No-SQL) para o armazenamento das informações dos usuários, sensores e dos dados em si. As leituras dos sensores são enviadas através do portocolo MQTT (Message Queuing Telemetry Transport) de um Raspberry Pi disposto geograficamente. A principal vantagem é a sua utilização para a alta transferêcia de dados em pequenos intervalos de tempo e com baixos sinais de rede.

## Script do Client
O script funciona em forma de loop onde o dado é coletado e enviado para o Broker MQTT. O requisito obrigatório é, como mencionado acima, a biblioteca “paho-mqtt” que oferece suporte para o uso do protocolo MQTT integrado ao Python.

## Entendendo o sistema
Após criar o programa que será usado para enviar os dados para o sistema algumas observações devem ser cumpridas. A primeira delas é o modelo de envio de dados, este é utilizado para organizar o envio corretamente para que o servidor identifique e armazene cada dado. O modelo é definido por um objeto que contém as informações do sistema que está enviando os dados, bem como usuário, local, dispositivo que está enviando, dia, hora, tipo do sensor, modelo, e o valor da leitura. A segunda, deve-se indicar o tópico de envio do dado para o servidor. O tópico é uma string que redireciona o dado para um determinado canal que somente o cliente que possui acesso a ele pode receber as mensagens. E por último, deve ser indicado o endereço de chegada do dado, que é o IP do servidor de armazenamento de dados.
```
{
   “user”: “Dalton”,
   “local”: “laboratório”,
   ”device”: “raspberry pi”,
   “hour”: ”15:31:22”,
   “day”: “10-07-2017”,
   "name_sensor": "corrente01",
   “type_sensor”: “corrente”,
   “model_sensor”: “ACS712”,
   “value”: “0.45”
 }
 ```
## Cliente simulado
Um cliente simulado foi criado para testar se o sistema está funcionando. Um cliente simulado é um programa genérico que simula os dados e suas informações de acordo com o que o usuário define, por exemplo, ao iniciar a simulação, configurações como número de leituras, intervalo entre elas, em segundos, e o valor de cada leitura pode ser determinado por um número aleatório definido por um intervalo numérico como um número entre 0.40 e 0.60. O cliente simulado ajuda nos testes e não depende de sensores, o que facilita bastante para definir se o sistema funciona corretamente. Após preencher as configurações básicas do modelo do banco de dados devemos preencher os campos do envio dos dados, como o tópico em formato de string que deve ser definido tanto no servidor quanto cliente e por último o local onde está instalado o servidor, se os dois, cliente e servidor, estão no mesmo dispositivo pode-se usar “localhost” para defini-lo, no entanto, o IP da máquina/servidor deverá ser o endereço.

## Descrição da Plataforma

### Servidor Flask
Possui algumas configurações e atua principalmente como ponte entre o Raspberry Pi e o banco de dados MongoDB.
### Página Web
 Atua como gerencidador de dispositivos (Raspberry Pi) e de sensores, além da vizualização em tempo real dos dados, bem como seu gerenciamento e disposição para download.
### MQTT
É o protocolo para o envio e recepção das leituras dos dados dos sensores.
### MongoDB
Banco de dados para o armazenamento das informações de usuários e dos dados.

## Dependências
Vide [requirements.txt](https://github.com/daltonvarao/energysaver-flask/blob/master/requirements.txt)

## Instalação e dependências
 - Fazer o clone do repositório
 - Instalar e ativar um [ambiente virtual](https://pythonacademy.com.br/blog/python-e-virtualenv-como-programar-em-ambientes-virtuais)
 - Instalar as dependências `$ pip install -r requirements.txt`
 - Ter uma versão do [MongoDB](https://docs.mongodb.com/manual/installation/) rodando em sua máquina
 - Ter um broker [MQTT](https://mosquitto.org/) rodando em sua máquina

## Rodar a aplicação
Após o processo de instalação, rode o comando `$ python run.py`
