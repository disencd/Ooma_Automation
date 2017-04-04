#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdlib.h>
#include <strings.h>
#include <sys/mman.h>
#include <netdb.h>
#include <pthread.h>
#include <assert.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>


#define MAP_SIZE   (4096)


#define NJP 5
#define NDEV 3

typedef struct gpio {
	int     gpio;
        int     bit;
} gpio;

volatile unsigned long *(gpio_set[4]);
volatile unsigned long *(gpio_clr[4]);
volatile unsigned long *(gpio_read[4]);
volatile unsigned long *(gpio_oe[4]);
volatile void *gpio0_addr;
volatile void *gpio1_addr;
volatile void *gpio2_addr;
volatile void *gpio3_addr;
int verbose=0;
int port=888;

//	connector		0	1	2
//	JP1			PR1U2	PR1U7	PR1U0
//	JP2			PR1U3	PR1U4	PR1U5
//	JP3			PR0U0	PR1U1	PR1U6
//	JP4			PR0U3	PR0U2	PR0U5
//	JP5			PR0U6	PR0U1	PR0U4
//
//	JP1			p8.43	p8.40	p8.45
//	JP2			p8.44	p8.41	p8.42
//	JP3			p9.31	p8.46	p8.39
//	JP4			p9.28	p9.30	p9.25
//	JP5			p8.12	p9.29	p9.27
//
//	JP1			2/8	2/13	2/6
//	JP2			2/9	2/10	2/11
//	JP3			3/14	2/7	2/12
//	JP4			3/17	3/16	3/21
//	JP5			1/12	3/15	3/19
//

gpio 	jp1[] = {{2,8}, {2,13}, {2,6}};
gpio	jp2[] = {{2,9}, {2,10}, {2,11}};
gpio	jp3[] = {{3,14}, {2,7}, {2,12}};
gpio	jp4[] = {{3,17}, {3,16}, {3,21}};
gpio	jp5[] = {{1,12}, {3,15}, {3,19}};

gpio *(jp[]) = {&jp1[0], &jp2[0], &jp3[0], &jp4[0], &jp5[0]};

void
set_oe(gpio g, int val)
{
        if (val) {
                *(gpio_oe[g.gpio]) &= ~(1<<g.bit);
        } else {
                *(gpio_oe[g.gpio]) |= 1<<g.bit;
        }
}

void
set_gpio(gpio g, int val)
{
        if (val) {
                *(gpio_set[g.gpio]) = 1<<g.bit;
        } else {

                *(gpio_clr[g.gpio]) = 1<<g.bit;
        }
}


void
init()
{
	int i, j;
	int mem_fd = open("/dev/mem", O_RDWR|O_SYNC);
        void *p= mmap(0, MAP_SIZE, PROT_READ|PROT_WRITE, MAP_SHARED, mem_fd, 0x44e00000);
        *(volatile unsigned long *)(((unsigned char *)p)+0xac) = 2;
        *(volatile unsigned long *)(((unsigned char *)p)+0xb0) = 2;
        *(volatile unsigned long *)(((unsigned char *)p)+0xb4) = 2;
        *(volatile unsigned long *)(((unsigned char *)p)+0x408) = 2;
        munmap(p, 0x1000);


        gpio0_addr = mmap(0, MAP_SIZE, PROT_READ|PROT_WRITE, MAP_SHARED, mem_fd, 0x44e07000);
printf("gpio0_addr = %x\n",(unsigned )gpio0_addr);
        gpio1_addr = mmap(0, MAP_SIZE, PROT_READ|PROT_WRITE, MAP_SHARED, mem_fd, 0x4804c000);
printf("gpio1_addr = %x\n",(unsigned )gpio1_addr);
        gpio2_addr = mmap(0, MAP_SIZE, PROT_READ|PROT_WRITE, MAP_SHARED, mem_fd, 0x481ac000);
printf("gpio2_addr = %x\n",(unsigned )gpio2_addr);
        gpio3_addr = mmap(0, MAP_SIZE, PROT_READ|PROT_WRITE, MAP_SHARED, mem_fd, 0x481ae000);
printf("gpio3_addr = %x\n",(unsigned )gpio3_addr);

        gpio_set[0]  = (volatile unsigned long *)(((unsigned char *)gpio0_addr)+0x194);
        gpio_clr[0]  = (volatile unsigned long *)(((unsigned char *)gpio0_addr)+0x190);
        gpio_oe[0]   = (volatile unsigned long *)(((unsigned char *)gpio0_addr)+0x134);
        gpio_read[0] = (volatile unsigned long *)(((unsigned char *)gpio0_addr)+0x138);
        gpio_set[1]  = (volatile unsigned long *)(((unsigned char *)gpio1_addr)+0x194);
        gpio_clr[1]  = (volatile unsigned long *)(((unsigned char *)gpio1_addr)+0x190);
        gpio_oe[1]   = (volatile unsigned long *)(((unsigned char *)gpio1_addr)+0x134);
        gpio_read[1] = (volatile unsigned long *)(((unsigned char *)gpio1_addr)+0x138);
        gpio_set[2]  = (volatile unsigned long *)(((unsigned char *)gpio2_addr)+0x194);
        gpio_clr[2]  = (volatile unsigned long *)(((unsigned char *)gpio2_addr)+0x190);
        gpio_oe[2]   = (volatile unsigned long *)(((unsigned char *)gpio2_addr)+0x134);
        gpio_read[2] = (volatile unsigned long *)(((unsigned char *)gpio2_addr)+0x138);
        gpio_set[3]  = (volatile unsigned long *)(((unsigned char *)gpio3_addr)+0x194);
        gpio_clr[3]  = (volatile unsigned long *)(((unsigned char *)gpio3_addr)+0x190);
        gpio_oe[3]   = (volatile unsigned long *)(((unsigned char *)gpio3_addr)+0x134);
        gpio_read[3] = (volatile unsigned long *)(((unsigned char *)gpio3_addr)+0x138);
	
	for (i = 0; i < NJP; i++) {
		for (j = 0; j < NDEV; j++) {
			set_gpio(jp[i][j], 0);
                	set_oe(jp[i][j], 1);
		}
	}
}

