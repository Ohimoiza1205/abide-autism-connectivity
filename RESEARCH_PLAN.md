# Fall 2026 Research Plan

## Autism Spectrum Classification Using Resting State fMRI Functional Connectivity

**Semester:** Fall 2026  
**Project Period:** September to December 2026  
**Dataset:** ABIDE I  
**Primary Language:** Python  

---

## 1. Project Overview

This project investigates whether patterns of resting state functional connectivity can be used to distinguish participants with Autism Spectrum Disorder (ASD) from typically developing controls.

The main computational goal is to compare several machine learning approaches using the same functional connectivity data and determine how model choice affects classification performance.

The project will also examine what information the models are using. Rather than ending with classification accuracy, I want to identify connections that consistently contribute to the predictions and investigate whether the brain regions or networks involved are consistent with findings in existing ASD research.

The project is intended as a computational study of group differences and predictive patterns. It is not intended to develop a clinical diagnostic tool.

---

## 2. Research Questions

### RQ1: Model Performance

How do different machine learning algorithms compare when classifying ASD versus typically developing controls using resting state functional connectivity?

The initial models I plan to investigate are:

* Logistic Regression
* Support Vector Machine
* Random Forest
* Gradient Boosting or XGBoost

### RQ2: Generalization Across Sites

How well do the models perform when evaluated on participants from an ABIDE imaging site that was not represented during training?

### RQ3: Connectivity Interpretation

Which functional connections consistently contribute to classification, and what brain regions or functional networks do those connections involve?

The first research question is the primary focus. The second and third questions will be investigated after a reliable classification pipeline has been established.

---

## 3. Dataset

The project uses data from the Autism Brain Imaging Data Exchange, specifically ABIDE I.

ABIDE contains resting state fMRI data and phenotypic information from participants with ASD and typically developing controls collected across multiple imaging sites.

### Phenotypic and Quality Control Data

I downloaded the ABIDE phenotypic and quality control spreadsheet. It contains information including:

* Diagnosis
* Participant ID
* Imaging site
* Age
* Sex
* IQ measures
* Functional MRI quality measures
* File identifiers that connect participants to their preprocessed imaging data

These variables will be used to identify participants, obtain ASD and control labels, describe the study cohort, apply quality criteria, and investigate possible sources of variation in the data.

### Imaging Data

For the initial analysis, I selected the following ABIDE configuration:

* Preprocessing pipeline: C PAC
* Brain atlas: CC200
* Imaging derivative: ROI time series
* Processing strategy: filtered data without global signal regression

The CC200 atlas divides the brain into approximately 200 regions of interest. For each participant, the ROI file contains the resting state signal measured from each region across the duration of the scan.

Starting from these regional signals allows the project to focus on functional connectivity without performing raw fMRI preprocessing as part of the current semester work.

---

# 4. Progress to Date

## Early September: Research Direction and Background

The project began with a broader interest in applying machine learning to fMRI data. I first needed to understand what information fMRI provides and what type of question would be realistic for an undergraduate research project.

During this stage, I:

* Reviewed the basic distinction between task based and resting state fMRI
* Learned how the BOLD signal is used in fMRI
* Considered possible sources of public neuroimaging data
* Investigated OpenNeuro and ABIDE
* Identified ABIDE as a useful source for studying ASD with resting state fMRI
* Discussed using machine learning to compare different approaches to analyzing neuroimaging data
* Narrowed the project toward functional connectivity rather than raw imaging data
* Identified the need for both a computational question and a biological interpretation component

One important question that came from these discussions was how to make the project useful beyond simply reporting which algorithm has the highest classification score.

This led to the current direction:

> Compare machine learning approaches for ASD classification using resting state functional connectivity while also investigating what connectivity information contributes to the models' predictions.

### Outcome

The broad research area was narrowed from general fMRI analysis to ASD classification using resting state functional connectivity.

---

## Mid September: Dataset and Method Selection

After selecting ABIDE, I investigated how its imaging and phenotypic data are organized.

I identified diagnosis, age, sex, IQ, acquisition site, and imaging quality measures in the phenotypic data.

I also investigated the preprocessed ABIDE derivatives so that the project would not require starting with raw fMRI volumes.

For the initial analysis, I selected:

* C PAC preprocessing
* The CC200 brain atlas
* ROI time series as the imaging representation

