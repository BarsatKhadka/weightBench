What we are investigating (NEURIPS WORKSHOP AS TARGET) 
Weight-space structure and behavioral benchmarks describe fine-tuned models from different angles. We believe the combination tells us more than either alone. We will demonstrate this on fine-tuned LLMs, in two settings: within a single base model, and across two base models.

The within-model setting (Experiment 1). One base model. A population of LoRAs trained at fixed parameterization across multiple tasks and seeds. Each LoRA is a point in the same parameter space. Each LoRA has a benchmark score vector. We study the geometry of the population and how it relates to behavioral signal.

The cross-model setting (Experiment 2). Two base models. Same task families fine-tuned on each. The question becomes whether models with similar benchmark scores have similar or different internal structure. The cross-model story is what makes the work compelling beyond methodology — it gestures at the real question of whether behavioral evaluation hides mechanism differences.


The components you'll build, regardless of specifics

A LoRA training pipeline. Whatever tasks you pick, you'll need to train many LoRAs at fixed configuration. This is infrastructure.(Lets see if theres better ways to do this) 

A benchmark evaluation pipeline. Score every LoRA on a battery. Collect into a behavioral signal matrix.

A weight-space representation. Some way to extract a comparable representation from each LoRA. Could be raw $\Delta W$, could be a learned encoding, could be functional probes, could be something else , we decide later. We will iterate.

Analysis tooling. Distance computations, visualizations, statistical tests. Standard stuff but you build it once.

A predictive demonstration. Some downstream task where you show combined signal beats single-signal at predicting it. Could be merging compatibility, transfer prediction, OOD generalization, capability decomposition — you'll pick based on what the data suggests.



The two signals and how they interact

For every LoRA you have:



A weight-space coordinate (some representation of the parameters).

A behavioral coordinate (its benchmark score vector).

The whole project is studying the joint structure. Are the two coordinate systems redundant or complementary? Where do they agree, where do they disagree, and does the disagreement carry useful information?

You'll explore many ways to extract and compare weight-space signal. Raw distances, symmetry-aware distances, functional probes, decompositions, learned encoders. The right method emerges from contact with the data.



What changes between the two experiments

Experiment 1 is methodology validation. You establish that the dual-signal framing produces useful findings within a controlled setting. You don't have to solve cross-architecture comparison. You demonstrate the principle.

Experiment 2 is the harder, more interesting claim. Two architectures, same tasks, comparable benchmark scores — do their adaptations differ structurally? This requires solving (or working around) cross-architecture comparison. The methodology choice for cross-model — direct weight comparison, relational geometry, behavioral fingerprinting, or something else — you'll figure out as you go.



The shape of the paper

Three parts:


Methodology for extracting and combining weight-space and behavioral signals from fine-tuned LLM populations.

Within-model demonstration: dual signal carries information benchmark-only doesn't, proven via downstream prediction.

Cross-model finding: similar benchmark scores can mask structurally different adaptations.

If the cross-model work doesn't pan out cleanly, the within-model work alone is publishable. The cross-model work is upside.



What you're committing to

The framing is fixed: weight space and benchmarks as combined signals, in fine-tuned LLMs, demonstrated within-model first and cross-model second. Everything else — datasets, exact tasks, methods for weight-space comparison, the specific predictive demonstration — you'll figure out through contact with the substrate. The framing is the commitment. The methods are the research.



What I'd flag

Three things I think you'll have to decide as you go, but shouldn't pre-commit on:

The unit of weight-space analysis. Raw $\Delta W$? Layer-wise statistics? Functional probes? Some learned encoding? Different choices will reveal different things. You'll likely try multiple.

The cross-model methodology. The hardest open question in your project. There's no obvious right answer; you'll experiment.

The downstream demonstration. Merging is the natural choice but not the only one. The data may suggest a better one.

