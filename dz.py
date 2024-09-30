# СТРОКИ
#1
s = input("Введите строку: ")

if len(s) > 1:
    s = '!' + s[1:-1] + '!'
else:
    s = '!'
print(s)

#2
s = input("Введите слово: ")
l = len(s)
first = s[0]
last = s[-1]

print(f"Длина слова: {l}")
print(f"Первая буква: {first}")
print(f"Последняя буква: {last}")

#3
k = int(input("Введите максимально возможную длину строки (k): "))

s = input("Введите строку: ")

if len(s) > k:
    c = s[k:]
    print("Лишние символы:", c)
else:
    print("Длина строки не превышает k")

#4
s = input("Введите два слова через пробел: ")

words = s.split()

if len(words) == 2:
    second = words[1]
    print("Второе слово:", second)
else:
    print("Некорректный ввод, требуется два слова")

#5
s = input("Введите строку слов через пробелы: ")

words = s.split()

longest = max(words, key=len)

print("Самое длинное слово:", longest)

#6
s = input("Введите строку: ")

lowercase_count = sum(1 for char in s if char.islower() and char.isalpha() and 'a' <= char <= 'z')
uppercase_count = sum(1 for char in s if char.isupper() and char.isalpha() and 'A' <= char <= 'Z')

print("Количество строчных букв:", lowercase_count)
print("Количество прописных букв:", uppercase_count)


# СПИСКИ
#1
