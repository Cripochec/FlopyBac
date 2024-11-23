# СТРОКИ
# #1
# s = input("Введите строку: ")
#
# if len(s) > 1:
#     s = '!' + s[1:-1] + '!'
# else:
#     s = '!'
# print(s)
#
# #2
# s = input("Введите слово: ")
# l = len(s)
# first = s[0]
# last = s[-1]
#
# print(f"Длина слова: {l}")
# print(f"Первая буква: {first}")
# print(f"Последняя буква: {last}")
#
# #3
# k = int(input("Введите максимально возможную длину строки (k): "))
#
# s = input("Введите строку: ")
#
# if len(s) > k:
#     c = s[k:]
#     print("Лишние символы:", c)
# else:
#     print("Длина строки не превышает k")
#
# #4
# s = input("Введите два слова через пробел: ")
#
# words = s.split()
#
# if len(words) == 2:
#     second = words[1]
#     print("Второе слово:", second)
# else:
#     print("Некорректный ввод, требуется два слова")
#
# #5
# s = input("Введите строку слов через пробелы: ")
#
# words = s.split()
#
# longest = max(words, key=len)
#
# print("Самое длинное слово:", longest)
#
# #6
# s = input("Введите строку: ")
#
# lowercase_count = 0
# for char in s:
#     if char.islower() and char.isalpha() and 'a' <= char <= 'z':
#         lowercase_count += 1
#
# uppercase_count = 0
# for char in s:
#     if char.isupper() and char.isalpha() and 'A' <= char <= 'Z':
#         uppercase_count += 1
#
# print("Количество строчных букв:", lowercase_count)
# print("Количество прописных букв:", uppercase_count)


# СПИСКИ
#1
my_list = [1, 2, 3, 4, 5]

# Обращение к элементу по индексу
element = my_list[2]

# Замена элемента
my_list[2] = 10

# Добавление элемента
my_list.append(6)

# Удаление элемента
my_list.remove(4)

# Дублирование списка
duplicate_list = my_list[:]

print("Обращение к элементу:", element)
print("После замены:", my_list)
print("После добавления:", my_list)
print("После удаления:", my_list)
print("Дублированный список:", duplicate_list)

#2
lst = [5, 3, 9, 1, 7, 4]
min_index = lst.index(min(lst))

print("Индекс минимального элемента:", min_index)

#3
numbers = [-3, 4, -1, 7, 0, 2]

positive_numbers = [x for x in numbers if x > 0]
other_numbers = [x for x in numbers if x <= 0]

print("Положительные элементы:", positive_numbers)
print("Остальные элементы:", other_numbers)

#4
D = [1, 2, 3, 4, 5, 6, 7, 8]

odd_index_sum = sum(D[i] for i in range(len(D)) if i % 2 != 0)

print("Список D:", D)
print("Сумма элементов с нечетными индексами:", odd_index_sum)

#5
arr = [10, 15, 8, 20, 13, 25, 5, 30]

arr = [x * 2 if x < 15 else x for x in arr]

print("Преобразованный список:", arr)

#6
list1 = [1, 2, 3, 4, 5]
list2 = [3, 4, 5, 6, 7]

common_elements = sorted(set(list1) & set(list2))

print("Общие элементы:", common_elements)
