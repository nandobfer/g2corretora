import webview

def maximize(window):
    window.maximize()


if __name__ == '__main__':
    window = webview.create_window('G2 Corretora', 'https://sistema.g2corretora.com.br:5002/', text_select=True, confirm_close=True)
    webview.start()
    