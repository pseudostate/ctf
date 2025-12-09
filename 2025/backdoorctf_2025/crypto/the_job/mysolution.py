import re
from pwn import context, remote
from sage.all import GF

def get_flag(data: str, prefix: str) -> str:
    return next(iter(re.findall(rf"{prefix}\{{.*?\}}", data)), "")

def get_lagrange_polynomial_coefficients(x_list: list[int], y_list: list[int], modulo: int) -> list[int]:
    '''
    return coefficients
        ex. x ** 2 + 2 * x + 3 -> [1, 2, 3]
    '''
    points = list(zip(x_list, y_list))
    polynomial = GF(modulo)["x"].lagrange_polynomial(points)
    return polynomial.list()[::-1]

def make_y_list(count_4_list: list[int], count_3_list: list[int]) -> list[int]:
    y_list = []
    for y in count_4_list: y_list.extend([y] * 4)
    for y in count_3_list: y_list.extend([y] * 3)
    return y_list

def solution(host: str, port: str, prefix: str) -> str | None:
    context.update({"log_level":"error"})
    k = 256             # slot count of hash table
    mod = 10 ** 9 + 7   # modulo
    n = 896             # data count = (256 / 2) * 4 + (256 / 2) * 3 = 128 * 4 + 128 * 3
    with remote(host, port) as rem:
        rem.sendlineafter(b"Press Enter to start > ", b"")
        rem.recvuntil(b"Here are the leaked numbers : ")
        leaked_numbers = list(map(int, rem.recvline().strip().decode().split(",")))
        y_list = make_y_list(list(range(k // 2)), list(range(k // 2, k)))
        coefficients = get_lagrange_polynomial_coefficients(leaked_numbers, y_list, mod)
        rem.sendlineafter(b"The degree of the polynomial should be less than the count of input numbers.\n> ", ",".join(map(str, coefficients)).encode())
        rem.sendlineafter(b"Press Enter to continue > ", b"")

        candidates = list(range(k))
        for _ in range(6):
            mid = len(candidates) // 2
            guess_list = candidates[:mid]
            not_guess_list = [i for i in range(k) if i not in guess_list]
            y_list = make_y_list(guess_list + not_guess_list[:k // 2 - len(guess_list)], not_guess_list[k // 2 - len(guess_list):])
            coefficients = get_lagrange_polynomial_coefficients(leaked_numbers, y_list, mod)
            rem.sendlineafter(b"Enter the coefficients of the polynomial.\n> ", ",".join(map(str, coefficients)).encode())
            if "Manager says the hash failed in distributing input equally." in rem.recvuntil(b"\n\n").decode():
                candidates = guess_list
            else:
                candidates = candidates[mid:]
        rem.sendlineafter(b"index : ", str(candidates[0]).encode())
        result = rem.recvall(timeout = 1).decode()
    return get_flag(result, prefix)

if __name__ == "__main__":
    host = "remote.infoseciitr.in"
    port = "4006"
    prefix = "flag"
    while (flag := solution(host, port, prefix)) == "":
        continue
    print(flag)
