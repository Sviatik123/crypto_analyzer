with open('pairs.txt', 'r+') as file:
    text = file.read()
    text = 't' + text.replace(' ', '').replace(',', '').upper().replace('\n','\nt')
    print(text)
    file.truncate(0)
    file.write(text)
