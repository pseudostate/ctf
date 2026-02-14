from pwn import context, remote
import numpy as np

def solution(host: str, port: str) -> str:
    context.update({"log_level":"error"})
    coefficients_list = []
    values = []
    with remote(host, port) as rem:
        data = rem.recvuntil(b"\nSolve the system of equations to find the flag!").decode()
        lines = data.strip().split("\n")
        for line in lines:
            if " = " not in line:
                continue
            terms, value = line.split(" = ")
            values.append(int(value))
            coefficients = []
            for term in terms.split(" + "):
                coefficient = int(term.split("*")[0])
                coefficients.append(coefficient)
            coefficients_list.append(coefficients)
    return "".join([chr(int(round(c))) for c in np.linalg.solve(np.array(coefficients_list), np.array(values))])

if __name__ == "__main__":
    host = "cramer.ctf.pascalctf.it"
    port = "5002"
    print(f"pascalCTF{{{solution(host, port)}}}")
    