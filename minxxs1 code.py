# -*- coding: utf-8 -*-
"""
Created on Sun May 31 11:39:20 2026

@author: ADMIN
"""

"""
EDA — MinXSS-1 Solar SXR NetCDF Data Products
Intelligent Power Generation for Satellites Using ML-Driven Orientation Systems
Group 6 | Dept. of Aerospace Engineering | MIT-ADT University

Supports all 6 MinXSS-1 NCDF data levels:
  Level 0C — raw housekeeping (10-sec cadence)
  Level 0D — calibrated housekeeping (10-sec cadence)  ← most detailed
  Level 1   — calibrated SXR irradiance spectra
  Level 2 1-min average
  Level 2 1-hour average
  Level 3 1-day average

Required:  pip install netCDF4 numpy pandas matplotlib seaborn scipy
"""

import os
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────────────────────
# FILE PATHS  ←  update these to match your local paths
# ─────────────────────────────────────────────────────────────
BASE = r"C:\Users\ADMIN\Downloads\minxss-1_data_archive\minxss-1_data_archive"

FILES = {
    "level0C" : os.path.join(BASE, "minxss1_solarSXR_level0C_2016-05-16-mission_V002.ncdf"),
    "level0D" : os.path.join(BASE, "minxss1_solarSXR_level0D_2016-05-16-mission_V002.ncdf"),
    "level1"  : os.path.join(BASE, "minxss1_solarSXR_level1_2016-05-16-mission_V002.ncdf"),
    "level2m" : os.path.join(BASE, "minxss1_solarSXR_level2_1minute_average_2016-05-16-mission_V002.ncdf"),
    "level2h" : os.path.join(BASE, "minxss1_solarSXR_level2_1hour_average_2016-05-16-mission_V002.ncdf"),
    "level3"  : os.path.join(BASE, "minxss1_solarSXR_level3_1day_average_2016-05-16-mission_V002.ncdf"),
}

# Output directory — saves all plots here
OUT_DIR = r"C:\Users\ADMIN\Downloads\minxss-1_data_archive"

# ─────────────────────────────────────────────────────────────
# COLOUR PALETTE
# ─────────────────────────────────────────────────────────────
C = {
    "blue"    : "#185FA5",
    "orange"  : "#ff7f0e",
    "green"   : "#3B6D11",
    "purple"  : "#534AB7",
    "red"     : "#d62728",
    "teal"    : "#1D9E75",
    "amber"   : "#BA7517",
    "eclipse" : "#d62728",
    "sunlit"  : "#f7c637",
}

try:
    plt.style.use('seaborn-v0_8-whitegrid')
except OSError:
    plt.style.use('seaborn-whitegrid')

os.makedirs(OUT_DIR, exist_ok=True)


# ─────────────────────────────────────────────────────────────
# UTILITY — save figure
# ─────────────────────────────────────────────────────────────
def savefig(name):
    path = os.path.join(OUT_DIR, name)
    plt.savefig(path, dpi=150, bbox_inches='tight')
    print(f"  [Saved] {path}")


# ─────────────────────────────────────────────────────────────
# UTILITY — read NetCDF variable safely
# ─────────────────────────────────────────────────────────────
def read_var(ds, name, fill_nan=True):
    """Extract a 1-D or 2-D variable from a netCDF4 Dataset as a numpy array."""
    import netCDF4 as nc
    v = ds.variables[name]
    data = v[:]
    if hasattr(data, 'filled'):
        data = data.filled(np.nan) if fill_nan else data.filled(0)
    return np.array(data, dtype=float) if data.dtype.kind in ('f', 'i', 'u') else data


# ─────────────────────────────────────────────────────────────
# UTILITY — build Julian Date → datetime
# ─────────────────────────────────────────────────────────────
def jd_to_datetime(jd_array):
    """Convert Julian Date array to pandas DatetimeIndex."""
    unix_days = jd_array - 2440587.5          # JD → days since 1970-01-01
    return pd.to_datetime(unix_days * 86400, unit='s', utc=True)


# ─────────────────────────────────────────────────────────────
# STEP 1: LOAD ALL DATASETS
# ─────────────────────────────────────────────────────────────
def load_datasets():
    """
    Load all available MinXSS-1 NetCDF files.
    Returns a dict: { level_key : netCDF4.Dataset }
    """
    try:
        import netCDF4 as nc
    except ImportError:
        raise ImportError("Run:  pip install netCDF4")

    print("\n" + "=" * 60)
    print("STEP 1: LOADING DATASETS")
    print("=" * 60)

    datasets = {}
    for key, path in FILES.items():
        if os.path.exists(path):
            ds = nc.Dataset(path, 'r')
            n  = len(ds.dimensions.get('structure_elements',
                     list(ds.dimensions.values())[0]))
            print(f"  [OK] {key:10s}  {n:,} records  —  {path}")
            datasets[key] = ds
        else:
            print(f"  [--] {key:10s}  not found  —  {path}")

    if not datasets:
        raise FileNotFoundError("No MinXSS-1 files found. Check BASE path.")
    return datasets


# ─────────────────────────────────────────────────────────────
# STEP 2: VARIABLE INVENTORY (what's in each file)
# ─────────────────────────────────────────────────────────────
def variable_inventory(datasets):
    """Print all variables, units, and shapes for each loaded file."""
    print("\n" + "=" * 60)
    print("STEP 2: VARIABLE INVENTORY")
    print("=" * 60)

    for key, ds in datasets.items():
        print(f"\n{'─'*50}")
        print(f"Level: {key.upper()}  ({getattr(ds, 'Data_type', 'N/A')})")
        print(f"Time resolution: {getattr(ds, 'Time_resolution', 'N/A')}")
        print(f"\n{'Variable':<40} {'Shape':<18} {'Units'}")
        print("-" * 75)
        for name, var in ds.variables.items():
            units = getattr(var, 'UNITS', '—')
            print(f"  {name:<38} {str(var.shape):<18} {units}")


