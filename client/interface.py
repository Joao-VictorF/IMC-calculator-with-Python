from tkinter import * 
import socket
import pickle

class Interface:
  calcs = 0
  mI = 0
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

    # Mudando cor de background dos containers
    self.titleContainer['bg'] = 'SlateGray4'
    self.pesoContainer['bg'] = 'SlateGray4'
    self.alturaContainer['bg'] = 'SlateGray4'
    self.enviarContainer['bg'] = 'SlateGray4'
    self.resultContainer['bg'] = 'SlateGray4'

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

    self.peso = Entry(self.pesoContainer)
    self.peso["width"] = 30
    self.peso["font"] = ("Calibri", "13")
    self.peso.pack(side=BOTTOM)  

    # Label para o input altura
    self.alturaLabel = Label(self.alturaContainer, text="Altura em m")
    self.alturaLabel["font"] = ("Calibri", "15")
    self.alturaLabel["fg"] = 'white'
    self.alturaLabel.pack(side=TOP)

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

    # Mudando cor de background dos Labels
    self.titleLabel['bg'] = 'SlateGray4'
    self.pesoLabel['bg'] = 'SlateGray4'
    self.alturaLabel['bg'] = 'SlateGray4'
    self.feedback['bg'] = 'SlateGray4'


  def enviar(self):
    #Verificando se os dados foram informados antes de enviar ao servidor
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

      #Mostrando resultado assim que receber do servidor
      if result:
        self.showResult()
        if self.calcs > 0:
          self.imcLabel.destroy()
          self.resultLabel.destroy()
          self.imageC.destroy()
          self.space.destroy()
          self.calcular.destroy()        
          if self.mI > 0:
            self.massaIdeal.destroy()
            self.mI = 0

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

        imgUrl = PhotoImage(file=result['img'])

        self.imageC = Label(self.resultContainer, image=imgUrl)
        self.imageC.imagem = imgUrl
        self.imageC.pack()

        self.space = Label(self.resultContainer, text="")
        self.space['pady'] = 5
        self.space.pack ()

        if result['mI'] > 0:
          diferenca = round(result['mI']-float(self.peso.get()), 1)
          if result['mI'] > float(self.peso.get()):
            massaIdeal = "Você deveria pesar " + str(result['mI']) + ' Kg para estar com o peso normal. Ganhe ' + str(diferenca) + ' Kg'
          else:
            massaIdeal = "Você deveria pesar " + str(result['mI']) + ' Kg para estar com o peso normal. Perca ' + str(diferenca*-1) + ' Kg'
          self.massaIdeal = Label(self.resultContainer, text=massaIdeal)
          self.massaIdeal["font"] = ("Calibri", "18",)
          self.massaIdeal['pady'] = 5 
          self.massaIdeal["fg"] = 'white'
          self.massaIdeal.pack ()
          self.mI = 1

        self.calcular = Button(self.resultContainer)
        self.calcular["text"] = "Voltar ao inicio"
        self.calcular["font"] = ("Calibri", "13")
        self.calcular['padx'] = 5
        self.calcular["command"] = self.showStart
        self.calcular.pack ()

        self.calcs += 1

        self.imcLabel['bg'] = 'SlateGray4'
        self.resultLabel['bg'] = 'SlateGray4'
        self.imageC['bg'] = 'SlateGray4'
        self.space['bg'] = 'SlateGray4'
        if self.mI > 0:
          self.massaIdeal['bg'] = 'SlateGray4'

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
    root.geometry("800x350")
    root.configure(bg='SlateGray4')
    Interface(root) 
    root.mainloop() 
