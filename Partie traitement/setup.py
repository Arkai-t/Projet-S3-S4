from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

base = 'Console'

executables = [
    Executable('AjoutBKLaPSR.py', base=base)
]

setup(name='EduKeys',
      version = '1.0',
      description = 'Executable de la production du fichier fusionne',
      options = dict(build_exe = buildOptions),
      executables = executables)
