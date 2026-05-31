# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 21:49:36 2026

@author: ADMIN
"""

import matplotlib
matplotlib.use('Qt5Agg') 



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

DATASET_PATHS = {
    "NEPALISAT":   "C:/Users/ADMIN/Downloads/8kp25ycf63-1/8kp25ycf63-1/NEPALISAT.csv",       # NEPALISAT
    "RAAVANA": "C:/Users/ADMIN/Downloads/8kp25ycf63-1/8kp25ycf63-1/RAAVANA.csv",   # RAAVANA
    "TSURU":    "C:/Users/ADMIN/Downloads/8kp25ycf63-1/8kp25ycf63-1/TSURU.csv",      # TSURU
    "UGUISU":  "C:/Users/ADMIN/Downloads/8kp25ycf63-1/8kp25ycf63-1/UGUISU.csv",    # UGUISU
}


# All 4 satellites share the same BIRDS EPS schema.
# NOTE: TSURU uses 'Time stamp' (lowercase s); others use 'Time Stamp'.
#       We normalise this during loading.
 
# Columns we care about (using the human-readable, calibrated columns — not the raw hex ones)
PANEL_VOLT_COLS = ['Vpy (mV)', 'Vpx (mV)', 'Vmz (mV)', 'Vmx (mV)', 'Vpz (mV)']
PANEL_CURR_COLS = ['Ipy (mA)', 'Ipx (mA)', 'Imz (mA)', 'Imx (mA)', 'Ipz (mA)']
PANEL_TEMP_COLS = ['Tpy (°C)', 'Tpx (°C)', 'Tmz (°C)', 'Tmx (°C)', 'Tpz (°C)']
 
BATT_VOLT_COL  = 'Vbat (V)'
BATT_CURR_COL  = 'Ibatt(mA)'
BATT_TEMP_COL  = 'Tbatt (?)'   # °C, sensor label has encoding issue in source file
TIME_COL       = 'Time Stamp'  # normalised during loading
 
# Face labels for panels (+y, +x, -z, -x, +z)
FACE_LABELS = ['py', 'px', 'mz', 'mx', 'pz']
 
plt.style.use('seaborn-v0_8-whitegrid')
 
COLORS = {
    "nepalisat": "#1f77b4",
    "raavana":   "#ff7f0e",
    "tsuru":     "#2ca02c",
    "uguisu":    "#9467bd",
    "eclipse":   "#d62728",
    "sunlit":    "#f7c637",
}
 
FACE_COLORS = {
    'py': '#1f77b4',
    'px': '#ff7f0e',
    'mz': '#2ca02c',
    'mx': '#d62728',
    'pz': '#9467bd',
}


# STEP 1: LOAD DATASETS

def load_datasets():
    """Load all 4 BIRDS EPS datasets and normalise the time-stamp column name."""
    print("\n" + "=" * 60)
    print("STEP 1: LOADING DATASETS")
    print("=" * 60)
 
    dfs = {}
    for name, path in DATASET_PATHS.items():
        try:
            df = pd.read_csv(path, encoding='latin1', low_memory=False)
 
            # Normalise time-stamp column name (TSURU uses lowercase 's')
            df.columns = [c.strip() for c in df.columns]
            if 'Time stamp' in df.columns:
                df.rename(columns={'Time stamp': 'Time Stamp'}, inplace=True)
 
            # Convert Time Stamp to numeric (seconds elapsed)
            df[TIME_COL] = pd.to_numeric(df[TIME_COL], errors='coerce')
 
            # Convert all calibrated numeric columns to float
            cal_cols = PANEL_VOLT_COLS + PANEL_CURR_COLS + PANEL_TEMP_COLS + \
                       [BATT_VOLT_COL, BATT_CURR_COL, BATT_TEMP_COL]
            for col in cal_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
 
            dfs[name] = df
            print(f"[OK] {name.upper():12s} — {df.shape[0]:,} rows × {df.shape[1]} columns")
 
        except FileNotFoundError:
            print(f"[!!] {name.upper():12s} — File not found: {path}")
 
    return dfs

# STEP 2: BASIC INSPECTION

def basic_inspection(dfs):
    """Print shape, dtypes, and statistical summary of each dataset."""
    print("\n" + "=" * 60)
    print("STEP 2: BASIC INSPECTION")
    print("=" * 60)
 
    for name, df in dfs.items():
        print(f"\n{'─' * 50}")
        print(f"Dataset : {name.upper()}")
        print(f"Shape   : {df.shape[0]:,} rows × {df.shape[1]} columns")
        print(f"\nColumn dtypes:")
        print(df.dtypes.to_string())
        print(f"\nFirst 3 rows (calibrated columns only):")
        cal_cols = [c for c in PANEL_VOLT_COLS + PANEL_CURR_COLS + PANEL_TEMP_COLS +
                    [BATT_VOLT_COL, BATT_CURR_COL, BATT_TEMP_COL, TIME_COL]
                    if c in df.columns]
        print(df[cal_cols].head(3).to_string())
        print(f"\nStatistical Summary (calibrated columns):")
        print(df[cal_cols].describe().round(3).to_string())
        

#  STEP 3: MISSING VALUES ANALYSIS

def missing_value_analysis(dfs):
    """Detect and visualise missing values."""
    print("\n" + "=" * 60)
    print("STEP 3: MISSING VALUES ANALYSIS")
    print("=" * 60)
 
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    axes = axes.flatten()
 
    for i, (name, df) in enumerate(dfs.items()):
        miss = df.isnull().sum()
        miss_pct = (miss / len(df) * 100).round(2)
        miss_df = pd.DataFrame({"Missing Count": miss, "Missing %": miss_pct})
        miss_df = miss_df[miss_df["Missing Count"] > 0].sort_values("Missing %", ascending=False)
 
        if miss_df.empty:
            print(f"[{name.upper()}] No missing values found.")
            axes[i].text(0.5, 0.5, "No missing values", ha='center', va='center',
                         fontsize=13, transform=axes[i].transAxes)
        else:
            print(f"\n[{name.upper()}] Missing values:\n{miss_df.to_string()}")
            miss_df["Missing %"].plot(kind='bar', ax=axes[i],
                                      color=COLORS[name], edgecolor='black')
            axes[i].set_ylabel("Missing %")
            axes[i].tick_params(axis='x', rotation=45)
 
        axes[i].set_title(f"{name.upper()} — Missing Values")
 
    plt.tight_layout()
    plt.savefig("step3_missing_values.png", dpi=150, bbox_inches='tight')
    plt.show()
    print("[Saved] step3_missing_values.png")
 
 
def handle_missing_values(dfs):
    """
    Handle missing values:
    - Drop columns with >40% missing
    - Linear interpolation for numeric sensor columns
    - Forward/backward fill for any remaining gaps
    """
    print("\n[Handling missing values...]")
    cleaned = {}
 
    for name, df in dfs.items():
        df = df.copy()
        threshold = 0.4 * len(df)
        df = df.dropna(thresh=threshold, axis=1)
 
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].interpolate(
            method='linear', limit_direction='both')
        df = df.ffill().bfill()
 
        cleaned[name] = df
        remaining = df.isnull().sum().sum()
        print(f"  [{name.upper()}] Missing after cleaning: {remaining}")
 
    return cleaned


# STEP 4: DUPLICATE & OUTLIER DETECTION

def check_duplicates(dfs):
    """Check and remove duplicate rows."""
    print("\n" + "=" * 60)
    print("STEP 4A: DUPLICATE CHECK")
    print("=" * 60)
 
    cleaned = {}
    for name, df in dfs.items():
        dupes = df.duplicated().sum()
        print(f"[{name.upper()}] Duplicate rows: {dupes}")
        cleaned[name] = df.drop_duplicates().reset_index(drop=True)
 
    return cleaned
 
 
def detect_outliers_iqr(df, col):
    """Return a boolean mask of outliers using the IQR method."""
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    return (df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)
 
 
def outlier_analysis(dfs):
    """
    Detect outliers in key EPS columns for all 4 satellites and compare via boxplots.
    Uses battery voltage, total panel current, battery temperature.
    """
    print("\n" + "=" * 60)
    print("STEP 4B: OUTLIER ANALYSIS")
    print("=" * 60)
 
    # ── Per-satellite boxplots (battery + panel key cols)
    key_cols = [BATT_VOLT_COL, BATT_CURR_COL, BATT_TEMP_COL]
    key_cols = [c for c in key_cols]  # all should exist
 
    for name, df in dfs.items():
        available = [c for c in key_cols if c in df.columns]
        if not available:
            continue
 
        fig, axes = plt.subplots(1, len(available), figsize=(5 * len(available), 5))
        if len(available) == 1:
            axes = [axes]
 
        for i, col in enumerate(available):
            outlier_count = detect_outliers_iqr(df, col).sum()
            print(f"  [{name.upper()}][{col}] Outliers: {outlier_count} "
                  f"({outlier_count / len(df) * 100:.2f}%)")
            axes[i].boxplot(df[col].dropna(), patch_artist=True,
                            boxprops=dict(facecolor=COLORS[name], alpha=0.6))
            axes[i].set_title(f"{col}\n({outlier_count} outliers)", fontsize=10)
            axes[i].set_ylabel("Value")
 
        plt.suptitle(f"{name.upper()} — Outlier Detection (IQR Method)", fontsize=13, y=1.02)
        plt.tight_layout()
        plt.savefig(f"step4_outliers_{name}.png", dpi=150, bbox_inches='tight')
        plt.show()
        print(f"[Saved] step4_outliers_{name}.png")
 
    # ── Cross-satellite comparison: battery voltage across all 4 sats
    fig, ax = plt.subplots(figsize=(10, 5))
    data_for_box = [dfs[n][BATT_VOLT_COL].dropna() for n in dfs if BATT_VOLT_COL in dfs[n].columns]
    labels = [n.upper() for n in dfs if BATT_VOLT_COL in dfs[n].columns]
    bps = ax.boxplot(data_for_box, patch_artist=True, labels=labels)
    for patch, name in zip(bps['boxes'], dfs.keys()):
        patch.set_facecolor(COLORS[name])
        patch.set_alpha(0.7)
    ax.set_ylabel("Battery Voltage (V)")
    ax.set_title("Cross-Satellite Battery Voltage Comparison")
    plt.tight_layout()
    plt.savefig("step4_outliers_crosssat_vbat.png", dpi=150, bbox_inches='tight')
    plt.show()
    print("[Saved] step4_outliers_crosssat_vbat.png")
    print("\n  [NOTE] Satellite outliers often represent real orbital events (eclipse entry, etc.).")
    print("         They are flagged, not dropped.")
 
    
 
# STEP 5: UNIVARIATE ANALYSIS

def univariate_analysis(dfs):
    """
    Distribution histograms + KDE for key EPS parameters per satellite.
    Also plots total solar panel current distribution (sum of all 5 faces).
    """
    print("\n" + "=" * 60)
    print("STEP 5: UNIVARIATE ANALYSIS")
    print("=" * 60)
 
    for name, df in dfs.items():
        # Select calibrated numeric columns of interest
        cols_to_plot = [c for c in PANEL_CURR_COLS + [BATT_VOLT_COL, BATT_TEMP_COL]
                        if c in df.columns]
        if not cols_to_plot:
            continue
 
        fig, axes = plt.subplots(2, len(cols_to_plot),
                                 figsize=(4 * len(cols_to_plot), 7))
 
        for i, col in enumerate(cols_to_plot):
            data = df[col].dropna()
 
            # Histogram
            axes[0, i].hist(data, bins=40, color=COLORS[name],
                            edgecolor='white', alpha=0.85)
            axes[0, i].set_title(col, fontsize=9)
            axes[0, i].set_xlabel("Value")
            axes[0, i].set_ylabel("Frequency")
 
            # KDE
            sns.kdeplot(data, ax=axes[1, i], color=COLORS[name], fill=True, alpha=0.4)
            axes[1, i].set_title(f"KDE — {col}", fontsize=9)
            axes[1, i].set_xlabel("Value")
 
        plt.suptitle(f"{name.upper()} — Univariate Distributions", fontsize=13)
        plt.tight_layout()
        plt.savefig(f"step5_univariate_{name}.png", dpi=150, bbox_inches='tight')
        plt.show()
        print(f"[Saved] step5_univariate_{name}.png")
 
    # ── Total solar current distribution across all satellites (overlaid)
    fig, ax = plt.subplots(figsize=(10, 5))
    for name, df in dfs.items():
        avail = [c for c in PANEL_CURR_COLS if c in df.columns]
        if avail:
            total_curr = df[avail].sum(axis=1)
            sns.kdeplot(total_curr, ax=ax, label=name.upper(),
                        color=COLORS[name], fill=True, alpha=0.25)
    ax.set_xlabel("Total Solar Panel Current (mA)")
    ax.set_ylabel("Density")
    ax.set_title("Total Solar Panel Current Distribution — All Satellites")
    ax.legend()
    plt.tight_layout()
    plt.savefig("step5_univariate_total_current_comparison.png", dpi=150, bbox_inches='tight')
    plt.show()
    print("[Saved] step5_univariate_total_current_comparison.png")
    

# STEP 6: TIME SERIES ANALYSIS

def time_series_analysis(dfs):
    """
    Plot battery voltage and total solar panel current over elapsed time.
    One plot per satellite, plus a cross-satellite battery voltage comparison.
    """
    print("\n" + "=" * 60)
    print("STEP 6: TIME SERIES ANALYSIS")
    print("=" * 60)
 
    for name, df in dfs.items():
        avail_curr = [c for c in PANEL_CURR_COLS if c in df.columns]
        if TIME_COL not in df.columns or BATT_VOLT_COL not in df.columns:
            print(f"  [{name.upper()}] Required columns missing, skipping.")
            continue
 
        df = df.sort_values(TIME_COL).copy()
        if avail_curr:
            df['total_panel_current_mA'] = df[avail_curr].sum(axis=1)
 
        fig, axes = plt.subplots(2, 1, figsize=(14, 7), sharex=True)
 
        axes[0].plot(df[TIME_COL], df[BATT_VOLT_COL],
                     color=COLORS[name], linewidth=1.2)
        axes[0].set_ylabel("Battery Voltage (V)")
        axes[0].set_title(f"{name.upper()} — Battery Voltage over Time")
 
        if 'total_panel_current_mA' in df.columns:
            axes[1].plot(df[TIME_COL], df['total_panel_current_mA'],
                         color=COLORS["sunlit"], linewidth=1.0)
            axes[1].set_ylabel("Total Solar Panel Current (mA)")
            axes[1].set_title("Total Panel Current (dips = eclipse entry)")
 
        axes[1].set_xlabel("Elapsed Time (s)")
        plt.tight_layout()
        plt.savefig(f"step6_timeseries_{name}.png", dpi=150, bbox_inches='tight')
        plt.show()
        print(f"[Saved] step6_timeseries_{name}.png")
 
    # ── Cross-satellite battery voltage over time
    fig, ax = plt.subplots(figsize=(14, 5))
    for name, df in dfs.items():
        if TIME_COL in df.columns and BATT_VOLT_COL in df.columns:
            df_s = df.sort_values(TIME_COL)
            ax.plot(df_s[TIME_COL], df_s[BATT_VOLT_COL],
                    label=name.upper(), color=COLORS[name],
                    linewidth=1.0, alpha=0.85)
    ax.set_xlabel("Elapsed Time (s)")
    ax.set_ylabel("Battery Voltage (V)")
    ax.set_title("Cross-Satellite Battery Voltage Comparison Over Time")
    ax.legend()
    plt.tight_layout()
    plt.savefig("step6_timeseries_crosssat_vbat.png", dpi=150, bbox_inches='tight')
    plt.show()
    print("[Saved] step6_timeseries_crosssat_vbat.png")
 
 
def eclipse_detection(dfs):
    """
    Detect eclipse vs sunlit periods using total solar panel current threshold.
    Threshold: < 5% of the median total current → eclipse.
    Adds 'eclipse_flag' column to each DataFrame.
    """
    print("\n[Eclipse Detection — All Satellites]")
 
    for name, df in dfs.items():
        avail_curr = [c for c in PANEL_CURR_COLS if c in df.columns]
        if not avail_curr:
            continue
 
        df = df.copy()
        df['total_panel_current_mA'] = df[avail_curr].sum(axis=1)
 
        median_curr = df['total_panel_current_mA'].median()
        threshold   = 0.05 * median_curr
 
        df['eclipse_flag'] = (df['total_panel_current_mA'] < threshold).astype(int)
        eclipse_pct = df['eclipse_flag'].mean() * 100
 
        print(f"  [{name.upper()}] Median total current: {median_curr:.1f} mA | "
              f"Threshold: {threshold:.1f} mA | Eclipse: {eclipse_pct:.1f}%"
              f"  (expected ~35–40% for LEO)")
        dfs[name] = df
 
    return dfs
 
    
# STEP 7: CORRELATION ANALYSIS

def correlation_analysis(dfs):
    """Compute and visualise correlation matrices for calibrated EPS columns."""
    print("\n" + "=" * 60)
    print("STEP 7: CORRELATION ANALYSIS")
    print("=" * 60)
 
    for name, df in dfs.items():
        # Use only calibrated (non-raw) numeric columns
        cal_cols = [c for c in PANEL_VOLT_COLS + PANEL_CURR_COLS + PANEL_TEMP_COLS +
                    [BATT_VOLT_COL, BATT_CURR_COL, BATT_TEMP_COL]
                    if c in df.columns]
        # Also include any engineered features that exist
        extra = [c for c in ['total_panel_current_mA', 'panel_power_W',
                              'temp_efficiency_factor', 'eclipse_flag']
                 if c in df.columns]
        cols = cal_cols + extra
 
        numeric_df = df[cols].select_dtypes(include=[np.number])
        if numeric_df.shape[1] < 2:
            continue
 
        corr = numeric_df.corr()
        print(f"\n[{name.upper()}] Correlation matrix ({corr.shape}):")
        print(corr.round(3).to_string())
 
        n = corr.shape[0]
        fig_size = max(8, n)
        plt.figure(figsize=(fig_size, fig_size - 1))
        mask = np.triu(np.ones_like(corr, dtype=bool))
        sns.heatmap(corr, mask=mask, annot=True, fmt=".2f",
                    cmap='RdYlGn', center=0, linewidths=0.5,
                    annot_kws={"size": 8})
        plt.title(f"{name.upper()} — Correlation Heatmap (EPS Columns)", fontsize=13)
        plt.xticks(rotation=45, ha='right', fontsize=8)
        plt.yticks(fontsize=8)
        plt.tight_layout()
        plt.savefig(f"step7_correlation_{name}.png", dpi=150, bbox_inches='tight')
        plt.show()
        print(f"[Saved] step7_correlation_{name}.png")
 
# STEP 8: BIVARIATE ANALYSIS

def bivariate_analysis(dfs):
    """
    Key bivariate plots for BIRDS EPS:
    1. Battery voltage vs total panel current (eclipse coloured) — per satellite
    2. Panel temperature vs panel current (face-by-face) — all satellites combined
    3. Cross-satellite: battery voltage vs battery current
    """
    print("\n" + "=" * 60)
    print("STEP 8: BIVARIATE ANALYSIS")
    print("=" * 60)
 
    # ── 1. Battery voltage vs total panel current (eclipse context)
    for name, df in dfs.items():
        if BATT_VOLT_COL not in df.columns or 'total_panel_current_mA' not in df.columns:
            continue
 
        plt.figure(figsize=(8, 5))
        color_vals = df.get('eclipse_flag', pd.Series(0, index=df.index))
        scatter = plt.scatter(df['total_panel_current_mA'], df[BATT_VOLT_COL],
                              c=color_vals, cmap='RdYlGn_r',
                              alpha=0.4, s=8)
        plt.colorbar(scatter, label="Eclipse (1) / Sunlit (0)")
        plt.xlabel("Total Solar Panel Current (mA)")
        plt.ylabel("Battery Voltage (V)")
        plt.title(f"{name.upper()} — Panel Current vs Battery Voltage\n"
                  f"(coloured by eclipse state)")
        plt.tight_layout()
        plt.savefig(f"step8_bivariate_{name}_vbat_vs_curr.png", dpi=150, bbox_inches='tight')
        plt.show()
        print(f"[Saved] step8_bivariate_{name}_vbat_vs_curr.png")
 
    # ── 2. Panel temperature vs current (per face) — all satellites combined
    fig, axes = plt.subplots(1, len(FACE_LABELS), figsize=(5 * len(FACE_LABELS), 5))
    for i, face in enumerate(FACE_LABELS):
        t_col = f'T{face} (°C)'
        i_col = f'I{face} (mA)'
        for name, df in dfs.items():
            if t_col in df.columns and i_col in df.columns:
                axes[i].scatter(df[t_col], df[i_col],
                                alpha=0.25, s=5,
                                color=COLORS[name],
                                label=name.upper())
        axes[i].set_xlabel(f"Panel Temp {face} (°C)")
        axes[i].set_ylabel(f"Panel Current {face} (mA)")
        axes[i].set_title(f"Face {face.upper()}")
        if i == 0:
            axes[i].legend(fontsize=7, markerscale=3)
    plt.suptitle("Panel Temperature vs Current — All Faces & Satellites", fontsize=13)
    plt.tight_layout()
    plt.savefig("step8_bivariate_temp_vs_current_all_faces.png", dpi=150, bbox_inches='tight')
    plt.show()
    print("[Saved] step8_bivariate_temp_vs_current_all_faces.png")
 
    # ── 3. Battery voltage vs battery current — cross-satellite overlay
    plt.figure(figsize=(9, 5))
    for name, df in dfs.items():
        if BATT_VOLT_COL in df.columns and BATT_CURR_COL in df.columns:
            plt.scatter(df[BATT_CURR_COL], df[BATT_VOLT_COL],
                        alpha=0.3, s=6, color=COLORS[name], label=name.upper())
    plt.xlabel("Battery Current (mA)")
    plt.ylabel("Battery Voltage (V)")
    plt.title("Cross-Satellite — Battery Voltage vs Battery Current")
    plt.legend()
    plt.tight_layout()
    plt.savefig("step8_bivariate_crosssat_vbat_vs_ibat.png", dpi=150, bbox_inches='tight')
    plt.show()
    print("[Saved] step8_bivariate_crosssat_vbat_vs_ibat.png")


# STEP 9: FEATURE ENGINEERING

def feature_engineering(dfs):
    """
    Create derived features for ML training:
    - total_panel_current_mA  : sum of currents across all 5 faces
    - total_panel_voltage_mV  : average voltage across active faces (sum/5)
    - panel_power_W           : total_panel_voltage_mV × total_panel_current_mA / 1e6
    - dominant_face           : face with the highest current (best-oriented panel)
    - temp_efficiency_factor  : per-face thermal efficiency (avg across faces)
    - charge_rate             : Δ battery voltage per time step
    - eclipse_flag            : already added by eclipse_detection()
    - cycle_phase             : position within ~90-min orbital cycle (0–1)
    """
    print("\n" + "=" * 60)
    print("STEP 9: FEATURE ENGINEERING")
    print("=" * 60)
 
    for name, df in dfs.items():
        df = df.copy()
 
        # ── Total & average panel quantities
        avail_curr = [c for c in PANEL_CURR_COLS if c in df.columns]
        avail_volt = [c for c in PANEL_VOLT_COLS if c in df.columns]
        avail_temp = [c for c in PANEL_TEMP_COLS if c in df.columns]
 
        if avail_curr:
            df['total_panel_current_mA'] = df[avail_curr].sum(axis=1)
 
        if avail_volt:
            df['avg_panel_voltage_mV'] = df[avail_volt].mean(axis=1)
 
        # ── Panel power (W)  =  avg_V (mV) × total_I (mA) / 1e6
        if 'avg_panel_voltage_mV' in df.columns and 'total_panel_current_mA' in df.columns:
            df['panel_power_W'] = (df['avg_panel_voltage_mV'] *
                                   df['total_panel_current_mA'] / 1e6)
 
        # ── Dominant face (face label with highest current at each timestep)
        if avail_curr:
            face_labels_avail = [f.replace('(mA)', '').strip() for f in avail_curr]
            # Map back to short names
            face_map = {c: f for c, f in zip(avail_curr, FACE_LABELS[:len(avail_curr)])}
            df['dominant_face'] = df[avail_curr].idxmax(axis=1).map(face_map)
 
        # ── Average temperature-efficiency factor across faces
        if avail_temp:
            avg_temp = df[avail_temp].mean(axis=1)
            df['temp_efficiency_factor'] = 1 - 0.004 * (avg_temp - 25).clip(lower=0)
 
        # ── Battery charge rate (delta V per sample)
        if BATT_VOLT_COL in df.columns:
            df['charge_rate_V_per_sample'] = df[BATT_VOLT_COL].diff().fillna(0)
 
        # ── Cycle phase (0–1 within ~90-min orbit, assuming 5s sampling)
        samples_per_orbit = int(90 * 60 / 5)  # 1080 samples for 90 min at 5s cadence
        df['cycle_phase'] = (df.index % samples_per_orbit) / samples_per_orbit
 
        dfs[name] = df
 
        new_features = ['total_panel_current_mA', 'avg_panel_voltage_mV',
                        'panel_power_W', 'dominant_face',
                        'temp_efficiency_factor', 'charge_rate_V_per_sample',
                        'cycle_phase']
        added = [f for f in new_features if f in df.columns]
        print(f"  [{name.upper()}] New features: {added}")
 
    # ── Visualise panel power over time for all satellites
    fig, ax = plt.subplots(figsize=(14, 5))
    for name, df in dfs.items():
        if TIME_COL in df.columns and 'panel_power_W' in df.columns:
            df_s = df.sort_values(TIME_COL)
            ax.plot(df_s[TIME_COL], df_s['panel_power_W'],
                    label=name.upper(), color=COLORS[name],
                    linewidth=1.0, alpha=0.85)
    ax.set_xlabel("Elapsed Time (s)")
    ax.set_ylabel("Estimated Solar Panel Power (W)")
    ax.set_title("Cross-Satellite Solar Panel Power Generation")
    ax.legend()
    plt.tight_layout()
    plt.savefig("step9_panel_power_comparison.png", dpi=150, bbox_inches='tight')
    plt.show()
    print("[Saved] step9_panel_power_comparison.png")
 
    return dfs


# STEP 10: EDA SUMMARY REPORT


def generate_eda_summary(dfs):
    """Print a clean EDA summary report for all 4 satellites."""
    print("\n" + "=" * 60)
    print("STEP 10: EDA SUMMARY REPORT")
    print("=" * 60)
 
    for name, df in dfs.items():
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        print(f"\n{'─' * 50}")
        print(f"Satellite   : {name.upper()}")
        print(f"Shape       : {df.shape[0]:,} rows × {df.shape[1]} columns")
        print(f"Missing     : {df.isnull().sum().sum()} total cells")
        print(f"Duplicates  : {df.duplicated().sum()}")
        print(f"Numeric cols: {len(numeric_cols)}")
 
        if 'eclipse_flag' in df.columns:
            ec = df['eclipse_flag'].mean() * 100
            print(f"Eclipse %   : {ec:.1f}%")
 
        if 'panel_power_W' in df.columns:
            print(f"Panel Power : min={df['panel_power_W'].min():.3f} W | "
                  f"mean={df['panel_power_W'].mean():.3f} W | "
                  f"max={df['panel_power_W'].max():.3f} W")
 
        if 'dominant_face' in df.columns:
            dom = df['dominant_face'].value_counts()
            print(f"Dominant face distribution:\n{dom.to_string()}")
 
        # Top correlations with panel_power_W
        if 'panel_power_W' in df.columns:
            corr = df[numeric_cols].corr()['panel_power_W'].drop('panel_power_W')
            top = corr.abs().sort_values(ascending=False).head(5)
            print(f"Top features correlated with panel_power_W:")
            for feat, val in top.items():
                direction = "+" if corr[feat] > 0 else "-"
                print(f"    {direction}{val:.3f}  {feat}")
 
    print("\n[EDA COMPLETE] All plots saved. Cleaned DataFrames ready for ML pipeline.")
    print("Next step: split train/test sets and begin model selection.")
    
    
