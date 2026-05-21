-- SPDX-License-Identifier: MIT
-- README MADD2 example: 1 + 2 -> 3 in c (needs macro expansion by bas)

01:
  madd2 a, b
  sto c
  hlt

a:
  num 1
b:
  num 1 + 1
c:
  num 0
tmp:
  num 0
