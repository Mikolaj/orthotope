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

- Bugfixes, stricter checks of arguments, normalize copying an array out of a larger vector, a default for vFromListN, rotate in DynamicU, a boxed outer array in RankedU and ShapedU ravel and unravel, fewer constraints on iota, Ranked normalize and RankedS.foldrA, and the new internal operations normalizeT, readRangeT and dropBroadcastT
- convertE's Left messages name convert, as in "convert: rank mismatch"; allSameA of a broadcast NaN is False, and of a boxed broadcast of an undefined element fails, as allSame of its list does; and iota converts each index to the element type rather than counting in that type, so for Word8 past 255 it gives as many elements as its shape, wrapped, and for Float past 2^24 the nearest value to each index

#### 0.2.0.0

- The NFData instance of Shaped arrays and the Convert instances between Shaped arrays need a Shape constraint on the shape, which breaks the API, as does 0.1.9.0's boxed outer array in RankedU and ShapedU ravel and unravel
- sumA, productA, maximumA and minimumA fold more views in the order of their vector, a reversed view among them, so floating-point results can differ: a sum or a product in rounding and overflow, a maximum or a minimum where an element is NaN
- rnf of a boxed array forces only the elements of the view, and convert converts only the part of the vector a view reads
- concatOuter, ravel, rerank, rerank2, rotate and pad, where they concatenate one part, as concatOuter of one array does, use that part's vector uncopied, which, as a view's, can be a slice of a longer vector and keep it alive
- On arrays of differing shapes, the errors of ravel, rerank and rerank2 name the first array's shape and the first that differs
- reduce, anyA, allA, toList, foldrA, traverseA and convert to boxed of Storable arrays hand on each element read and forced to weak head normal form, where vector-0.13.2.0 leaves a thunk holding the vector; mapA and the zips of Storable and Unboxed arrays, and toList, foldrA and traverseA of Unboxed arrays on a view that no slice serves, do the same, where they handed on a thunk holding the vector, and on such a view those of boxed arrays hand on the element stored, where a thunk of the read stood
- Speedups of the conversions of views to vectors and lists, of pad, of == and compare, of the reductions, of ravel and rerank, of the zips and rerank2, of mapA, reshape, rotate and concatOuter of Storable and Unboxed arrays, and of anyA, allA, traverseA and convert of Storable arrays, of traverseA on a view that no slice serves, of generate and of iota, fewer constraints on Eq and Ord of the generic arrays, reduce of a boxed array forcing its initial value when the result array is forced, the new Vector methods vFillStrided, vConcatN, vConcatPadN, vWithElem, vGenerate', vZipWithStrided, vZipWith3Strided, vZipWith4Strided and vZipWith5Strided, with defaults, and the new internal operations routeT, convertT and rnfViewT
