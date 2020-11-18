import os, fnmatch, time, win32print, re
from win32printing import Printer

rcptregex = re.compile(r'receipt')
voidregex = re.compile(r'void')
invcregex = re.compile(r'invoice')
returnregex = re.compile(r'creditnote')

while 1:
    for file in os.listdir(r'c:\Users\User\Downloads'):
        if fnmatch.fnmatch(file, '*.txt'):
            if rcptregex.search(file) or voidregex.search(file):
                print(file)
                with open(r'c:\Users\User\Downloads\\' + file, 'r') as receipt:
                    with Printer(linegap=1) as printer:
                        for line in receipt:
                            if 'Copy' in line:
                                break
                            print('true')
                            font = {'height': 11}
                            printer.text(line, font_config=font)
                        win32print.EndPage
                with open(r'c:\Users\User\Downloads\\' + file, 'r') as receipt:
                    with Printer(linegap=1) as printer:
                        for line in receipt:
                            if 'Copy' in line:
                                for line in receipt:
                                    print('true')
                                    font = {'height': 11}
                                    printer.text(line, font_config=font)
                        win32print.EndPage

                time.sleep(5.0)
                os.unlink(r'c:\Users\User\Downloads\\' + file)
        
        elif fnmatch.fnmatch(file, '*.txt'):
            if invcregex.search(file) or returnregex.search(file)
                with open(r'c:\Users\User\Downloads\\' + file, 'r') as invoice:
                    with Printer(linegap=1) as printer:
                        for line in invoice:
                            print('true')
                            font = {'height': 11}
                            printer.text(line, font_config=font)
                        win32print.EndPage

                time.sleep(5.0)
                os.unlink(r'c:\Users\User\Downloads\\' + file)
