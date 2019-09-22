import socket
import pickle 

print("\nServer socket started!")

# create server socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()
port = 3333
# bind to port
serversocket.bind((host, port))

serversocket.listen(10)
while True:
  # estabilish a connection
  clientsocket, addr = serversocket.accept()

  dados = pickle.loads(clientsocket.recv(1024))
  massa = float(dados["massa"])
  altura = float(dados["altura"])
  imc = round(massa/(altura*altura), 1)
  resultado= {}
  if imc < 18.5 :
    resultado['text'] = "abaixo do peso!"
    resultado['imc'] = imc
    resultado['img'] = 'images/1.png'

  elif imc >= 18.5 and imc <= 24.9:
    resultado['text'] = "com o peso normal!" 
    resultado['imc'] = imc
    resultado['img'] = 'images/2.png'

  elif imc >= 25 and imc <= 29.9:
    resultado['text'] = "com sobrepeso!" 
    resultado['imc'] = imc
    resultado['img'] = 'images/3.png'

  elif imc >= 30 and imc <= 34.9:
    resultado['text'] = "com obesidade grau 1!" 
    resultado['imc'] = imc
    resultado['img'] = 'images/4.png'

  elif imc >= 35 and imc <= 39.9:
    resultado['text'] = "com obesidade grau 2!" 
    resultado['imc'] = imc
    resultado['img'] = 'images/5.png'

  elif imc >= 40:
    resultado['text'] = "com obesidade grau 3!" 
    resultado['imc'] = imc
    resultado['img'] = 'images/6.png'

  clientsocket.send(pickle.dumps(resultado))

  clientsocket.close()