This produced the initial analysis pipeline:

`ROI time series -> functional connectivity -> machine learning`

The purpose of this stage was to move from the broad idea of classifying ASD from fMRI to a specific representation that could realistically be used for a semester research project.

### Outcome

The project was narrowed to a specific and testable workflow based on resting state functional connectivity.

---

## September 24: Initial Data Acquisition

I downloaded the ABIDE I phenotypic and quality control spreadsheet and inspected its structure.

The spreadsheet provides participant information including diagnosis, site, demographic information, IQ measures, and functional imaging quality measures.

I also identified `FILE_ID` as the field that connects a participant in the spreadsheet to the corresponding preprocessed imaging file.

This established the connection between the two main parts of the project:

`Participant information + imaging data`

I then downloaded the first CC200 ROI time series:

`Pitt_0050003_rois_cc200.1D`

This participant's file contains:

* 196 time points
* 200 brain regions

This gave me the first real imaging derived data for testing the proposed analysis.

### Outcome

The phenotypic data and imaging data were successfully identified and connected through the ABIDE participant identifiers.

---

## September 24: Functional Connectivity Proof of Concept

I built a small Python proof of concept to determine whether I could transform the ABIDE ROI data into a representation suitable for machine learning.

For the first participant, I loaded the 196 by 200 ROI time series using NumPy.

The 196 rows represent measurements across time during the resting state scan. The 200 columns represent the brain regions defined by the CC200 atlas.

The goal is not to classify the participant directly from these raw time series. Instead, I want to measure how the signals from different brain regions relate to one another.

I calculated the Pearson correlation between every pair of brain regions.

This produced a:

`200 x 200 functional connectivity matrix`

Each value in this matrix represents how similarly the resting state signals of two brain regions changed over time.

A positive correlation means that the signals from two regions tended to vary in the same direction. A value near zero indicates little linear relationship between the signals. A negative correlation means that the signals tended to vary in opposite directions.

I generated a heatmap of this matrix to visually confirm that the transformation worked.

The heatmap itself is not a research result. It represents only one participant and therefore cannot be used to make conclusions about ASD. Its purpose was to confirm that I could successfully move from the ABIDE ROI data to a functional connectivity representation.

### Feature Representation

The connectivity matrix contains 40,000 cells, but not all of them provide unique information.

The diagonal compares each brain region with itself, so those values are always one.

The matrix is also symmetric. The connection between Region A and Region B is the same as the connection between Region B and Region A.

Therefore, only one half of the matrix is required after removing the diagonal.

For 200 regions:

`200 x 199 / 2 = 19,900`

This gives 19,900 unique region to region connections for each participant.

Each participant can therefore initially be represented as:

`1 participant -> 19,900 connectivity measurements`

These measurements will become the input features for the machine learning models.

### Current Data Transformation

The current working transformation is:

```text
ABIDE participant
        |
        v
CC200 ROI time series
        |
        v
200 regional signals across time
        |
        v
Pearson correlation between region pairs
        |
        v
200 x 200 functional connectivity matrix
        |
        v
Remove diagonal and duplicate connections
        |
        v
19,900 unique connectivity measurements
```

### Reproducibility

I also created a Git repository and GitHub repository for the project:

`abide-autism-connectivity`

The repository currently contains the initial Python proof of concept and project documentation.

Participant imaging data is excluded from version control so that the repository contains the analysis code rather than copies of the ABIDE data.

### Outcome

The complete transformation for one participant has been demonstrated:

`ABIDE ROI time series -> functional connectivity -> machine learning features`

This is a proof of concept for the data processing approach. It is not yet a classification result.

---

# 5. Plan for the Rest of the Semester

The remaining work is organized around research milestones rather than strict weekly requirements. The dates below are targets and may change depending on what is learned during each stage.

---

## Late September to Early October: Build the Dataset Pipeline

### Goal

Extend the current proof of concept from one participant to multiple ASD and control participants.

The first objective is not to process the entire ABIDE dataset. I will first use a small balanced sample to make sure the pipeline works consistently.

### Small Cohort Test

The initial test will use approximately:

* 5 participants with ASD
* 5 typically developing controls

Where possible, the first small sample will be selected in a way that reduces unnecessary variation while the pipeline itself is being tested.

For each participant, the pipeline should:

