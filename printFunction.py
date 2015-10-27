def printma():
    x = "0"*42
    matrix = map(int, list(x))

    toPrint = ''
    for i, j in enumerate(matrix):
        toPrint += '{0:^7}|'.format(j)
        if i == 7 or i == 14 or i == 21 or i ==28 or i == 35\
           or i ==42:
            toPrint += '\n'
    print (toPrint)
if __name__ == "__main__":
    printma()
