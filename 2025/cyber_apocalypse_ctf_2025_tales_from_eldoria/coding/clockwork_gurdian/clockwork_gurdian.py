# 2차원 리스트에서 출발지(0,0)부터 도착지('E')까지 최소거리 계산
def bfs(map_data: list[list[int]]) -> int:
    direction = [[0, 1], [1, 0], [0, -1], [-1, 0]]
    step = [0]
    position = [0]
    passed = [0]
    while len(position) > 0:
        current_step = step.pop(0)
        current_position_data = position.pop(0)
        current_row = current_position_data // len(map_data[0])
        current_col = current_position_data % len(map_data[0])
        if map_data[current_row][current_col] == "'E'":
            return current_step
        else:
            for d in direction:
                next_row = current_row + d[0]
                next_col = current_col + d[1]
                next_position_data = next_row * len(map_data[0]) + next_col
                if 0 <= next_row < len(map_data) and 0 <= next_col < len(map_data[0]) and map_data[next_row][next_col] != '1' and next_position_data not in passed:
                    step.append(current_step + 1)
                    position.append(next_position_data)
                    passed.append(next_position_data)
    return None

def solution(map_text: str) -> int:
    map_text = map_text.strip("[]").split("], [")
    map_data = [map_line_text.split(", ") for map_line_text in map_text]
    return bfs(map_data)

if __name__=="__main__":
    parameter1 = input() # "[[0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0], [1, 0, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 1], [0, 1, 0, 1, 0, 0, 'E']]"
    print(solution(parameter1)) # 11