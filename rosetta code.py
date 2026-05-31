# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 09:47:58 2026

@author: ADMIN
"""

"""
EDA — Rosetta Spacecraft Solar Array & Power Engineering Data
PDS3 LBL/TAB format  |  2016 Q3 housekeeping telemetry
Intelligent Power Generation for Satellites Using ML-Driven Orientation Systems
Group 6 | Dept. of Aerospace Engineering | MIT-ADT University

Each dataset = one .lbl (metadata) + one .tab (time-series data)
TAB format  : ISO-8601 timestamp , VALUE  (2 columns, comma-separated)
Parameters  : master bus voltage · PCU voltage · PDU primary current
              SA incidence angle · SA measured angle · SA misalignment

Required:  pip install pandas numpy matplotlib seaborn scipy
"""

"""
EDA — Rosetta Spacecraft Solar Array & Power Engineering Data
PDS3 LBL/TAB format  |  2016 Q3 housekeeping telemetry
Intelligent Power Generation for Satellites Using ML-Driven Orientation Systems
Group 6 | Dept. of Aerospace Engineering | MIT-ADT University

Each dataset = one .lbl (metadata) + one .tab (time-series data)
TAB format  : ISO-8601 timestamp , VALUE  (2 columns, comma-separated)
Parameters  : master bus voltage · PCU voltage · PDU primary current
              SA incidence angle · SA measured angle · SA misalignment