1. Match the participant to the phenotypic data
2. Obtain the diagnosis
3. Record the imaging site
4. Locate or download the corresponding CC200 ROI file
5. Load the ROI time series
6. Calculate the functional connectivity matrix
7. Extract the 19,900 unique connections
8. Store the connectivity values with the participant information

The immediate technical target is to produce:

`X.shape = (number of participants, 19900)`

and:

`y.shape = (number of participants,)`

where:

* `X` contains functional connectivity measurements
* `y` contains ASD or control labels

For the first 10 participant test, the expected structure would therefore be:

`X.shape = (10, 19900)`

`y.shape = (10,)`

The small cohort is intended only to verify the data pipeline. It will not be used to draw scientific conclusions about ASD.

### Expected Outcome

A reproducible script that can transform multiple ABIDE participants into the same functional connectivity representation.

---

## Early to Mid October: Define the Study Cohort

### Goal

Determine exactly which ABIDE participants should be included in the main analysis.

The complete ABIDE dataset should not be passed directly into the machine learning models without first understanding the quality and structure of the available data.

This stage will include:

* Identifying participants with available CC200 data
* Reviewing the available functional MRI quality measures
* Examining head motion measures
* Identifying missing or incomplete imaging files
* Identifying missing phenotypic information
* Examining participant counts by diagnosis
* Examining participant counts by imaging site
* Checking the balance between ASD and control participants
* Examining age distributions
* Examining sex distributions
* Reviewing the availability of IQ measures

The inclusion and exclusion decisions will be documented before training the main models.

### Phenotypic Variables

An additional question at this stage is how variables such as age, sex, IQ, and site should be handled.

The primary research question concerns functional connectivity.

Therefore, the main imaging experiment should remain distinguishable from experiments that include demographic information.

Phenotypic variables may initially be used for:

* Cohort description
* Quality checks
* Investigation of possible confounding factors
* Site analysis

A separate experiment may later investigate whether adding phenotypic variables changes classification performance.

### Expected Outcome

A documented study cohort with clear inclusion and exclusion criteria and a summary of the participants included in the analysis.

---

## Mid October: Construct the Main Connectivity Dataset

### Goal

Scale the working pipeline to the qualifying participants.

Once the small sample pipeline and cohort criteria are established, the processing step will be automated for the selected participants.

For each participant, the pipeline will:

1. Read the participant information
2. Obtain the corresponding CC200 ROI time series
3. Verify that the file can be processed
4. Calculate the functional connectivity matrix
5. Extract the same 19,900 connections in the same order
6. Store the participant ID
7. Store the diagnosis
8. Store the imaging site
9. Store the connectivity features

The processing code will also identify missing, malformed, or unusable files rather than silently including them.

The feature ordering must remain identical for every participant. For example, if the first feature represents the connection between Regions 1 and 2 for one participant, it must represent the same connection for every other participant.

At the end of this stage, the main dataset should have the form:

`participants x 19,900 connectivity features`

with corresponding diagnosis and site information.

### Expected Outcome

A reproducible analysis dataset that can be used consistently across all machine learning experiments.

---

## Mid to Late October: Establish the Classification Baseline

### Goal

Determine whether the functional connectivity representation contains useful predictive information under the selected experimental setup.

The first model will be Logistic Regression.

Logistic Regression provides a relatively simple starting point and gives the project a baseline before introducing more complex models.

### Initial Evaluation

The model will be evaluated using measures such as:

* Balanced accuracy
* ROC AUC
* Sensitivity
* Specificity
* Confusion matrix

Accuracy alone will not be treated as sufficient because the number of ASD and control participants may not be perfectly balanced.

### Preventing Information Leakage

Any preprocessing step that learns information from the dataset must be fitted using training data only.

For example, if the features are standardized, the mean and standard deviation must be calculated from the training participants and then applied to the evaluation participants.

The evaluation procedure will be designed before comparing multiple models so that every model is tested under comparable conditions.

### Expected Outcome

The first complete ASD versus control classification result and a baseline against which later models can be compared.

---

## Late October to Early November: Compare Machine Learning Models

### Goal

Address the primary research question by comparing multiple algorithms using the same functional connectivity representation.

The initial models are:

* Logistic Regression
* Support Vector Machine
* Random Forest
* Gradient Boosting or XGBoost

Each model will use the same participant cohort.

Where appropriate, the same evaluation splits will be used so that differences in performance are more likely to reflect the models rather than different train and evaluation samples.

