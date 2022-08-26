from browser import document, alert, bind

plusbutton = document["plusbutton"]
numero = 0

def funcao(ev):
    global numero
    numero += 1
    alert(numero)

plusbutton.bind("click", funcao)