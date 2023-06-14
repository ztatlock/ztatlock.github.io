Precision tuning and rewriting can improve both the accuracy and speed of
floating point expressions, yet these techniques are typically applied
separately. This paper explores how finer-grained interleaving of precision
tuning and rewriting can help automatically generate a richer set of
Pareto-optimal accuracy versus speed trade-offs.

We introduce Pherbie (Pareto Herbie), a tool providing both precision tuning
and rewriting, and evaluate interleaving these two strategies at different
granularities. Our results demonstrate that finer-grained interleavings improve
both the Pareto curve of candidate implementations and overall optimization
time. On a popular set of tests from the FPBench suite, Pherbie finds both
implementations that are significantly more accurate for a given cost and
significantly faster for a given accuracy bound compared to baselines using
precision tuning and rewriting alone or in sequence.
