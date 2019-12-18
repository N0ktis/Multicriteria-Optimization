import numpy
import copy


def norma(w, s):
    for i in range(0, len(w), 1):
        w[i] = w[i] / s
    return w


def consistency_relation(A, A_sum):
    A_max = 0
    c_r = 0
    for i in range(len(A)):
        for j in range(len(A[i])):
            A_max += A[j][i]
        c_r += A_max * A_sum[i][1]
        A_max = 0
    return (c_r - 4) / 3


def print_matrix(A):
    for i in range(0, len(A), 1):
        for j in range(0, len(A[i]), 1):
            if (j != 0 and i != 0):
                print('%.2f' % A[i][j], (len(A[0][j]) - 7) * ' ', '|', end='')
            else:

                print(A[i][j], end='')
        print()


def replacement_of_criteria(A, main_crit):
    min_ = [11, 11, 11, 11]
    max_ = [-1, -1, -1, -1]
    permissible_val = [0.3, 0.2, 0.5, 0.1]
    print("We compose matrix A of estimates for alternatives.")
    print_matrix(A)
    print()
    for i in range(1, 5):
        if (i == main_crit): continue
        for j in range(1, 5):
            if (A[j][i] < min_[i - 1]): min_[i - 1] = A[j][i]
            if (A[j][i] > max_[i - 1]): max_[i - 1] = A[j][i]
        permissible_val[i - 1] *= max_[i - 1]
    max_crit = -1
    ans = "no suitable varianat "
    for i in range(1, 5):
        flag = 0
        for j in range(1, 5):
            if (j == main_crit): continue
            if (A[i][j] < permissible_val[j - 1]):  flag = 1
        if (flag == 0 and A[i][main_crit] > max_crit):
            max_crit = A[i][main_crit]
            ans = A[i][0]
    for i in range(1, 5):
        if (i == main_crit): continue
        for j in range(1, 5):
            A[j][i] = (A[j][i] - min_[i - 1]) / (max_[i - 1] - min_[i - 1])
    print("Normalized matrix:")
    print_matrix(A)
    print()
    return ans[:-1]


def Pareto(A, main_crit1, main_crit2):
    max_ = [10, 10, 10, 10]
    print("Utopia: ", A[0][main_crit1][:-1], '-', max_[main_crit1], ';', A[0][main_crit2][:-1], '-', max_[main_crit2])
    min_dist = abs(max_[main_crit1 - 1] - A[1][main_crit1]) + abs(max_[main_crit2 - 1] - A[1][main_crit2])
    ans = A[1][0]
    print("Distance:")
    for i in range(1, 5):
        dist = abs(max_[main_crit1 - 1] - A[i][main_crit1]) + abs(max_[main_crit2 - 1] - A[i][main_crit2])
        print(A[i][0][:-1], '-', '%.3f' % dist)
        if (dist < min_dist):
            min_dist = dist
            ans = A[i][0]
    return ans[:-1]


def combining_criteria(A):
    print_matrix(A)
    print()
    gamma = [[0, 0.5, 0, 0],
             [0.5, 0, 0, 0],
             [1, 1, 0, 0],
             [1, 1, 1, 0]]
    alpha = [0, 0, 0, 0]
    for i in range(0, 4):
        for j in range(0, 4):
            alpha[i] += gamma[i][j]
    A_diff = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for i in range(1, 5, 1):
        for j in range(1, 5, 1):
            A_diff[i - 1][j - 1] = A[j][i]
        A_diff[i - 1] = norma(A_diff[i - 1], sum(A_diff[i - 1]))

    for i in range(1, 5, 1):
        for j in range(1, 5, 1):
            A[j][i] = A_diff[i - 1][j - 1]
    print_matrix(A)
    print()
    print("Vector of criteria:")
    print(alpha[0], alpha[1], alpha[2], alpha[3])
    alpha = numpy.array(norma(alpha, sum(alpha))).transpose()
    print("Normalized vector of criteria:")
    print('%.3f' % alpha[0], '%.3f' % alpha[1], '%.3f' % alpha[2], '%.3f' % alpha[3])
    print()
    A_diff = numpy.array(A_diff).transpose()
    ans_matr = A_diff.dot(weight)
    m = max(ans_matr)
    for i in range(4):
        print(A[i + 1][0][:-1:], ':', '%.3f' % ans_matr[i])
    for i, num in enumerate(ans_matr):
        if num == m:
            return (A[i + 1][0][:-1])
    return


