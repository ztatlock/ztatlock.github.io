Tensor kernels in machine learning (ML) often correspond to pure mathematical
expressions, making term rewriting an attractive strategy for optimization and
mapping to specialized hardware accelerators. However, existing ML intermediate
representations (IRs) tend to either be *pure but high-level*, making low-level
rewrites to hardware targets inexpressible, or *low-level but impure*,
hampering the use of term rewriting altogether.

This paper introduces Glenside, a pure IR whose core abstraction — the access
pattern — enables low-level, layout-aware, hardware-centric program rewrites.
We demonstrate how term rewriting in Glenside can be used to map program
fragments to hardware accelerator invocations and automatically discover
classic data layout transformations like `im2col`. Glenside establishes a new
foundation for exploring further term rewriting techniques in optimizing
low-level tensor programs.
