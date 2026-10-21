-- The boxed, Storable and Unboxed lists of one size, which OPSB, OPSS and
-- OPSU name, each made by ranked-ops.inc at its kind.

#define ARR B
#define IARR IB
#define CONV S
#define CD DB
#define CS SB
#define BOXED
#define OPS OPSB
#include "ranked-ops.inc"
#undef OPS
#undef BOXED
#undef CS
#undef CD
#undef CONV
#undef IARR
#undef ARR

#define ARR S
#define IARR IS
#define CONV B
#define STORABLE
#define CS SS
#define OPS OPSS
#include "ranked-ops.inc"
#undef OPS
#undef CS
#undef STORABLE
#undef CONV
#undef IARR
#undef ARR

#define ARR U
#define IARR IU
#define CONV B
#define OPS OPSU
#include "ranked-ops.inc"
#undef OPS
#undef CONV
#undef IARR
#undef ARR
