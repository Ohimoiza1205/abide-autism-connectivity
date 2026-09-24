# Research Plan
## Autism Spectrum Classification from Resting-State fMRI Functional Connectivity

**Semester:** Fall 2026  
**Project Period:** September – December 2026  
**Dataset:** ABIDE I  
**Primary Language:** Python

---

## 1. Project Goal

This project investigates whether resting-state functional connectivity can
be used to distinguish participants with Autism Spectrum Disorder (ASD) from
typically developing controls.

The primary goal is to compare several machine learning approaches using the
same functional-connectivity representation and determine how model choice
affects classification performance.

A secondary goal is to move beyond classification accuracy and investigate
which functional connections consistently contribute to the predictions and
whether those patterns are consistent with findings reported in ASD research.

---

## 2. Research Questions

### RQ1: Model Performance
How do different machine learning algorithms compare when classifying ASD
versus typically developing controls using resting-state functional connectivity?

Initial models:

- Logistic Regression
- Support Vector Machine (SVM)
- Random Forest
- Gradient Boosting / XGBoost

### RQ2: Cross-Site Generalization
How well do the models generalize to participants collected at imaging sites
that were not represented during training?

### RQ3: Connectivity Interpretation
Which functional connections consistently contribute to ASD classification,
and what brain regions or functional networks do those connections involve?

---

## 3. Data

The project uses the Autism Brain Imaging Data Exchange (ABIDE I).

ABIDE contains resting-state fMRI and phenotypic information collected across
multiple imaging sites.

### Phenotypic / QC Data

The downloaded ABIDE phenotypic and quality-control spreadsheet contains
information including:

- Diagnosis
- Participant ID
- Imaging site
- Age
- Sex
- IQ measures
- Functional MRI quality-control measures
- File identifiers linking participants to preprocessed imaging data

These variables will be used for participant selection, labels, quality
control, cohort description, and later analysis of possible confounding
variables.

### Imaging Representation

Initial preprocessing configuration:

- Pipeline: C-PAC
- Atlas: CC200
- Derivative: ROI time series
- Strategy: filtered, no global signal regression (`filt_noglobal`)

The CC200 atlas represents the brain using approximately 200 regions of
interest (ROIs).

---

# 4. Work Completed

## Week 1 — Research Direction and Background
**Early September 2026**

- Began investigating possible fMRI-based research questions.
- Reviewed the difference between task-based and resting-state fMRI.
- Identified ABIDE as a suitable source of resting-state fMRI data for ASD.
- Discussed using machine learning to analyze neuroimaging data.
- Narrowed the broad topic toward ASD classification using functional
  connectivity.
- Identified the need for both a computational question and an interpretable
  biological component.

### Outcome

Initial direction established:

> Compare machine learning approaches for ASD classification using
> resting-state fMRI while investigating what information the models learn
> from functional connectivity.

---

## Week 2 — Dataset and Method Selection
**Mid-September 2026**

- Investigated the structure of the ABIDE dataset.
- Identified phenotypic variables including diagnosis, age, sex, IQ, and
  acquisition site.
- Investigated preprocessed ABIDE derivatives to avoid beginning with raw
  fMRI volumes.
- Selected C-PAC as the initial preprocessing pipeline.
- Selected the CC200 atlas as the initial brain parcellation.
- Chose ROI time-series data as the starting imaging representation.
- Developed the initial analysis pipeline:

  `ROI time series -> functional connectivity -> machine learning`

### Outcome

The project was reduced from a broad fMRI classification idea to a specific,
testable workflow based on resting-state functional connectivity.

---

## Week 3 — Initial Data Acquisition and Proof of Concept
**September 24, 2026**

### Phenotypic Data

- Downloaded the ABIDE I phenotypic/QC spreadsheet.
- Inspected participant IDs, diagnosis labels, site information, demographic
  variables, IQ measures, and quality-control fields.
- Identified `FILE_ID` as the link between participant metadata and
  preprocessed imaging derivatives.

### Imaging Data

Downloaded the first CC200 ROI time-series file:

`Pitt_0050003_rois_cc200.1D`

The participant's data contained:

- 196 time points
- 200 brain regions

### Functional Connectivity

Loaded the ROI time series using Python and NumPy.

Calculated Pearson correlation between every pair of brain regions.

This produced a:

`200 x 200 functional connectivity matrix`

The matrix represents how similarly the resting-state signals of pairs of
brain regions vary over time.

### Visualization

Generated the first functional-connectivity heatmap.

This visualization is a proof of concept rather than a biological result.
A single participant cannot establish an ASD-related connectivity pattern.

### Feature Representation

Because the connectivity matrix is symmetric and its diagonal contains
self-correlations, only the upper triangle is required.

