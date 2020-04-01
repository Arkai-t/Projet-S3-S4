from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

base = 'Console'

executables = [
    Executable('Lancement.py', base=base, targetName = 'Traitement')
]

setup(name='EduKeys',
      version = '1.0',
      description = 'Tous le traitement des fichiers de traces',
      options = dict(build_exe = buildOptions),
      executables = executables)
