# Energysaver

## Sobre
Energysaver é uma plataforma IoT para monitoramento de sensores e dados implementada em Python com o micro-framework Flask. A plataforma possui uma página web de gerenciamento de usuarios e sensores, onde os dados de cada sensor podem ser visualizados ou baixados em um arquivo `.csv` para uma futura análise em softwares exeternos. Atualmente a plataforma está em desenvolvimento, mas já possui uma fase de teste que está em andamento nas dependências da Universidade Federal do Oeste do Pará.

A plataforma é conectada a um banco de dados (MongoDB) do tipo não-relacional orientado a documentos (No-SQL) para o armazenamento das informações dos usuários, sensores e dos dados em si. As leituras dos sensores são enviadas através do portocolo MQTT (Message Queuing Telemetry Transport) de um Raspberry Pi disposto geograficamente. A principal vantagem é a sua utilização para a alta transferêcia de dados em pequenos intervalos de tempo e com baixos sinais de rede.

## Descrição da Plataforma

### Servidor Flask
Possui algumas configurações e atua principalmente como ponte entre o Raspberry Pi e o banco de dados MongoDB.
### Página Web
 Atua como gerencidador de dispositivos (Raspberry Pi) e de sensores, além da vizualização em tempo real dos dados, bem como seu gerenciamento e disposição para download.
### MQTT
É o protocolo para o envio e recepção das leituras dos dados dos sensores.
### MongoDB
Banco de dados para o armazenamento das informações de usuários e dos dados.


