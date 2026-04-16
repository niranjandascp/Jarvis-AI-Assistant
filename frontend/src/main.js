const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
    // Create the browser window.
    const win = new BrowserWindow({
        width: 450,
        height: 700,
        backgroundColor: '#0a0a0a',
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    // Load the React app from the local dev server
    win.loadURL('http://localhost:3000');

    // Optional: Open DevTools automatically to see errors
    // win.webContents.openDevTools();

    // Handle cases where the React server isn't ready yet
    win.webContents.on('did-fail-load', () => {
        console.log("React server not found, retrying in 2s...");
        setTimeout(() => {
            win.loadURL('http://localhost:3000');
        }, 2000);
    });
}

// This method will be called when Electron has finished initialization
app.whenReady().then(createWindow);

// Quit when all windows are closed, except on macOS
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});