<!--
Draft prose for §7 (Preliminary conclusions & future work). Anonymized,
double-blind-ready third-person prose, real citations added inline (see REFERENCES.md).

Explicitly states the two held-out results as ongoing/future work WITHOUT
claiming their findings -- see ../README.md's scope boundary. Do not add
any actual number, formula, or conclusion from either of those threads here;
if a specific figure from that work seems tempting to cite, stop and check
with Neal first.

Rough length: ~430 words, targeting the outlined 1-page budget.
-->

# 7. Preliminary conclusions and future work

A normalized, extensively-cleaned dataset spanning ten years of a
state's production risk-limiting audits facilitates the study
of several questions that were previously difficult to approach via the public record.

[TODO: discrepancies!]

The next natural goal is calculating risk levels for contests audited opportunistically.
Early analysis suggests that a significant fraction of all the contests actually met
the risk limit. But a rigorous analysis is complicated.
Calculating risk levels for opportunistic contests which cover multiple counties requires a defensible
risk-calculation methodology since the sampling rate is not uniform across
all the counties.
In addition, the current sampling method draws each contest's
audit sample by reducing the seed, a shared per-election random value, against that
contest's own ballot-population size. When two contests' population sizes
share a common factor, this construction means that the samples in the
two counties are not independent. Any auditing method that requires
independence would need to properly take the correlations into account.
Note that this doesn't affect any of the risk calculations that the audit
guarantees for targeted contests.

An excellent way to solve that problem is to adopt Rivest's
"consistent sampling" method \cite{rivest2018consistent}, which derives
each ballot's sampling priority from the ballot's own identity rather than
a population-size-dependent reduction. It would also be a valuable
upgrade for Colorado's audit software since it
supports efficient sampling across overlapping contests and
supports the many benefits of style-based sampling more generally
\cite{glazer2021style}.
