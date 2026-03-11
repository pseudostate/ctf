// --- fixed utilities (as requested) ---
function hex(val){ return "0x" + val.toString(16); }
let sbxMemView = new Sandbox.MemoryView(0, 0x100000000);
let dv = new DataView(sbxMemView);
let addrOf = (o) => Sandbox.getAddressOf(o);
let readHeap4 = (offset) => dv.getUint32(offset, true);

const arg = (this.arguments && this.arguments[0]) ?? "0";
const USER = Number(arg);

let target = [USER];

let target_addr   = addrOf(target);
let elements_addr = readHeap4(target_addr + 0x8);
let smi_raw       = readHeap4(elements_addr + 0x7);

if (smi_raw === 0x7FFFFFFE){
        const flag = read('./flag.txt');
        print(flag);
}
else print("no-match");