# ─────────────────────────────────────────────────────────────
# STEP 3: BUILD TIDY DATAFRAME FROM LEVEL 0D
# ─────────────────────────────────────────────────────────────
def build_dataframe_0D(datasets):
    """
    Extract the key scalar variables from Level 0D into a pandas DataFrame.
    Level 0D is the most information-rich file for EPS/ADCS/orbital EDA.
    """
    print("\n" + "=" * 60)
    print("STEP 3: BUILDING TIDY DATAFRAME (Level 0D)")
    print("=" * 60)

    if "level0D" not in datasets:
        print("  Level 0D not loaded — skipping.")
        return None

    ds = datasets["level0D"]

    # ── time ──────────────────────────────────────────────────
    jd        = read_var(ds, "TIME.JD")
    datetime_ = jd_to_datetime(jd)

    # ── 1-D scalar variables to extract ──────────────────────
    VARS = {
        # EPS (power system)
        "eps_5v_voltage_V"       : "EPS_5V_VOLT",
        "eps_5v_current_mA"      : "EPS_5V_CUR",
        # ADCS / orientation
        "sun_point_angle_error_deg" : "XACT_SUN_POINT_ANGLE_ERROR",
        "sun_body_vec_x"         : "XACT_MEASURED_SUN_BODY_VECTOR_X",
        "sun_body_vec_y"         : "XACT_MEASURED_SUN_BODY_VECTOR_Y",
        "sun_body_vec_z"         : "XACT_MEASURED_SUN_BODY_VECTOR_Z",
        "wheel_speed_y_rads"     : "XACT_WHEEL1_MEASURED_SPEED",
        "wheel_speed_x_rads"     : "XACT_WHEEL2_MEASURED_SPEED",
        "wheel_speed_z_rads"     : "XACT_WHEEL3_MEASURED_SPEED",
        "adcs_mode"              : "ADCS_MODE",
        "attitude_valid"         : "MEASURED_ATTITUDE_VALID",
        # Orbital
        "altitude_km"            : "ALTITUDE",
        "latitude_deg"           : "LATITUDE",
        "longitude_deg"          : "LONGITUDE",
        "earth_sun_dist_AU"      : "EARTH_SUN_DISTANCE",
        "sun_declination_deg"    : "SUN_DECLINATION",
        "sun_ra_deg"             : "SUN_RIGHT_ASCENSION",
        # Flags
        "eclipse_flag"           : "ECLIPSE",
        "spacecraft_in_saa"      : "SPACECRAFT_IN_SAA",
        "spacecraft_mode"        : "SPACECRAFT_MODE",
        # Thermal
        "x123_board_temp_C"      : "X123_BOARD_TEMPERATURE",
        "x123_detector_temp_C"   : "X123_DETECTOR_TEMPERATURE",
        "sps_xps_temp_C"         : "SPS_XPS_TEMPERATURE",
        # X-ray science
        "x123_slow_count_cps"    : "X123_SLOW_COUNT",
        "x123_fast_count_cps"    : "X123_FAST_COUNT",
        "x123_live_time_ms"      : "X123_LIVE_TIME",
        "x123_accum_time_ms"     : "X123_ACCUM_TIME",
        "xps_hk_DN_per_s"        : "XPS_DATA_HK",
        "sps_sum_fC"             : "SPS_SUM_HK",
    }

    data = {"time": datetime_}
    for col_name, nc_name in VARS.items():
        if nc_name in ds.variables:
            arr = read_var(ds, nc_name)
            if arr.ndim == 1:
                data[col_name] = arr
        else:
            print(f"  [warn] {nc_name} not found in Level 0D")

    df = pd.DataFrame(data).set_index("time").sort_index()

    # Clamp fill values that appear as large outliers
    df["adcs_mode"]      = df["adcs_mode"].where(df["adcs_mode"].isin([0, 1]), np.nan)
    df["eclipse_flag"]   = df["eclipse_flag"].where(df["eclipse_flag"].isin([0, 1]), np.nan)
    df["spacecraft_mode"]= df["spacecraft_mode"].where(
        df["spacecraft_mode"].isin([1, 2, 4]), np.nan)
    df["attitude_valid"] = df["attitude_valid"].where(
        df["attitude_valid"].isin([0, 1]), np.nan)

    print(f"  DataFrame shape   : {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"  Time range        : {df.index.min()} → {df.index.max()}")
    print(f"\n  Columns:\n  {df.columns.tolist()}")
    print(f"\n  Statistical summary:\n{df.describe().round(4).to_string()}")

    return df


# ─────────────────────────────────────────────────────────────
# STEP 4: MISSING VALUE ANALYSIS
# ─────────────────────────────────────────────────────────────
def missing_value_analysis(df):
    print("\n" + "=" * 60)
    print("STEP 4: MISSING VALUES ANALYSIS")
    print("=" * 60)

    miss     = df.isnull().sum()
    miss_pct = (miss / len(df) * 100).round(2)
    miss_df  = pd.DataFrame({"Missing": miss, "Missing %": miss_pct})
    miss_df  = miss_df[miss_df["Missing"] > 0].sort_values("Missing %", ascending=False)

    print(f"\n  Total NaN cells : {df.isnull().sum().sum():,}")
    print(f"  Columns with gaps:\n{miss_df.to_string()}")

    # Visualise
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))

    if miss_df.empty:
        axes[0].text(0.5, 0.5, "No missing values", ha='center', va='center',
                     fontsize=13, transform=axes[0].transAxes)
    else:
        miss_df["Missing %"].plot(kind='barh', ax=axes[0],
                                  color=C["red"], edgecolor='black')
        axes[0].set_xlabel("Missing %")
    axes[0].set_title("Missing Values per Column")

    # Overall quality counts
    eclipse_known = df["eclipse_flag"].notna().sum()
    sunlit_n      = (df["eclipse_flag"] == 0).sum()
    eclipse_n     = (df["eclipse_flag"] == 1).sum()
    saa_n         = (df["spacecraft_in_saa"] == 1).sum()

    cats   = ["All records", "Eclipse", "Sunlit", "In SAA"]
    counts = [len(df), eclipse_n, sunlit_n, saa_n]
    colors = [C["blue"], C["eclipse"], C["sunlit"], C["orange"]]
    axes[1].barh(cats, counts, color=colors, edgecolor='black')
    axes[1].set_xlabel("Count")
    axes[1].set_title("Record Classification (Level 0D)")
    for i, v in enumerate(counts):
        axes[1].text(v + 50, i, f"{v:,}", va='center', fontsize=9)

    plt.suptitle("MinXSS-1 Level 0D — Data Quality Overview", fontsize=13)
    plt.tight_layout()
    savefig("step4_missing_values.png")
    plt.show()

    return df


