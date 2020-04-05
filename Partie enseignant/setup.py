from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('IHMEnseignant.py', base=base, targetName = 'TelecommandeEnseignant')
]

setup(name='EduKeys',
      version = '1.0',
      description = "Telecommande de l'enseignant pour visualiser un fichier consolide",
      options = dict(build_exe = buildOptions),
      executables = executables)
