from browser import document, ajax, html, bind, window, alert

jQuery = window.jQuery
missing_data = []

def _ajax(url, onComplete, method='GET', data={}):
    req = ajax.Ajax()
    req.bind('complete', onComplete)
    req.open(method, url, True)
    req.set_header('content-type', 'application/x-www-form-urlencoded')
    req.send(data)
    
def buildFooter(data):
    for item in data:
        print(item)

    
def initialRender(req):
    data = eval(req.text)
    buildFooter(data[7:])
    for item in data:
        row = f'<tr><td><input type="checkbox" name="checkbox" id="checkbox-{item[0]}">'
        item.pop(0)
        for info in item:
            row += f'<td>{info}</td>'
            if item.index(info) == 5:
                break
        row += '<td><img src="/static/images/seta-roxa.svg" alt="seta-roxa"></img></td></tr>'
        jQuery('tbody').append(row)
        if data.index(item) == 6:
            break
    
_ajax('/get_table_data/', initialRender, method='GET')