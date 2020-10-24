import os, fnmatch, time

while 1:
    files = os.listdir(r'c:\Users\User\Downloads')
    for file in files:
        if fnmatch.fnmatch(file, '*.txt'):
            os.startfile(
                r'c:\Users\User\Downloads\\' + file,
                'print'
            )
            time.sleep(5.0)
            os.unlink(r'c:\Users\User\Downloads\\' + file)
            time.sleep(25.0)