# ─────────────────────────────────────────────────────────────
# STEP 5: OUTLIER DETECTION
# ─────────────────────────────────────────────────────────────
def detect_outliers_iqr(series):
    Q1, Q3 = series.quantile(0.25), series.quantile(0.75)
    IQR = Q3 - Q1
    return (series < Q1 - 1.5 * IQR) | (series > Q3 + 1.5 * IQR)


def outlier_analysis(df):
    print("\n" + "=" * 60)
    print("STEP 5: OUTLIER DETECTION")
    print("=" * 60)

    # Key columns to inspect for outliers
    check_cols = [
        "eps_5v_voltage_V", "eps_5v_current_mA",
        "sun_point_angle_error_deg",
        "altitude_km", "earth_sun_dist_AU",
        "x123_board_temp_C", "x123_detector_temp_C",
    ]
    check_cols = [c for c in check_cols if c in df.columns]

    for col in check_cols:
        mask = detect_outliers_iqr(df[col].dropna())
        print(f"  {col:<35} outliers: {mask.sum():,} "
              f"({mask.sum()/df[col].notna().sum()*100:.2f}%)")

    # Boxplots
    fig, axes = plt.subplots(2, 4, figsize=(20, 8))
    axes = axes.flatten()
    for i, col in enumerate(check_cols[:8]):
        data = df[col].dropna()
        axes[i].boxplot(data, patch_artist=True,
                        boxprops=dict(facecolor=C["blue"], alpha=0.5))
        out_n = detect_outliers_iqr(data).sum()
        axes[i].set_title(f"{col}\n({out_n} outliers)", fontsize=9)
        axes[i].set_ylabel(col.split("_")[-1])

    for j in range(i + 1, 8):
        axes[j].set_visible(False)

    plt.suptitle("MinXSS-1 Level 0D — Outlier Detection (IQR)", fontsize=13)
    plt.tight_layout()
    savefig("step5_outliers.png")
    plt.show()

    print("\n  [NOTE] Outliers in satellite data often mark real events:")
    print("         • eclipse entry/exit  • SAA passages  • instrument warmup")
    print("         Flag with is_anomaly column — do not blindly drop.")


# ─────────────────────────────────────────────────────────────
# STEP 6: UNIVARIATE ANALYSIS
# ─────────────────────────────────────────────────────────────
def univariate_analysis(df):
    print("\n" + "=" * 60)
    print("STEP 6: UNIVARIATE ANALYSIS")
    print("=" * 60)

    fig, axes = plt.subplots(3, 3, figsize=(18, 14))
    axes = axes.flatten()

    plots = [
        ("eps_5v_voltage_V",           "X123 Supply Voltage (V)",      C["blue"]),
        ("eps_5v_current_mA",          "X123 Supply Current (mA)",     C["teal"]),
        ("sun_point_angle_error_deg",  "Sun Point Angle Error (deg)",  C["amber"]),
        ("altitude_km",                "Orbital Altitude (km)",        C["green"]),
        ("earth_sun_dist_AU",          "Earth-Sun Distance (AU)",      C["purple"]),
        ("x123_board_temp_C",          "X123 Board Temp (°C)",         C["orange"]),
        ("x123_detector_temp_C",       "X123 Detector Temp (°C)",      C["red"]),
        ("x123_slow_count_cps",        "X123 Slow Count (cps)",        C["blue"]),
        ("sps_sum_fC",                 "SPS Signal (fC)",              C["teal"]),
    ]

    for i, (col, label, color) in enumerate(plots):
        if col not in df.columns:
            axes[i].set_visible(False)
            continue
        data = df[col].dropna()
        axes[i].hist(data, bins=60, color=color, edgecolor='white', alpha=0.85)
        axes[i].set_title(label, fontsize=10)
        axes[i].set_xlabel("Value")
        axes[i].set_ylabel("Count")
        # Add mean line
        axes[i].axvline(data.mean(), color='black', linewidth=1.5,
                        linestyle='--', label=f"mean={data.mean():.2f}")
        axes[i].legend(fontsize=8)

    plt.suptitle("MinXSS-1 Level 0D — Univariate Distributions", fontsize=14)
    plt.tight_layout()
    savefig("step6_univariate.png")
    plt.show()

    # ── Categorical variables
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    for ax, col, title, color_map in [
        (axes[0], "eclipse_flag",    "Eclipse (0=sunlit, 1=eclipse)",
            {0: C["sunlit"], 1: C["eclipse"]}),
        (axes[1], "spacecraft_mode", "Spacecraft Mode (1=Phoenix, 2=Safe, 4=Science)",
            {1: C["orange"], 2: C["red"], 4: C["green"]}),
        (axes[2], "adcs_mode",       "ADCS Mode (0=Sun Point, 1=Fine Ref)",
            {0: C["blue"], 1: C["teal"]}),
    ]:
        if col not in df.columns:
            continue
        counts = df[col].dropna().value_counts().sort_index()
        ax.bar([str(int(k)) for k in counts.index],
               counts.values,
               color=[color_map.get(k, C["blue"]) for k in counts.index],
               edgecolor='black')
        ax.set_title(title, fontsize=9)
        ax.set_ylabel("Count")
        for j, v in enumerate(counts.values):
            ax.text(j, v + 100, f"{v:,}", ha='center', fontsize=8)

    plt.suptitle("MinXSS-1 Level 0D — Categorical Variables", fontsize=13)
    plt.tight_layout()
    savefig("step6_categorical.png")
    plt.show()


