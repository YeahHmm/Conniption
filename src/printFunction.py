import os

def printboard(m):
    os.system('clear')
    matrix = m
    toPrint = ' ' + '----' * 14 + '\n|'
    #toPrint += '|'
    for i, j in enumerate(matrix):
        toPrint += '{0:^7}|'.format(j)
        if i == 6 or i == 13 or i == 20 or i ==27 or i == 34\
           or i ==41:
            toPrint += '\n'
            toPrint += ' ' + '----' * 14 + '\n|'
    toPrint = toPrint[:-1]
    print (toPrint)

if __name__ == "__main__":


    blah = input("Press to continue")
    os.system('clear')
    matrix[4] = 1
    printboard(matrix)
