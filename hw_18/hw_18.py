
user_text = input("Введите текст")
user_num = int(input("Введите число"))

char_text = ''
for sym in user_text:
    if sym.isspace():
        char_text += sym
    else:
        ord_text = ord(sym) + user_num
        char_text += chr(ord_text)

# final_text = ''.join(char_text)

print(f'Ваш текст: {user_text} \nЗашифрованный текст: {char_text}' )

