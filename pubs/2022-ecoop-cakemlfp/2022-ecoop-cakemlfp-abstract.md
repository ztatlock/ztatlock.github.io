Verified compilers such as CompCert and CakeML have become increasingly
realistic over the last few years, but their support for floating-point
arithmetic has thus far been limited. In particular, they lack the
“fast-math-style” optimizations that unverified mainstream compilers perform.
Supporting such optimizations in the setting of verified compilers is
challenging because these optimizations, for the most part, do not preserve the
IEEE-754 floating-point semantics. However, IEEE-754 floating-point numbers are
finite approximations of the real numbers, and we argue that any compiler
correctness result for fast-math optimizations should appeal to a real-valued
semantics rather than the rigid IEEE-754 floating-point numbers.

This paper presents RealCake, an extension of CakeML that achieves end-to-end
correctness results for fast-math-style optimized compilation of floating-point
arithmetic. This result is achieved by giving CakeML a flexible floating-point
semantics and integrating an external proof-producing accuracy analysis.
RealCake’s end-to-end theorems relate the I/O behavior of the original source
program under real-number semantics to the observable I/O behavior of the
compiler generated and fast-math-optimized machine code.
