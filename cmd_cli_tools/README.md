### + Example 3-2 goes far enough to print out a simple help message and accept arguments to the function:

    $ ./cli_tool.py --help
    Usage: ./cli_tool.py --name <NAME> --greeting <GREETING>

    $ ./cli_tool.py --name Sally --greeting Bonjour
    Bonjour Sally


### + Fire module

    fire then creates the UI based on the method’s name and arguments:
    $ ./simple_fire.py --help
    NAME
        simple_fire.py
    SYNOPSIS
        simple_fire.py <flags>
    FLAGS
        --greeting=GREETING
        --name=NAME

### + add python code to bash :

    csv2json () {
        python3 -c "exec('''
        import csv,json
        print(json.dumps(list(csv.reader(open(\'${1}\')))))
        ''')
        "
        }
    Use it in the shell, which is much simpler than remembering all the calls and modules:
    $ csv2json addresses.csv
