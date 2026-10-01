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

- Bugfixes, stricter checks of arguments, normalize copying an array out of a larger vector, a default for vFromListN, a boxed outer array in RankedU and ShapedU ravel and unravel, fewer constraints on iota, pad, reshape, stretchOuter, index, Ranked normalize, RankedS.foldrA and ShapedG's Show instance, documented failures and uniformly worded errors, with HasCallStack on the operations checking their arguments, and the new internal operations normalizeT, readRangeT and dropBroadcastT
- convertE's Left messages name convert, as in "convert: rank mismatch"; allSameA of a broadcast NaN is False, and of a boxed broadcast of an undefined element fails, as allSame of its list does; and iota converts each index to the element type rather than counting in that type, so for Word8 past 255 it gives as many elements as its shape, wrapped, and for Float past 2^24 the nearest value to each index
- mapA applies its function only to elements of the array, where it mapped the whole vector whenever that was no longer than the array, as the zips did only where one array's vector held a single element; that makes it faster on broadcasts and overlapping windows of part of a longer vector, and slower where a view that does not read every element of one part of its vector has, without its broadcast dimensions, more elements than the vector, as a window over a stride can, since mapA now builds that view and so runs the function once per element of it rather than of the vector; mapA and == analyse the strides on every call, which makes them several times slower on small arrays, as == is at any size on two arrays of one layout that read all of their vectors, to be improved in a later version