# ─────────────────────────────────────────────────────────────
# STEP 7: TIME SERIES ANALYSIS
# ─────────────────────────────────────────────────────────────
def time_series_analysis(df):
    print("\n" + "=" * 60)
    print("STEP 7: TIME SERIES ANALYSIS")
    print("=" * 60)

    # ── Full mission overview (4 panels)
    fig, axes = plt.subplots(4, 1, figsize=(16, 14), sharex=True)

    def plot_ts(ax, col, label, color, alpha=0.5):
        if col not in df.columns:
            return
        data = df[col].dropna()
        ax.plot(data.index, data.values, color=color, linewidth=0.5, alpha=alpha)
        # 1-hour rolling mean
        rolled = df[col].resample('1h').mean().dropna()
        ax.plot(rolled.index, rolled.values, color='black',
                linewidth=1.5, label="1-hr mean")
        ax.set_ylabel(label, fontsize=9)
        ax.legend(fontsize=8, loc='upper right')
        # Shade eclipse periods
        if "eclipse_flag" in df.columns:
            eclipse = df["eclipse_flag"].fillna(0)
            ax.fill_between(df.index, ax.get_ylim()[0], ax.get_ylim()[1],
                            where=eclipse == 1,
                            color=C["eclipse"], alpha=0.05, label='eclipse')

    plot_ts(axes[0], "eps_5v_voltage_V",          "EPS Voltage (V)",           C["blue"])
    plot_ts(axes[1], "eps_5v_current_mA",          "EPS Current (mA)",          C["teal"])
    plot_ts(axes[2], "sun_point_angle_error_deg",  "Sun Point Error (deg)",     C["amber"])
    plot_ts(axes[3], "x123_slow_count_cps",        "X-ray Count Rate (cps)",    C["purple"])

    axes[-1].set_xlabel("Date (UTC)")
    plt.suptitle("MinXSS-1 Level 0D — Full Mission Time Series\n"
                 "(red shading = eclipse periods)", fontsize=13)
    plt.tight_layout()
    savefig("step7_timeseries_overview.png")
    plt.show()

    # ── Zoom: one orbital cycle (~95 minutes for ISS orbit)
    # Take first 200 records
    zoom = df.head(200)

    fig, axes = plt.subplots(3, 1, figsize=(14, 9), sharex=True)

    for ax, col, label, color in [
        (axes[0], "eps_5v_voltage_V",  "EPS Voltage (V)",      C["blue"]),
        (axes[1], "eps_5v_current_mA", "EPS Current (mA)",     C["teal"]),
        (axes[2], "eclipse_flag",      "Eclipse (0/1)",        C["eclipse"]),
    ]:
        if col not in zoom.columns:
            continue
        ax.plot(zoom.index, zoom[col], color=color, linewidth=1.5, marker='.',
                markersize=2)
        ax.set_ylabel(label, fontsize=9)

    axes[-1].set_xlabel("Time (UTC)")
    plt.suptitle("MinXSS-1 — One Orbital Cycle Zoom (first 200 samples, 10-sec cadence)",
                 fontsize=12)
    plt.tight_layout()
    savefig("step7_timeseries_zoom.png")
    plt.show()

    # ── Thermal time series
    fig, ax = plt.subplots(figsize=(14, 5))
    for col, label, color in [
        ("x123_board_temp_C",    "X123 Board",    C["orange"]),
        ("x123_detector_temp_C", "X123 Detector", C["red"]),
        ("sps_xps_temp_C",       "SPS/XPS",       C["teal"]),
    ]:
        if col in df.columns:
            daily = df[col].resample('1D').mean().dropna()
            ax.plot(daily.index, daily.values, label=label, linewidth=1.5)
    ax.set_ylabel("Temperature (°C)")
    ax.set_xlabel("Date")
    ax.legend()
    ax.set_title("MinXSS-1 — Instrument Temperatures Over Mission Life (daily mean)")
    plt.tight_layout()
    savefig("step7_temperatures.png")
    plt.show()


# ─────────────────────────────────────────────────────────────
# STEP 8: ECLIPSE & ORBITAL ANALYSIS
# ─────────────────────────────────────────────────────────────
def eclipse_orbital_analysis(df):
    print("\n" + "=" * 60)
    print("STEP 8: ECLIPSE & ORBITAL ANALYSIS")
    print("=" * 60)

    if "eclipse_flag" not in df.columns:
        print("  eclipse_flag not available — skipping.")
        return df

    # Stats
    total      = df["eclipse_flag"].notna().sum()
    eclipse_n  = (df["eclipse_flag"] == 1).sum()
    sunlit_n   = (df["eclipse_flag"] == 0).sum()
    eclipse_pct = eclipse_n / total * 100

    print(f"  Total classified records : {total:,}")
    print(f"  Sunlit                   : {sunlit_n:,}  ({sunlit_n/total*100:.1f}%)")
    print(f"  Eclipse                  : {eclipse_n:,}  ({eclipse_pct:.1f}%)  "
          f"[expected ~35–40% for ISS orbit]")

    # Orbit altitude decay
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))

    # 1. Altitude over mission
    if "altitude_km" in df.columns:
        daily_alt = df["altitude_km"].resample('1D').mean().dropna()
        axes[0, 0].plot(daily_alt.index, daily_alt.values,
                        color=C["blue"], linewidth=1.5)
        axes[0, 0].set_title("Orbital Altitude — Mission Decay")
        axes[0, 0].set_ylabel("Altitude (km)")
        axes[0, 0].set_xlabel("Date")

    # 2. Ground track (lat vs lon)
    if "latitude_deg" in df.columns and "longitude_deg" in df.columns:
        # Sample 5000 points for plotting speed
        samp = df[["latitude_deg", "longitude_deg", "eclipse_flag"]].dropna().sample(
            min(5000, len(df)), random_state=42)
        axes[0, 1].scatter(samp["longitude_deg"], samp["latitude_deg"],
                           c=samp["eclipse_flag"], cmap='RdYlGn_r',
                           s=2, alpha=0.4)
        axes[0, 1].set_title("Ground Track  (green=sunlit, red=eclipse)")
        axes[0, 1].set_xlabel("Longitude (°)")
        axes[0, 1].set_ylabel("Latitude (°)")

    # 3. Earth-Sun distance over time
    if "earth_sun_dist_AU" in df.columns:
        daily_dist = df["earth_sun_dist_AU"].resample('1D').mean().dropna()
        axes[1, 0].plot(daily_dist.index, daily_dist.values,
                        color=C["amber"], linewidth=1.5)
        axes[1, 0].set_title("Earth-Sun Distance Over Mission")
        axes[1, 0].set_ylabel("Distance (AU)")
        axes[1, 0].set_xlabel("Date")
        axes[1, 0].axhline(1.0, color='black', linewidth=0.8,
                           linestyle='--', label='1 AU')
        axes[1, 0].legend()

    # 4. SAA passages
    if "spacecraft_in_saa" in df.columns:
        saa_pct = (df["spacecraft_in_saa"] == 1).sum() / len(df) * 100
        labels  = ["Not in SAA", "In SAA"]
        sizes   = [100 - saa_pct, saa_pct]
        axes[1, 1].pie(sizes, labels=labels, autopct='%1.1f%%',
                       colors=[C["blue"], C["red"]])
        axes[1, 1].set_title("South Atlantic Anomaly (SAA) Passages\n"
                             "(SAA data should be excluded from science analysis)")

    plt.suptitle("MinXSS-1 Level 0D — Eclipse & Orbital Analysis", fontsize=14)
    plt.tight_layout()
    savefig("step8_eclipse_orbital.png")
    plt.show()

    # Add computed column
    df = df.copy()
    df["sunlit_flag"] = (df["eclipse_flag"] == 0).astype(float)
    return df


