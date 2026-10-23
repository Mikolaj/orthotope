-- The boxed, Storable and Unboxed lists of one size, which OPSB, OPSS and
-- OPSU name, each made by the family's ops file, FAMILY_OPS, at its kind, with
-- CD, CR and CS the kind's Dynamic, Ranked and Shaped modules at the boxed and
-- Storable kinds; OPSB, OPSS and OPSU are undefined after them.

#define ARR B
#define IARR IB
#define CONV S
#define CD DB
#define CR RB
#define CS SB
#define BOXED
#define OPS OPSB
#include FAMILY_OPS
#undef OPS
#undef BOXED
#undef CS
#undef CR
#undef CD
#undef CONV
#undef IARR
#undef ARR

#define ARR S
#define IARR IS
#define CONV B
#define STORABLE
#define CD DS
#define CR RS
#define CS SS
#define OPS OPSS
#include FAMILY_OPS
#undef OPS
#undef CS
#undef CR
#undef CD
#undef STORABLE
#undef CONV
#undef IARR
#undef ARR

#define ARR U
#define IARR IU
#define CONV B
#define OPS OPSU
#include FAMILY_OPS
#undef OPS
#undef CONV
#undef IARR
#undef ARR

#undef OPSU
#undef OPSS
#undef OPSB
