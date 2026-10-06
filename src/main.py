def input_matrix():
    n = int(input("Введите количество строк n: "))
    m = int(input("Введите количество столбцов m: "))
    matrix = []
    print("Введите элементы матрицы:")
    for i in range(n):
        row = []
        for j in range(m):
            x = float(input(f"a[{i}][{j}] = "))
            row.append(x)
        matrix.append(row)
    return matrix


def find_negative_columns(matrix, m):
    res = []
    for j in range(m):
        prov = True
        for i in range(len(matrix)):
            if matrix[i][j] >= 0:
                prov = False
                break
        if prov:
            res.append(j)
    return res


def main():
    n = int(input("Введите количество строк n: "))
    m = int(input("Введите количество столбцов m: "))
    matrix = []
    print("Введите элементы матрицы:")
    for i in range(n):
        row = []
        for j in range(m):
            x = float(input(f"a[{i}][{j}] = "))
            row.append(x)
        matrix.append(row)

    print("Исходная матрица:")
    for row in matrix:
        print(row)

    res = find_negative_columns(matrix, m)

    if res:
        print("Номера столбцов, содержащих только отрицательные элементы:")
        print(res)
    else:
        print("Столбцов, содержащих только отрицательные элементы, нет.")


if __name__ == "__main__":
    main()
