def solution(n: int, m: int) -> str:
    result = f"{n}\n"
    total = [m] * n
    singer = 0
    for _ in range(m):
        if total[singer] >= n:
            result += f"{n} {singer + 1} 0 {singer + 1}\n"
            total[singer] -= n
            if total[singer] == 0:
                singer += 1
        elif total[singer] > 0:
            result += f"{total[singer]} {singer + 1} {n - total[singer]} {(singer + 1) % n + 1}\n"
            total[singer + 1] -= (n - total[singer])
            total[singer] = 0
            singer = (singer + 1) % n
    return result


if __name__=="__main__":
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        print(solution(n, m))


        
