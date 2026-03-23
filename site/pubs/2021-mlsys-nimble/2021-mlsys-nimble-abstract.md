Modern deep neural networks increasingly make use of features such as control
flow, dynamic data structures, and dynamic tensor shapes. Existing deep
learning systems focus on optimizing and executing static neural networks
which assume a pre-determined model architecture and input data
shapes—assumptions that are violated by dynamic neural networks. Therefore,
executing dynamic models with deep learning systems is currently both
inflexible and sub-optimal, if not impossible. Optimizing dynamic neural
networks is more challenging than static neural networks; optimizations must
consider all possible execution paths and tensor shapes. This paper proposes
Nimble, a high-performance and flexible system to optimize, compile, and
execute dynamic neural networks on multiple platforms. Nimble handles model
dynamism by introducing a dynamic type system, a set of dynamism-oriented
optimizations, and a light-weight virtual machine runtime. Our evaluation
demonstrates that Nimble outperforms existing solutions for dynamic neural
networks by up to 20x on hardware platforms including Intel CPUs, ARM CPUs,
and Nvidia GPUs.