# ─────────────────────────────────────────────────────────────
# STEP 9: ADCS & SUN-POINTING ANALYSIS
# ─────────────────────────────────────────────────────────────
def adcs_analysis(df):
    """
    Key for the ML project — sun pointing quality directly determines
    X-ray (and solar panel) power generation efficiency.
    """
    print("\n" + "=" * 60)
    print("STEP 9: ADCS & SUN-POINTING ANALYSIS")
    print("=" * 60)

    angle_col = "sun_point_angle_error_deg"
    if angle_col not in df.columns:
        print("  XACT sun-point angle not available.")
        return

    sunlit = df[df.get("eclipse_flag", pd.Series(1, index=df.index)) == 0]
    angle  = sunlit[angle_col].dropna()

    print(f"  Sun-pointing angle (sunlit only):")
    print(f"    Mean  : {angle.mean():.2f}°")
    print(f"    Median: {angle.median():.2f}°")
    print(f"    Std   : {angle.std():.2f}°")
    print(f"    < 5°  : {(angle < 5).sum():,} samples  ({(angle<5).mean()*100:.1f}%)")
    print(f"    < 10° : {(angle < 10).sum():,} samples  ({(angle<10).mean()*100:.1f}%)")
    print(f"    > 30° : {(angle > 30).sum():,} samples  ({(angle>30).mean()*100:.1f}%)")

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # 1. Distribution of pointing error
    axes[0].hist(angle.clip(upper=90), bins=60,
                 color=C["amber"], edgecolor='white', alpha=0.85)
    axes[0].axvline(5,  color=C["green"], linewidth=2, linestyle='--', label='5° threshold')
    axes[0].axvline(10, color=C["orange"], linewidth=2, linestyle='--', label='10° threshold')
    axes[0].set_xlabel("Sun Point Angle Error (deg)")
    axes[0].set_ylabel("Count")
    axes[0].set_title("Pointing Error Distribution\n(sunlit periods only)")
    axes[0].legend()

    # 2. Scatter: pointing error vs X123 count rate
    if "x123_slow_count_cps" in df.columns:
        merged = pd.concat([
            sunlit[angle_col].rename("angle"),
            sunlit["x123_slow_count_cps"].rename("count_rate"),
        ], axis=1).dropna()
        # Clip for plot clarity
        merged = merged[merged["count_rate"] > 0]
        axes[1].scatter(merged["angle"], np.log10(merged["count_rate"] + 1),
                        alpha=0.2, s=5, color=C["purple"])
        axes[1].set_xlabel("Sun Point Angle Error (deg)")
        axes[1].set_ylabel("log₁₀(X123 Count Rate + 1)")
        axes[1].set_title("Pointing Error vs X-ray Count Rate")

    # 3. Pointing error over time (daily median)
    daily_angle = sunlit[angle_col].resample('1D').median().dropna()
    axes[2].plot(daily_angle.index, daily_angle.values,
                 color=C["amber"], linewidth=1.5)
    axes[2].set_xlabel("Date")
    axes[2].set_ylabel("Median Daily Angle Error (deg)")
    axes[2].set_title("Pointing Accuracy — Mission Trend")
    axes[2].axhline(5, color=C["green"], linewidth=1,
                    linestyle='--', label='5° goal')
    axes[2].legend()

    plt.suptitle("MinXSS-1 — ADCS Sun-Pointing Analysis", fontsize=14)
    plt.tight_layout()
    savefig("step9_adcs_pointing.png")
    plt.show()


