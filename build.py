import os
import subprocess
import customtkinter
import shutil

# 1. Get the path where CustomTkinter is installed
ctk_path = os.path.dirname(customtkinter.__file__)

# 2. Define the PyInstaller command
# We use ';' for Windows. Change to ':' if you are building on Linux.
separator = ';' if os.name == 'nt' else ':'

cmd = [
    'pyinstaller',
    '--noconfirm',
    '--onefile',
    '--windowed',
    f'--add-data={ctk_path}{separator}customtkinter/',
    'main.py'
]

print(f"--- Starting Build for Sell-X Labeler ---")
subprocess.run(cmd)

# 3. Cleanup: Move the exe out and delete temporary folders
if os.path.exists("dist/main.exe"):
    if os.path.exists("SellX_Labeler.exe"):
        os.remove("SellX_Labeler.exe")
    os.rename("dist/main.exe", "SellX_Labeler.exe")
    
    # Optional: Clean up build folders to keep your project tidy
    shutil.rmtree("build", ignore_errors=True)
    shutil.rmtree("dist", ignore_errors=True)
    os.remove("main.spec")

print("--- Build Complete! Run 'SellX_Labeler.exe' ---")