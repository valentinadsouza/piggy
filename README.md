# piggy
Pig latin translator in Python
   fileName= input('Please enter the file name: ')

    validate_file(fileName)
    newWords= convert_file(fileName)
    print(newWords)


def validate_file(fileName):
    try:
        inputFile= open(fileName, 'r')
        inputFile.close()
    except IOError:
        print('File not found.')


def convert_file(fileName):
    inputFile= open(fileName, 'r')
    line_string= [line.split() for line in inputFile]

    for line in line_string:
        for word in line:
            endString= str(word[1:])
            them=endString, str(word[0:1]), 'ay'
            newWords="".join(them)
            return newWords
