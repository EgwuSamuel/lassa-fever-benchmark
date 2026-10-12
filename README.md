# Lassa fever prediction using data from Nigeria’s national surveillance registry

Analysis code for the article of the same title (Egwu, Edoh, Abdulazeez and Longkang). The code
predicts laboratory confirmation among suspected Lassa fever cases from information available
before the laboratory result, and compares nine classifiers under one preprocessing and
validation protocol. It is a methodological benchmark; no new algorithm is proposed.

Everything runs on CPU with a fixed seed. One notebook produces every table and figure in the
article.

## Data

Dan-Nwafor, C. (2022). *Epidemiological data on Lassa fever in Nigeria, 2018-2021* [dataset].
Zenodo. https://doi.org/10.5281/zenodo.7309567 (CC BY 4.0).

The dataset is not copied into this repository. `download_data.py` fetches it from Zenodo, and the
notebook downloads it automatically if it is missing.

## How to run

```bash
pip install -r requirements.txt
```

```bash
python download_data.py
```

```bash
python -m nbconvert --to notebook --execute lassa_fever_benchmark.ipynb --output lassa_fever_benchmark.ipynb --ExecutePreprocessor.timeout=14400
```

The full run takes about 45 minutes on a four-core laptop. Results were produced with Python
3.14.2, scikit-learn 1.9.0, imbalanced-learn 0.14.2,
XGBoost 3.3.0 and SHAP 0.52.0 (`requirements.txt` pins all versions). Other
versions may change values in the third decimal place. Two full runs on the same machine agreed
to within 0.00002 on every value, and exactly at the three decimal places reported; the last
digits can vary because the random-forest models are fitted in parallel.

## What the notebook does

| Section | Content | Main outputs |
|---|---|---|
| 2-5 | Load data, define the outcome, exclude variables not available before the laboratory result, build 51 predictors | `excluded_variables.csv` |
| 6 | Stratified 80:20 split | |
| 7 | Missing-data audit: Yes / No / "Unknown" / blank for every predictor | `missing_data_audit.csv`, `missing_data_summary.csv` |
| 8 | Cohort description | `cohort_characteristics.csv` |
| 9 | Descriptive association (ANOVA F, chi-square, mutual information), training set only | `association_training_set.csv` |
| 10 | Nine models in one pipeline (imputation, scaling, one-hot encoding, SMOTE inside folds); hyperparameter record | `hyperparameters.csv`, `hyperparameters_full.json` |
| 11 | Stratified five-fold cross-validation with t-based 95% confidence intervals | `cv_results.csv`, `cv_fold_scores.csv` |
| 12 | Held-out test set, all metrics for all nine models, bootstrap confidence intervals, paired differences | `test_results.csv`, `test_differences_vs_selected_model.csv` |
| 13 | Calibration and decision threshold of the selected model (threshold chosen in cross-validation) | `calibration_selected_model.csv`, `threshold_analysis_selected_model.csv` |
| 14 | Coefficients and SHAP values of the logistic regression | `logistic_regression_coefficients.csv`, `shap_logistic_regression_by_variable.csv` |
| 15 | Permutation importance on the test set; XGBoost SHAP as a secondary check; rank agreement | `permutation_importance_test_set.csv`, `importance_rankings.csv` |
| 16 | Five ways of handling missing data, all nine models | `missingness_sensitivity.csv` |
| 17 | Subgroup discrimination by sex and state | `subgroup_auc.csv` |

Tables are written to `outputs/` and figures to `figures/`.

## Main results

9 classifiers, 20,027 suspected cases, 15.8% laboratory-confirmed. Cross-validation
(CV) is five-fold in the training set; the test set has 4,006 cases. Threshold metrics use 0.5.

| Model | CV balanced accuracy | CV F1 | CV ROC-AUC | Test balanced accuracy | Test recall | Test F1 | Test ROC-AUC | Test average precision |
|---|---|---|---|---|---|---|---|---|
| Logistic regression | 0.652 | 0.377 | 0.704 | 0.639 | 0.576 | 0.364 | 0.699 | 0.359 |
| Linear SVM | 0.650 | 0.375 | 0.702 | 0.641 | 0.581 | 0.366 | 0.698 | 0.359 |
| Soft voting | 0.614 | 0.358 | 0.719 | 0.608 | 0.282 | 0.346 | 0.709 | 0.376 |
| k-nearest neighbours | 0.607 | 0.330 | 0.633 | 0.596 | 0.470 | 0.318 | 0.622 | 0.225 |
| Histogram gradient boosting | 0.590 | 0.305 | 0.703 | 0.574 | 0.177 | 0.265 | 0.692 | 0.357 |
| Stacking | 0.588 | 0.304 | 0.703 | 0.590 | 0.266 | 0.308 | 0.695 | 0.289 |
| Multilayer perceptron | 0.586 | 0.304 | 0.608 | 0.576 | 0.350 | 0.290 | 0.612 | 0.296 |
| XGBoost | 0.575 | 0.268 | 0.698 | 0.570 | 0.163 | 0.254 | 0.683 | 0.357 |
| Random forest | 0.575 | 0.275 | 0.691 | 0.575 | 0.226 | 0.278 | 0.682 | 0.271 |

Logistic regression was selected in advance by cross-validated F1 score and balanced accuracy.
Soft voting had the highest test ROC-AUC and average precision; the difference from logistic
regression was not statistically distinguishable.

Sensitivity of the logistic regression to the handling of missing data:

| Analysis | CV ROC-AUC | Test ROC-AUC |
|---|---|---|
| A. Primary (imputation only) | 0.704 | 0.699 |
| B. Missingness indicators added | 0.711 | 0.703 |
| C. High-missingness predictors excluded | 0.695 | 0.685 |
| D. Unknown kept apart from blank | 0.711 | 0.702 |
| E. Missingness indicators only | 0.587 | 0.580 |

## Licence

Code: MIT (see `LICENSE`). Data: CC BY 4.0, Nigeria Centre for Disease Control (see the Zenodo
record).

## Citation

If you use this code, please cite the article (details will be added on publication) and the
dataset above.
