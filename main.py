import sys
import create_script as cr_script

if sys.argv[1] is not None:
    route_file = sys.argv[1]
    delimiter = ';'
    if sys.argv.__len__() == 3:
        delimiter = sys.argv[2]
    try:
        create_scripts = cr_script.Create_Script(route_file, delimiter)
        create_scripts.call_tables()
    except Exception as err:
        print(err)
