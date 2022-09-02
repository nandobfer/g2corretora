from browser import document, ajax, html, bind, window, alert
from datetime import datetime

jQuery = window.jQuery
pages = []
current_page = 1
status = []
cadastros = None
filtered = []
vencimentos_proximos = {
    "60": [],
    "30": [],
    "15": []
}
vencidos = []
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
    
def cleanPages():
    jQuery('.pages-buttons').remove()
    cleanTable()

def buildPages(data):
    global pages
    pages = []
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
        jQuery('#next-page').on('click', buildNextPage)
        jQuery('#previous-page').on('click', buildPreviousPage)
        
        

def cleanTable():
    jQuery('.active-page-button').removeClass('active-page-button')
    jQuery('tbody > *').remove()
    
def removeTooltips(ev):
    jQuery('.action-tooltip').remove()
    jQuery('.status-tooltip').remove()
    jQuery('.status').on('click', showStatusTooltip)
    jQuery('.action-container').on('click', showActionTooltip)

    
def changeStatus(ev, id = None):
    def onChangeStatus(req):
        global current_page
        global pages
        pages[current_page-1].table[int(cadastro_id)][3] = status[id][1]

    if not id:
        id = ev.target.attrs['id'].split('-')
        cadastro_id = id[3]
        id = int(id[2])
        _ajax('/change_status/', onChangeStatus, method = 'POST', data = {'mass': False, 'id': cadastro_id, 'status': status[id][1]})
    else:
        cadastro_id = int(id.pop(0))
        id = int(id.pop(0))
    jQuery(f'#statustext-{cadastro_id}').text(status[id][1])


    
def showStatusTooltip(ev):
    global status
    removeTooltips(True)
    id = ev.target.attrs['id'].split('-')[1]
    parent = jQuery(f'#status-{id}')
    container = f'<div id="status-tooltip-{id}" class="status-tooltip">\
                </div>'
    parent.append(container)
    container = jQuery(f'#status-tooltip-{id}')
    for item in status:
        row = f'<div id="status-row-{item[0]}-{id}"><p id="status-text-{item[0]}-{id}">{item[1]}</p></div>'
        container.append(row)
        row = jQuery(f'#status-row-{item[0]}-{id}')
        row.on('click', changeStatus)
        
    position_left = -container.width()/3 + parent.width()/3
    container.css('left', position_left)
    
    jQuery(f'.status-{id}').off('click')
    jQuery(f'.status-{id}').on('click', removeTooltips)
    
def buildMassTooltip():
    global status
    parent = jQuery('.mass-status-tooltip')

    def changeMassStatus(ev):
        def onStatusChange(req):
            global current_page
            global pages
            pages[current_page-1].table[int(cadastro_id)][3] = status[int(status_id)][1]
        
        ids = []
        status_id = ev.target.attrs['id'].split('-')[3]
        for item in document.select('input[type="checkbox"]:checked'):
            cadastro_id = item.attrs['id'].split('-')[1]
            ids.append(cadastro_id)
            id = [cadastro_id, status_id]
            changeStatus(True, id)
            
        _ajax('/change_status/', onStatusChange, method='POST', data={'mass': True, 'ids': str(ids), 'status': status[int(status_id)][1]})

    for item in status:
        row = f'<div id="mass-status-row-{item[0]}"><p id="mass-status-text-{item[0]}">{item[1]}</p></div>'
        parent.append(row)
        row = jQuery(f'#mass-status-row-{item[0]}')
        row.on('click', changeMassStatus)
        
    parent.toggle()
    jQuery('.mass-action-container').toggle()
    
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
    # jQuery(f'#action-tooltip-{id}').on('click', removeTooltips)
    jQuery(ev.target).off('click')
    jQuery(ev.target).on('click', removeTooltips)
    
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
                row += f'<td><div id="status-{item[0]}" class="status status-{item[0]}"><p id="statustext-{item[0]}">{info}</p><div id="arrowdown-{item[0]}" class="arrow-down"></div><div id="arrowup-{item[0]}" class="arrow-up"></div></div></td>'
                continue
                
            if item.index(info) == 6:
                date = item[6].split('-')
                row += f'<td><p>{date[2]}/{date[1]}/{date[0]}</p></td>'
                break

            row += f'<td><p>{info}</p></td>'
            
            
        vencimento = item[6].split('-')
        vencimento = datetime(int(vencimento[0]), int(vencimento[1]), int(vencimento[2]))
        agora = datetime.now()
        prazo = (vencimento-agora).days + 1
        prazo_texto = str(prazo)
        color = None
        if prazo > 60:
            prazo_texto = '-'
        else:
            if prazo <= 30:
                color = 'var(--yellow)'
            if prazo <= 15:
                color = 'var(--red)'
            if prazo == 1:
                prazo_texto += ' dia'
            else:
                prazo_texto += ' dias'
                
            if prazo < 0:
                prazo_texto = 'Vencido'

        row += f'<td id="prazo-{item[0]}">{prazo_texto}</td>'
        row += f'<td><div id="action-container-{item[0]}" class="action-container"><img id="action-{item[0]}" src="/static/images/seta-roxa.svg" alt="seta-roxa"></img></div></td></tr>'
        jQuery('tbody').append(row)
        if color:
            jQuery(f'#prazo-{item[0]}').css('color', color)
    jQuery(f'.status').on('click', showStatusTooltip)
    jQuery(f'.action-container').on('click', showActionTooltip)
        
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
        jQuery('.mass-action-container').fadeIn()
    else:
        jQuery('input[type="checkbox"]:not("#header-checkbox")').prop('checked', False)
        jQuery('.mass-action-container').fadeOut()
    jQuery('input[type="checkbox"]:not("#header-checkbox")').change()
        
