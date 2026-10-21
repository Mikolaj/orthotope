-- The boxed, Storable and Unboxed lists of one size, which OPSB, OPSS and
-- OPSU name, each made by dynamic-ops.inc at its kind.

#define ARR B
#define IARR IB
#define CONV S
#define CR RB
#define CS SB
#define BOXED
#define OPS OPSB
#include "dynamic-ops.inc"
#undef OPS
#undef BOXED
#undef CS
#undef CR
#undef CONV
#undef IARR
#undef ARR

#define ARR S
#define IARR IS
#define CONV B
#define STORABLE
#define CR RS
#define CS SS
#define OPS OPSS
#include "dynamic-ops.inc"
#undef OPS
#undef CS
#undef CR
#undef STORABLE
#undef CONV
#undef IARR
#undef ARR

#define ARR U
#define IARR IU
#define CONV B
#define OPS OPSU
#include "dynamic-ops.inc"
#undef OPS
#undef CONV
#undef IARR
#undef ARR