# ─────────────────────────────────────────────────────────────
# STEP 10: X-RAY SPECTRUM ANALYSIS (Level 0D — X123_SPECTRUM)
# ─────────────────────────────────────────────────────────────
def spectrum_analysis(datasets):
    """
    Analyse the 1024-channel X123 SXR spectrum array.
    Each row = one 10-second observation × 1024 energy bins.
    """
    print("\n" + "=" * 60)
    print("STEP 10: X-RAY SPECTRUM ANALYSIS")
    print("=" * 60)

    if "level0D" not in datasets:
        print("  Level 0D not available — skipping spectrum analysis.")
        return

    ds = datasets["level0D"]
    if "X123_SPECTRUM" not in ds.variables:
        print("  X123_SPECTRUM not found.")
        return

    spec_all = read_var(ds, "X123_SPECTRUM")   # shape: (N, 1024)
    eclipse  = read_var(ds, "ECLIPSE")

    print(f"  Spectrum array shape: {spec_all.shape}")

    # Filter: sunlit, reasonable data
    sunlit_mask  = (eclipse == 0)
    slow_count   = read_var(ds, "X123_SLOW_COUNT")
    good_mask    = sunlit_mask & (slow_count > 10) & (slow_count < 1e5)

    spec_sunlit  = spec_all[good_mask, :]
    print(f"  Good sunlit spectra : {spec_sunlit.shape[0]:,}")

    # Channel → energy (approximate: each bin ≈ 0.03 keV, starting at ~0.5 keV)
    energy_keV = 0.5 + np.arange(1024) * 0.03

    # Mean and std spectrum
    mean_spec = np.nanmean(spec_sunlit, axis=0)
    std_spec  = np.nanstd(spec_sunlit, axis=0)

    fig, axes = plt.subplots(2, 2, figsize=(16, 10))

    # 1. Mean SXR spectrum (linear)
    ax = axes[0, 0]
    ax.plot(energy_keV, mean_spec, color=C["blue"], linewidth=1.2)
    ax.fill_between(energy_keV, mean_spec - std_spec, mean_spec + std_spec,
                    color=C["blue"], alpha=0.2, label='±1σ')
    ax.set_xlabel("Energy (keV)")
    ax.set_ylabel("Counts/sec/bin")
    ax.set_title("Mean Solar SXR Spectrum (all sunlit)")
    ax.legend()
    ax.set_xlim([0.5, 12])

    # 2. Log-scale spectrum
    ax = axes[0, 1]
    positive = mean_spec > 0
    ax.semilogy(energy_keV[positive], mean_spec[positive],
                color=C["purple"], linewidth=1.2)
    ax.set_xlabel("Energy (keV)")
    ax.set_ylabel("Counts/sec/bin (log)")
    ax.set_title("Mean Solar SXR Spectrum (log scale)")
    ax.set_xlim([0.5, 12])

    # 3. A few individual spectra
    ax = axes[1, 0]
    idxs = np.linspace(0, spec_sunlit.shape[0] - 1, 6, dtype=int)
    for idx in idxs:
        s = spec_sunlit[idx, :]
        if s.max() > 0:
            ax.semilogy(energy_keV, np.where(s > 0, s, np.nan),
                        linewidth=0.8, alpha=0.7)
    ax.set_xlabel("Energy (keV)")
    ax.set_ylabel("Counts/sec/bin (log)")
    ax.set_title("Individual SXR Spectra (6 samples)")
    ax.set_xlim([0.5, 12])

    # 4. Total counts distribution across spectra
    ax = axes[1, 1]
    total_counts = spec_sunlit.sum(axis=1)
    ax.hist(np.log10(total_counts[total_counts > 0]), bins=50,
            color=C["teal"], edgecolor='white', alpha=0.85)
    ax.set_xlabel("log₁₀(Total Counts per Spectrum)")
    ax.set_ylabel("Number of Spectra")
    ax.set_title("Integrated Count Rate Distribution")

    plt.suptitle("MinXSS-1 Level 0D — X123 Solar SXR Spectrum Analysis", fontsize=14)
    plt.tight_layout()
    savefig("step10_xray_spectrum.png")
    plt.show()


# ─────────────────────────────────────────────────────────────
# STEP 11: CORRELATION ANALYSIS
# ─────────────────────────────────────────────────────────────
def correlation_analysis(df):
    print("\n" + "=" * 60)
    print("STEP 11: CORRELATION ANALYSIS")
    print("=" * 60)

    # Select numeric columns with enough valid data
    num = df.select_dtypes(include=[np.number]).dropna(axis=1, thresh=int(0.5 * len(df)))
    # Drop quasi-constant columns
    num = num.loc[:, num.std() > 0]

    corr = num.corr()
    print(f"  Correlation matrix shape: {corr.shape}")

    # Top correlations with X-ray count rate (science target)
    if "x123_slow_count_cps" in corr.columns:
        top = (corr["x123_slow_count_cps"]
               .drop("x123_slow_count_cps", errors='ignore')
               .abs().sort_values(ascending=False).head(10))
        print(f"\n  Top correlates with x123_slow_count_cps:")
        for feat, val in top.items():
            sign = "+" if corr["x123_slow_count_cps"][feat] > 0 else "−"
            print(f"    {sign}{val:.3f}  {feat}")

    fig, axes = plt.subplots(1, 2, figsize=(20, 8))

    # Full heatmap
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f",
                cmap='RdYlGn', center=0, ax=axes[0],
                linewidths=0.3, annot_kws={"size": 7})
    axes[0].set_title("Correlation Heatmap — All Numeric Variables")
    axes[0].tick_params(axis='x', rotation=45, labelsize=7)
    axes[0].tick_params(axis='y', labelsize=7)

    # Sun-pointing angle vs count rate (key ML relationship)
    if all(c in df.columns for c in ["sun_point_angle_error_deg", "x123_slow_count_cps"]):
        sunlit = df[df.get("eclipse_flag", pd.Series(1, index=df.index)) == 0]
        merged = sunlit[["sun_point_angle_error_deg", "x123_slow_count_cps"]].dropna()
        merged = merged[(merged["x123_slow_count_cps"] > 0) &
                        (merged["sun_point_angle_error_deg"] < 60)]
        axes[1].hexbin(merged["sun_point_angle_error_deg"],
                       np.log10(merged["x123_slow_count_cps"] + 1),
                       gridsize=40, cmap='Blues')
        axes[1].set_xlabel("Sun Point Angle Error (deg)")
        axes[1].set_ylabel("log₁₀(X123 Count Rate + 1)")
        axes[1].set_title("Sun-Pointing vs X-ray Count Rate\n"
                          "(core relationship for ML orientation model)")

    plt.suptitle("MinXSS-1 Level 0D — Correlation Analysis", fontsize=14)
    plt.tight_layout()
    savefig("step11_correlation.png")
    plt.show()


