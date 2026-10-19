#!/usr/bin/env python3
"""Covariate-adjusted association audit for the frozen volume phenotype."""

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


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--features", type=Path, required=True)
    p.add_argument("--clinical", type=Path, required=True)
    p.add_argument("--audit", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--seed", type=int, default=20261019)
    return p.parse_args()


def make_design(frame: pd.DataFrame, train_reference: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, float]]:
    continuous = ["Age", "SmokingIndex", "DiseaseDuration"]
    ref: dict[str, float] = {}
    x = pd.DataFrame(index=frame.index)
    x["cluster_1"] = (frame["cluster"] == 1).astype(float)
    x["cluster_2"] = (frame["cluster"] == 2).astype(float)
    for col in continuous:
        reference_values = pd.to_numeric(train_reference[col], errors="coerce")
        frame_values = pd.to_numeric(frame[col], errors="coerce")
        mean = float(reference_values.mean())
        sd = float(reference_values.std(ddof=0))
        if not np.isfinite(sd) or sd <= 0:
            sd = 1.0
        ref[f"{col}_mean"] = mean
        ref[f"{col}_sd"] = sd
        x[col] = (frame_values - mean) / sd
    x["Sex_M"] = (frame["Sex"].astype(str).str.upper() == "M").astype(float)
    return sm.add_constant(x, has_constant="add"), ref


def model_summary(y: pd.Series, x: pd.DataFrame, family: str) -> dict[str, object]:
    if family == "ols":
        fit = sm.OLS(y.astype(float), x.astype(float), missing="drop").fit(cov_type="HC3")
        params = fit.params
        conf = fit.conf_int()
        effects = {
            k: {"estimate": float(params[k]), "ci95_low": float(conf.loc[k, 0]), "ci95_high": float(conf.loc[k, 1]), "p": float(fit.pvalues[k])}
            for k in ["cluster_1", "cluster_2"]
        }
        restriction = np.zeros((2, len(params)))
        restriction[0, list(params.index).index("cluster_1")] = 1
        restriction[1, list(params.index).index("cluster_2")] = 1
        wald = fit.wald_test(restriction, scalar=True)
        return {"family": family, "n": int(fit.nobs), "r_squared": float(fit.rsquared), "cluster_effects": effects, "cluster_overall": {"statistic": float(np.asarray(wald.statistic).squeeze()), "p": float(wald.pvalue)}}
    fit = sm.GLM(y.astype(float), x.astype(float), family=sm.families.Binomial(), missing="drop").fit(cov_type="HC3")
    params = fit.params
    conf = fit.conf_int()
    effects = {
        k: {"odds_ratio": float(np.exp(params[k])), "ci95_low": float(np.exp(conf.loc[k, 0])), "ci95_high": float(np.exp(conf.loc[k, 1])), "p": float(fit.pvalues[k])}
        for k in ["cluster_1", "cluster_2"]
    }
    restriction = np.zeros((2, len(params)))
    restriction[0, list(params.index).index("cluster_1")] = 1
    restriction[1, list(params.index).index("cluster_2")] = 1
    wald = fit.wald_test(restriction, scalar=True)
    return {"family": family, "n": int(fit.nobs), "cluster_effects": effects, "cluster_overall": {"statistic": float(np.asarray(wald.statistic).squeeze()), "p": float(wald.pvalue)}}


def fit_split(frame: pd.DataFrame, clinical: pd.DataFrame, train_reference: pd.DataFrame) -> dict[str, object]:
    merged = frame[["case_id", "cluster"]].merge(clinical, on="case_id", how="left", validate="one_to_one")
    merged["active_cas_ge_3"] = (merged["CAS"].astype(float) >= 3).astype(int)
    covariates = ["CAS", "active_cas_ge_3", "Age", "SmokingIndex", "DiseaseDuration", "Sex"]
    complete = merged.dropna(subset=covariates).copy()
    x, ref = make_design(complete, train_reference)
    out = {"n_total": int(len(merged)), "n_complete": int(len(complete)), "join_missing": int(merged.CAS.isna().sum()), "standardization_reference": ref}
    out["cas_continuous_ols"] = model_summary(complete["CAS"], x, "ols")
    out["active_cas_ge_3_logistic"] = model_summary(complete["active_cas_ge_3"], x, "logistic")
    return out


def main() -> None:
    args = parse_args()
    features = pd.read_csv(args.features)
    clinical = pd.read_csv(args.clinical)
    features["case_id"] = features["case_id"].astype(str)
    clinical["case_id"] = clinical["Id"].str.split("_").str[0].astype(str)
    volume = [c for c in features.columns if c.endswith("_volume_mm3") or c.endswith("_fraction")]
    train = features[features["split"] == "train"].copy()
    val = features[features["split"] == "val"].copy()
    x_train = train[volume].astype(float).fillna(train[volume].astype(float).median())
    x_val = val[volume].astype(float).fillna(train[volume].astype(float).median())
    scaler = StandardScaler().fit(x_train)
    model = KMeans(n_clusters=3, n_init=50, random_state=args.seed).fit(scaler.transform(x_train))
    train["cluster"] = model.labels_
    val["cluster"] = model.predict(scaler.transform(x_val))
    clinical_train = clinical[clinical.case_id.isin(set(train.case_id))].copy()
    report = {"design": {"phenotype": "frozen 3-cluster volume solution", "covariates": ["Age", "Sex", "SmokingIndex", "DiseaseDuration"], "validation_role": "within-validation sensitivity association, not external validation"}, "train": fit_split(train, clinical_train, clinical_train), "validation": fit_split(val, clinical, clinical_train), "mask_spacing_audit": json.loads(args.audit.read_text())}
    args.out.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
