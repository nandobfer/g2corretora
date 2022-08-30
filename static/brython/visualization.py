from browser import document, ajax, html, bind, window, alert

jQuery = window.jQuery
pages = []
current_page = 1
status = []
class Page():
    def __init__(self, number, button, table):
        self.number = number
        self.button = button
        self.table = table
        
        jQuery(self.button).on('click', self.renderPage)
        
    def renderPage(self, ev):
        cleanTable()
        buildTable(self)
        

def _ajax(url, onComplete, method='GET', data={}):
    req = ajax.Ajax()
    req.bind('complete', onComplete)
    req.open(method, url, True)
    req.set_header('content-type', 'application/x-www-form-urlencoded')
    req.send(data)
    
def buildPages(data):
    pages_number = (len(data) // 7) + 1
    for count in range(1, pages_number+1):
        table = []
        for i in range(7):
            try:
                table.append(data.pop(0))
            except:
                pass
            
        button = html.P(count, Class='pages-buttons')
        page = Page(count, button, table)
        pages.append(page)
        jQuery('.pages').append(page.button)

def cleanTable():
    jQuery('.active-page-button').removeClass('active-page-button')
    jQuery('tbody > *').remove()
    
def removeTooltips(ev):
    jQuery('.action-tooltip').remove()
    jQuery('.status-tooltip').remove()
    
def showStatusTooltip(ev):
    global status
    removeTooltips(True)
    id = ev.target.attrs['id'].split('-')[1]
    parent = jQuery(f'#status-{id}')
    container = f'<div id="status-tooltip-{id}" class="status-tooltip">\
                    <div><p>Aviso de 60 dias</p></div>\
                    <div><p>Aviso de 30 dias</p></div>\
                    <div><p>Aviso de 15 dias</p></div>\
                </div>'
    parent.append(container)
    container = jQuery(f'#status-tooltip-{id}')
    for item in status:
        row = f'<div><p>{item[1]}</p></div>'
        container.append(row)
        
    print(container.position().left, container.position().top)
    position_left = -container.width()/3 + parent.width()/3
    container.css('left', position_left)
    
    
def showActionTooltip(ev):
    removeTooltips(True)
    id = ev.target.attrs['id'].split('-')[1]
    parent = jQuery(f'#action-container-{id}')
    container = f'<div id="action-tooltip-{id}" class="action-tooltip">\
        <div class="arrow-up"></div>\
        <div>\
            <p>Ligar</p>\
        </div>\
        <hr>\
        <div>\
            <p>Mandar e-mail</p>\
        </div>\
        <hr>\
        <div>\
            <p>Ver cadastro</p>\
        </div>\
        <hr>\
        <div>\
            <p>Editar</p>\
        </div>\
        <hr>\
        <div>\
            <p>Deletar</p>\
        </div>\
    </div>'
    parent.append(container)
    jQuery(f'#action-tooltip-{id}').on('click', removeTooltips)
    
def buildTable(page):
    global current_page
    jQuery(page.button).addClass('active-page-button')
    current_page = page.number
    for item in page.table:
        row = f'<tr id="row-{item[0]}"><td><input type="checkbox" name="checkbox" id="checkbox-{item[0]}">'
        for info in item:
            if item.index(info) == 0:
                continue

            if item.index(info) == 3:
                row += f'<td><div id="status-{item[0]}" class="status"><p id="statustext-{item[0]}">{info}</p><div class="arrow-down"></div><div class="arrow-up"></div></div></td>'
                continue
                
            row += f'<td>{info}</td>'
            if item.index(info) == 6:
                break
        row += f'<td><div id="action-container-{item[0]}" class="action-container"><img id="action-{item[0]}" src="/static/images/seta-roxa.svg" alt="seta-roxa"></img></div></td></tr>'
        jQuery('tbody').append(row)
        jQuery(f'#status-{item[0]}').on('click', showStatusTooltip)
        jQuery(f'#action-{item[0]}').on('click', showActionTooltip)
        
    bindCheckboxes()
    if current_page == pages[0].number:
        jQuery('#previous-page').addClass('deactivated-button')
    else:
        jQuery('#previous-page').removeClass('deactivated-button')

    if current_page == pages[-1].number:
        jQuery('#next-page').addClass('deactivated-button')
    else:
        jQuery('#next-page').removeClass('deactivated-button')
        
    
def checkAllBoxes(ev):
    if ev.target.checked:
        jQuery('input[type="checkbox"]:not("#header-checkbox")').prop('checked', True)
    else:
        jQuery('input[type="checkbox"]:not("#header-checkbox")').prop('checked', False)
    jQuery('input[type="checkbox"]:not("#header-checkbox")').change() 
        
def hoverRow(ev):
    id = ev.target.attrs['id'].split('-')[1]
    row = jQuery(f'#row-{id}')
    if ev.target.checked:
        row.addClass('selected-row')
    else:
        row.removeClass('selected-row')
        
def toggleNotifications(ev):
    jQuery('.notifications-tooltip').toggle()
    
def bindCheckboxes():
    jQuery('input[type="checkbox"]:not("#header-checkbox")').on('change', hoverRow)
    jQuery('#header-checkbox').on('change', checkAllBoxes)
        
def bindElements():
    jQuery('#next-page').on('click', buildNextPage)
    jQuery('#previous-page').on('click', buildPreviousPage)
    jQuery('.notifications-container').on('click', toggleNotifications)
        
def buildNextPage(ev):
    cleanTable()
    buildTable(pages[current_page])
        
def buildPreviousPage(ev):
    cleanTable()
    buildTable(pages[current_page-2])
    print(current_page)
    
def getStatus(req):
    global status
    data = eval(req.text)
    status = data
    
def initialRender(req):
    data = eval(req.text)
    buildPages(data)
    buildTable(pages[0])
    bindElements()
    _ajax('/get_added_buttons/', getStatus)
    # jQuery('.notifications-tooltip').hide()
        
    
_ajax('/get_table_data/', initialRender, method='GET')