The comparison will consider:

* Balanced accuracy
* ROC AUC
* Sensitivity
* Specificity
* Variation across evaluation splits

The goal is not simply to report which model produces the largest number.

The analysis should also consider:

* How stable is the model?
* Does performance change substantially across splits?
* Are ASD and control participants treated differently by the classifier?
* Does a more complex model provide a meaningful improvement over the baseline?

### Expected Outcome

A model comparison using a consistent dataset and evaluation procedure.

---

## Early to Mid November: Investigate Model Reliability

### Goal

Determine whether the classification results are likely to generalize rather than simply fitting the available participants.

The initial connectivity representation contains 19,900 measurements per participant.

The number of features may therefore be much larger than the number of participants.

This creates an important risk of overfitting.

Depending on what is observed in the initial model results, I will investigate methods such as:

* Regularization
* Feature selection
* Dimensionality reduction

These methods will not automatically be added simply because they are available.

Instead, they will be used if the initial experiments show a reason to investigate the high dimensional feature space.

Any feature selection or dimensionality reduction method that learns from the data must be fitted using the training participants only.

The results will be compared with the original baseline so that any improvement or loss in performance can be measured.

### Expected Outcome

A better understanding of whether the models are learning patterns that generalize or are primarily fitting noise in the training data.

---

## November: Evaluate Generalization Across Imaging Sites

### Goal

Determine whether classification performance generalizes beyond the imaging sites represented during training.

ABIDE combines data collected at multiple institutions.

These sites can differ in:

* Scanner equipment
* Imaging parameters
* Participant populations
* Data collection procedures
* Sample size

A model could therefore appear to perform well while partly learning differences associated with imaging sites.

After the main classification pipeline is working, I plan to compare the standard evaluation with a site based evaluation.

A possible approach is:

```text
Training:
Participants from multiple ABIDE sites

Testing:
Participants from one site not used during training
```

The held out site can then be changed and the experiment repeated for other eligible sites.

The main questions will be:

* How much does performance change on an unseen site?
* Are results consistent across sites?
* Are some sites substantially more difficult than others?
* Could part of the classification performance be associated with site differences?

This analysis will depend on the number of usable ASD and control participants available at each site. Sites with very small samples may not support meaningful individual evaluation.

### Expected Outcome

An assessment of whether the classification results generalize to participants collected outside the sites represented during model training.

---

## Mid to Late November: Interpret Connectivity Patterns

### Goal

Investigate what functional connectivity information contributes to the models' predictions.

A classification score tells us whether a model can distinguish the groups under the selected experimental setup, but it does not by itself explain what the model learned.

For models that provide interpretable coefficients or feature importance, I will map influential features back to the pairs of CC200 regions they represent.

For example:

```text
Feature index
      |
      v
CC200 Region A <-> CC200 Region B
      |
      v
Strength and direction of model contribution
```

The analysis will focus on connections that are reasonably stable across evaluation runs rather than connections that appear important in only one split.

Questions at this stage include:

* Which connections repeatedly contribute to classification?
* Which brain regions are involved?
* Are multiple important connections concentrated within particular functional networks?
* Do different models identify similar connectivity patterns?
* Do the important features remain similar across evaluation splits?

The goal is not to claim that a connection causes ASD.

The goal is to identify connectivity patterns associated with the model's ability to distinguish the two groups.

### Expected Outcome

A set of candidate connectivity patterns that can be investigated in the context of existing ASD research.

---

## Late November: Connect the Results to ASD Research

### Goal

Determine whether the computational findings have a meaningful relationship to what is already known about ASD and functional connectivity.

Once candidate regions and connections have been identified, I will review relevant literature on resting state functional connectivity in ASD.

The analysis will ask:

* Have these regions or networks been discussed previously in ASD research?
* Have previous studies reported connectivity differences involving these systems?
* Are the direction and nature of the observed patterns consistent with previous findings?
* Are there conflicting findings in the literature?
* Could the patterns observed in this project be influenced by site, motion, age, or other factors?

This stage is important because the project should not end with a statement such as:

`Model A achieved a higher score than Model B.`

The larger goal is to understand what information in the functional connectivity data contributed to the classification and whether those patterns have a reasonable biological context.

Predictive importance will not be treated as evidence of biological causation.

### Expected Outcome

