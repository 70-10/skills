---
name: investigate
description: Use when the answer already exists in primary sources — what the code does, what the specification says, why an observed phenomenon happens — and must be established from them before answering or acting. Establish the root cause or the actual behavior with evidence, separating observation from inference.
---

Establish what is actually true about an identified subject before answering, changing, or building on it. The subject already exists — code that runs, a specification that is written, a phenomenon that occurs — so the answer is recoverable from primary sources rather than reached by judgment or produced by an experiment.

Separate the investigation from the response. Identify the primary sources that bear on the question — implementation, specifications, design documents, logs, measurements — and answer from what they contain rather than from what they are expected to contain. Where a source cannot be reached, say so and state how its absence limits the answer.

Distinguish observation from inference. An observation is what a source states or what a measurement shows, and anyone can re-check it; an inference is an interpretation, an attribution of intent, or a conclusion drawn from observations. Give load-bearing observations a source that can be re-checked, and state which premises were assumed without confirmation rather than letting them pass as established.

When a phenomenon appears confined to one condition or one target, establish how the thing is operated, where it is deployed, and what is already known to go wrong before forming any hypothesis, because missing any of these corrupts the hypotheses themselves. Treat the apparent confinement as the product of what was observed and what is internally true. Hold at least one hypothesis of each kind: the condition itself is at fault, or the fault is widespread and only that condition reaches it. Decide which difference between observations would separate them before observing anything, since observing a single target can only eliminate one side.

Stop when primary sources settle the question. When they cannot settle it, stop once the surviving explanations are stated together with the next observation that would separate them. Present what was established with its evidence, what remains assumed, and what the evidence does not support.

Do not propose or apply a fix, explore the codebase exhaustively, write the findings up as a specification file, or produce an implementation specification.
