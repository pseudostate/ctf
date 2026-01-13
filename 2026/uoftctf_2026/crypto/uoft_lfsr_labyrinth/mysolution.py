import json
from z3 import Solver, Bool, BoolVal, And, Xor, is_true, sat
from crypto import decrypt
from filter_cipher import WG_ANF_TERMS

def eval_anf(bits, terms):
    acc = BoolVal(False)
    for mon in terms:
        prod = BoolVal(True)
        for idx in mon:
            prod = And(prod, bits[idx])
        acc = Xor(acc, prod)
    return acc

def clock(solver, state, feedback_taps, filter_taps, terms, index):
    z = eval_anf([state[i] for i in filter_taps], terms)
    fb = BoolVal(False)
    for idx in feedback_taps:
        fb = Xor(fb, state[idx])
    solver_fb = Bool(f"feedback_bit_{index}")
    solver.add(solver_fb == fb)
    state = [solver_fb] + state[:-1]
    return z, state

def solution(json_file: str) -> str:
    json_data = json.load(open(json_file))
    l = json_data["L"]
    feedback_taps = json_data["feedback_taps"]
    filter_taps = json_data["filter_taps"]
    keystream = json_data["keystream"]
    
    solver = Solver()
    initial_state = [Bool(f"s_{i}") for i in range(l)]
    current_state = list(initial_state)

    for index, keystream_bit in enumerate(keystream):
        z, current_state = clock(solver, current_state, feedback_taps, filter_taps, WG_ANF_TERMS, index)
        target = BoolVal(True) if keystream_bit == 1 else BoolVal(False)
        solver.add(z == target)

    if solver.check() == sat:
        model = solver.model()
        recovered_bits = [1 if is_true(model[s]) else 0 for s in initial_state]
        flag = decrypt(bytes.fromhex(json_data["nonce"]), bytes.fromhex(json_data["ct"]), recovered_bits).decode()
    return flag

if __name__ == "__main__":
    json_file = "challenge.json"
    print(solution(json_file))
