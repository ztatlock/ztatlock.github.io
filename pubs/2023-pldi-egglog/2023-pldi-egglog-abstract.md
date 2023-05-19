We present egglog, a fixpoint reasoning system that unifies Datalog and
equality saturation (EqSat). Like Datalog, it supports efficient incremental
execution, cooperating analyses, and lattice-based reasoning. Like EqSat, it
supports term rewriting, efficient congruence closure, and extraction of
optimized terms.

We identify two recent applications -- a unification-based pointer analysis in
Datalog and an EqSat-based floating-point term rewriter -- that have been
hampered by features missing from Datalog but found in EqSat or vice-versa. We
evaluate egglog by reimplementing those projects in egglog. The resulting
systems in egglog are faster, simpler, and fix bugs found in the original
systems.