void
mdelay(int t)
{
	struct timespec ts;
	ts.tv_sec = 0;
	ts.tv_nsec = t*1000000;
	while (nanosleep(&ts,&ts));
}

void
command(char *cp)
{
	int d, p;

	if (verbose)
		fprintf(stderr, "Command '%s'\n", cp);
		printf("cp - %s", cp);

	if (*cp != 'c' && *cp != 'C')
		return;
	cp++;
	while (*cp == ' ' || *cp == '\t') cp++;
	if (*cp != 'd' && *cp != 'D')
		return;
	d = 0;
	cp++;
	while (*cp >= '0' && *cp <= '9')
		d = d*10+(*cp++ - '0');
	if (d < 0 || d >= NJP)
		return;
	while (*cp != 'i' && *cp != 'I') cp++;
	p = 0;
	cp++;
	while (*cp >= '0' && *cp <= '9')
		p = p*10+(*cp++ - '0');
	if (p < 0 || p >= NDEV)
		return;
	while (*cp == ' ' || *cp == '\t') cp++;
	if (*cp == '0') {
		set_gpio(jp[d][p], 0);
	} else
	if (*cp == '1') {
		set_gpio(jp[d][p], 1);
	}
}

void *
tcp_server_thread(void *p)
{
	int fd = (int)p;
	pthread_detach(pthread_self());
	char buff[1024];
	char b[1024];
	unsigned int off;

	off = 0;
	for (;;) {
		int i, l = read(fd, b, sizeof(p));
		if (l < 0) {
			if (off) {
				buff[off] = 0;
				command(buff);
			}
			break;
		}
		for (i = 0; i < l; i++) {
			if (b[i] == '\n') {
				buff[off] = 0;
				command(buff);
				off = 0;
			} else 
			if (off < (sizeof(buff)-1)) { 
				buff[off++] = b[i];
			}
		}
	}
	close(fd);
	return 0;
}

void *
tcp_thread(void *pp)
{
	int opt, fd;
	struct sockaddr_in serveraddr;

	pthread_detach(pthread_self());
	assert((fd=socket(AF_INET, SOCK_STREAM, 0))>=0);
	opt=1;
	setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, (const void *)&opt , sizeof(int));
	bzero((char *) &serveraddr, sizeof(serveraddr));
	serveraddr.sin_family = AF_INET;
	serveraddr.sin_addr.s_addr = htonl(INADDR_ANY);
	serveraddr.sin_port = htons((unsigned short)port);
	assert(bind(fd, (struct sockaddr *) &serveraddr, sizeof(serveraddr)) >=0);
	assert(listen(fd, 5) >=0); 
	for (;;) {
		struct sockaddr_in clientaddr;
		pthread_t tid;
		socklen_t clientlen = sizeof(clientaddr);
		int newfd = accept(fd, (struct sockaddr *)&clientaddr, &clientlen);
		assert(newfd >= 0);
		pthread_create(&tid, 0, tcp_server_thread, (void *)newfd);
	}
	return 0;
}

void *
udp_thread(void *pp)
{
	int fd, opt;
	char b[1024];
	struct sockaddr_in serveraddr;


printf("start udp thread\n");
	assert((fd=socket(AF_INET, SOCK_DGRAM, 0)) >=0);
	opt = 1;
	setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, (const void *)&opt , sizeof(int));
	bzero((char *) &serveraddr, sizeof(serveraddr));
  	serveraddr.sin_family = AF_INET;
  	serveraddr.sin_addr.s_addr = htonl(INADDR_ANY);
  	serveraddr.sin_port = htons((unsigned short)port);
	assert(bind(fd, (struct sockaddr *) &serveraddr, sizeof(serveraddr))>=0);
	for (;;) {
		struct sockaddr_in clientaddr;
		socklen_t clientlen = sizeof(clientaddr);
		int l = recvfrom(fd, b, sizeof(b), 0, (struct sockaddr *) &clientaddr, &clientlen); 
printf("udp thread read %d\n", l);
		if (l <= 0)
			continue;
		if (l >= sizeof(b))
			l -= sizeof(b)-1;
		b[l] = 0;
		command(b);
	}
	close(fd);
	return 0;
}

int
main(int argc, char **argv)
{
	int test = 0;
	int v=0;
	pthread_t tid;

	init();
	if (argc > 1) {
		if (strcasecmp(argv[1], "-v") ==0) {
			verbose = 1;
			argv++;
			argc--;
		}
	}
	if (argc > 1) {
		if (strcasecmp(argv[1], "-t") ==0) {
			test = 1;
			argv++;
			argc--;
		}
	}
	if (argc > 1) {
		port = atoi(argv[1]);
	}
	if (test) 
	for (;;) {
		int i, j;

		for (i = 0; i < NJP; i++) {
			for (j = 0; j < NDEV; j++) {
				printf("Setting jp%d pin %d\n", i, j);
				set_gpio(jp[i][j], 1);
				mdelay(100);
				set_gpio(jp[i][j], 0);
			}
		}
		v=1-v;
	}
	
	pthread_create(&tid, 0, tcp_thread, 0);
	udp_thread(0);
	return 0;
}
