import cx_Freeze

executables = [cx_Freeze.Executable("play.py")]

cx_Freeze.setup(
    name="A bit Racey",
    options={"build_exe": {"packages":["pygame","configparser"],
                           "include_files":["config.cfg", "images", 'Sounds']}},
    executables = executables

    )