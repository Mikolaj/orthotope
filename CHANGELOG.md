## Changes

#### 0.1.0.0

- Initial version

#### 0.1.0.1

- Relax base library constraints

#### 0.1.1.0

- Remove toArrayG function and add some documentation

#### 0.1.8.0

- Various bugfixes, speedups and the new internal operations toVectorListT and toUnorderedVectorListT

#### 0.1.9.0

- Bugfixes, stricter checks of arguments, normalize copying an array out of a larger vector, a default for vFromListN, a boxed outer array in RankedU and ShapedU ravel and unravel, fewer constraints on iota, pad, reshape, index, Ranked normalize, RankedS.foldrA and ShapedG's Show instance, documented failures and uniformly worded errors, with HasCallStack on the operations checking their arguments, and the new internal operations normalizeT, readRangeT and dropBroadcastT
- convertE's Left messages name convert, as in "convert: rank mismatch"; allSameA of a broadcast NaN is False, and of a boxed broadcast of an undefined element fails, as allSame of its list does; and iota converts each index to the element type rather than counting in that type, so for Word8 past 255 it gives as many elements as its shape, wrapped, and for Float past 2^24 the nearest value to each index
- mapA applies its function only to elements of the array, where it mapped the whole vector whenever that was no longer than the array, as the zips did only where one array's vector held a single element; that makes it faster on broadcasts and overlapping windows of part of a longer vector, and slower where a view that does not read every element of one part of its vector has, without its broadcast dimensions, more elements than the vector, as a window over a stride can, since mapA now builds that view and so runs the function once per element of it rather than of the vector; mapA and == analyse the strides on every call, which makes them several times slower on small arrays, as == is at any size on two arrays of one layout that read all of their vectors, to be improved in a later version

#### 0.2.0.0

- The NFData instance of Shaped arrays and the Convert instances between Shaped arrays need a Shape constraint on the shape, which breaks the API, as do the Shape constraint window of Shaped arrays needs on its result, the KnownNat constraint ShapedG's stretchOuter needs on the extent it stretches to, and 0.1.9.0's boxed outer array in RankedU and ShapedU ravel and unravel
- Operations some array modules had, added to their siblings that lacked them
- sumA, productA, maximumA, minimumA, anyA, allA and allSameA fold more views in the order of their vector, a reversed view among them, so floating-point results can differ: a sum or a product in rounding and overflow, a maximum or a minimum where an element is NaN and in which of 0.0 and -0.0 it returns where both occur; and on those views anyA, allA and allSameA of a boxed array can throw on an undefined element where the row-major walk returned, and return where it threw, so allSameA, which folded every view row-major, as allSame of its list does, can now disagree with it on a transposed or reversed view, while anyA and allA already folded a transposed view in the order of its vector
- rnf of a boxed array forces only the elements of the view, and convert converts only the part of the vector a view reads
- concatOuter, ravel, rerank, rerank2, rotate and pad, where they concatenate one part, as concatOuter of one array does, use that part's vector uncopied, which, as a view's, can be a slice of a longer vector and keep it alive
- On arrays of differing shapes, the errors of ravel, rerank and rerank2 name the first array's shape and the first that differs
- reduce, anyA, allA, toList, foldrA, traverseA and convert to boxed of Storable arrays hand on each element read and forced to weak head normal form, where vector-0.13.2.0 leaves a thunk holding the vector; mapA and the zips of Storable arrays do the same, where they handed on a thunk holding the vector; mapA and the zips of Unboxed arrays, and toList, foldrA and traverseA of Unboxed arrays on a view that no slice serves, hand on the element as vector's unsafeIndexM reads it, evaluated for a primitive representation and as stored for vector's DoNotUnboxLazy, where they handed on a thunk holding the vector; and on such a view toList, foldrA and traverseA of boxed arrays hand on the element stored, where a thunk of the read stood
- Speedups of the conversions of views to vectors and lists, of pad, of mapA on small arrays, of ==, of compare of views not read in the order of their vectors, of the reductions, of ravel and rerank, of the zips and rerank2, of mapA, reshape, rotate and concatOuter of Storable and Unboxed arrays, and of anyA, allA, traverseA and convert of Storable arrays, of traverseA on a view that no slice serves, of generate and of iota, which now stores each element evaluated, so that it fails where fromInteger fails on an index, fewer constraints on Eq and Ord of the generic arrays, reduce of a boxed array forcing its initial value when the result array is forced, the new Vector methods vUnsafeIndex, vUnsafeSlice, vUnsafeFillStrided, vUnsafeConcatN, vUnsafeWithElem and vGenerate', with defaults, and the new internal operations routeT, convertT, rnfViewT and fillStrided, which checks the contract of vUnsafeFillStrided before calling it; the vector instances of vUnsafeIndex, vUnsafeSlice, vUnsafeFillStrided and vUnsafeWithElem, and the Storable and Unboxed ones of vUnsafeConcatN, do not check bounds, and the operations now read and slice views through them, so a call that breaks a method's contract, or a view built by hand that reaches outside its vector, reads outside the vectors or writes outside the result, which can corrupt memory, unless vector's unsafe checks are on
- permute, of Data.Array.Internal, is strict in the spine of its result and in every element it selects, where it was map (xs !!)
- The Shape class documents the shapes it rejects: those any inner part of which, the dimensions from some one inward, has more elements than an Int counts, even where an outer extent of 0 leaves the shape none, as '[0, 4611686018427387904, 4]; transpose, stride and rev of Shaped arrays no longer apply that check to their type-level permutation, strides or dimensions, which a 22-axis permutation starting at 0 failed; convertE to a Shaped array of a rejected shape returns Left "convert: bad shape" rather than throwing; and the new Shape method natsP and functions listP and validShape read a type-level list without the check and say whether a shape passes it; transpose, pad, rotate, stretchOuter and window of Shaped arrays reject such a shape as they make it, as stretch and broadcast do; and the Shaped operations fail on a type-level number past maxBound, where iota, iterateN, index, concatOuter, pad, rotate and slice took it modulo 2^64