# ─────────────────────────────────────────────────────────────
# STEP 12: MULTI-LEVEL COMPARISON (all 6 files)
# ─────────────────────────────────────────────────────────────
def multi_level_comparison(datasets):
    """Compare record counts and time coverage across all 6 data levels."""
    print("\n" + "=" * 60)
    print("STEP 12: MULTI-LEVEL DATASET COMPARISON")
    print("=" * 60)

    summary = []
    for key, ds in datasets.items():
        n = len(list(ds.dimensions.values())[0])
        title = getattr(ds, 'Time_resolution', key)
        data_type = getattr(ds, 'Data_type', '—')
        nvars = len(ds.variables)
        summary.append({
            "Level"     : key,
            "Records"   : n,
            "Variables" : nvars,
            "Resolution": title,
        })
    s_df = pd.DataFrame(summary)
    print(f"\n{s_df.to_string(index=False)}")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    axes[0].barh(s_df["Level"], s_df["Records"],
                 color=[C["blue"], C["teal"], C["green"],
                        C["amber"], C["orange"], C["purple"]][:len(s_df)],
                 edgecolor='black')
    axes[0].set_xlabel("Number of Records (log scale)")
    axes[0].set_xscale('log')
    axes[0].set_title("Records per Data Level")
    for i, v in enumerate(s_df["Records"]):
        axes[0].text(v * 1.05, i, f"{v:,}", va='center', fontsize=9)

    axes[1].barh(s_df["Level"], s_df["Variables"],
                 color=[C["blue"], C["teal"], C["green"],
                        C["amber"], C["orange"], C["purple"]][:len(s_df)],
                 edgecolor='black')
    axes[1].set_xlabel("Number of Variables")
    axes[1].set_title("Variables per Data Level")
    for i, v in enumerate(s_df["Variables"]):
        axes[1].text(v + 0.3, i, str(v), va='center', fontsize=9)

    plt.suptitle("MinXSS-1 — Data Level Comparison", fontsize=13)
    plt.tight_layout()
    savefig("step12_level_comparison.png")
    plt.show()


# ─────────────────────────────────────────────────────────────
# STEP 13: FEATURE ENGINEERING
# ─────────────────────────────────────────────────────────────
def feature_engineering(df):
    print("\n" + "=" * 60)
    print("STEP 13: FEATURE ENGINEERING")
    print("=" * 60)

    df = df.copy()

    # 1. Instrument power (EPS 5V rail: P = V × I)
    if all(c in df.columns for c in ["eps_5v_voltage_V", "eps_5v_current_mA"]):
        df["x123_power_mW"] = df["eps_5v_voltage_V"] * df["eps_5v_current_mA"]
        print("  [+] x123_power_mW = V × I")

    # 2. Pointing cosine factor (1 = perfect, 0 = 90° off)
    if "sun_point_angle_error_deg" in df.columns:
        df["cos_pointing"] = np.cos(np.deg2rad(df["sun_point_angle_error_deg"]))
        print("  [+] cos_pointing = cos(angle_error)")

    # 3. Live-time fraction (detector quality flag)
    if all(c in df.columns for c in ["x123_live_time_ms", "x123_accum_time_ms"]):
        df["live_time_fraction"] = (df["x123_live_time_ms"] /
                                    df["x123_accum_time_ms"].replace(0, np.nan))
        df["live_time_fraction"] = df["live_time_fraction"].clip(0, 1)
        print("  [+] live_time_fraction = live_time / accum_time")

    # 4. Orbital position (derived)
    if "altitude_km" in df.columns:
        R_EARTH = 6371.0
        df["orbital_velocity_km_s"] = np.sqrt(
            398600.4418 / (R_EARTH + df["altitude_km"]))
        print("  [+] orbital_velocity_km_s = sqrt(GM / r)")

    # 5. Day-of-year & mission elapsed day
    df["day_of_year"]   = df.index.dayofyear
    df["mission_day"]   = (df.index - df.index.min()).days
    df["hour_of_day"]   = df.index.hour + df.index.minute / 60
    print("  [+] day_of_year, mission_day, hour_of_day")

    # 6. Log X-ray count rate (target for ML)
    if "x123_slow_count_cps" in df.columns:
        df["log_count_rate"] = np.log1p(df["x123_slow_count_cps"].clip(lower=0))
        print("  [+] log_count_rate = log(1 + slow_count)")

    # 7. Science quality flag
    #    = sunlit + not in SAA + good live time + pointing < 10°
    quality = pd.Series(True, index=df.index)
    if "eclipse_flag"          in df.columns: quality &= df["eclipse_flag"] == 0
    if "spacecraft_in_saa"     in df.columns: quality &= df["spacecraft_in_saa"] == 0
    if "live_time_fraction"    in df.columns: quality &= df["live_time_fraction"] > 0.9
    if "sun_point_angle_error_deg" in df.columns:
        quality &= df["sun_point_angle_error_deg"] < 10
    df["science_quality"] = quality.astype(int)
    sci_pct = quality.mean() * 100
    print(f"  [+] science_quality flag  ({sci_pct:.1f}% good)")

    new_features = ["x123_power_mW", "cos_pointing", "live_time_fraction",
                    "orbital_velocity_km_s", "day_of_year", "mission_day",
                    "hour_of_day", "log_count_rate", "science_quality"]
    print(f"\n  Sample of engineered features:\n"
          f"{df[[c for c in new_features if c in df.columns]].head(5).to_string()}")

    # Visualise key features
    fig, axes = plt.subplots(2, 3, figsize=(18, 9))
    axes = axes.flatten()

    feats_to_plot = [
        ("x123_power_mW",       "X123 Instrument Power (mW)",        C["blue"]),
        ("cos_pointing",        "cos(Sun Point Angle)",               C["amber"]),
        ("live_time_fraction",  "Live Time Fraction",                 C["green"]),
        ("log_count_rate",      "log(1 + Count Rate)",                C["purple"]),
        ("mission_day",         "Mission Day",                        C["teal"]),
        ("science_quality",     "Science Quality (0=bad, 1=good)",    C["orange"]),
    ]
    for i, (col, label, color) in enumerate(feats_to_plot):
        if col not in df.columns:
            axes[i].set_visible(False)
            continue
        axes[i].hist(df[col].dropna(), bins=50, color=color,
                     edgecolor='white', alpha=0.85)
        axes[i].set_title(label, fontsize=10)
        axes[i].set_xlabel("Value")
        axes[i].set_ylabel("Count")

    plt.suptitle("MinXSS-1 — Engineered Features", fontsize=14)
    plt.tight_layout()
    savefig("step13_features.png")
    plt.show()

    return df