def hoverRow(ev):
    id = ev.target.attrs['id'].split('-')[1]
    row = jQuery(f'#row-{id}')
    if ev.target.checked:
        row.addClass('selected-row')
        jQuery('.mass-action-container').fadeIn()
    else:
        row.removeClass('selected-row')
        if not jQuery('input[type="checkbox"]:checked').length:
            jQuery('.mass-action-container').fadeOut()
            
        
def toggleNotifications(ev):
    jQuery('.notifications-tooltip').toggle()
    
def bindCheckboxes():
    jQuery('input[type="checkbox"]:not("#header-checkbox")').on('change', hoverRow)
    jQuery('#header-checkbox').on('change', checkAllBoxes)
        
def bindElements():
    jQuery('.notifications-container').on('click', toggleNotifications)
    jQuery('.mass-status').on('click', jQuery('.mass-status-tooltip').toggle)
        
def buildNextPage(ev):
    cleanTable()
    buildTable(pages[current_page])
        
def buildPreviousPage(ev):
    cleanTable()
    buildTable(pages[current_page-2])
    
def getStatus(req):
    global status
    data = eval(req.text)
    status = data
    buildMassTooltip()  
    buildFilterTooltip()
    jQuery('.loading-container').fadeToggle()
    
def buildNotifications():
    global vencidos
    dias_60 = len(vencimentos_proximos['60'])
    dias_30 = len(vencimentos_proximos['30'])
    dias_15 = len(vencimentos_proximos['15'])
    vencidos_dias = len(vencidos)
    jQuery('#vencimentos-cadastros-60').text(dias_60)
    jQuery('#vencimentos-cadastros-30').text(dias_30)
    jQuery('#vencimentos-cadastros-15').text(dias_15)
    jQuery('#vencidos-dias').text(vencidos_dias)
    
    total = dias_60 + dias_30 + dias_15 + vencidos_dias
    jQuery('#notifications-number').text(total)
    
    if total:
        jQuery('.notifications-circle').show()
        # colocar um browser timer aqui
        jQuery('.notifications-tooltip').fadeToggle()
        
    
def getVencimentosProximos():
    for page in pages:
        for cadastro in page.table:
            vencimento = cadastro[6].split('-')
            vencimento = datetime(int(vencimento[0]), int(vencimento[1]), int(vencimento[2]))
            agora = datetime.now()
            prazo = (vencimento-agora).days + 1
            if prazo > 60:
                continue
            elif prazo > 30:
                vencimentos_proximos["60"].append(cadastro)
            elif prazo > 15:
                vencimentos_proximos["30"].append(cadastro)
            elif prazo >= 0:
                vencimentos_proximos["15"].append(cadastro)
            elif prazo < 0:
                vencidos.append(cadastro)
                
    buildNotifications()
    
def filter(status):
    global filtered
    global cadastros
    for cadastro in cadastros:
        if cadastro[3] == status:
            filtered.append(cadastro)
        
    return filtered

def unfilter(status):
    global filtered
    global cadastros
    for cadastro in cadastros:
        if cadastro[3] == status:
            filtered.remove(cadastro)
        
    return filtered
    
def doFilter(ev):
    global filtered
    global cadastros
    id = ev.target.attrs['id'].split('-')[2]
    container = jQuery(f'#filter-row-{id}')
    if container.hasClass('selected-filter'):
        container.removeClass('selected-filter')
        cleanPages()
        
        data = unfilter(status[int(id)][1]).copy()
        if data:
            buildPages(data)
        else:
            buildPages(cadastros)
            filtered = []
        buildTable(pages[0])
    else:
        container.addClass('selected-filter')
        cleanPages()
        
        data = filter(status[int(id)][1]).copy()
        buildPages(data)
        buildTable(pages[0])
    
def buildFilterTooltip():
    global status
    container = jQuery('.filter-tooltip')
    for item in status:
        row = f'<div id="filter-row-{item[0]}"><p id="filter-text-{item[0]}">{item[1]}</p></div>'
        container.append(row)
        row = jQuery(f'#filter-row-{item[0]}')
        
        row.on('click', doFilter)
        # row.on('click', changeStatus)
        
    
    jQuery('.filter-tooltip').off('click', container.toggle)
    jQuery('.filter-container').on('click', container.toggle)
    
def initialRender(req):
    global cadastros
    data = eval(req.text)
    cadastros = data.copy()
    buildPages(data)
    buildTable(pages[0])
    bindElements()
    _ajax('/get_added_buttons/', getStatus)
    jQuery('.notifications-tooltip').hide()
    jQuery('.filter-tooltip').hide()
    jQuery('.notifications-circle').hide()
    getVencimentosProximos()
        
    
_ajax('/get_table_data/', initialRender, method='GET')