Past work on optimizing fabrication plans given a carpentry design can provide
Pareto-optimal plans trading off between material waste, fabrication time,
precision, and other considerations. However, when developing fabrication
plans, experts rarely restrict to a single design, instead considering families
of design variations, sometimes adjusting designs to simplify fabrication.
Jointly exploring the design and fabrication plan spaces for each design is
intractable using current techniques. We present a new approach to jointly
optimize design and fabrication plans for carpentered objects. To make this
bi-level optimization tractable, we adapt recent work from program synthesis
based on equality graphs (e-graphs), which encode sets of equivalent programs.
Our insight is that subproblems within our bi-level problem share significant
substructures. By representing both designs and fabrication plans in a new bag
of parts (BOP) e-graph, we amortize the cost of optimizing design components
shared among multiple candidates. Even using BOP e-graphs, the optimization
space grows quickly in practice. Hence, we also show how a feedback-guided
search strategy dubbed Iterative Contraction and Expansion on E-graphs (ICEE)
can keep the size of the e-graph manageable and direct the search toward
promising candidates. We illustrate the advantages of our pipeline through
examples from the carpentry domain.
