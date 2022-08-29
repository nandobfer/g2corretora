from browser import document, alert, bind, ajax, window, html

numero = 0
jquery = window.jQuery
plusbutton = jquery('.plusbutton')
added_buttons = None


def _ajax(url, onComplete, method='GET', data={}):
    req = ajax.Ajax()
    req.bind('complete', onComplete)
    req.open(method, url, True)
    req.set_header('content-type', 'application/x-www-form-urlencoded')
    req.send(data)


def check_column():
    coluna = document.select('.current-column > button')
    qtd = len(coluna)

    if qtd == 3:
        jquery('.current-column').removeClass('current-column')
        nova_coluna = '<div class="buttons-column current-column"></div>'
        jquery('.buttons-area').append(nova_coluna)


def change_plusbutton():
    global plusbutton
    button = jquery('.current-column > button')
    plusbutton.text(button.text())
    button.text('+')

    button.addClass('plusbutton')
    plusbutton.removeClass('plusbutton')

    button.on('click', new_status)
    plusbutton.off('click')

    plusbutton = button


def add_button(req):
    global added_buttons
    global plusbutton
    data = eval(req.text)
    added_buttons = data
    print(data)
    for item in data:
        check_column()
        coluna = jquery('.current-column')

        button = f'<button class="added-button">{item[1]}</button>'
        coluna.prepend(button)

        if jquery('.current-column > button').length == 1:
            change_plusbutton()


def get_added_buttons():
    _ajax('/get_added_buttons/', add_button)


def submit(ev):
    input = jquery('.current-column > form > input')
    form = jquery('.current-column > form')
    texto = input.val()
    id = len(added_buttons)
    data = {
        'button_name': texto,
        'id': id
    }

    # enviar pro servidor

    _ajax(url='/new_button/', onComplete=create_button, method='POST', data=data)


def create_button(req):
    form = jquery('.current-column > form')
    form.remove()
    jquery('.current-column').append(plusbutton)
    plusbutton.on('click', new_status)


def new_status(ev):
    global plusbutton
    plusbutton.remove()
    coluna = jquery('.current-column')
    form = '<form action="javascript:void(0)"></form>'
    input = '<input type="text">'
    coluna.append(form)
    form = jquery('.current-column > form')
    form.append(input)
    input = jquery('.current-column > form > input')
    form.on('submit', submit)
    input.focus()


def pre_render():
    get_added_buttons()
    plusbutton.on('click', new_status)


pre_render()
