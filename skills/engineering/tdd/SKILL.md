---
name: tdd
description: Drive an implementation test-first so that the resulting tests have neither gaps nor redundant duplicates. Use once what to build is settled and code is about to be written — a new feature, a bug fix, a change to existing behavior — even when the user does not mention TDD, tests, or red-green-refactor. Not for settling requirements that are still open.
---

Implement test-first: work out what the implementation must satisfy, satisfy it one failing test at a time, and keep the resulting set of tests free of both gaps and redundant duplicates.

Before writing any code, work out the conditions the implementation must satisfy. Take them from whatever defines the intended behavior — a specification where one exists, otherwise the request itself and the observable behavior of the surrounding code — rather than from the implementation you have in mind. Distinguish the classes of input and state that the behavior treats differently, the boundaries between them, and the combinations of conditions that lead to different results. Investigate what is available first, and ask the user only when a distinction cannot be placed without their answer, one question at a time, waiting for each answer. Ambiguity that changes no condition is not worth a question.

Present the conditions before writing code and continue without waiting for approval, so the user can intervene while the tests are still unwritten. Keep them in the conversation; do not write them to a file.

Then take one condition at a time: write a test that fails for it, confirm it fails for the reason expected, and write only the code needed to pass it. Once it passes, improve the code and the tests without changing any behavior a test can observe, and leave them passing before starting the next condition.

Keep the set free of gaps and duplicates as it grows. A gap is a distinguished class, boundary, or combination that no test exercises. A duplicate is a test that reveals nothing the existing tests would not. When implementing exposes a distinction the conditions missed, revise the conditions, say what changed, and cover it.

Derive every assertion from the intended behavior and from what is observable through the interface under test. A test that reaches into internal structure, or whose expected value is recomputed the way the implementation computes it, cannot disagree with the code and does not belong in the set.

Stop and explain when the work cannot proceed test-first: the behavior is not observable through any interface a test can reach, no test infrastructure exists and establishing it is a larger decision than the work at hand, or a distinction remains unresolved after asking.

Do not add tests no condition calls for, weaken a test to make it pass, or leave a known gap uncovered without saying so.
