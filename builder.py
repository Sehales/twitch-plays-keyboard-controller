import os

import PyInstaller.__main__

PyInstaller.__main__.run([
    '--windowed',
    "-c",
    "-F",
    os.path.join('.', 'run_controller.py'),
])
