Satisfiability Modulo Theory (SMT) solvers and equality saturation engines
must generate proof certificates from e-graph-based congruence closure
procedures to enable verification and conflict clause generation. Smaller
proof certificates speed up these activities. Though the problem of generating
proofs of minimal size is known to be NP-complete, existing proof minimization
algorithms for congruence closure generate unnecessarily large proofs and
introduce asymptotic overhead over the core congruence closure procedure. In
this paper, we introduce an O(n^5^) time algorithm which generates optimal
proofs under a new relaxed "proof tree size" metric that directly bounds proof
size. We then relax this approach further to a practical O(n\ log(n)) greedy
algorithm which generates small proofs with no asymptotic overhead. We
implemented our techniques in the egg equality saturation toolkit, yielding
the first certifying equality saturation engine. We show that our greedy
approach in egg quickly generates substantially smaller proofs than the
state-of-the-art Z3 SMT solver on a corpus of 3760 benchmarks.