# ─────────────────────────────────────────────────────────────
# STEP 14: SAVE CLEAN DATASET
# ─────────────────────────────────────────────────────────────
def save_clean_dataset(df):
    print("\n" + "=" * 60)
    print("STEP 14: SAVE CLEAN DATASET")
    print("=" * 60)

    clean = df.copy()

    # Keep only science-quality rows (recommended for ML training)
    if "science_quality" in clean.columns:
        before = len(clean)
        clean_sci = clean[clean["science_quality"] == 1].copy()
        print(f"  Science-quality rows : {len(clean_sci):,} / {before:,} "
              f"({len(clean_sci)/before*100:.1f}%)")
    else:
        clean_sci = clean

    # Reset index so timestamp becomes a column
    clean_sci = clean_sci.reset_index()
    clean_sci = clean_sci.rename(columns={"time": "timestamp_utc"})

    # Forward-fill any residual NaNs
    clean_sci = clean_sci.ffill().bfill()

    out_all = os.path.join(OUT_DIR, "minxss1_level0D_eda_all.csv")
    out_sci = os.path.join(OUT_DIR, "minxss1_level0D_eda_science.csv")

    df.reset_index().to_csv(out_all, index=False)
    clean_sci.to_csv(out_sci, index=False)

    print(f"\n  [Saved all records]     {out_all}")
    print(f"  [Saved science-quality] {out_sci}")
    print(f"\n  Columns in clean file: {clean_sci.columns.tolist()}")

    return clean_sci


# ─────────────────────────────────────────────────────────────
# STEP 15: EDA SUMMARY REPORT
# ─────────────────────────────────────────────────────────────
def eda_summary(df, clean_df):
    print("\n" + "=" * 60)
    print("EDA SUMMARY REPORT — MinXSS-1 Level 0D")
    print("=" * 60)

    print(f"Raw records         : {len(df):,}")
    print(f"Science-quality rows: {len(clean_df):,}")
    print(f"Time range          : {df.index.min()} → {df.index.max()}")

    if "eclipse_flag" in df.columns:
        ec = (df["eclipse_flag"] == 1).mean() * 100
        print(f"Eclipse fraction    : {ec:.1f}%")

    if "spacecraft_in_saa" in df.columns:
        saa = (df["spacecraft_in_saa"] == 1).mean() * 100
        print(f"SAA fraction        : {saa:.1f}%")

    if "sun_point_angle_error_deg" in df.columns:
        sunlit = df[df.get("eclipse_flag", pd.Series(1, index=df.index)) == 0]
        ang    = sunlit["sun_point_angle_error_deg"].dropna()
        print(f"Mean pointing error : {ang.mean():.2f}° (sunlit periods)")

    if "altitude_km" in df.columns:
        print(f"Altitude range      : {df['altitude_km'].min():.0f} – "
              f"{df['altitude_km'].max():.0f} km")

    if "x123_slow_count_cps" in df.columns:
        print(f"\nX-ray count rate (science quality):")
        crs = clean_df.get("x123_slow_count_cps", pd.Series(dtype=float))
        if len(crs):
            print(f"  Mean  : {crs.mean():.1f} cps")
            print(f"  Median: {crs.median():.1f} cps")
            print(f"  Max   : {crs.max():.1f} cps")

    print("\n─── Top correlates with x123_slow_count_cps ───")
    num = df.select_dtypes(include=[np.number]).dropna(axis=1, thresh=int(0.3 * len(df)))
    if "x123_slow_count_cps" in num.columns:
        corr = (num.corr()["x123_slow_count_cps"]
                .drop("x123_slow_count_cps", errors='ignore')
                .abs().sort_values(ascending=False).head(8))
        for feat, val in corr.items():
            sign = "+" if num.corr()["x123_slow_count_cps"][feat] > 0 else "−"
            print(f"  {sign}{val:.3f}  {feat}")

    print("\n─── Suggested ML targets ───")
    print("  1. Regression : predict x123_slow_count_cps from pointing + orbital params")
    print("  2. Regression : predict x123_power_mW from sun_point_angle + altitude")
    print("  3. Sequence   : LSTM on time-ordered EPS/ADCS data to predict next count rate")
    print("  4. Class.     : classify eclipse vs sunlit from EPS voltage alone")

    print("\n[EDA COMPLETE] All plots saved to:", OUT_DIR)


# ─────────────────────────────────────────────────────────────
# MAIN PIPELINE
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":

    # 1. Load
    datasets = load_datasets()

    # 2. Inventory (what's in each file)
    variable_inventory(datasets)

    # 3. Build tidy DataFrame from Level 0D
    df = build_dataframe_0D(datasets)
    if df is None:
        print("Level 0D not available. Exiting.")
        exit()

    # 4–6. Quality + distributions
    df = missing_value_analysis(df)
    outlier_analysis(df)
    univariate_analysis(df)

    # 7. Time series
    time_series_analysis(df)

    # 8. Eclipse & orbital
    df = eclipse_orbital_analysis(df)

    # 9. ADCS / sun pointing
    adcs_analysis(df)

    # 10. X-ray spectrum
    spectrum_analysis(datasets)

    # 11. Correlation
    correlation_analysis(df)

    # 12. Multi-level comparison
    multi_level_comparison(datasets)

    # 13. Feature engineering
    df = feature_engineering(df)

    # 14. Save
    clean_df = save_clean_dataset(df)

    # 15. Summary
    eda_summary(df, clean_df)

    # Close all NetCDF file handles
    for ds in datasets.values():
        ds.close()

    print("\n[Done] EDA complete. Clean CSV ready for ML pipeline.")