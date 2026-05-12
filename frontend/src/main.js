const { app, BrowserWindow, ipcMain, Tray, Menu, globalShortcut } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const net = require('net');

let flaskProcess = null;
let mainWindow = null;
let tray = null;

// Ensure only one instance runs
const gotTheLock = app.requestSingleInstanceLock();
if (!gotTheLock) {
    app.quit();
} else {
    app.on('second-instance', () => {
        if (mainWindow) {
            if (mainWindow.isMinimized()) mainWindow.restore();
            mainWindow.focus();
        }
    });
}

function checkPort(port, host = '127.0.0.1') {
    return new Promise((resolve) => {
        const socket = new net.Socket();
        const timeout = setTimeout(() => {
            socket.destroy();
            resolve(false);
        }, 1000);
        socket.on('connect', () => {
            clearTimeout(timeout);
            socket.destroy();
            resolve(true);
        });
        socket.on('error', () => {
            clearTimeout(timeout);
            resolve(false);
        });
        socket.connect(port, host);
    });
}

async function waitForServices(isProd) {
    console.log("⏳ Syncing Neural Cores...");
    let backendReady = false;
    while (!backendReady) {
        backendReady = await checkPort(5000);
        if (!backendReady) await new Promise(r => setTimeout(r, 1000));
    }
    if (!isProd) {
        let frontendReady = false;
        while (!frontendReady) {
            frontendReady = await checkPort(3000);
            if (!frontendReady) await new Promise(r => setTimeout(r, 1000));
        }
    }
}

function startFlask() {
    const isPackaged = app.isPackaged;
    console.log(`🚀 JARVIS_CORE: Syncing Backend (Packaged: ${isPackaged})`);

    let pythonExe = isPackaged 
        ? path.join(process.resourcesPath, 'backend', 'server.exe')
        : 'python';
    
    let serverPath = isPackaged 
        ? null 
        : path.join(app.getAppPath(), '..', 'backend', 'server.py');

    const spawnOptions = { shell: true };

    if (isPackaged) {
        flaskProcess = spawn(pythonExe, [], spawnOptions);
    } else {
        console.log(`DEBUG: Deploying neural brain at ${serverPath}`);
        flaskProcess = spawn(pythonExe, [`"${serverPath}"`], spawnOptions);
    }

    flaskProcess.stdout.on('data', (data) => console.log(`[CORE]: ${data}`));
    flaskProcess.stderr.on('data', (data) => console.error(`[CORE_ERR]: ${data}`));
}

async function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        minWidth: 900,
        minHeight: 600,
        frame: false, // CRITICAL: Frameless
        transparent: false,
        backgroundColor: '#000000',
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
            webSecurity: false
        }
    });

    const isProd = app.isPackaged || process.env.NODE_ENV === 'production';
    const startUrl = isProd 
        ? `file://${path.join(__dirname, '../build/index.html')}`
        : 'http://localhost:3000';

    await waitForServices(isProd);
    mainWindow.loadURL(startUrl);
    
    mainWindow.once('ready-to-show', () => {
        mainWindow.show();
        mainWindow.focus();
    });

    // Cleanup on close
    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

// --- UNIVERSAL IPC HANDLERS ---
ipcMain.on('window-minimize', (event) => {
    const win = BrowserWindow.fromWebContents(event.sender);
    if (win) win.minimize();
});

ipcMain.on('window-maximize', (event) => {
    const win = BrowserWindow.fromWebContents(event.sender);
    if (win) {
        if (win.isMaximized()) win.unmaximize();
        else win.maximize();
    }
});

ipcMain.on('window-close', (event) => {
    const win = BrowserWindow.fromWebContents(event.sender);
    if (win) win.close();
});

app.whenReady().then(() => {
    startFlask();
    createWindow();

    // --- SYSTEM TRAY ---
    const iconPath = path.join(__dirname, '../../icon.png');
    tray = new Tray(iconPath);
    
    const contextMenu = Menu.buildFromTemplate([
        { label: 'JARVIS_HUD', click: () => { if (mainWindow) mainWindow.show(); } },
        { type: 'separator' },
        { label: 'TERMINATE', click: () => { app.quit(); } }
    ]);

    tray.setToolTip('JARVIS Neural Interface');
    tray.setContextMenu(contextMenu);

    tray.on('click', () => {
        if (mainWindow) {
            mainWindow.isVisible() ? mainWindow.hide() : mainWindow.show();
        }
    });

    // --- GLOBAL SHORTCUT (ALT+J) ---
    globalShortcut.register('Alt+J', () => {
        if (mainWindow) {
            if (mainWindow.isVisible() && mainWindow.isFocused()) {
                mainWindow.hide();
            } else {
                mainWindow.show();
                mainWindow.focus();
            }
        }
    });
});

app.on('will-quit', () => {
    // Unregister all shortcuts
    globalShortcut.unregisterAll();
});

app.on('window-all-closed', () => {
    if (flaskProcess) {
        if (process.platform === 'win32') {
            spawn('taskkill', ['/pid', flaskProcess.pid, '/f', '/t']);
        } else {
            flaskProcess.kill();
        }
    }
    if (process.platform !== 'darwin') app.quit();
});