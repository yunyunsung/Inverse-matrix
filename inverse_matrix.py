def input_matrix():
    while True:
        try:
            n = int(input("정방행렬의 차수를 입력하세요 (1~4): "))
        except ValueError:
            print("숫자를 입력해주세요.")
            continue
        if 1 <= n <= 4:
            break
        print("1~4 사이의 값만 입력할 수 있습니다.")

    matrix = []
    i = 0
    while i < n:
        row = input(f"{i + 1}행: ").split()
        if len(row) != n:
            print(f"숫자 {n}개를 입력해야 합니다. 다시 입력하세요.")
            continue
        try:
            matrix.append([float(x) for x in row])
        except ValueError:
            print("숫자만 입력해주세요.")
            continue
        i += 1
    return matrix


def fmt(x):
    if abs(x) < 1e-10:
        x = 0.0
    return f"{x:8.3f}"


def print_matrix(m):
    for row in m:
        print(" ".join(fmt(x) for x in row))


def print_augmented(a, n):
    for row in a:
        left = " ".join(fmt(x) for x in row[:n])
        right = " ".join(fmt(x) for x in row[n:])
        print(left, " |", right)


# 행렬식 이용

def get_minor(m, row, col):
    minor = []
    for i in range(len(m)):
        if i == row:
            continue
        minor.append(m[i][:col] + m[i][col + 1:])
    return minor


def determinant(m):
    n = len(m)
    if n == 1:
        return m[0][0]
    if n == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]

    det = 0
    for j in range(n):
        det += ((-1) ** j) * m[0][j] * determinant(get_minor(m, 0, j))
    return det


def inverse_by_det(m):
    n = len(m)
    det = determinant(m)
    if abs(det) < 1e-10:
        return None

    if n == 1:
        return [[1 / m[0][0]]]

    inv = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            cofactor = ((-1) ** (i + j)) * determinant(get_minor(m, i, j))
            inv[j][i] = cofactor / det  # 수반행렬이라 전치해서 넣음
    return inv


# 가우스-조던 소거법 이용

def inverse_by_gauss(m):
    n = len(m)
    a = []
    for i in range(n):
        identity_row = [1.0 if i == j else 0.0 for j in range(n)]
        a.append(m[i][:] + identity_row)

    print("\n[초기 첨가행렬 A | I]")
    print_augmented(a, n)

    step = 1
    for col in range(n):
        pivot = col
        while pivot < n and abs(a[pivot][col]) < 1e-10:
            pivot += 1
        if pivot == n:
            print(f"\n{col + 1}열에 0이 아닌 피벗이 없어서 역행렬을 구할 수 없습니다.")
            return None

        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            print(f"\n[Step {step}] R{col + 1} <-> R{pivot + 1}")
            print_augmented(a, n)
            step += 1

        p = a[col][col]
        if abs(p - 1) > 1e-10:
            a[col] = [x / p for x in a[col]]
            print(f"\n[Step {step}] R{col + 1} = R{col + 1} / ({p:.3f})")
            print_augmented(a, n)
            step += 1

        for r in range(n):
            if r == col or abs(a[r][col]) < 1e-10:
                continue
            k = a[r][col]
            a[r] = [a[r][j] - k * a[col][j] for j in range(2 * n)]
            print(f"\n[Step {step}] R{r + 1} = R{r + 1} - ({k:.3f}) * R{col + 1}")
            print_augmented(a, n)
            step += 1

    return [row[n:] for row in a]


def is_same(a, b):
    n = len(a)
    for i in range(n):
        for j in range(n):
            if abs(a[i][j] - b[i][j]) > 1e-9:
                return False
    return True


def main():
    matrix = input_matrix()

    print("\n입력한 행렬:")
    print_matrix(matrix)

    det = determinant(matrix)
    print(f"\n행렬식 = {det:.3f}")

    print("\n========== 행렬식으로 구한 역행렬 ==========")
    inv1 = inverse_by_det(matrix)
    if inv1 is None:
        print("행렬식이 0이므로 역행렬이 존재하지 않습니다.")
    else:
        print_matrix(inv1)

    print("\n========== 가우스-조던 소거법 과정 ==========")
    inv2 = inverse_by_gauss(matrix)

    print("\n========== 가우스-조던 소거법으로 구한 역행렬 ==========")
    if inv2 is None:
        print("역행렬이 존재하지 않습니다.")
    else:
        print_matrix(inv2)

    print()
    if inv1 is None and inv2 is None:
        print("두 방법 모두 역행렬이 존재하지 않는다는 결과가 나왔습니다.")
    elif inv1 is None or inv2 is None:
        print("두 방법의 결과가 다릅니다.")
    elif is_same(inv1, inv2):
        print("두 방법의 결과가 동일합니다.")
    else:
        print("두 방법의 결과가 다릅니다.")


if __name__ == "__main__":
    main()
