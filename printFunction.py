def printma():
    x = "0"*42
    matrix = map(int, list(x))

    toPrint = ''
    for i, j in enumerate(matrix):
        toPrint += '{0:^7}|'.format(j)
        if i == 6 or i == 13 or i == 20 or i ==27 or i == 34\
           or i ==41:
            toPrint += '\n'
    print (toPrint)
if __name__ == "__main__":
    printma()