def hierarchy_analysis(A):
    buff_matr = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    buff_matr_crit = [0, 0, 0, 0]
    A_1 = [[1, 2, 1 / 2, 3],
           [1 / 2, 1, 3, 2],
           [2, 1 / 3, 1, 4],
           [1 / 3, 1 / 2, 1 / 4, 1]]
    A_2 = [[1, 1 / 2, 4, 4],
           [2, 1, 7, 7],
           [1 / 4, 1 / 7, 1, 2],
           [1 / 4, 1 / 7, 1 / 2, 1]]
    A_3 = [[1, 1 / 3, 1 / 2, 1 / 4],
           [3, 1, 2, 1 / 2],
           [2, 1 / 2, 1, 1 / 3],
           [4, 2, 3, 1]]
    A_4 = [[1, 1 / 2, 1 / 7, 1 / 7],
           [2, 1, 1 / 6, 1 / 6],
           [7, 6, 1, 1 / 2],
           [7, 6, 2, 1]]
    A_crit = [[1, 1 / 2, 1 / 4, 1 / 7],
              [2, 1, 1 / 2, 1 / 6],
              [4, 2, 1, 1 / 3],
              [7, 6, 3, 1]]
    A_sum1 = [[0, 0],
              [0, 0],
              [0, 0],
              [0, 0]]
    A_sum2 = [[0, 0],
              [0, 0],
              [0, 0],
              [0, 0]]
    A_sum3 = [[0, 0],
              [0, 0],
              [0, 0],
              [0, 0]]
    A_sum4 = [[0, 0],
              [0, 0],
              [0, 0],
              [0, 0]]
    A_sum_crit = [[0, 0],
                  [0, 0],
                  [0, 0],
                  [0, 0]]
    comparison_matr = [A_1, A_2, A_3, A_4, A_crit]
    sum_crit = [A_sum1, A_sum2, A_sum3, A_sum4, A_sum_crit]
    for i in range(0, 5):
        for j in range(0, len(comparison_matr[i])):
            sum_stroke = 0
            for k in range(0, len(comparison_matr[i][j])):
                sum_stroke += comparison_matr[i][j][k]
            sum_crit[i][j][0] = sum_stroke
    for i in range(0, 5):
        sum_column = 0
        for j in range(0, len(sum_crit[i])):
            sum_column += sum_crit[i][j][0]
        for j in range(0, len(sum_crit[i])):
            sum_crit[i][j][1] = sum_crit[i][j][0] / sum_column

    print(A[0][1][:-1] + ':')
    print(' ' * 16 + '|', A[1][0], A[2][0], A[3][0], A[4][0], "  Sum  |", "  Norm sum  |")
    print(
        "----------------+-----------------+-----------------+-----------------+-----------------+--------+-------------+")
    for i in range(4):
        print(A[i + 1][0], '%.3f' % A_1[i][0], ' ' * 10 + '|', '%.3f' % A_1[i][1], ' ' * 10 + '|', '%.3f' % A_1[i][2],
              ' ' * 10 + '|', '%.3f' % A_1[i][3], ' ' * 10 + '|',
              '%.3f' % A_sum1[i][0], ' ' + '|', '%.3f' % A_sum1[i][1], ' ' * 6 + '|')
    print("Consistency relation:", '%.3f' % consistency_relation(A_1, A_sum1))
    print()

    print(A[0][2][:-1] + ':')
    print(' ' * 16 + '|', A[1][0], A[2][0], A[3][0], A[4][0], "  Sum  |", "  Norm sum  |")
    print(
        "----------------+-----------------+-----------------+-----------------+-----------------+--------+-------------+")
    for i in range(4):
        print(A[i + 1][0], '%.3f' % A_2[i][0], ' ' * 10 + '|', '%.3f' % A_2[i][1], ' ' * 10 + '|', '%.3f' % A_2[i][2],
              ' ' * 10 + '|', '%.3f' % A_2[i][3], ' ' * 10 + '|',
              '%.3f' % A_sum2[i][0], ' ' + '|', '%.3f' % A_sum2[i][1], ' ' * 6 + '|')
    print("Consistency relation:", '%.3f' % consistency_relation(A_2, A_sum2))
    print()

    print(A[0][3][:-1] + ':')
    print(' ' * 16 + '|', A[1][0], A[2][0], A[3][0], A[4][0], "  Sum  |", "  Norm sum  |")
    print(
        "----------------+-----------------+-----------------+-----------------+-----------------+--------+-------------+")
    for i in range(4):
        print(A[i + 1][0], '%.3f' % A_3[i][0], ' ' * 10 + '|', '%.3f' % A_3[i][1], ' ' * 10 + '|', '%.3f' % A_3[i][2],
              ' ' * 10 + '|', '%.3f' % A_3[i][3], ' ' * 10 + '|',
              '%.3f' % A_sum3[i][0], ' ' + '|', '%.3f' % A_sum3[i][1], ' ' * 6 + '|')
    print("Consistency relation:", '%.3f' % consistency_relation(A_3, A_sum3))
    print()

    print(A[0][4][:-1] + ':')
    print(' ' * 16 + '|', A[1][0], A[2][0], A[3][0], A[4][0], "  Sum  |", "  Norm sum  |")
    print(
        "----------------+-----------------+-----------------+-----------------+-----------------+--------+-------------+")
    for i in range(4):
        print(A[i + 1][0], '%.3f' % A_4[i][0], ' ' * 10 + '|', '%.3f' % A_4[i][1], ' ' * 10 + '|', '%.3f' % A_4[i][2],
              ' ' * 10 + '|', '%.3f' % A_4[i][3], ' ' * 10 + '|',
              '%.3f' % A_sum4[i][0], ' ' + '|', '%.3f' % A_sum4[i][1], ' ' * 6 + '|')
    print("Consistency relation:", '%.3f' % consistency_relation(A_4, A_sum4))
    print()

    print("Criteries:")
    print(' ' * 20 + '|', A[0][1], A[0][2], A[0][3], A[0][4], "  Sum  |", "  Norm sum  |")
    print(
        "--------------------+-----------------+----------------+-----------------+---------------------+--------+-------------+")
    for i in range(4):
        print(A[0][i + 1][:-1] + (21 - len(A[0][i + 1])) * ' ' + '|', '%.3f' % A_crit[i][0], ' ' * 10 + '|',
              '%.3f' % A_crit[i][1], ' ' * 9 + '|', '%.3f' % A_crit[i][2],
              ' ' * 10 + '|', '%.3f' % A_crit[i][3], ' ' * 14 + '|',
              '%.3f' % A_sum_crit[i][0], ' ' + '|', '%.3f' % A_sum_crit[i][1], ' ' * 6 + '|')
    print("Consistency relation:", '%.3f' % consistency_relation(A_crit, A_sum_crit))
    print()
    for i in range(0, 4):
        for j in range(0, len(sum_crit[i])):
            buff_matr[i][j] = sum_crit[i][j][1]
        buff_matr_crit[i] = A_sum_crit[i][1]
    print()

    print("Sum matrix:")
    for i in range(4):
        print('%.3f' % buff_matr[i][0], '|', '%.3f' % buff_matr[i][1], '|', '%.3f' % buff_matr[i][2], '|',
              '%.3f' % buff_matr[i][3])

    print("Norm sum matrix:")
    for i in range(4):
        print('%.3f' % buff_matr_crit[i])
    buff_matr_crit = numpy.array(buff_matr_crit)
    buff_matr = numpy.array(buff_matr)
    ans_matr = buff_matr.dot(buff_matr_crit)
    print("Answer matrix:")
    for i in range(4):
        print('%.3f' % ans_matr[i])
    m = max(ans_matr)
    for i, num in enumerate(ans_matr):
        if num == m:
            return (A[i + 1][0][:-1])
    return


