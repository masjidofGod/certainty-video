# Variant and workflow comparison

Read this file when ranking takes, comparing prompt revisions, or choosing quality/speed workflows.

## Comparison design [QC-17]

- Use the same shot contract, fixtures, rubric and evidence scope.
- Blind variant labels and generation order when practical; allow ties.
- Inspect every complete clip before pairwise preference.
- Record platform/model/version, prompt/reference/parameter differences, seed when documented, and actual duration/spec.
- Treat same-seed runs as only approximately comparable where officially supported; never assume deterministic equality.
- Compare variants at the same quality tier, or declare the tier difference and exclude the dimensions that tier cannot settle. [QC-26]
- Keep failed, missing, corrupt, moderated and unevaluable outputs in denominators according to a declared rule.

## Scoring order

1. Rights/safety/delivery and required-beat hard gates.
2. Correct entity/reference fidelity and prompt adherence.
3. Intra-shot temporal/anatomy/physics/camera/audio quality.
4. Cross-shot continuity and neighbor cut.
5. Editorial usability and human fix burden.
6. Aesthetic preference only after the above.

A variant that is attractive but uses the wrong identity or omits an end state cannot beat a correct variant on overall approval.

## Pairwise record

```text
Comparison ID:
Evidence scope and sampling:
Hard-gate results A / B:
Prompt adherence A / B:
Continuity A / B:
Temporal/anatomy/physics A / B:
Camera/acting/audio/text A / B:
Editorial usability A / B:
Preference: A / tie / B
Direct evidence and timecodes:
Unknowns:
Expected repair time/cost:
Decision and route:
```

Do not grade by fixed headings, regex, keywords, verbosity, or whether a model parrots the rubric. Grade the actual decisions and production artifact.

## Workflow comparison

For quality-max, speed-with-floor and hybrid, first apply common quality floors. Then compare:

- first-pass approval;
- retries (median/distribution/P90);
- usable seconds/hour;
- cost per approved second;
- artifact rate and continuity;
- human prep/review/correction time;
- waste and queue time;
- quality vector for adherence, identity, stability, motion, camera, sound and editorial use.

Do not compress to a single weighted score before checking floors. A workflow is Pareto-dominant only if it is no worse on all required dimensions and better on at least one. Otherwise multiple modes may remain rational choices.

Report conclusions only for the actual suite, model ID, platform, date, quality floor, reviewers and budget. Without controlled paid tests, describe the modes as policies, not measured winners.

## Reviewer independence

The generator/author does not approve its own final take. Preserve reviewer role, conflicts, evidence and adjudication. Automated metrics can prioritize review but never replace semantic judgment of story, identity, physics, audio or edit usability.
