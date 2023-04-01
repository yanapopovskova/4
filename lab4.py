""" С клавиатуры вводится два числа K и N.Квадратная матрица А(N,N), состоящая из 4-х равных по размерам подматриц, B,C,D,E
заполняется случайным образом целыми числами в интервале [-10,10]. Для отладки использовать не случайное заполнение,
а целенаправленное. Вид матрицы А:
D E
C B
Вариант 12. Формируется матрица F следующим образом: скопировать в нее А и  если в B количество простых чисел в нечётных
столбцах больше, чем сумма чисел в четных строках, то поменять местами B и E симметрично, иначе C и Е поменять местами
несимметрично. При этом матрица А не меняется. После чего если определитель матрицы А больше суммы диагональных
элементов матрицы F, то вычисляется выражение: A^(-1)*AT–K*F^(-1), иначе вычисляется выражение (A^(-1) +G-F^(-1))*K, где G-нижняя
треугольная матрица, полученная из А. Выводятся по мере формирования А, F и все матричные операции последовательно.
"""

from math import ceil, floor
import random
import numpy as np
from matplotlib import pyplot as plt



def printMatrix(matrix):  # вывод матрицы
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print("{:5d}".format(matrix[i][j]), end="")
        print()


k = int(input("Введите число K: "))
n = int(input("Введите число N, больше 3: "))
while n <= 3:  # ошибка в случае введения слишком малого порядка матрицы
    n = int(input("Вы ввели число, неподходящее по условию, введите число N>3:\n"))

A = np.random.randint(-10.0, 10.0, (n, n))  # создаётся матрицы А
print("\nМатрица A:\n")
printMatrix(A)

F = A.copy()  # Создание матрицы F
F_dump = F.copy()

submatrix_order = ceil(n / 2)  # определитель матрицы  для смены C на E
submatrix_length = n // 2  # # определитель матрицы для смены B на E
b = np.array(A[submatrix_length + n % 2:n, submatrix_length + n % 2:n])  # подматрицы B
e = np.array(A[submatrix_length + n % 2:n, :submatrix_length])  # подматрицы C

# вычленяем подматрицу Е через срезы
# проверка n на четность нужна, чтобы матрица А делилась на равные 4 подматрицы.
if n % 2 == 0:
    c = [F[i][submatrix_order:n] for i in range(0, submatrix_order)]
else:
    c = [F[i][submatrix_order - 1:n] for i in range(0, submatrix_order)]


lst = []
for i in range(submatrix_order):
    for j in range(submatrix_order):
        if (j + 1) % 2 != 0:
            lst.append(c[i][j])
maxvalue = max(lst)


sumvalue = 0
for i in range(submatrix_order):
    for j in range(submatrix_order):
        if (i + 1) % 2 == 0:
            sumvalue += c[i][j]

# матрицa F по условию
if maxvalue > sumvalue:
    # меняем B и E симметрично
    F[submatrix_length + n % 2:n, submatrix_length + n % 2:n] = b[::, ::-1]
    F[submatrix_length + n % 2:n, :submatrix_length] = e[::, ::-1]
    print("Матрица F:")
    printMatrix(F)
else:
    # меняем C и E несимметрично
    for i in range(ceil(n / 2)):
        for j in range(ceil(n / 2), n):
            F[i][j] = F_dump[floor(n / 2) + i][j]
            F[floor(n / 2) + i][j] = F_dump[i][j]
    print("Матрица F:")
    printMatrix(F)

# ниже вычисляем и выводим выражения по условию
np.set_printoptions(linewidth=1000)
try:
    if np.linalg.det(A) > sum(np.diagonal(F)):
        print("\nРезультат выражения A^(-1)*AT – K * F^(-1):\n",
              np.linalg.inv(A) * A.transpose() - k * np.linalg.inv(F))
    else:
        G = np.tri(n) * A
        print("\nРезультат выражения (A^(-1) + G - F^(-1)) * K:\n",
              (np.linalg.inv(A) + G - np.linalg.inv(F)) * k)
except np.linalg.LinAlgError:
    print(" Обратную матрицу найти невозможно.")




fig, axs = plt.subplots(2, 2, figsize=(11, 15)) #создаем окно и 4 графика на нем

# ниже первый график с фунцией plot
x = list(range(1, n + 1))  # получаем значения х
for j in range(n):
    y = list(F[j, ::])  #получаем значения у
    axs[0, 1].plot(x, y)  # строим график справа вверху
    axs[0, 1].set(title="График с использованием функции plot:",  #обозначения на графике
                  xlabel='Номер элемента в строке',
                  ylabel='Значение элемента')
    axs[0, 1].grid(True)  # сетка на графике

    # ниже второй график с фунцией bar
    axs[1, 0].bar(x, y, 0.4, label=f"{j+1} строка.")  # строим график слева снизу
    axs[1, 0].set(title="График с использованием функции bar:",
                  xlabel='Номер элемента в строке',
                  ylabel='Значение элемента')

# ниже блок для создания массива, чтобы потом скормить его функции pie
av = [np.mean(abs(F[i, ::])) for i in range(n)]
av = int(sum(av))
sizes = [round(np.mean(abs(F[i, ::])) * 100/av, 1) for i in range(n)]
axs[0, 0].set(title="График с использованием функции pie:",)
axs[0, 0].pie(sizes, labels=list(range(1, n+1)), autopct='%1.1f%%', shadow=True)  # строим график слева вверху

# ниже третий комбинированный график plot и bar
x = list(range(1, n + 1))  # получаем значения х
for j in range(n):
    y = list(F[j, ::])
    plt.plot(x, y)
    plt.bar(x, y, 0.4, label=f"{j + 1} строка.")

plt.xlabel('Номер элемента в строке')
plt.ylabel('Значение элемента')
plt.title(' Комбинированние графиков bar и plot')


plt.show()