For 200 regions:

`200 x 199 / 2 = 19,900`

Therefore, each participant can initially be represented using 19,900 unique
functional-connectivity features.

### Reproducibility

- Created a Git repository for the project.
- Created the GitHub repository:
  `abide-autism-connectivity`
- Added the initial proof-of-concept Python code.
- Excluded participant data from version control using `.gitignore`.

### Outcome

The complete single-participant transformation has been demonstrated:

`ABIDE ROI time series -> functional connectivity matrix -> connectivity features`

The next milestone is scaling this process from one participant to a usable
ASD/control cohort.

---

# 5. Remaining Semester Plan

## Week 4 — Small Cohort Pipeline
**Late September / Early October**

### Goal
Make the pipeline work reliably for multiple participants before attempting
the full dataset.

### Tasks

- Select a small balanced sample of ASD and control participants.
- Download their CC200 ROI time-series files automatically.
- Match each imaging file to its diagnosis using `FILE_ID`.
- Convert every participant into a functional-connectivity matrix.
- Extract the 19,900 unique connections for each participant.
- Combine participants into a single feature matrix.

Expected structure:

`X.shape = (number_of_participants, 19900)`

`y.shape = (number_of_participants,)`

where:

- `X` contains functional-connectivity features.
- `y` contains ASD/control labels.

### Deliverable

A working end-to-end pipeline for a small cohort.

---

## Week 5 — Cohort Definition and Quality Control
**Early October**

### Goal
Define exactly which ABIDE participants will be included in the study.

### Tasks

- Identify participants with available CC200 derivatives.
- Review ABIDE functional quality-control measures.
- Define exclusion criteria before model training.
- Examine missing phenotypic values.
- Examine head-motion measures.
- Determine how age, sex, IQ, and site will be handled.
- Record ASD/control counts after exclusions.
- Document participant counts by imaging site.
- Check class balance.

### Important Question

Determine whether phenotypic variables will be:

1. used only for cohort description/confound analysis, or
2. included as additional model features in a separate experiment.

The primary imaging experiment should remain clearly distinguishable from
models that include demographic information.

### Deliverable

A documented final cohort and inclusion/exclusion procedure.

---

## Week 6 — Full Connectivity Dataset
**Mid-October**

### Goal
Generate the complete machine-learning dataset.

### Tasks

- Automate CC200 ROI downloads for qualifying participants.
- Calculate one connectivity matrix per participant.
- Extract upper-triangle connectivity features.
- Detect missing, malformed, or unusable files.
- Store participant IDs, labels, and site information alongside features.
- Verify that feature ordering is identical for every participant.
- Generate basic summary statistics.

### Deliverable

Final analysis-ready dataset:

`participants x 19,900 connectivity features`

with corresponding diagnosis and site labels.

---

## Week 7 — Logistic Regression Baseline
**Mid/Late October**

### Goal
Establish the first classification baseline.

### Tasks

- Create a reproducible train/evaluation pipeline.
- Standardize features using training data only.
- Prevent information leakage between training and evaluation data.
- Train Logistic Regression.
- Evaluate using cross-validation.
- Record:

  - Balanced accuracy
  - ROC-AUC
  - Sensitivity
  - Specificity
  - Confusion matrix

### Why Logistic Regression First?

It provides a relatively simple and interpretable baseline before testing
more complex models.

### Deliverable

First complete ASD-versus-control classification results.

---

## Week 8 — Model Comparison
**Late October / Early November**

### Goal
Answer the primary research question.

### Models

- Logistic Regression
- SVM
- Random Forest
- Gradient Boosting / XGBoost

### Tasks

- Use the same participant cohort for every model.
- Use the same evaluation splits where appropriate.
- Perform reasonable hyperparameter tuning without using the test data.
- Record the same metrics for every model.
- Compare performance and variability across folds.

### Deliverable

A model-comparison table and initial performance figures.

---

## Week 9 — High-Dimensional Feature Analysis
**Early November**

### Goal
Investigate the effect of having many more connectivity features than
participants.

The initial representation contains 19,900 features per participant, making
overfitting an important concern.

### Tasks

Investigate appropriate approaches such as:

- regularization
- feature selection
- dimensionality reduction

Any feature-selection or dimensionality-reduction step must be fitted using
training data only.

Compare results against the original baseline rather than assuming that
feature reduction improves performance.

### Deliverable

Documented comparison of the selected feature strategy against the initial
baseline.

---

## Week 10 — Cross-Site Generalization
**Mid-November**

### Goal
Determine whether classification performance generalizes across acquisition
sites.

### Method

Use site-aware evaluation, such as leave-one-site-out validation:

`Train: multiple ABIDE sites`

`Test: one unseen ABIDE site`

