const { app, BrowserWindow } = require("electron");
const path = require("path");

function createWindow() {
  const win = new BrowserWindow({
    width: 450,
    height: 700,
    // frame: false,  <-- Ippo ithu comment cheyyu, window control cheyyaan eluppathinu
    webPreferences: {
        nodeIntegration: true,
        contextIsolation: false,
        // 🔴 ITHU ADD CHEYYUKA
        permissions: ['microphone'] 
    },
    backgroundColor: "#0a0a0a",
  });

  // 🔴 ITHU ADD CHEYYUKA: Window load aayi kazhinju maathram show cheyyaan
  win.webContents.on("did-fail-load", () => {
    console.log("React server kittiilla! URL onnu check cheyyu.");
    win.loadURL("http://localhost:3000");
  });

  // DevTools thurakkaam error enthaanennu ariyan
  win.webContents.openDevTools();

  win.loadURL("http://localhost:3000");

  const { session } = require('electron');
session.defaultSession.setPermissionCheckHandler((webContents, permission) => {
    if (permission === 'media') return true;
    return false;
});
app.whenReady().then(createWindow);

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});
