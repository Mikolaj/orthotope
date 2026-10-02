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
- Speedups of the conversions of views to vectors and lists, of == and compare, of the reductions and of mapA and the zips of Storable and Unboxed arrays, fewer constraints on Eq and Ord of the generic arrays, reduce of a boxed array forcing its initial value when the result array is forced, the new Vector method vFillStrided, with a default, and the new internal operations routeT, convertT and rnfViewT
