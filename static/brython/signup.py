from browser import document, ajax, html, bind, window, alert

jQuery = window.jQuery

# só aceita input numerico no input type text
@bind('#input-cep', 'input')
def cep(ev):
    try:
        int(document['input-cep'].value[-1:])
        if len(document['input-cep'].value) == 5:
            document['input-cep'].value += '-'
    except:
        document['input-cep'].value = document['input-cep'].value[:-1]

def changePerson(ev):
    documento = jQuery('#input-documento')
    person = jQuery('.radios[name="person"]:checked').val()
    jQuery('#label-documento').text(person.upper())
    documento.val('')
    documento.off('input')
    
    if person == 'cpf':
        documento.attr('maxlength', '14')
        jQuery('.empresa').hide()
        jQuery('.pessoa').show()
    elif person == 'cnpj':
        documento.attr('maxlength', '18')
        jQuery('.empresa').show()
        jQuery('.pessoa').hide()

def maskCPF(ev):
    jQuery('#input-cpf').mask('000.000.000-00')

def maskCNPJ(ev):
    jQuery('#input-cnpj').mask('00.000.000/0000-00')

        
def maskPhone(ev):
    jQuery('#input-telefone').mask('(00) 00000-0000')
        
def sendForm(ev):
    inputs = document.select('form > input')
    data = {}

    for item in inputs:
        key = item.attrs['id'][6:]
        data.update({key: item.value})

    def signupFeedback(req):
        data = req.text
        jQuery('#feedback').text(data)
        
    print(data)
    _ajax('/try_signup/', signupFeedback, method='POST', data=data)
    
def _ajax(url, onComplete, method='GET', data={}):
    req = ajax.Ajax()
    req.bind('complete', onComplete)
    req.open(method, url, True)
    req.set_header('content-type', 'application/x-www-form-urlencoded')
    req.send(data)

jQuery('document').ready(maskPhone)
jQuery('document').ready(maskCPF)
jQuery('document').ready(maskCNPJ)
jQuery('.radios').on('change', changePerson)
jQuery('#radio-cpf').prop("checked", True).change()
jQuery('form').on('submit', sendForm)