Required:  pip install pandas numpy matplotlib seaborn scipy
"""

import os
import re
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from scipy import stats

warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────────────────────
# FILE PATHS  ←  update if you move the files
# ─────────────────────────────────────────────────────────────
BASE = r"C:\Users\ADMIN\Desktop\ROSETTA"

FILES = {
    "master_bus_voltage_V": {
        "lbl": os.path.join(BASE, "master bus voltage",                   "ros_hk_npwd1024_2016_q2.lbl"),
        "tab": os.path.join(BASE, "master bus voltage",                   "ros_hk_npwd1024_2016_q2.tab"),
    },
    "pcu_voltage_V": {
        "lbl": os.path.join(BASE, "power control unit volt",              "ros_hk_npwd1704_2016_06.lbl"),
        "tab": os.path.join(BASE, "power control unit volt",              "ros_hk_npwd1704_2016_06.tab"),
    },
    "pdu_primary_current_A": {
        "lbl": os.path.join(BASE, "power dist unit primary current",      "ros_hk_npwd2920_2016_q2.lbl"),
        "tab": os.path.join(BASE, "power dist unit primary current",      "ros_hk_npwd2920_2016_q2.tab"),
    },
    "sa_incidence_angle_deg": {
        "lbl": os.path.join(BASE, "solar array incidence angle",          "ros_hk_nawg0026_2016_06.lbl"),
        "tab": os.path.join(BASE, "solar array incidence angle",          "ros_hk_nawg0026_2016_06.tab"),
    },
    "sa_meas_angle_pos_deg": {
        "lbl": os.path.join(BASE, "solar array measure angle pos deg",    "ros_hk_nacx0021_2016_q2.lbl"),
        "tab": os.path.join(BASE, "solar array measure angle pos deg",    "ros_hk_nacx0021_2016_q2.tab"),
    },
    "sa_misalignment_deg": {
        "lbl": os.path.join(BASE, "solar array misalignment",             "ros_hk_nacx0022_2016_06.lbl"),
        "tab": os.path.join(BASE, "solar array misalignment",             "ros_hk_nacx0022_2016_06.tab"),
    },
}

# Output directory for plots & clean CSV
OUT_DIR = os.path.join(BASE, "EDA_outputs")

# ─────────────────────────────────────────────────────────────
# PARAMETER METADATA  (units, physical description, thresholds)
# ─────────────────────────────────────────────────────────────
PARAM_INFO = {
    "master_bus_voltage_V": {
        "label"    : "Master Bus Voltage (V)",
        "unit"     : "V",
        "color"    : "#185FA5",
        "nominal"  : (27.5, 29.5),          # expected nominal range
        "desc"     : "MBUS voltage — PCU CM-A/B. Primary power bus of Rosetta. "
                     "Deviation from ~28 V indicates power anomaly.",
    },
    "pcu_voltage_V": {
        "label"    : "PCU Auxiliary Voltage (V)",
        "unit"     : "V",
        "color"    : "#1D9E75",
        "nominal"  : (4.5, 5.5),
        "desc"     : "Power Control Unit CM-A auxiliary supply voltage. "
                     "Used to power secondary electronics.",
    },
    "pdu_primary_current_A": {
        "label"    : "PDU Primary Current (A)",
        "unit"     : "A",
        "color"    : "#BA7517",
        "nominal"  : (0.0, 5.0),
        "desc"     : "Power Distribution Unit SS-PDU primary current. "
                     "Indicates total load drawn from the solar array power chain.",
    },
    "sa_incidence_angle_deg": {
        "label"    : "SA Incidence Angle (deg)",
        "unit"     : "deg",
        "color"    : "#ff7f0e",
        "nominal"  : (-90.0, 90.0),
        "desc"     : "Angle between the solar array normal and the Sun direction. "
                     "0° = perfect face-on; irradiance ∝ cos(angle).",
    },
    "sa_meas_angle_pos_deg": {
        "label"    : "SA Measured Angle Position (deg)",
        "unit"     : "deg",
        "color"    : "#534AB7",
        "nominal"  : (-180.0, 180.0),
        "desc"     : "SADE measured angular position of solar array Y+ wing. "
                     "Tracks actual rotation vs. commanded.",
    },
    "sa_misalignment_deg": {
        "label"    : "SA Misalignment (deg)",
        "unit"     : "deg",
        "color"    : "#d62728",
        "nominal"  : (-5.0, 5.0),
        "desc"     : "Difference between commanded and measured SA angle. "
                     "Large values → power losses due to pointing error.",
    },
}

try:
    plt.style.use('seaborn-v0_8-whitegrid')
except OSError:
    plt.style.use('seaborn-whitegrid')

os.makedirs(OUT_DIR, exist_ok=True)


# ─────────────────────────────────────────────────────────────
# UTILITY
# ─────────────────────────────────────────────────────────────
def savefig(name):
    path = os.path.join(OUT_DIR, name)
    plt.savefig(path, dpi=150, bbox_inches='tight')
    print(f"  [Saved] {path}")


def color(key):
    return PARAM_INFO.get(key, {}).get("color", "#185FA5")


def label(key):
    return PARAM_INFO.get(key, {}).get("label", key)


# ─────────────────────────────────────────────────────────────
# STEP 1: PARSE LBL FILES
# ─────────────────────────────────────────────────────────────
def parse_lbl(lbl_path):
    """
    Parse a PDS3 .lbl file and return a dict of key metadata fields.
    Handles multi-line string values and keyword = value format.
    """
    meta = {}
    if not os.path.exists(lbl_path):
        return meta

    with open(lbl_path, 'r', errors='replace') as f:
        content = f.read()

    # Key fields to extract
    fields = [
        "DATA_SET_NAME", "PRODUCT_ID", "START_TIME", "STOP_TIME",
        "FILE_RECORDS", "RECORD_BYTES", "ROWS", "COLUMNS",
        "ROSETTA:SUBSYSTEM_DATA_TYPE", "DESCRIPTION",
    ]

    for field in fields:
        pattern = rf'{field}\s*=\s*"?([^"\r\n]+)"?'
        match = re.search(pattern, content)
        if match:
            meta[field] = match.group(1).strip()

    # Units for VALUE column
    unit_match = re.search(r'NAME\s*=\s*"VALUE".*?UNIT\s*=\s*"([^"]+)"',
                           content, re.DOTALL)
    if unit_match:
        meta["VALUE_UNIT"] = unit_match.group(1).strip()

    return meta


# ─────────────────────────────────────────────────────────────
# STEP 2: LOAD ALL TAB FILES
# ─────────────────────────────────────────────────────────────
def load_datasets():
    """
    Load all 6 TAB files into a dict of DataFrames.
    Each DataFrame has columns: [timestamp, value]
    The parameter name (key) becomes the value column name.
    """
    print("\n" + "=" * 60)
    print("STEP 1–2: LOADING DATASETS")
    print("=" * 60)

    dfs  = {}
    meta = {}

    for param, paths in FILES.items():
        tab_path = paths["tab"]
        lbl_path = paths["lbl"]

        # Parse metadata from LBL
        lbl_meta = parse_lbl(lbl_path)
        meta[param] = lbl_meta

        if not os.path.exists(tab_path):
            print(f"  [--] {param:<35}  TAB not found: {tab_path}")
            continue

        # Read TAB: 2 columns, comma-separated, fixed-width
        # Column 1: ISO timestamp (23 chars), Column 2: float in scientific notation
        df = pd.read_csv(
            tab_path,
            header=None,
            names=["timestamp", param],
            sep=",",
            skipinitialspace=True,
            parse_dates=["timestamp"],
        )

        df["timestamp"] = pd.to_datetime(df["timestamp"], format="ISO8601", errors='coerce')
        df[param]       = pd.to_numeric(df[param], errors='coerce')
        df              = df.dropna(subset=["timestamp"]).sort_values("timestamp")
        df              = df.set_index("timestamp")

        dfs[param] = df

        start = lbl_meta.get("START_TIME", "?")
        stop  = lbl_meta.get("STOP_TIME",  "?")
        rows  = lbl_meta.get("FILE_RECORDS", str(len(df)))
        unit  = lbl_meta.get("VALUE_UNIT",   "?")

        print(f"  [OK] {param:<35}  {int(rows):>7,} rows  "
              f"unit={unit:<4}  {start[:10]} → {stop[:10]}")

    print(f"\n  {len(dfs)} / {len(FILES)} parameters loaded.")
    return dfs, meta


# ─────────────────────────────────────────────────────────────
# STEP 3: LABEL METADATA REPORT
# ─────────────────────────────────────────────────────────────
def print_metadata(meta):
    print("\n" + "=" * 60)
    print("STEP 3: LBL METADATA SUMMARY")
    print("=" * 60)

    for param, m in meta.items():
        print(f"\n  ── {param} ──")
        for k, v in m.items():
            print(f"     {k:<35} {v}")


# ─────────────────────────────────────────────────────────────
# STEP 4: BASIC INSPECTION
# ─────────────────────────────────────────────────────────────
def basic_inspection(dfs):
    print("\n" + "=" * 60)
    print("STEP 4: BASIC INSPECTION")
    print("=" * 60)

    rows = []
    for param, df in dfs.items():
        col   = df[param]
        info  = PARAM_INFO.get(param, {})
        rows.append({
            "Parameter"  : param,
            "Records"    : len(df),
            "Start"      : df.index.min().strftime("%Y-%m-%d"),
            "End"        : df.index.max().strftime("%Y-%m-%d"),
            "Mean"       : round(col.mean(), 4),
            "Std"        : round(col.std(), 4),
            "Min"        : round(col.min(), 4),
            "Max"        : round(col.max(), 4),
            "Unit"       : info.get("unit", "?"),
            "NaN count"  : col.isna().sum(),
        })

    summary = pd.DataFrame(rows)
    print(f"\n{summary.to_string(index=False)}")

    for param, df in dfs.items():
        print(f"\n  {param} — first 3 rows:")
        print(df.head(3).to_string())

    return summary


# ─────────────────────────────────────────────────────────────
# STEP 5: MISSING VALUE ANALYSIS
# ─────────────────────────────────────────────────────────────
def missing_value_analysis(dfs):
    print("\n" + "=" * 60)
    print("STEP 5: MISSING VALUES ANALYSIS")
    print("=" * 60)

    report = {}
    for param, df in dfs.items():
        col         = df[param]
        nan_n       = col.isna().sum()
        nan_pct     = nan_n / len(df) * 100
        zero_n      = (col == 0).sum()
        report[param] = {"NaN count": nan_n, "NaN %": round(nan_pct, 3),
                          "Zero count": zero_n}
        print(f"  {param:<35}  NaN={nan_n:,} ({nan_pct:.3f}%)   zeros={zero_n:,}")

    fig, ax = plt.subplots(figsize=(14, 5))
    params  = list(report.keys())
    nan_pcts = [report[p]["NaN %"] for p in params]
    short_labels = [p.replace("_", "\n") for p in params]

    bars = ax.bar(short_labels, nan_pcts,
                  color=[color(p) for p in params], edgecolor='black', alpha=0.85)
    ax.set_ylabel("Missing %")
    ax.set_title("Rosetta HK — Missing Values per Parameter")
    for bar, v in zip(bars, nan_pcts):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 0.01,
                f"{v:.3f}%", ha='center', fontsize=8)

    plt.tight_layout()
    savefig("step5_missing_values.png")
    plt.show()

    return report


# ─────────────────────────────────────────────────────────────
# STEP 6: OUTLIER DETECTION
# ─────────────────────────────────────────────────────────────
def detect_outliers_iqr(series):
    Q1, Q3 = series.quantile(0.25), series.quantile(0.75)
    IQR = Q3 - Q1
    return (series < Q1 - 1.5 * IQR) | (series > Q3 + 1.5 * IQR)


def outlier_analysis(dfs):
    print("\n" + "=" * 60)
    print("STEP 6: OUTLIER DETECTION (IQR Method)")
    print("=" * 60)

    n_params = len(dfs)
    fig, axes = plt.subplots(2, 3, figsize=(18, 9))
    axes = axes.flatten()

    for i, (param, df) in enumerate(dfs.items()):
        col      = df[param].dropna()
        out_mask = detect_outliers_iqr(col)
        out_n    = out_mask.sum()
        out_pct  = out_n / len(col) * 100
        print(f"  {param:<35}  outliers: {out_n:,} ({out_pct:.3f}%)")

        axes[i].boxplot(col, patch_artist=True,
                        boxprops=dict(facecolor=color(param), alpha=0.55),
                        medianprops=dict(color='black', linewidth=2),
                        flierprops=dict(marker='.', markersize=2,
                                        markerfacecolor=color(param), alpha=0.4))
        nom = PARAM_INFO.get(param, {}).get("nominal")
        if nom:
            axes[i].axhline(nom[0], color='green',  linewidth=1,
                            linestyle='--', label=f"low {nom[0]}")
            axes[i].axhline(nom[1], color='orange', linewidth=1,
                            linestyle='--', label=f"high {nom[1]}")
            axes[i].legend(fontsize=7)
        axes[i].set_title(f"{label(param)}\n({out_n:,} IQR outliers)", fontsize=9)
        axes[i].set_ylabel(PARAM_INFO.get(param, {}).get("unit", ""))

    for j in range(i + 1, 6):
        axes[j].set_visible(False)

    plt.suptitle("Rosetta HK — Outlier Detection (IQR, dashed = nominal range)",
                 fontsize=13)
    plt.tight_layout()
    savefig("step6_outliers.png")
    plt.show()

    print("\n  [NOTE] Outliers in Rosetta data likely represent:")
    print("         • eclipse entry/exit  • comet closest approach manoeuvres")
    print("         • thruster firings    • end-of-mission power-down sequence")


# ─────────────────────────────────────────────────────────────
# STEP 7: UNIVARIATE ANALYSIS
# ─────────────────────────────────────────────────────────────
def univariate_analysis(dfs):
    print("\n" + "=" * 60)
    print("STEP 7: UNIVARIATE ANALYSIS")
    print("=" * 60)

    fig, axes = plt.subplots(2, 3, figsize=(18, 9))
    axes = axes.flatten()

    for i, (param, df) in enumerate(dfs.items()):
        col  = df[param].dropna()
        ax   = axes[i]
        c    = color(param)

        ax.hist(col, bins=80, color=c, edgecolor='white', alpha=0.8)
        ax.axvline(col.mean(),   color='black',  linewidth=2,
                   linestyle='--', label=f"mean={col.mean():.3f}")
        ax.axvline(col.median(), color='gray',   linewidth=1.5,
                   linestyle=':',  label=f"median={col.median():.3f}")

        nom = PARAM_INFO.get(param, {}).get("nominal")
        if nom:
            ax.axvspan(nom[0], nom[1], alpha=0.08, color='green',
                       label=f"nominal {nom}")

        ax.set_title(label(param), fontsize=10)
        ax.set_xlabel(PARAM_INFO.get(param, {}).get("unit", ""))
        ax.set_ylabel("Count")
        ax.legend(fontsize=7)

        skew = stats.skew(col)
        kurt = stats.kurtosis(col)
        ax.text(0.97, 0.95, f"skew={skew:.2f}\nkurt={kurt:.2f}",
                transform=ax.transAxes, ha='right', va='top',
                fontsize=8, color='dimgray')

    plt.suptitle("Rosetta HK — Univariate Distributions (Q3 2016)", fontsize=14)
    plt.tight_layout()
    savefig("step7_univariate.png")
    plt.show()

    # KDE overlay (all params in common units on same scale would not make sense
    # — plot per-family instead)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Electrical params
    elec = ["master_bus_voltage_V", "pcu_voltage_V"]
    for p in elec:
        if p in dfs:
            sns.kdeplot(dfs[p][p].dropna(), ax=axes[0],
                        label=label(p), color=color(p), fill=True, alpha=0.3)
    axes[0].set_title("KDE — Voltage Parameters")
    axes[0].set_xlabel("Voltage (V)")
    axes[0].legend(fontsize=8)

    # SA angle params
    angle_params = ["sa_incidence_angle_deg", "sa_meas_angle_pos_deg", "sa_misalignment_deg"]
    for p in angle_params:
        if p in dfs:
            sns.kdeplot(dfs[p][p].dropna(), ax=axes[1],
                        label=label(p), color=color(p), fill=True, alpha=0.25)
    axes[1].set_title("KDE — Solar Array Angle Parameters")
    axes[1].set_xlabel("Angle (deg)")
    axes[1].legend(fontsize=8)

    plt.suptitle("Rosetta HK — KDE by Parameter Family", fontsize=13)
    plt.tight_layout()
    savefig("step7_kde.png")
    plt.show()


# ─────────────────────────────────────────────────────────────
# STEP 8: TIME SERIES ANALYSIS
# ─────────────────────────────────────────────────────────────
def time_series_analysis(dfs):
    print("\n" + "=" * 60)
    print("STEP 8: TIME SERIES ANALYSIS")
    print("=" * 60)

    # ── Full Q3 overview
    fig, axes = plt.subplots(6, 1, figsize=(16, 20), sharex=False)

    for i, (param, df) in enumerate(dfs.items()):
        col    = df[param].dropna()
        ax     = axes[i]

        # Raw data (subsampled if very dense)
        step = max(1, len(col) // 5000)
        ax.plot(col.index[::step], col.values[::step],
                color=color(param), linewidth=0.5, alpha=0.5, label="raw")

        # Daily mean
        daily = col.resample('1D').mean().dropna()
        ax.plot(daily.index, daily.values, color='black',
                linewidth=1.8, label="daily mean")

        nom = PARAM_INFO.get(param, {}).get("nominal")
        if nom:
            ax.axhspan(nom[0], nom[1], alpha=0.07, color='green',
                       label=f"nominal {nom}")

        ax.set_ylabel(f"{PARAM_INFO[param]['unit']}", fontsize=9)
        ax.set_title(label(param), fontsize=10)
        ax.legend(fontsize=7, loc='upper right')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=30)

    plt.suptitle("Rosetta HK — Full Q3 2016 Time Series", fontsize=14, y=1.001)
    plt.tight_layout()
    savefig("step8_timeseries_overview.png")
    plt.show()

    # ── September zoom (params that cover only Sep)
    sep_params = ["pcu_voltage_V", "sa_incidence_angle_deg", "sa_misalignment_deg"]
    sep_avail  = [p for p in sep_params if p in dfs]

    if sep_avail:
        fig, axes = plt.subplots(len(sep_avail), 1, figsize=(14, 4 * len(sep_avail)),
                                 sharex=True)
        if len(sep_avail) == 1:
            axes = [axes]

        for ax, param in zip(axes, sep_avail):
            df  = dfs[param]
            col = df[param].dropna()
            ax.plot(col.index, col.values,
                    color=color(param), linewidth=0.8, alpha=0.7)
            # 6-hour rolling mean
            rolled = col.resample('6h').mean().dropna()
            ax.plot(rolled.index, rolled.values, color='black',
                    linewidth=2, label="6-hr mean")
            ax.set_ylabel(PARAM_INFO[param]["unit"])
            ax.set_title(label(param))
            ax.legend(fontsize=8)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))

        axes[-1].set_xlabel("Date (Sep 2016)")
        plt.suptitle("Rosetta HK — September 2016 Zoom", fontsize=13)
        plt.tight_layout()
        savefig("step8_timeseries_sep_zoom.png")
        plt.show()

    # ── Short zoom: first 48 hours of bus voltage
    if "master_bus_voltage_V" in dfs:
        df  = dfs["master_bus_voltage_V"]
        col = df["master_bus_voltage_V"].dropna()
        t48 = col.index.min() + pd.Timedelta(hours=48)
        seg = col[col.index <= t48]

        fig, ax = plt.subplots(figsize=(14, 4))
        ax.plot(seg.index, seg.values, color=color("master_bus_voltage_V"),
                linewidth=1.2)
        ax.set_title("Master Bus Voltage — First 48 Hours (Jul 1–2 2016)")
        ax.set_ylabel("Voltage (V)")
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b %H:%M'))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=30)
        plt.tight_layout()
        savefig("step8_mbus_48hr_zoom.png")
        plt.show()


# ─────────────────────────────────────────────────────────────
# STEP 9: POWER ANALYSIS
# ─────────────────────────────────────────────────────────────
def power_analysis(dfs):
    """
    Core analysis for the ML project:
    - Estimated solar array power  P = V × I
    - Power efficiency vs SA misalignment
    - Power efficiency vs SA incidence angle (irradiance ∝ cos(θ))
    """
    print("\n" + "=" * 60)
    print("STEP 9: POWER ANALYSIS")
    print("=" * 60)

    v_key = "master_bus_voltage_V"
    i_key = "pdu_primary_current_A"

    if v_key not in dfs or i_key not in dfs:
        print("  Bus voltage or PDU current not available — skipping.")
        return None

    # Resample both to 1-minute mean to align timestamps
    v = dfs[v_key][v_key].resample('1min').mean()
    i = dfs[i_key][i_key].resample('1min').mean()

    power = (v * i).dropna()
    power.name = "sa_power_W"
    print(f"  Power series: {len(power):,} 1-min samples")
    print(f"  Power range : {power.min():.1f} – {power.max():.1f} W")
    print(f"  Mean power  : {power.mean():.1f} W")

    fig, axes = plt.subplots(2, 2, figsize=(16, 10))

    # 1. Power over time
    daily_pow = power.resample('1D').mean().dropna()
    axes[0, 0].plot(daily_pow.index, daily_pow.values,
                    color="#185FA5", linewidth=1.8)
    axes[0, 0].fill_between(daily_pow.index, 0, daily_pow.values,
                             color="#185FA5", alpha=0.15)
    axes[0, 0].set_title("Estimated Solar Array Power (daily mean)")
    axes[0, 0].set_ylabel("Power (W)")
    axes[0, 0].xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))

    # 2. Power distribution
    axes[0, 1].hist(power, bins=80, color="#185FA5", edgecolor='white', alpha=0.8)
    axes[0, 1].axvline(power.mean(), color='black', linewidth=2,
                       linestyle='--', label=f"mean={power.mean():.1f} W")
    axes[0, 1].set_title("Power Distribution")
    axes[0, 1].set_xlabel("Power (W)")
    axes[0, 1].set_ylabel("Count (1-min bins)")
    axes[0, 1].legend()

    # 3. Power vs SA incidence angle
    if "sa_incidence_angle_deg" in dfs:
        ang = dfs["sa_incidence_angle_deg"]["sa_incidence_angle_deg"].resample('1min').mean()
        merged = pd.concat([power, ang], axis=1).dropna()
        merged.columns = ["power_W", "incidence_deg"]

        axes[1, 0].scatter(merged["incidence_deg"], merged["power_W"],
                           alpha=0.15, s=3, color="#ff7f0e")
        # Theoretical cos curve
        θ = np.linspace(merged["incidence_deg"].min(),
                        merged["incidence_deg"].max(), 200)
        p_max = merged["power_W"].max()
        axes[1, 0].plot(θ, p_max * np.cos(np.deg2rad(np.abs(θ))),
                        color='black', linewidth=2,
                        label="P_max × cos(|θ|)  (theoretical)")
        axes[1, 0].set_xlabel("SA Incidence Angle (deg)")
        axes[1, 0].set_ylabel("Power (W)")
        axes[1, 0].set_title("Power vs SA Incidence Angle\n"
                             "(key relationship for ML model)")
        axes[1, 0].legend(fontsize=8)

        r, p_val = stats.pearsonr(merged["incidence_deg"], merged["power_W"])
        print(f"\n  Pearson r (power vs incidence angle) : {r:.4f}  p={p_val:.2e}")

    # 4. Power vs SA misalignment
    if "sa_misalignment_deg" in dfs:
        mis = dfs["sa_misalignment_deg"]["sa_misalignment_deg"].resample('1min').mean()
        merged2 = pd.concat([power, mis], axis=1).dropna()
        merged2.columns = ["power_W", "misalignment_deg"]

        axes[1, 1].scatter(merged2["misalignment_deg"], merged2["power_W"],
                           alpha=0.15, s=3, color="#d62728")
        axes[1, 1].set_xlabel("SA Misalignment (deg)")
        axes[1, 1].set_ylabel("Power (W)")
        axes[1, 1].set_title("Power vs SA Misalignment\n"
                             "(misalignment → power loss)")

        r2, _ = stats.pearsonr(merged2["misalignment_deg"].abs(),
                               merged2["power_W"])
        print(f"  Pearson r (power vs |misalignment|)  : {r2:.4f}")

    plt.suptitle("Rosetta — Solar Array Power Analysis", fontsize=14)
    plt.tight_layout()
    savefig("step9_power_analysis.png")
    plt.show()

    return power


# ─────────────────────────────────────────────────────────────
# STEP 10: SOLAR ARRAY GEOMETRY ANALYSIS
# ─────────────────────────────────────────────────────────────
def sa_geometry_analysis(dfs):
    """
    Analyse the three SA angle parameters together:
    incidence angle, measured position, misalignment.
    Key for understanding pointing efficiency and ADCS performance.
    """
    print("\n" + "=" * 60)
    print("STEP 10: SOLAR ARRAY GEOMETRY ANALYSIS")
    print("=" * 60)

    sa_params = {
        "sa_incidence_angle_deg" : ("SA Incidence Angle (deg)", "#ff7f0e"),
        "sa_meas_angle_pos_deg"  : ("SA Measured Pos (deg)",    "#534AB7"),
        "sa_misalignment_deg"    : ("SA Misalignment (deg)",    "#d62728"),
    }

    available = {k: v for k, v in sa_params.items() if k in dfs}
    if not available:
        print("  No SA geometry data available.")
        return

    fig, axes = plt.subplots(2, 2, figsize=(16, 10))

    # 1. Misalignment distribution with ±1° / ±3° lines
    if "sa_misalignment_deg" in dfs:
        mis = dfs["sa_misalignment_deg"]["sa_misalignment_deg"].dropna()
        axes[0, 0].hist(mis, bins=80, color="#d62728", edgecolor='white', alpha=0.8)
        for v, lbl_text, c in [(1, '±1°', 'green'), (3, '±3°', 'orange')]:
            axes[0, 0].axvline( v, color=c, linewidth=1.8, linestyle='--', label=lbl_text)
            axes[0, 0].axvline(-v, color=c, linewidth=1.8, linestyle='--')
        axes[0, 0].set_title("SA Misalignment Distribution")
        axes[0, 0].set_xlabel("Misalignment (deg)")
        axes[0, 0].set_ylabel("Count")
        axes[0, 0].legend()
        pct_1deg = (mis.abs() <= 1).mean() * 100
        pct_3deg = (mis.abs() <= 3).mean() * 100
        print(f"  SA misalignment ≤ 1° : {pct_1deg:.1f}%  |  ≤ 3° : {pct_3deg:.1f}%")

    # 2. Incidence angle distribution
    if "sa_incidence_angle_deg" in dfs:
        inc = dfs["sa_incidence_angle_deg"]["sa_incidence_angle_deg"].dropna()
        axes[0, 1].hist(inc, bins=80, color="#ff7f0e", edgecolor='white', alpha=0.8)
        axes[0, 1].axvline(0, color='black', linewidth=2,
                           linestyle='--', label='0° = face-on')
        axes[0, 1].set_title("SA Incidence Angle Distribution")
        axes[0, 1].set_xlabel("Incidence Angle (deg)")
        axes[0, 1].set_ylabel("Count")
        axes[0, 1].legend()
        near_normal = (inc.abs() <= 10).mean() * 100
        print(f"  SA within 10° of normal : {near_normal:.1f}%")

    # 3. Measured angle position over time
    if "sa_meas_angle_pos_deg" in dfs:
        col = dfs["sa_meas_angle_pos_deg"]["sa_meas_angle_pos_deg"].dropna()
        step = max(1, len(col) // 4000)
        axes[1, 0].plot(col.index[::step], col.values[::step],
                        color="#534AB7", linewidth=0.6, alpha=0.6)
        axes[1, 0].set_title("SA Measured Angle Position (Y+ wing)")
        axes[1, 0].set_ylabel("Angle (deg)")
        axes[1, 0].set_xlabel("Date")
        axes[1, 0].xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))

    # 4. Misalignment vs incidence angle scatter
    if all(k in dfs for k in ["sa_misalignment_deg", "sa_incidence_angle_deg"]):
        mis = dfs["sa_misalignment_deg"]["sa_misalignment_deg"].resample('1min').mean()
        inc = dfs["sa_incidence_angle_deg"]["sa_incidence_angle_deg"].resample('1min').mean()
        merged = pd.concat([mis, inc], axis=1).dropna()
        merged.columns = ["misalignment", "incidence"]

        axes[1, 1].hexbin(merged["incidence"], merged["misalignment"],
                          gridsize=40, cmap='Oranges')
        axes[1, 1].set_xlabel("Incidence Angle (deg)")
        axes[1, 1].set_ylabel("Misalignment (deg)")
        axes[1, 1].set_title("SA Incidence Angle vs Misalignment\n"
                             "(large incidence → higher misalignment risk)")

    plt.suptitle("Rosetta — Solar Array Geometry Analysis", fontsize=14)
    plt.tight_layout()
    savefig("step10_sa_geometry.png")
    plt.show()


# ─────────────────────────────────────────────────────────────
# STEP 11: CORRELATION ANALYSIS
# ─────────────────────────────────────────────────────────────
def correlation_analysis(dfs):
    print("\n" + "=" * 60)
    print("STEP 11: CORRELATION ANALYSIS")
    print("=" * 60)

    # Resample everything to 1-minute mean and merge
    resampled = {}
    for param, df in dfs.items():
        resampled[param] = df[param].resample('1min').mean()

    merged = pd.DataFrame(resampled).dropna()
    print(f"  Merged DataFrame (1-min aligned): {merged.shape[0]:,} rows × {merged.shape[1]} cols")

    if merged.empty:
        print("  Insufficient overlapping time → correlation skipped.")
        return merged

    corr = merged.corr()
    print(f"\n  Correlation matrix:\n{corr.round(4).to_string()}")

    fig, axes = plt.subplots(1, 2, figsize=(18, 7))

    # Heatmap
    mask = np.triu(np.ones_like(corr, dtype=bool))
    # Shorten labels for heatmap
    short = {p: p.replace("_deg", "°").replace("_V", "(V)").replace("_A", "(A)")
                 .replace("master_bus_voltage", "mbus_volt")
                 .replace("pcu_voltage", "pcu_volt")
                 .replace("pdu_primary_current", "pdu_curr")
                 .replace("sa_", "SA_")
             for p in merged.columns}
    corr.index   = [short[p] for p in corr.index]
    corr.columns = [short[p] for p in corr.columns]

    sns.heatmap(corr, mask=mask, annot=True, fmt=".3f",
                cmap='RdYlGn', center=0, ax=axes[0],
                linewidths=0.5, annot_kws={"size": 10})
    axes[0].set_title("Correlation Heatmap — All Parameters (1-min aligned)")
    axes[0].tick_params(axis='x', rotation=35, labelsize=9)
    axes[0].tick_params(axis='y', labelsize=9)

    # Scatter: bus voltage vs PDU current (power relationship)
    if "master_bus_voltage_V" in dfs and "pdu_primary_current_A" in dfs:
        v_s = dfs["master_bus_voltage_V"]["master_bus_voltage_V"].resample('1min').mean()
        i_s = dfs["pdu_primary_current_A"]["pdu_primary_current_A"].resample('1min').mean()
        both = pd.concat([v_s, i_s], axis=1).dropna()
        both.columns = ["voltage", "current"]

        axes[1].scatter(both["voltage"], both["current"],
                        alpha=0.2, s=4, color="#185FA5")
        axes[1].set_xlabel("Master Bus Voltage (V)")
        axes[1].set_ylabel("PDU Primary Current (A)")
        axes[1].set_title("Bus Voltage vs PDU Current\n"
                          "(product = estimated SA power)")

    plt.suptitle("Rosetta HK — Correlation Analysis", fontsize=14)
    plt.tight_layout()
    savefig("step11_correlation.png")
    plt.show()

    return merged


# ─────────────────────────────────────────────────────────────
# STEP 12: FEATURE ENGINEERING
# ─────────────────────────────────────────────────────────────
def feature_engineering(dfs):
    print("\n" + "=" * 60)
    print("STEP 12: FEATURE ENGINEERING")
    print("=" * 60)

    # Resample all to 1-min and merge
    frames = {p: dfs[p][p].resample('1min').mean() for p in dfs}
    df = pd.DataFrame(frames).sort_index()

    # 1. Estimated SA power
    if "master_bus_voltage_V" in df and "pdu_primary_current_A" in df:
        df["sa_power_W"] = df["master_bus_voltage_V"] * df["pdu_primary_current_A"]
        print("  [+] sa_power_W = bus_voltage × pdu_current")

    # 2. Cosine of incidence angle (irradiance factor)
    if "sa_incidence_angle_deg" in df:
        df["cos_incidence"] = np.cos(np.deg2rad(df["sa_incidence_angle_deg"]))
        print("  [+] cos_incidence = cos(incidence_angle)")

    # 3. Absolute misalignment (loss factor)
    if "sa_misalignment_deg" in df:
        df["abs_misalignment"] = df["sa_misalignment_deg"].abs()
        print("  [+] abs_misalignment = |misalignment_deg|")

    # 4. Voltage deviation from nominal 28V
    if "master_bus_voltage_V" in df:
        df["bus_volt_deviation"] = df["master_bus_voltage_V"] - 28.0
        print("  [+] bus_volt_deviation = voltage − 28.0 V")

    # 5. Estimated power loss due to misalignment
    #    P_loss ≈ sa_power × (1 − cos(misalignment))
    if "sa_power_W" in df and "sa_misalignment_deg" in df:
        df["power_loss_misalign_W"] = (
            df["sa_power_W"] * (1 - np.cos(np.deg2rad(df["sa_misalignment_deg"]))))
        print("  [+] power_loss_misalign_W = P × (1 − cos(misalignment))")

    # 6. Time features
    df["hour_of_day"]  = df.index.hour + df.index.minute / 60
    df["day_of_year"]  = df.index.dayofyear
    df["mission_day"]  = (df.index - df.index.min()).days
    df["week_of_q3"]   = np.clip((df.index - df.index.min()).days // 7, 0, 13)
    print("  [+] hour_of_day, day_of_year, mission_day, week_of_q3")

    # 7. Log SA power (target for ML)
    if "sa_power_W" in df:
        df["log_sa_power"] = np.log1p(df["sa_power_W"].clip(lower=0))
        print("  [+] log_sa_power = log(1 + sa_power)")

    print(f"\n  Engineered DataFrame: {df.shape[0]:,} rows × {df.shape[1]} cols")
    new_cols = ["sa_power_W", "cos_incidence", "abs_misalignment",
                "bus_volt_deviation", "power_loss_misalign_W",
                "hour_of_day", "day_of_year", "log_sa_power"]
    print(f"\n  Sample:\n{df[[c for c in new_cols if c in df.columns]].head(5).to_string()}")

    # Visualise engineered features
    plot_cols = [c for c in new_cols if c in df.columns]
    fig, axes = plt.subplots(2, 4, figsize=(20, 8))
    axes = axes.flatten()

    feat_colors = ["#185FA5","#ff7f0e","#d62728","#1D9E75",
                   "#BA7517","#534AB7","#3B6D11","#185FA5"]
    for i, col in enumerate(plot_cols[:8]):
        data = df[col].dropna()
        axes[i].hist(data, bins=60, color=feat_colors[i],
                     edgecolor='white', alpha=0.85)
        axes[i].set_title(col, fontsize=9)
        axes[i].set_ylabel("Count")

    for j in range(len(plot_cols), 8):
        axes[j].set_visible(False)

    plt.suptitle("Rosetta — Engineered Features", fontsize=14)
    plt.tight_layout()
    savefig("step12_features.png")
    plt.show()

    return df


# ─────────────────────────────────────────────────────────────
# STEP 13: SAVE CLEAN DATASET
# ─────────────────────────────────────────────────────────────
def save_clean_dataset(df):
    print("\n" + "=" * 60)
    print("STEP 13: SAVE CLEAN DATASET")
    print("=" * 60)

    clean = df.copy().reset_index()
    clean = clean.rename(columns={"index": "timestamp", "timestamp": "timestamp"})

    # Drop rows where all value columns are NaN
    val_cols = [c for c in clean.columns if c != "timestamp"]
    before   = len(clean)
    clean    = clean.dropna(subset=val_cols, how='all')
    print(f"  Dropped all-NaN rows : {before - len(clean):,}")

    # Forward fill gaps ≤ 5 minutes
    clean = clean.ffill(limit=5).bfill(limit=5)

    out_path = os.path.join(OUT_DIR, "rosetta_hk_clean.csv")
    clean.to_csv(out_path, index=False)

    print(f"  Final shape    : {clean.shape[0]:,} rows × {clean.shape[1]} cols")
    print(f"  Remaining NaN  : {clean.isnull().sum().sum():,}")
    print(f"  [Saved]  {out_path}")
    print(f"\n  Columns: {clean.columns.tolist()}")

    return clean


# ─────────────────────────────────────────────────────────────
# STEP 14: EDA SUMMARY REPORT
# ─────────────────────────────────────────────────────────────
def eda_summary(dfs, df_engineered, power):
    print("\n" + "=" * 60)
    print("EDA SUMMARY REPORT — Rosetta HK 2016 Q3")
    print("=" * 60)

    for param, df in dfs.items():
        col = df[param].dropna()
        print(f"\n  {label(param)}")
        print(f"    Records : {len(df):,}   |   Valid: {len(col):,}")
        print(f"    Range   : {col.min():.4f} – {col.max():.4f} "
              f"{PARAM_INFO[param]['unit']}")
        print(f"    Mean±Std: {col.mean():.4f} ± {col.std():.4f}")

    if power is not None:
        print(f"\n  Estimated SA Power")
        print(f"    Mean  : {power.mean():.1f} W")
        print(f"    Max   : {power.max():.1f} W")
        print(f"    Min   : {power.min():.1f} W")

    if "sa_misalignment_deg" in dfs:
        mis = dfs["sa_misalignment_deg"]["sa_misalignment_deg"].dropna()
        print(f"\n  SA Misalignment ≤ 1° : {(mis.abs()<=1).mean()*100:.1f}%")
        print(f"  SA Misalignment > 5° : {(mis.abs()> 5).mean()*100:.1f}%")

    print("\n─── Correlation with sa_power_W (engineered) ───")
    if "sa_power_W" in df_engineered.columns:
        num = df_engineered.select_dtypes(include=[np.number]).dropna(
            axis=1, thresh=int(0.3 * len(df_engineered)))
        corr_pow = (num.corr()["sa_power_W"]
                    .drop("sa_power_W", errors='ignore')
                    .abs().sort_values(ascending=False).head(8))
        for feat, val in corr_pow.items():
            sign = "+" if num.corr()["sa_power_W"][feat] > 0 else "−"
            print(f"  {sign}{val:.3f}  {feat}")

    print("\n─── Suggested ML targets ───")
    print("  1. Regression : predict sa_power_W from incidence_angle + misalignment + time")
    print("  2. Regression : predict bus_voltage from cos_incidence + pdu_current")
    print("  3. Anomaly    : detect high-misalignment events from power deviation")
    print("  4. Sequence   : LSTM to predict next-step power from SA angle history")

    print(f"\n[EDA COMPLETE] All plots & clean CSV saved to: {OUT_DIR}")


# ─────────────────────────────────────────────────────────────
# MAIN PIPELINE
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":

    # 1–2. Load TAB files + parse LBL metadata
    dfs, meta = load_datasets()

    if not dfs:
        print("No datasets loaded. Check BASE path and file locations.")
        exit()

    # 3. Print LBL metadata
    print_metadata(meta)

    # 4. Basic inspection
    basic_inspection(dfs)

    # 5. Missing values
    missing_value_analysis(dfs)

    # 6. Outlier detection
    outlier_analysis(dfs)

    # 7. Univariate distributions
    univariate_analysis(dfs)

    # 8. Time series
    time_series_analysis(dfs)

    # 9. Power analysis (V × I, incidence angle vs power)
    power = power_analysis(dfs)

    # 10. Solar array geometry
    sa_geometry_analysis(dfs)

    # 11. Correlation
    df_merged = correlation_analysis(dfs)

    # 12. Feature engineering
    df_eng = feature_engineering(dfs)

    # 13. Save clean CSV
    clean_df = save_clean_dataset(df_eng)

    # 14. Summary report
    eda_summary(dfs, df_eng, power)

    print("\n[Done] EDA complete. Clean dataset ready for ML pipeline.")