#!/usr/bin/env python3
"""Server-side ordinal-logistic sensitivity analysis for the frozen phenotype.

This script does not refit the imaging phenotype. It reuses the fixed
three-cluster solution, then fits proportional-odds models for CAS and
threshold-specific binary logistic models as an exploratory check of the
proportional-odds assumption.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import chi2
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from statsmodels.miscmodels.ordinal_model import OrderedModel


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--features", type=Path, required=True)
    parser.add_argument("--clinical", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=20261019)
    return parser.parse_args()


def make_design(frame: pd.DataFrame, train_reference: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, float]]:
    continuous = ["Age", "SmokingIndex", "DiseaseDuration"]
    reference: dict[str, float] = {}
    design = pd.DataFrame(index=frame.index)
    design["cluster_1"] = (frame["cluster"] == 1).astype(float)
    design["cluster_2"] = (frame["cluster"] == 2).astype(float)
    for column in continuous:
        ref_values = pd.to_numeric(train_reference[column], errors="coerce")
        values = pd.to_numeric(frame[column], errors="coerce")
        mean = float(ref_values.mean())
        sd = float(ref_values.std(ddof=0))
        if not np.isfinite(sd) or sd <= 0:
            sd = 1.0
        reference[f"{column}_mean"] = mean
        reference[f"{column}_sd"] = sd
        design[column] = (values - mean) / sd
    design["Sex_M"] = (frame["Sex"].astype(str).str.upper() == "M").astype(float)
    return design.astype(float), reference


def ordered_summary(y: pd.Series, x: pd.DataFrame) -> dict[str, object]:
    # OrderedModel adds its own threshold parameters; an explicit intercept is
    # therefore intentionally omitted from x.
    fit = OrderedModel(y.astype(int), x.astype(float), distr="logit").fit(method="bfgs", disp=False, maxiter=2000)
    params = fit.params
    conf = fit.conf_int()
    effects = {}
    for column in ["cluster_1", "cluster_2"]:
        effects[column] = {
            "common_odds_ratio": float(np.exp(params[column])),
            "ci95_low": float(np.exp(conf.loc[column, 0])),
            "ci95_high": float(np.exp(conf.loc[column, 1])),
            "p": float(fit.pvalues[column]),
        }
    cluster_positions = [list(params.index).index("cluster_1"), list(params.index).index("cluster_2")]
    restriction = np.zeros((2, len(params)))
    restriction[0, cluster_positions[0]] = 1.0
    restriction[1, cluster_positions[1]] = 1.0
    wald = fit.wald_test(restriction, scalar=True)
    return {
        "family": "proportional_odds_logistic",
        "n": int(fit.nobs),
        "categories": sorted(int(v) for v in pd.unique(y)),
        "converged": bool(getattr(fit, "mle_retvals", {}).get("converged", True)),
        "log_likelihood": float(fit.llf),
        "aic": float(fit.aic),
        "cluster_effects": effects,
        "cluster_overall": {
            "wald_statistic": float(np.asarray(wald.statistic).squeeze()),
            "df": 2,
            "p": float(wald.pvalue),
        },
        "threshold_parameters": {str(k): float(v) for k, v in params.items() if str(k) not in {"cluster_1", "cluster_2", "Age", "SmokingIndex", "DiseaseDuration", "Sex_M"}},
    }


def threshold_check(y: pd.Series, x: pd.DataFrame) -> dict[str, object]:
    thresholds = []
    for threshold in range(1, int(y.max()) + 1):
        binary = (y >= threshold).astype(int)
        if binary.nunique() < 2:
            continue
        fit = sm.Logit(binary, sm.add_constant(x, has_constant="add")).fit(disp=False, maxiter=2000)
        row = {"threshold": threshold, "n_positive": int(binary.sum()), "n_negative": int((1 - binary).sum()), "converged": bool(fit.mle_retvals.get("converged", True))}
        for column in ["cluster_1", "cluster_2"]:
            ci = fit.conf_int().loc[column]
            row[column] = {
                "log_odds_ratio": float(fit.params[column]),
                "odds_ratio": float(np.exp(fit.params[column])),
                "ci95_low": float(np.exp(ci.iloc[0])),
                "ci95_high": float(np.exp(ci.iloc[1])),
                "p": float(fit.pvalues[column]),
            }
        thresholds.append(row)

    diagnostics: dict[str, object] = {"threshold_models": thresholds}
    for column in ["cluster_1", "cluster_2"]:
        estimates = np.array([row[column]["log_odds_ratio"] for row in thresholds], dtype=float)
        variances = []
        for threshold in [row["threshold"] for row in thresholds]:
            binary = (y >= threshold).astype(int)
            fit = sm.Logit(binary, sm.add_constant(x, has_constant="add")).fit(disp=False, maxiter=2000)
            variances.append(float(fit.cov_params().loc[column, column]))
        variances = np.maximum(np.asarray(variances), 1e-12)
        weights = 1.0 / variances
        pooled = float(np.sum(weights * estimates) / np.sum(weights))
        q = float(np.sum(weights * (estimates - pooled) ** 2))
        df = max(len(estimates) - 1, 1)
        diagnostics[f"{column}_heterogeneity"] = {
            "log_or_range": [float(estimates.min()), float(estimates.max())],
            "q_statistic_independent_threshold_approximation": q,
            "df": df,
            "p": float(chi2.sf(q, df)),
            "interpretation": "descriptive threshold-coefficient check; threshold estimates are correlated because they use the same cases",
        }
    diagnostics["overall_interpretation"] = (
        "The proportional-odds form was treated as a sensitivity model. "
        "Threshold-specific coefficients were inspected for direction and magnitude; "
        "the heterogeneity p-values are exploratory because threshold fits are correlated."
    )
    return diagnostics


def fit_partition(frame: pd.DataFrame, clinical: pd.DataFrame, train_reference: pd.DataFrame) -> dict[str, object]:
    merged = frame[["case_id", "cluster"]].merge(clinical, on="case_id", how="left", validate="one_to_one")
    for column in ["CAS", "Age", "SmokingIndex", "DiseaseDuration"]:
        merged[column] = pd.to_numeric(merged[column], errors="coerce").replace([np.inf, -np.inf], np.nan)
    complete = merged.dropna(subset=["CAS", "Age", "SmokingIndex", "DiseaseDuration", "Sex"]).copy()
    complete = complete.loc[(complete["CAS"] >= 0) & (complete["CAS"] <= 6)].copy()
    x, reference = make_design(complete, train_reference)
    return {
        "n_total": int(len(merged)),
        "n_complete": int(len(complete)),
        "join_missing": int(merged["CAS"].isna().sum()),
        "standardization_reference": reference,
        "ordered_model": ordered_summary(complete["CAS"], x),
        "proportional_odds_check": threshold_check(complete["CAS"], x),
    }


def main() -> None:
    args = parse_args()
    features = pd.read_csv(args.features)
    clinical = pd.read_csv(args.clinical)
    features["case_id"] = features["case_id"].astype(str)
    clinical["case_id"] = clinical["Id"].astype(str).str.split("_").str[0]
    volume = [column for column in features.columns if column.endswith("_volume_mm3") or column.endswith("_fraction")]
    train = features[features["split"] == "train"].copy()
    validation = features[features["split"] == "val"].copy()
    x_train = train[volume].astype(float)
    x_validation = validation[volume].astype(float)
    medians = x_train.median()
    scaler = StandardScaler().fit(x_train.fillna(medians))
    model = KMeans(n_clusters=3, n_init=50, random_state=args.seed).fit(scaler.transform(x_train.fillna(medians)))
    train["cluster"] = model.labels_
    validation["cluster"] = model.predict(scaler.transform(x_validation.fillna(medians)))
    train_clinical = clinical[clinical["case_id"].isin(set(train["case_id"]))].copy()
    report = {
        "design": {
            "phenotype": "frozen 3-cluster volume solution",
            "covariates": ["Age", "Sex", "SmokingIndex", "DiseaseDuration"],
            "primary_sensitivity": "proportional-odds ordinal logistic regression for CAS 0-6",
            "assumption_check": "threshold-specific binary logistic coefficients, exploratory correlated-threshold approximation",
            "validation_role": "fixed internal validation partition, not external validation",
        },
        "train": fit_partition(train, train_clinical, train_clinical),
        "validation": fit_partition(validation, clinical, train_clinical),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
