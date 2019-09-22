from tkinter import * 
import socket
import pickle

class Interface:
  calcs = 0
  def __init__(self, master = None):
    # Criando o 1 container
    self.titleContainer = Frame(master)
    self.titleContainer["pady"] = 20
    self.titleContainer.pack()

    # Criando o 2 container
    self.pesoContainer = Frame(master)
    self.pesoContainer["padx"] = 20
    self.pesoContainer["pady"] = 5
    self.pesoContainer.pack()

    # Criando o 3 container 
    self.alturaContainer = Frame(master)
    self.alturaContainer["padx"] = 20
    self.alturaContainer["pady"] = 5
    self.alturaContainer.pack()

    # Criando o 4 container
    self.enviarContainer = Frame(master)
    self.enviarContainer["pady"] = 20
    self.enviarContainer.pack()

    # Criando o 5 container
    self.resultContainer = Frame(master)
    self.resultContainer.pack()

    self.titleContainer['bg'] = 'gray25'
    self.pesoContainer['bg'] = 'gray25'
    self.alturaContainer['bg'] = 'gray25'
    self.enviarContainer['bg'] = 'gray25'
    self.resultContainer['bg'] = 'gray25'

    
    
    # --------------------------------------------------------------

    # Mostrando o titulo da interface no container 1
    self.titleLabel = Label(self.titleContainer, text="Calcular IMC")
    self.titleLabel["font"] = ("Calibri", "25", "bold")
    self.titleLabel["fg"] = 'white'
    self.titleLabel.pack ()

    # Label para o input peso
    self.pesoLabel = Label(self.pesoContainer, text="Peso em kg")
    self.pesoLabel["font"] = ("Calibri", "15")
    self.pesoLabel["fg"] = 'white'
    self.pesoLabel.pack(side=TOP)

    # Input para o peso da pessoa
    self.peso = Entry(self.pesoContainer)
    self.peso["width"] = 30
    self.peso["font"] = ("Calibri", "13")
    self.peso.pack(side=BOTTOM)  

    # Label para o input altura
    self.alturaLabel = Label(self.alturaContainer, text="Altura em m")
    self.alturaLabel["font"] = ("Calibri", "15")
    self.alturaLabel["fg"] = 'white'
    self.alturaLabel.pack(side=TOP)

    # Input para o altura da pessoa
    self.altura = Entry(self.alturaContainer)
    self.altura["width"] = 30
    self.altura["font"] = ("Calibri", "13")
    self.altura.pack(side=BOTTOM) 

    # Botão para enviar os dados
    self.calcular = Button(self.enviarContainer)
    self.calcular["text"] = "Calcular"
    self.calcular["font"] = ("Calibri", "13")
    self.calcular["width"] = 10
    self.calcular["command"] = self.enviar
    self.calcular.pack ()

    # Msg de feedback
    self.feedback = Label(self.enviarContainer, text="")
    self.feedback["font"] = ("Calibri", "13", "bold")
    self.feedback["fg"] = 'white'
    self.feedback["pady"] = 15
    self.feedback["padx"] = 20
    self.feedback.pack()

    self.titleLabel['bg'] = 'gray25'
    self.pesoLabel['bg'] = 'gray25'
    self.alturaLabel['bg'] = 'gray25'
    self.feedback['bg'] = 'gray25'


  def enviar(self):
    if self.peso.get() and self.altura.get():
      self.feedback["fg"] = "green" 
      self.pesoLabel["fg"] = "black"
      self.alturaLabel["fg"] = "black"
      self.feedback["text"] = "Calculando..."
      dadosCalc = {}
      dadosCalc['massa'] = self.peso.get()
      dadosCalc['altura'] = self.altura.get() 

      clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

      host = socket.gethostname()
      port = 3333

      clientSocket.connect((host, port))

      clientSocket.send(pickle.dumps(dadosCalc))
      result = pickle.loads(clientSocket.recv(1024))

      if result:
        self.showResult()
        if self.calcs > 0:
          # print('clear')
          self.imcLabel.destroy()
          self.resultLabel.destroy()
          self.imageC.destroy()
          self.space.destroy()
          self.calcular.destroy()

        imc = "IMC = " + str(result['imc'])
        self.imcLabel = Label(self.resultContainer, text=imc)
        self.imcLabel["font"] = ("Calibri", "25", "bold")
        self.imcLabel['pady'] = 10
        self.imcLabel["fg"] = 'white'
        self.imcLabel.pack ()

        resultado = "Você está " + result['text']
        self.resultLabel = Label(self.resultContainer, text=resultado)
        self.resultLabel["font"] = ("Calibri", "18",)
        self.resultLabel['pady'] = 15 
        self.resultLabel["fg"] = 'white'
        self.resultLabel.pack ()

        imagem = PhotoImage(file=result['img'])

        self.imageC = Label(self.resultContainer, image=imagem)
        self.imageC.imagem = imagem
        self.imageC.pack()

        self.space = Label(self.resultContainer, text="")
        self.space['pady'] = 5
        self.space.pack ()
        
        self.calcular = Button(self.resultContainer)
        self.calcular["text"] = "Voltar ao inicio"
        self.calcular["font"] = ("Calibri", "13")
        self.calcular['padx'] = 5
        self.calcular["command"] = self.showStart
        self.calcular.pack ()

        self.calcs += 1

        self.imcLabel['bg'] = 'gray25'
        self.resultLabel['bg'] = 'gray25'
        self.imageC['bg'] = 'gray25'
        self.space['bg'] = 'gray25'

      else :
        return;  
      
      clientSocket.close()
    else:
      self.feedback["text"] = "Informe os dados acima antes de continuar!" 
      self.pesoLabel["fg"] = "red"
      self.alturaLabel["fg"] = "red"
      self.feedback["fg"] = "red" 
      return; 

  def showResult(self):
    self.resultContainer.pack()
    self.titleContainer.pack_forget()
    self.pesoContainer.pack_forget()
    self.alturaContainer.pack_forget()
    self.enviarContainer.pack_forget()

  def showStart(self):
    self.feedback["text"] = "" 
    self.resultContainer.pack_forget()
    self.titleContainer.pack()
    self.pesoContainer.pack()
    self.alturaContainer.pack()
    self.enviarContainer.pack()
    self.pesoLabel["fg"] = 'white'
    self.alturaLabel["fg"] = 'white'

  def start ():
    root = Tk()
    root.geometry("600x350")
    root.configure(bg='gray25')
    Interface(root) 
    root.mainloop() 