An interpretation of the computational results in the context of existing ASD functional connectivity research.

---

## Late November to First Week of December: Final Analysis and Research Summary

### Goal

Produce a complete and reproducible semester research result.

During the final stage, I will:

* Reproduce the selected final experiments
* Verify reported metrics
* Review the evaluation procedure for possible leakage or inconsistencies
* Organize model comparison results
* Organize site based results if completed
* Prepare final figures
* Prepare final tables
* Document limitations
* Document important methodological decisions
* Clean the project repository
* Update the README and research documentation
* Prepare the final semester research summary or presentation

### Expected Final Outputs

The target outputs for the semester are:

1. A documented ABIDE participant cohort
2. A reproducible functional connectivity processing pipeline
3. A dataset containing connectivity features and participant labels
4. A Logistic Regression baseline
5. A comparison of several machine learning approaches
6. A consistent model evaluation procedure
7. An analysis of generalization across imaging sites, if supported by the available cohort
8. An analysis of stable connectivity patterns
9. A comparison of those patterns with existing ASD literature
10. Final figures and tables
11. A documented GitHub repository
12. A final research summary or presentation

The first five outputs represent the core project. The later interpretation and site analyses depend on successful completion of the main classification pipeline and the quality of the available data.

---

# 6. Experimental Workflow

The current planned workflow is:

```text
ABIDE I
    |
    v
Phenotypic and quality control data
    |
    v
Participant selection
    |
    v
C PAC CC200 ROI time series
    |
    v
Functional connectivity using Pearson correlation
    |
    v
19,900 unique connectivity measurements per participant
    |
    v
Machine learning dataset
    |
    v
Logistic Regression baseline
    |
    v
Model comparison
    |
    +--> Logistic Regression
    |
    +--> Support Vector Machine
    |
    +--> Random Forest
    |
    +--> Gradient Boosting or XGBoost
    |
    v
Model evaluation
    |
    +--> Standard participant based evaluation
    |
    +--> Site based evaluation
    |
    v
Connectivity interpretation
    |
    +--> Important connections
    |
    +--> Stability across experiments
    |
    +--> Brain regions and networks
    |
    v
Comparison with ASD literature
```

This workflow is the current plan rather than a fixed requirement.

The later stages may be adjusted if the quality control analysis, cohort structure, or initial modeling results show that a different approach is needed.

---

# 7. What Each Stage Is Intended to Answer

## Data Preparation

**Question:** Can the ABIDE data be transformed consistently into a usable functional connectivity representation?

This is the stage currently being tested.

---

## Baseline Classification

**Question:** Does the selected functional connectivity representation contain enough predictive information to distinguish ASD and control participants better than would be expected from a poorly performing classifier?

This establishes whether there is a useful signal to investigate further.

---

## Model Comparison

**Question:** How does the choice of machine learning algorithm affect classification performance when the underlying data and evaluation procedure remain consistent?

This addresses the primary research question.

---

## Site Evaluation

**Question:** Does the observed performance remain when the model encounters participants from an imaging site that was not represented during training?

This tests whether the results generalize beyond the conditions seen during model development.

---

## Connectivity Interpretation

**Question:** Which functional connections contribute to the predictions, and are those connections stable enough to investigate further?

This moves the project beyond a simple model performance comparison.

---

## Biological Context

**Question:** Do the connectivity patterns identified by the computational analysis relate to findings already reported in ASD neuroscience research?

This connects the computational results back to the biological motivation for the project.

---

# 8. Project Scope

## Current Scope

The current semester project focuses on:

* ABIDE I
* Resting state fMRI
* Functional connectivity
* CC200 brain regions
* ASD versus typically developing control classification
* Traditional supervised machine learning
* Evaluation across imaging sites
* Interpretation of connectivity patterns
* Comparison with existing ASD literature

---

## Possible Extensions

The following are not required for the initial semester project but could be considered later if the main analysis is completed and the results justify additional work:

* Alternative brain atlases
* Alternative connectivity measures
* Site harmonization methods
* Additional feature selection approaches
* Additional machine learning algorithms
* Comparison between preprocessing strategies

These should only be added if they answer a clear question that emerges from the primary analysis.

---

## Outside the Current Scope

The following are not part of the current Fall 2026 plan:

