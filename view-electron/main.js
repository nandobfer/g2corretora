const { app, BrowserWindow } = require('electron')

const createWindow = () => {
  const window = new BrowserWindow({
    titleBarStyle: 'hidden',
    titleBarOverlay: true,
    width: 800,
    height: 600
  })

  window.loadURL('https://sistema.g2corretora.com.br:5002/tabela/')
  window.maximize()
}

app.whenReady().then(() => {
  createWindow()
})