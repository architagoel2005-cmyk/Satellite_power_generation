# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 09:29:15 2026

@author: ADMIN
"""

"""
EDA - CSIM Solar Spectral Irradiance (SSI) L3 Dataset
Columns:
    time (Julian Date)                 — observation timestamp
    wavelength (nm)                    — wavelength of measurement
    irradiance (W/m^2/nm)             — solar spectral irradiance
    instrument_uncertainty (W/m^2/nm) — measurement uncertainty
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────

DATASET_PATH = r"C:\Users\ADMIN\Desktop\CSIM\csim_ssi_l3.csv"

# Column name constants
TIME_COL        = 'time (Julian Date)'
WAVE_COL        = 'wavelength (nm)'
IRR_COL         = 'irradiance (W/m^2/nm)'
UNC_COL         = 'instrument_uncertainty (W/m^2/nm)'

# Wavelength bands (nm) — standard solar spectrum divisions
UV_BAND     = (210,  400)
VIS_BAND    = (400,  700)
NIR_BAND    = (700, 1000)
SWIR_BAND   = (1000, 2600)

BAND_LABELS = {
    'UV'   : UV_BAND,
    'VIS'  : VIS_BAND,
    'NIR'  : NIR_BAND,
    'SWIR' : SWIR_BAND,
}

BAND_COLORS = {
    'UV'   : '#9467bd',
    'VIS'  : '#f7c637',
    'NIR'  : '#ff7f0e',
    'SWIR' : '#d62728',
}

try:
    plt.style.use('seaborn-v0_8-whitegrid')
except OSError:
    plt.style.use('seaborn-whitegrid')


# ─────────────────────────────────────────────
# HELPER — assign wavelength band label
# ─────────────────────────────────────────────

def assign_band(wavelength):
    if wavelength < 400:
        return 'UV'
    elif wavelength < 700:
        return 'VIS'
    elif wavelength < 1000:
        return 'NIR'
    else:
        return 'SWIR'


# ─────────────────────────────────────────────
# STEP 1: LOAD DATASET
# ─────────────────────────────────────────────

