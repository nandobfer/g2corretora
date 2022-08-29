from browser import document, ajax, html, bind, window, alert

jQuery = window.jQuery
pages = []
current_page = 1

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
                row += f'<td><div class="status"><p>{info}</p><div class="arrow-down"></div><div class="arrow-up"></div></div></td>'
                continue
                
            row += f'<td>{info}</td>'
            if item.index(info) == 6:
                break
        row += '<td><img src="/static/images/seta-roxa.svg" alt="seta-roxa"></img></td></tr>'
        jQuery('tbody').append(row)
        
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
        
        
def bindElements():
    jQuery('#next-page').on('click', buildNextPage)
    jQuery('#previous-page').on('click', buildPreviousPage)
    jQuery('input[type="checkbox"]:not("#header-checkbox")').on('change', hoverRow)
    jQuery('#header-checkbox').on('change', checkAllBoxes)
        
def buildNextPage(ev):
    cleanTable()
    buildTable(pages[current_page])
        
def buildPreviousPage(ev):
    cleanTable()
    buildTable(pages[current_page-2])
    print(current_page)
    
def initialRender(req):
    data = eval(req.text)
    buildPages(data)
    buildTable(pages[0])
    bindElements()
        
    
_ajax('/get_table_data/', initialRender, method='GET')