Repeat across eligible sites.

### Questions

- Does performance decrease on unseen sites?
- Are some sites substantially harder to generalize to?
- Are apparent classification results partly associated with acquisition site?

### Deliverable

Cross-site performance results and comparison with standard cross-validation.

---

## Week 11 — Connectivity Interpretation
**Mid/Late November**

### Goal
Determine what connectivity information contributes to classification.

### Tasks

- Extract interpretable feature importance or model coefficients where
  appropriate.
- Map important feature indices back to pairs of CC200 regions.
- Examine whether important connections are stable across folds/models.
- Avoid interpreting features that appear important only in a single split.
- Group connections by brain regions or functional networks where possible.

### Deliverable

A ranked set of stable candidate connections/networks for further
interpretation.

---

## Week 12 — Biological Context
**Late November**

### Goal
Connect computational results to existing ASD research.

### Tasks

- Review literature concerning resting-state functional connectivity in ASD.
- Investigate brain regions/networks identified by the models.
- Compare observed patterns with previously reported findings.
- Identify agreements, contradictions, and limitations.
- Avoid interpreting predictive association as biological causation.

### Deliverable

Initial biological interpretation of the computational findings.

---

## Final Week — Results and Research Summary
**Late November – First Week of December**

### Goal
Produce a complete semester research result.

### Tasks

- Re-run the final analysis reproducibly.
- Verify figures and metrics.
- Organize final results.
- Document methodological limitations.
- Clean and document the GitHub repository.
- Prepare final figures and tables.
- Write the semester research summary/presentation.

### Expected Final Outputs

1. Documented ABIDE cohort
2. Reproducible functional-connectivity pipeline
3. Logistic Regression baseline
4. Comparison of multiple ML algorithms
5. Standard cross-validation results
6. Cross-site generalization results
7. Connectivity interpretation
8. Biological literature comparison
9. Final figures/tables
10. Reproducible GitHub repository

---

# 6. Experimental Pipeline

The planned end-to-end workflow is:

ABIDE I
    |
    v
Phenotypic + QC data
    |
    v
Participant selection
    |
    v
C-PAC CC200 ROI time series
    |
    v
Functional connectivity
(Pearson correlation)
    |
    v
19,900 unique connectivity features per participant
    |
    v
Quality control + preprocessing
    |
    v
Machine learning
    |
    +-- Logistic Regression
    +-- SVM
    +-- Random Forest
    +-- Gradient Boosting / XGBoost
    |
    v
Model evaluation
    |
    +-- Standard cross-validation
    +-- Cross-site validation
    |
    v
Interpretation
    |
    +-- Important connections
    +-- Stability across experiments
    +-- Brain regions/networks
    |
    v
Comparison with ASD literature

---

# 7. Scope

## In Scope

- ABIDE I
- Resting-state fMRI
- Functional connectivity
- CC200 parcellation
- ASD versus typically developing control classification
- Traditional supervised machine learning
- Cross-site generalization
- Model interpretation
- Biological contextualization of connectivity findings

## Out of Scope for the Initial Semester Project

Unless results or available time justify expansion:

- Raw fMRI preprocessing
- Deep neural networks
- Graph neural networks
- Large language models
- Training on raw 4D MRI volumes
- Combining multiple neuroimaging modalities
- ASD subtype discovery
- Clinical diagnosis claims
- Causal claims about autism

Keeping these outside the initial scope makes completion by December realistic.

---

# 8. Current Status

As of September 24, 2026:

- [x] Select broad research area
- [x] Identify ABIDE
- [x] Select resting-state fMRI
- [x] Select C-PAC preprocessing
- [x] Select CC200 ROI representation
- [x] Download phenotypic/QC data
- [x] Download first participant ROI time series
- [x] Load ROI time series in Python
- [x] Generate 200 x 200 connectivity matrix
- [x] Visualize connectivity matrix
- [x] Establish 19,900-feature representation
- [x] Create GitHub repository
- [ ] Confirm final research questions with supervisor
- [ ] Process small ASD/control cohort
- [ ] Define QC and inclusion criteria
- [ ] Build full connectivity dataset
- [ ] Establish Logistic Regression baseline
- [ ] Compare ML algorithms
- [ ] Evaluate cross-site generalization
- [ ] Identify stable connectivity features
- [ ] Interpret relevant regions/networks
- [ ] Prepare final semester results

---

# 9. Immediate Next Milestone

The next technical milestone is:

> Build a small, balanced ASD/control cohort and automatically transform each
> participant's CC200 ROI time series into the same 19,900-feature
> representation.

The pipeline will not be scaled to the complete dataset until the research
questions, cohort strategy, and quality-control approach have been reviewed
with the research supervisor.