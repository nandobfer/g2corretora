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
        documento.on('input', formatCPF)
    elif person == 'cnpj':
        documento.attr('maxlength', '18')
        documento.on('input', formatCNPJ)

def formatCPF(ev):
    documento = jQuery('#input-documento')
    try:
        int(documento.val()[-1:])
        if len(documento.val()) == 3:
            documento.val(f'{documento.val()}.')
        if len(documento.val()) == 7:
            documento.val(f'{documento.val()}.')
        if len(documento.val()) == 11:
            documento.val(f'{documento.val()}-')
    except:
        documento.val(documento.val()[:-1])

def formatCNPJ(ev):
    documento = jQuery('#input-documento')
    try:
        int(documento.val()[-1:])
        if len(documento.val()) == 2:
            documento.val(f'{documento.val()}.')
        if len(documento.val()) == 6:
            documento.val(f'{documento.val()}.')
        if len(documento.val()) == 10:
            documento.val(f'{documento.val()}/')
        if len(documento.val()) == 15:
            documento.val(f'{documento.val()}-')
    except:
        documento.val(documento.val()[:-1])
        
def sendForm(ev):
    inputs = document.select('form > input')
    data = {}

    for item in inputs:
        key = item.attrs['id'][6:]
        data.update({key: item.value})

    def signupFeedback(req):
        data = eval(req.text)
        jQuery('#feedback').text(data)
        
    _ajax('/try_signup/', signupFeedback, method='POST', data=data)
    
def _ajax(url, onComplete, method='GET', data={}):
    req = ajax.Ajax()
    req.bind('complete', onComplete)
    req.open(method, url, True)
    req.set_header('content-type', 'application/x-www-form-urlencoded')
    req.send(data)

jQuery('.radios').on('change', changePerson)
jQuery('#radio-cpf').prop("checked", True).change()
jQuery('form').on('submit', sendForm)