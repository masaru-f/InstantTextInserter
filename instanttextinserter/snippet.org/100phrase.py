# encoding: shift-jis

import os

#mode = 'create'
mode = 'remove'

for i in range(100):
    filename = 'zzz_%03d' % i

    if mode=='create':
        s = '==s%03d==' % i
        s += '\n'
        s += 'this is ' + str(i) + ' phrase.'

        f = file(filename, 'w')
        f.write(s)
        f.close()
    elif mode=='remove':
        os.remove(filename)
