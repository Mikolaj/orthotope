-- The boxed, Storable and Unboxed lists of one size, which OPSB, OPSS and
-- OPSU name, each made by shaped-ops.inc at its kind.

#define ARR B
#define IARR IB
#define CONV S
#define CD DB
#define CR RB
#define BOXED
#define OPS OPSB
#include "shaped-ops.inc"
#undef OPS
#undef BOXED
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
#define OPS OPSS
#include "shaped-ops.inc"
#undef OPS
#undef CD
#undef STORABLE
#undef CONV
#undef IARR
#undef ARR

#define ARR U
#define IARR IU
#define CONV B
#define OPS OPSU
#include "shaped-ops.inc"
#undef OPS
#undef CONV
#undef IARR
#undef ARR
