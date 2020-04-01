from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

base = 'Console'

executables = [
    Executable('PreparationFichiers.py', base=base)
]

setup(name='EduKeys',
      version = '1.0',
      description = 'Executable de la preparation des fichiers',
      options = dict(build_exe = buildOptions),
      executables = executables)