* Raw fMRI preprocessing
* Deep neural networks
* Graph neural networks
* Large language models
* Training directly on raw 4D MRI volumes
* Combining multiple neuroimaging modalities
* ASD subtype discovery
* Clinical diagnosis claims
* Claims about biological causation

These boundaries are intended to keep the project achievable within the semester.

---

# 9. Current Status

As of September 24, 2026:

### Research Definition

* [x] Explore possible fMRI research directions
* [x] Learn the basic distinction between task based and resting state fMRI
* [x] Identify ABIDE as the primary dataset
* [x] Narrow the project to resting state functional connectivity
* [x] Define the initial machine learning comparison direction
* [ ] Confirm the final research questions and scope with the research supervisor

### Data Selection

* [x] Investigate ABIDE phenotypic data
* [x] Investigate available preprocessed imaging derivatives
* [x] Select C PAC as the initial preprocessing pipeline
* [x] Select CC200 as the initial brain atlas
* [x] Select ROI time series as the initial imaging representation
* [x] Download the ABIDE phenotypic and quality control spreadsheet
* [x] Identify `FILE_ID` as the connection between participant metadata and imaging files

### Proof of Concept

* [x] Download the first participant CC200 ROI time series
* [x] Load the ROI time series in Python
* [x] Confirm a shape of 196 time points by 200 regions for the first participant
* [x] Calculate Pearson correlations between the 200 regions
* [x] Generate a 200 by 200 functional connectivity matrix
* [x] Visualize the connectivity matrix
* [x] Establish the 19,900 unique connection representation
* [x] Confirm the proposed transformation from ROI data to machine learning features

### Project Organization

* [x] Create the local Git repository
* [x] Create the GitHub repository
* [x] Add the initial proof of concept code
* [x] Exclude participant data from version control
* [x] Document the Fall 2026 research plan

### Next Technical Work

* [ ] Select a small ASD and control sample
* [ ] Build the multiple participant processing script
* [ ] Produce the first `X` feature matrix
* [ ] Produce the corresponding `y` diagnosis vector
* [ ] Define quality and inclusion criteria
* [ ] Construct the main study cohort
* [ ] Build the complete connectivity dataset
* [ ] Establish the Logistic Regression baseline
* [ ] Compare machine learning models
* [ ] Investigate model reliability
* [ ] Evaluate generalization across imaging sites
* [ ] Identify stable connectivity patterns
* [ ] Compare findings with ASD literature
* [ ] Prepare final semester results

---

# 10. Immediate Next Milestone

The immediate technical goal is to move from the current one participant proof of concept to a small balanced sample containing participants with ASD and typically developing controls.

The first target is approximately:

```text
5 ASD participants
+
5 control participants
=
10 participant pipeline test
```

Each participant will go through the same transformation:

```text
Participant
    |
    v
CC200 ROI time series
    |
    v
Functional connectivity matrix
    |
    v
19,900 unique connectivity measurements
```

The desired result is:

```text
X.shape = (10, 19900)
y.shape = (10,)
```

This will demonstrate that the processing approach works consistently across multiple participants.

The 10 participant sample will not be treated as a scientific classification experiment. Its purpose is to test the pipeline before applying it to the main cohort.

---

# 11. Next Decision Point

Before scaling the processing pipeline to the complete qualifying ABIDE cohort, I will review three areas with the research supervisor:

### Research Scope

Confirm that the primary question should remain a comparison of machine learning approaches for ASD classification using functional connectivity.

### Cohort Strategy

Confirm how participants should be selected and whether there are specific demographic or site considerations that should be included in the study design.

### Quality Control

Confirm the quality criteria that should be applied before building the main analysis dataset.

Once these decisions are established, the project can move from the proof of concept stage into the main experimental analysis.

---

# 12. Semester Completion Target

By the first week of December, the minimum successful outcome for the project is:

> A reproducible analysis that transforms ABIDE resting state fMRI data into functional connectivity features, compares multiple machine learning approaches for ASD versus control classification, evaluates the reliability of those results, and documents what can and cannot be concluded from the analysis.

If the main pipeline and model comparison are completed early enough, the project will additionally examine:

> Whether classification performance generalizes across ABIDE imaging sites and which functional connections consistently contribute to the models' predictions.

The final interpretation will distinguish between predictive patterns and biological conclusions. A connection that contributes to classification will be treated as a candidate pattern for investigation, not evidence that the connection causes or explains ASD.