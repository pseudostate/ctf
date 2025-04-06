import os, struct, z3

def get_data(file_name: str) -> list[float]:
    data = []
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name), "r") as f:
        data = [float(d) for d in f.read().split()]
    return data

def random_predict(sequence: list[float]) -> float:
    predict_value = None
    sequence = sequence[::-1]
    solver = z3.Solver()
    se_state0, se_state1 = z3.BitVecs("se_state0 se_state1", 64)
    for i in range(len(sequence)):
        se_s1 = se_state0
        se_s0 = se_state1
        se_state0 = se_s0
        se_s1 ^= se_s1 << 23
        se_s1 ^= z3.LShR(se_s1, 17)
        se_s1 ^= se_s0
        se_s1 ^= z3.LShR(se_s0, 26)
        se_state1 = se_s1
        float_64 = struct.pack("d", sequence[i] + 1)
        u_long_long_64 = struct.unpack("<Q", float_64)[0]
        mantissa = u_long_long_64 & ((1 << 52) - 1)
        solver.add(int(mantissa) == z3.LShR(se_state0, 12))
    if solver.check() == z3.sat:
        model = solver.model()
        states = {}
        for state in model.decls():
            states[state.__str__()] = model[state]
        state0 = states["se_state0"].as_long()
        u_long_long_64 = (state0 >> 12) | 0x3FF0000000000000
        float_64 = struct.pack("<Q", u_long_long_64)
        next_sequence = struct.unpack("d", float_64)[0]
        next_sequence -= 1
        predict_value = next_sequence
    return predict_value

def solution(file_name: str) -> str:
    flag = ""
    data = get_data(file_name)
    start_index = 0
    end_index = start_index + 24
    bits = ""
    while end_index <= len(data):
        sub_data = data[start_index:end_index]
        sample = sub_data[:-1]
        answer = sub_data[-1]
        predict = random_predict(sample)
        if predict is not None and abs(predict - answer) < 0.0001: # can predict = using node
            bits += "1"
        else: # can't predict = using d8
            bits += "0"
        if end_index % (24 * 8) == 0:
            flag += chr(int(bits, 2))
            bits = ""
        start_index += 24
        end_index += 24
    return flag

if __name__ == "__main__":
    file_name = "output.txt"
    print(solution(file_name))
    