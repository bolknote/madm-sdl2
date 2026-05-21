; Retrocomputing SE answer — Joseph Adams / gobaby factor 2^18
; https://retrocomputing.stackexchange.com/a/2869
; Run with: gobaby -t -l 27 -p=f examples/factor.asm
; Catalog: programs/gobaby_factor.store (= ccs_factorct bytes)

00  JMP  0
01  LDN 24
02  STO 26
03  LDN 26
04  STO 27
05  LDN 23
06  SUB 27
07  CMP
08  JRP 20
09  SUB 26
10  STO 25
11  LDN 25
12  CMP
13  STP
14  LDN 26
15  SUB 21
16  STO 27
17  LDN 27
18  STO 26
19  JMP 22
20  NUM -3
21  NUM  1
22  NUM  4
23  NUM -262144
24  NUM 262143
25  NUM  0
26  NUM  0
27  NUM  0
28  NUM  0
29  NUM  0
30  NUM  0
31  NUM  0
