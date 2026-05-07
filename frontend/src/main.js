const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const net = require('net');

let flaskProcess = null;

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
    console.log("⏳ Polling for Neural Backend and UI Engine...");
    
    // Check Backend (5000)
    let backendReady = false;
    while (!backendReady) {
        backendReady = await checkPort(5000);
        if (!backendReady) {
            console.log("Waiting for Backend (Port 5000)...");
            await new Promise(r => setTimeout(r, 1000));
        }
    }

    // Check Frontend (3000) - Only in dev mode
    if (!isProd) {
        let frontendReady = false;
        while (!frontendReady) {
            frontendReady = await checkPort(3000);
            if (!frontendReady) {
                console.log("Waiting for React Engine (Port 3000)...");
                await new Promise(r => setTimeout(r, 1000));
            }
        }
    }

    console.log("✅ All systems online. Launching UI.");
}

function startFlask() {
    const isPackaged = app.isPackaged;
    let pythonExe = isPackaged 
        ? path.join(process.resourcesPath, 'backend', 'server.exe')
        : 'python';
    
    let serverPath = isPackaged 
        ? null 
        : path.join(__dirname, '..', '..', 'backend', 'server.py');

    if (isPackaged) {
        flaskProcess = spawn(pythonExe);
    } else {
        flaskProcess = spawn(pythonExe, [serverPath]);
    }

    flaskProcess.stdout.on('data', (data) => console.log(`Flask: ${data}`));
    flaskProcess.stderr.on('data', (data) => console.error(`Flask Error: ${data}`));
}

async function createWindow() {
    const win = new BrowserWindow({
        width: 450,
        height: 800,
        frame: false,
        backgroundColor: '#0a0a0a',
        show: false, // Don't show until ready
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    const isProd = app.isPackaged || process.env.NODE_ENV === 'production';
    const startUrl = isProd 
        ? `file://${path.join(__dirname, '../build/index.html')}`
        : 'http://localhost:3000';

    // Wait for services before loading
    await waitForServices(isProd);

    win.loadURL(startUrl);
    win.once('ready-to-show', () => win.show());
}

app.whenReady().then(() => {
    startFlask();
    createWindow();
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