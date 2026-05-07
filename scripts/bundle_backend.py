import os
import subprocess
import shutil

def bundle_python():
    print("📦 Starting Python bundling process...")
    
    # Path to the server script
    server_script = os.path.join("backend", "server.py")
    
    # Run PyInstaller
    # --onefile: bundle everything into a single exe
    # --distpath: where to put the final exe
    # --workpath: where to put temp files
    # --name: name of the exe
    cmd = [
        "pyinstaller",
        "--onefile",
        "--noconsole",
        "--distpath", os.path.join("backend", "dist"),
        "--workpath", os.path.join("backend", "build"),
        "--name", "server",
        server_script
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    
    print("✅ Python bundled successfully in backend/dist/server.exe")

if __name__ == "__main__":
    bundle_python()