weight = [7, 5, 3, 1]
print("| Качество лечения |", "Уровень сервиса |", "Качество питания |", "Расстояние от Москвы |")
print("+------------------+-----------------+------------------+----------------------+")
print("|        ", weight[0], "         |        ", weight[1], "        |        ", weight[2], "         |          ",
      weight[3], "           |", sep="")
weight = norma(weight, sum(weight))
print()
print("Normalized:")
print("| Качество лечения |", "Уровень сервиса |", "Качество питания |", "Расстояние от Москвы |")
print("+------------------+-----------------+------------------+----------------------+")
print("|      ", weight[0], "      |      ", weight[1], "     |      ", weight[2], "      |       ", weight[3],
      "         |", sep="")
A = [["      \\         |", "Качество лечения|", "Уровень сервиса|", "Качество питания|", "Расстояние от Москвы|"],
     ["     Липецк     |", 8, 1, 2, 7],
     ["  Сосновый бор  |", 2, 7, 2, 4],
     ["Лесная жемчужина|", 5, 1, 7, 4],
     ["     Сосны      |", 7, 6, 8, 2]]
main_crit1 = 1
main_crit2 = 3
print()
print("Replacement of criteria:")
print("Answer: ", replacement_of_criteria(copy.deepcopy(A), main_crit1))
print()
print("Pareto:")
print("Answer: ", Pareto(copy.deepcopy(A), main_crit1, main_crit2))
print()
print("Combining criteria:")
print("Answer: ", combining_criteria(copy.deepcopy(A)))
print()
print("Hierarchy analysis:")
print("Answer: ", hierarchy_analysis(copy.deepcopy(A)))
