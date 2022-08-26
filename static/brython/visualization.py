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
        row = f'<tr><td><input type="checkbox" name="checkbox" id="checkbox-{item[0]}">'
        for info in item:
            if item.index(info) == 0:
                continue
            row += f'<td>{info}</td>'
            if item.index(info) == 6:
                break
        row += '<td><img src="/static/images/seta-roxa.svg" alt="seta-roxa"></img></td></tr>'
        jQuery('tbody').append(row)
        
        
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
    jQuery('#next-page').on('click', buildNextPage)
    jQuery('#previous-page').on('click', buildPreviousPage)
    
    
_ajax('/get_table_data/', initialRender, method='GET')