def load_dataset():
    print("\n" + "=" * 60)
    print("STEP 1: LOADING DATASET")
    print("=" * 60)

    df = pd.read_csv(DATASET_PATH)
    df.columns = [c.strip() for c in df.columns]

    # Convert Julian Date to readable date
    # Julian Date 2458569.5 = 2019-04-01 (approx)
    # Offset from J2000 epoch: JD 2451545.0 = 2000-01-01 12:00 UTC
    df['date'] = pd.to_datetime(df[TIME_COL] - 2440587.5, unit='D', origin='unix')

    # Assign spectral band
    df['band'] = df[WAVE_COL].apply(assign_band)

    print(f"[OK] Loaded {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"\nColumns     : {df.columns.tolist()}")
    print(f"Date range  : {df['date'].min().date()} → {df['date'].max().date()}")
    print(f"Wavelength  : {df[WAVE_COL].min():.1f} nm → {df[WAVE_COL].max():.1f} nm")
    print(f"Irradiance  : {df[IRR_COL].min():.6f} → {df[IRR_COL].max():.6f} W/m²/nm")
    print(f"\nBand distribution:\n{df['band'].value_counts().to_string()}")

    return df


# ─────────────────────────────────────────────
# STEP 2: BASIC INSPECTION
# ─────────────────────────────────────────────

def basic_inspection(df):
    print("\n" + "=" * 60)
    print("STEP 2: BASIC INSPECTION")
    print("=" * 60)

    print(f"\nShape   : {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"\nDtypes:\n{df.dtypes.to_string()}")
    print(f"\nFirst 5 rows:\n{df.head(5).to_string()}")
    print(f"\nStatistical Summary:\n{df.describe().round(6).to_string()}")

    # Unique timestamps and wavelengths
    n_times = df[TIME_COL].nunique()
    n_waves = df[WAVE_COL].nunique()
    print(f"\nUnique timestamps  : {n_times:,}")
    print(f"Unique wavelengths : {n_waves:,}")
    print(f"Wavelengths per obs: ~{len(df) // n_times}")


# ─────────────────────────────────────────────
# STEP 3: MISSING VALUES ANALYSIS
# ─────────────────────────────────────────────

def missing_value_analysis(df):
    print("\n" + "=" * 60)
    print("STEP 3: MISSING VALUES ANALYSIS")
    print("=" * 60)

    miss = df.isnull().sum()
    miss_pct = (miss / len(df) * 100).round(4)
    miss_df = pd.DataFrame({"Missing Count": miss, "Missing %": miss_pct})
    print(f"\nMissing values:\n{miss_df.to_string()}")

    # Zero irradiance check (physically suspect)
    zero_irr = (df[IRR_COL] == 0).sum()
    print(f"\nZero irradiance rows : {zero_irr:,} ({zero_irr/len(df)*100:.2f}%)")

    # Uncertainty == 0 check
    zero_unc = (df[UNC_COL] == 0).sum()
    print(f"Zero uncertainty rows: {zero_unc:,} ({zero_unc/len(df)*100:.2f}%)")

    # Visualise
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Missing values bar
    if miss_df["Missing Count"].sum() == 0:
        axes[0].text(0.5, 0.5, "No missing values", ha='center', va='center',
                     fontsize=13, transform=axes[0].transAxes)
    else:
        miss_df["Missing %"].plot(kind='bar', ax=axes[0], color='#d62728', edgecolor='black')
    axes[0].set_title("Missing Values per Column")
    axes[0].set_ylabel("Missing %")

    # Data quality summary
    quality = {
        'Valid rows'          : len(df) - zero_irr,
        'Zero irradiance'     : zero_irr,
        'Zero uncertainty'    : zero_unc,
        'Duplicate rows'      : df.duplicated().sum(),
    }
    axes[1].barh(list(quality.keys()), list(quality.values()),
                 color=['#2ca02c','#d62728','#ff7f0e','#9467bd'])
    axes[1].set_title("Data Quality Overview")
    axes[1].set_xlabel("Count")
    for i, v in enumerate(quality.values()):
        axes[1].text(v + 100, i, f"{v:,}", va='center', fontsize=9)

    plt.suptitle("CSIM SSI — Data Quality", fontsize=13)
    plt.tight_layout()
    plt.savefig("csim_step3_missing.png", dpi=150, bbox_inches='tight')
    plt.show()
    print("[Saved] csim_step3_missing.png")

    return df


# ─────────────────────────────────────────────
# STEP 4: OUTLIER DETECTION
# ─────────────────────────────────────────────

def detect_outliers_iqr(series):
    Q1, Q3 = series.quantile(0.25), series.quantile(0.75)
    IQR = Q3 - Q1
    return (series < Q1 - 1.5 * IQR) | (series > Q3 + 1.5 * IQR)


def outlier_analysis(df):
    print("\n" + "=" * 60)
    print("STEP 4: OUTLIER ANALYSIS")
    print("=" * 60)

    for col in [IRR_COL, WAVE_COL]:
        out = detect_outliers_iqr(df[col])
        print(f"  [{col}] Outliers: {out.sum():,} ({out.sum()/len(df)*100:.3f}%)")

    # Boxplots per band
    fig, axes = plt.subplots(1, 4, figsize=(18, 5))
    for i, (band, color) in enumerate(BAND_COLORS.items()):
        data = df[df['band'] == band][IRR_COL]
        axes[i].boxplot(data, patch_artist=True,
                        boxprops=dict(facecolor=color, alpha=0.6))
        out_count = detect_outliers_iqr(data).sum()
        axes[i].set_title(f"{band} Band\n({out_count:,} outliers)", fontsize=10)
        axes[i].set_ylabel("Irradiance (W/m²/nm)")
        axes[i].set_xlabel(f"{BAND_LABELS[band][0]}–{BAND_LABELS[band][1]} nm")

    plt.suptitle("CSIM SSI — Irradiance Outliers by Spectral Band (IQR Method)", fontsize=13)
    plt.tight_layout()
    plt.savefig("csim_step4_outliers.png", dpi=150, bbox_inches='tight')
    plt.show()
    print("[Saved] csim_step4_outliers.png")


# ─────────────────────────────────────────────
# STEP 5: UNIVARIATE ANALYSIS
# ─────────────────────────────────────────────

def univariate_analysis(df):
    print("\n" + "=" * 60)
    print("STEP 5: UNIVARIATE ANALYSIS")
    print("=" * 60)

    fig, axes = plt.subplots(2, 3, figsize=(18, 10))

    # 1. Irradiance distribution (full)
    axes[0, 0].hist(df[IRR_COL], bins=100, color='#1f77b4', edgecolor='white', alpha=0.8)
    axes[0, 0].set_title("Irradiance Distribution (all wavelengths)")
    axes[0, 0].set_xlabel("Irradiance (W/m²/nm)")
    axes[0, 0].set_ylabel("Frequency")

    # 2. KDE of irradiance
    sns.kdeplot(df[IRR_COL], ax=axes[0, 1], color='#1f77b4', fill=True, alpha=0.4)
    axes[0, 1].set_title("Irradiance KDE")
    axes[0, 1].set_xlabel("Irradiance (W/m²/nm)")

    # 3. Wavelength distribution
    axes[0, 2].hist(df[WAVE_COL], bins=100, color='#ff7f0e', edgecolor='white', alpha=0.8)
    axes[0, 2].set_title("Wavelength Distribution")
    axes[0, 2].set_xlabel("Wavelength (nm)")
    axes[0, 2].set_ylabel("Count")

    # 4. Irradiance per band (overlaid KDE)
    for band, color in BAND_COLORS.items():
        data = df[df['band'] == band][IRR_COL]
        sns.kdeplot(data, ax=axes[1, 0], label=band, color=color, fill=True, alpha=0.25)
    axes[1, 0].set_title("Irradiance KDE by Spectral Band")
    axes[1, 0].set_xlabel("Irradiance (W/m²/nm)")
    axes[1, 0].legend()

    # 5. Band sample counts
    band_counts = df['band'].value_counts()
    axes[1, 1].bar(band_counts.index, band_counts.values,
                   color=[BAND_COLORS[b] for b in band_counts.index], edgecolor='black')
    axes[1, 1].set_title("Sample Count per Spectral Band")
    axes[1, 1].set_ylabel("Count")
    for i, v in enumerate(band_counts.values):
        axes[1, 1].text(i, v + 500, f"{v:,}", ha='center', fontsize=9)

    # 6. Log-scale irradiance distribution
    log_irr = np.log1p(df[IRR_COL])
    axes[1, 2].hist(log_irr, bins=100, color='#2ca02c', edgecolor='white', alpha=0.8)
    axes[1, 2].set_title("Log(1+Irradiance) Distribution")
    axes[1, 2].set_xlabel("log(1 + Irradiance)")

    plt.suptitle("CSIM SSI — Univariate Analysis", fontsize=14)
    plt.tight_layout()
    plt.savefig("csim_step5_univariate.png", dpi=150, bbox_inches='tight')
    plt.show()
    print("[Saved] csim_step5_univariate.png")


# ─────────────────────────────────────────────
# STEP 6: TIME SERIES ANALYSIS
# ─────────────────────────────────────────────

def time_series_analysis(df):
    print("\n" + "=" * 60)
    print("STEP 6: TIME SERIES ANALYSIS")
    print("=" * 60)

    # Aggregate: mean irradiance per timestamp (integrated spectrum)
    ts = df.groupby(TIME_COL).agg(
        mean_irradiance   =(IRR_COL, 'mean'),
        total_irradiance  =(IRR_COL, 'sum'),
        date              =('date', 'first')
    ).reset_index().sort_values('date')

    print(f"  Unique observation times: {len(ts):,}")

    fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)

    # Mean irradiance over time
    axes[0].plot(ts['date'], ts['mean_irradiance'], color='#1f77b4', linewidth=1.2)
    axes[0].set_ylabel("Mean Irradiance\n(W/m²/nm)")
    axes[0].set_title("Mean Spectral Irradiance Over Time")

    # Total integrated irradiance over time
    axes[1].plot(ts['date'], ts['total_irradiance'], color='#ff7f0e', linewidth=1.2)
    axes[1].set_ylabel("Total Irradiance\n(W/m²/nm · sum)")
    axes[1].set_title("Total (Integrated) Irradiance Over Time")

    # Rolling mean (smoothed trend)
    window = max(3, len(ts) // 20)
    axes[2].plot(ts['date'], ts['mean_irradiance'], color='#aec7e8', linewidth=0.8, alpha=0.5)
    axes[2].plot(ts['date'], ts['mean_irradiance'].rolling(window, center=True).mean(),
                 color='#d62728', linewidth=2, label=f"Rolling mean (w={window})")
    axes[2].set_ylabel("Mean Irradiance")
    axes[2].set_title("Smoothed Trend")
    axes[2].set_xlabel("Date")
    axes[2].legend()

    plt.suptitle("CSIM SSI — Time Series Analysis", fontsize=14)
    plt.tight_layout()
    plt.savefig("csim_step6_timeseries.png", dpi=150, bbox_inches='tight')
    plt.show()
    print("[Saved] csim_step6_timeseries.png")

    return ts


# ─────────────────────────────────────────────
# STEP 7: SPECTRAL ANALYSIS
# ─────────────────────────────────────────────

def spectral_analysis(df):
    print("\n" + "=" * 60)
    print("STEP 7: SPECTRAL ANALYSIS")
    print("=" * 60)

    # Mean spectrum across all observations
    spectrum = df.groupby(WAVE_COL)[IRR_COL].mean().reset_index()
    spectrum.columns = ['wavelength', 'mean_irradiance']

    fig, axes = plt.subplots(2, 2, figsize=(16, 10))

    # 1. Full mean spectrum
    ax = axes[0, 0]
    for band, color in BAND_COLORS.items():
        lo, hi = BAND_LABELS[band]
        mask = (spectrum['wavelength'] >= lo) & (spectrum['wavelength'] < hi)
        ax.fill_between(spectrum['wavelength'][mask],
                        spectrum['mean_irradiance'][mask],
                        alpha=0.6, color=color, label=band)
    ax.set_title("Mean Solar Spectrum (all observations)")
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Mean Irradiance (W/m²/nm)")
    ax.legend()

    # 2. Log-scale spectrum
    ax = axes[0, 1]
    ax.semilogy(spectrum['wavelength'], spectrum['mean_irradiance'],
                color='#1f77b4', linewidth=1)
    ax.set_title("Mean Solar Spectrum (log scale)")
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Irradiance (log W/m²/nm)")

    # 3. Spectrum std (variability)
    spec_std = df.groupby(WAVE_COL)[IRR_COL].std().reset_index()
    spec_std.columns = ['wavelength', 'std_irradiance']
    ax = axes[1, 0]
    ax.plot(spec_std['wavelength'], spec_std['std_irradiance'],
            color='#d62728', linewidth=1)
    ax.set_title("Irradiance Variability by Wavelength (std)")
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Std Dev (W/m²/nm)")

    # 4. Mean irradiance per band (bar)
    band_mean = df.groupby('band')[IRR_COL].mean().reindex(['UV','VIS','NIR','SWIR'])
    ax = axes[1, 1]
    bars = ax.bar(band_mean.index, band_mean.values,
                  color=[BAND_COLORS[b] for b in band_mean.index],
                  edgecolor='black')
    ax.set_title("Mean Irradiance per Spectral Band")
    ax.set_ylabel("Mean Irradiance (W/m²/nm)")
    for bar, v in zip(bars, band_mean.values):
        ax.text(bar.get_x() + bar.get_width()/2, v + 0.002,
                f"{v:.4f}", ha='center', fontsize=9)

    plt.suptitle("CSIM SSI — Spectral Analysis", fontsize=14)
    plt.tight_layout()
    plt.savefig("csim_step7_spectral.png", dpi=150, bbox_inches='tight')
    plt.show()
    print("[Saved] csim_step7_spectral.png")


# ─────────────────────────────────────────────
# STEP 8: CORRELATION ANALYSIS
# ─────────────────────────────────────────────

def correlation_analysis(df):
    print("\n" + "=" * 60)
    print("STEP 8: CORRELATION ANALYSIS")
    print("=" * 60)

    num_cols = [TIME_COL, WAVE_COL, IRR_COL, UNC_COL]
    corr = df[num_cols].corr()
    print(f"\nCorrelation matrix:\n{corr.round(4).to_string()}")

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Heatmap
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt=".3f",
                cmap='RdYlGn', center=0, ax=axes[0],
                linewidths=0.5, annot_kws={"size": 11})
    axes[0].set_title("Correlation Heatmap")
    axes[0].tick_params(axis='x', rotation=30)
    axes[0].tick_params(axis='y', rotation=0)

    # Wavelength vs irradiance scatter (sampled for speed)
    sample = df.sample(min(20000, len(df)), random_state=42)
    for band, color in BAND_COLORS.items():
        mask_b = sample['band'] == band
        axes[1].scatter(sample[mask_b][WAVE_COL], sample[mask_b][IRR_COL],
                        alpha=0.15, s=3, color=color, label=band)
    axes[1].set_xlabel("Wavelength (nm)")
    axes[1].set_ylabel("Irradiance (W/m²/nm)")
    axes[1].set_title("Wavelength vs Irradiance (20k sample)")
    axes[1].legend(markerscale=5)

    plt.suptitle("CSIM SSI — Correlation Analysis", fontsize=14)
    plt.tight_layout()
    plt.savefig("csim_step8_correlation.png", dpi=150, bbox_inches='tight')
    plt.show()
    print("[Saved] csim_step8_correlation.png")


# ─────────────────────────────────────────────
# STEP 9: FEATURE ENGINEERING
# ─────────────────────────────────────────────

def feature_engineering(df):
    print("\n" + "=" * 60)
    print("STEP 9: FEATURE ENGINEERING")
    print("=" * 60)

    df = df.copy()

    # Log irradiance (handles skew, useful for ML)
    df['log_irradiance']         = np.log1p(df[IRR_COL])

    # Normalised irradiance per observation (relative spectral shape)
    obs_max = df.groupby(TIME_COL)[IRR_COL].transform('max')
    df['irradiance_normalised']  = df[IRR_COL] / obs_max.replace(0, np.nan)

    # Wavelength band as numeric code
    band_code = {'UV': 0, 'VIS': 1, 'NIR': 2, 'SWIR': 3}
    df['band_code']              = df['band'].map(band_code)

    # Julian day of year (seasonality proxy)
    df['day_of_year']            = df['date'].dt.dayofyear

    # Solar cycle proxy: days since mission start
    t0 = df[TIME_COL].min()
    df['mission_day']            = (df[TIME_COL] - t0).round(0).astype(int)

    # Signal-to-noise ratio proxy (irradiance / uncertainty)
    # uncertainty is 0 for all rows in this dataset — flag this
    if (df[UNC_COL] == 0).all():
        df['snr']                = np.nan
        print("  [NOTE] All uncertainty values are 0 — SNR cannot be computed.")
    else:
        df['snr']                = df[IRR_COL] / df[UNC_COL].replace(0, np.nan)

    new_features = ['log_irradiance', 'irradiance_normalised', 'band_code',
                    'day_of_year', 'mission_day', 'snr']
    print(f"  New features added: {new_features}")
    print(f"\n  Sample:\n{df[new_features].head(5).to_string()}")

    # ── Visualise: normalised spectrum per observation (first 5 obs)
    fig, axes = plt.subplots(1, 2, figsize=(16, 5))

    first5 = df[TIME_COL].unique()[:5]
    for t in first5:
        sub = df[df[TIME_COL] == t].sort_values(WAVE_COL)
        axes[0].plot(sub[WAVE_COL], sub['irradiance_normalised'],
                     linewidth=1, alpha=0.8, label=f"JD {t:.1f}")
    axes[0].set_title("Normalised Spectral Shape (first 5 observations)")
    axes[0].set_xlabel("Wavelength (nm)")
    axes[0].set_ylabel("Normalised Irradiance")
    axes[0].legend(fontsize=8)

    # Log irradiance distribution
    sns.kdeplot(df['log_irradiance'], ax=axes[1], fill=True,
                color='#2ca02c', alpha=0.5)
    axes[1].set_title("Log(1 + Irradiance) Distribution")
    axes[1].set_xlabel("log(1 + Irradiance)")

    plt.suptitle("CSIM SSI — Engineered Features", fontsize=14)
    plt.tight_layout()
    plt.savefig("csim_step9_features.png", dpi=150, bbox_inches='tight')
    plt.show()
    print("[Saved] csim_step9_features.png")

    return df


# ─────────────────────────────────────────────
# STEP 10: CLEAN DATASET + EDA SUMMARY
# ─────────────────────────────────────────────

def generate_clean_dataset(df):
    print("\n" + "=" * 60)
    print("STEP 10: CLEAN DATASET GENERATION")
    print("=" * 60)

    clean = df.copy()

    # Rename columns to ML-friendly names
    clean = clean.rename(columns={
        TIME_COL : 'time_jd',
        WAVE_COL : 'wavelength_nm',
        IRR_COL  : 'irradiance_Wm2nm',
        UNC_COL  : 'uncertainty_Wm2nm',
    })

    # Drop rows where irradiance is exactly 0
    before = len(clean)
    clean = clean[clean['irradiance_Wm2nm'] > 0].reset_index(drop=True)
    print(f"  Dropped {before - len(clean):,} zero-irradiance rows")

    # Drop SNR column if all NaN
    if 'snr' in clean.columns and clean['snr'].isna().all():
        clean = clean.drop(columns=['snr'])

    # Final fill
    clean = clean.fillna(0)

    # Save
    import os
    out_dir = r"C:\Users\ADMIN\Desktop\CSIM"
    out_path = os.path.join(out_dir, "csim_ssi_clean.csv")
    clean.to_csv(out_path, index=False)

    print(f"\n  [SAVED] {clean.shape[0]:,} rows × {clean.shape[1]} cols")
    print(f"  Path   : {out_path}")
    print(f"\n  Columns: {clean.columns.tolist()}")
    print(f"\n  Sample:\n{clean.head(3).to_string()}")
    print(f"\n  Missing values: {clean.isnull().sum().sum()}")

    return clean


def eda_summary(df):
    print("\n" + "=" * 60)
    print("EDA SUMMARY REPORT — CSIM SSI L3")
    print("=" * 60)

    print(f"Shape            : {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"Date range       : {df['date'].min().date()} → {df['date'].max().date()}")
    print(f"Wavelength range : {df[WAVE_COL].min():.1f} – {df[WAVE_COL].max():.1f} nm")
    print(f"Irradiance range : {df[IRR_COL].min():.6f} – {df[IRR_COL].max():.6f} W/m²/nm")
    print(f"Missing values   : {df.isnull().sum().sum()}")
    print(f"Zero irradiance  : {(df[IRR_COL]==0).sum():,}")
    print(f"Duplicate rows   : {df.duplicated().sum()}")

    print(f"\nBand distribution:")
    print(df['band'].value_counts().to_string())

    print(f"\nMean irradiance per band:")
    print(df.groupby('band')[IRR_COL].mean().round(6).to_string())

    print(f"\nTop correlated features with irradiance:")
    num = df.select_dtypes(include=np.number)
    corr_irr = num.corr()[IRR_COL].drop(IRR_COL).abs().sort_values(ascending=False)
    print(corr_irr.head(6).round(4).to_string())

    print("\n[EDA COMPLETE] Clean dataset saved. Ready for ML pipeline.")
    print("Suggested ML targets:")
    print("  → Predict irradiance from wavelength + time (regression)")
    print("  → Classify spectral band from irradiance profile (classification)")
    print("  → Detect solar activity anomalies from time series (anomaly detection)")


# ─────────────────────────────────────────────
# MAIN PIPELINE
# ─────────────────────────────────────────────

if __name__ == "__main__":

    df = load_dataset()
    basic_inspection(df)
    df = missing_value_analysis(df)
    outlier_analysis(df)
    univariate_analysis(df)
    ts = time_series_analysis(df)
    spectral_analysis(df)
    correlation_analysis(df)
    df = feature_engineering(df)
    clean_df = generate_clean_dataset(df)
    eda_summary(df)

    print("\n[Done] All plots saved. Clean dataset ready for ML training.")