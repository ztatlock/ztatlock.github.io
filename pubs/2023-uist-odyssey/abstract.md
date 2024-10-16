In recent years, researchers have proposed a number of automated tools to
identify and improve floating-point rounding error in mathematical expressions.
However, users struggle to effectively apply these tools. In this paper, we
work with novices, experts, and tool developers to investigate user needs
during the expression rewriting process. We find that users follow an iterative
design process. They want to compare expressions on multiple input ranges,
integrate and guide various rewriting tools, and understand where errors come
from. We organize this investigation’s results into a three-stage workflow and
implement that workflow in a new, extensible workbench dubbed Odyssey. Odyssey
enables users to: (1) diagnose problems in an expression, (2) generate
solutions automatically or by hand, and (3) tune their results.  Odyssey tracks
a working set of expressions and turns a state-of-the-art automated tool
“inside out,” giving the user access to internal heuristics, algorithms, and
functionality. In a user study, Odyssey enabled five expert numerical analysts
to solve challenging rewriting problems where state-of-the-art automated tools
fail. In particular, the experts unanimously praised Odyssey’s novel support
for interactive range modification and local error visualization.

