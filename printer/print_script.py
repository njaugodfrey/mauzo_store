import os, fnmatch, time, win32print
from win32printing import Printer

while 1:
    for file in os.listdir(r'c:\Users\User\Downloads'):
        if fnmatch.fnmatch(file, '*.txt'):
            print(file)
            with open(file, 'r') as receipt:
                with Printer(linegap=1) as printer:
                    for line in receipt:
                        if 'Copy' in line:
                            break
                        print('true')
                        font = {'height': 11}
                        printer.text(line, font_config=font)
                    win32print.EndPage()
            with open(file, 'r') as receipt:
                with Printer(linegap=1) as printer:
                    for line in receipt:
                        if 'Copy' in line:
                            for line in receipt:
                                print('true')
                                font = {'height': 11}
                                printer.text(line, font_config=font)
                    win32print.EndPage()
            time.sleep(1.0)
            os.unlink(r'c:\Users\User\Downloads\\' + file)
