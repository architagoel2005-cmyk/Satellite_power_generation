<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Satellite Power ML Simulator</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Inter:wght@300;400;500;600&display=swap');
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#03040f;--panel:#080b1c;--panel2:#0c0f22;
  --b1:rgba(80,120,220,0.13);--b2:rgba(80,120,220,0.27);
  --t1:#dde4f8;--t2:#6a80aa;--t3:#38496a;
  --mono:'Space Mono',monospace;--sans:'Inter',sans-serif;
  --blue:#4fa3e8;--orange:#f5a623;--green:#4cc882;--red:#e85a5a;--purple:#a78bfa;
}
html,body{height:100%;overflow:hidden}
body{background:var(--bg);color:var(--t1);font-family:var(--sans);display:flex;flex-direction:column}

#sf{position:fixed;inset:0;pointer-events:none;z-index:0;overflow:hidden}
.st{position:absolute;border-radius:50%;background:#fff;animation:tw var(--d) ease-in-out infinite alternate}
@keyframes tw{from{opacity:var(--a0)}to{opacity:var(--a1)}}

#hdr{
  position:relative;z-index:10;flex-shrink:0;
  display:flex;align-items:center;justify-content:space-between;
  padding:9px 18px;background:rgba(3,4,15,0.92);
  border-bottom:1px solid var(--b2);backdrop-filter:blur(10px);
}
#hdr h1{font-family:var(--mono);font-size:11px;font-weight:700;letter-spacing:.1em;color:var(--blue);text-transform:uppercase}
#hdr p{font-size:9px;color:var(--t3);margin-top:1px;letter-spacing:.03em}
.badges{display:flex;gap:5px}
.badge{font-size:8.5px;font-family:var(--mono);padding:2px 7px;border-radius:3px;border:.5px solid;letter-spacing:.05em}
.b-blue  {color:var(--blue);  border-color:rgba(79,163,232,.4); background:rgba(79,163,232,.08)}
.b-green {color:var(--green); border-color:rgba(76,200,130,.4); background:rgba(76,200,130,.08)}
.b-orange{color:var(--orange);border-color:rgba(245,166,35,.4); background:rgba(245,166,35,.08)}

#layout{
  position:relative;z-index:1;display:grid;
  grid-template-columns:1fr 288px;
  flex:1;min-height:0;overflow:hidden;
}
#left{
  display:flex;flex-direction:column;gap:8px;
  padding:10px 8px 10px 12px;overflow-y:auto;min-height:0;
}
#cw{
  position:relative;border-radius:10px;overflow:hidden;
  border:.5px solid var(--b2);background:#020412;flex-shrink:0;
}
#cw canvas{display:block;border:none}
#cw::after{
  content:'';position:absolute;inset:0;pointer-events:none;border-radius:inherit;
  background:repeating-linear-gradient(0deg,transparent,transparent 3px,rgba(0,0,0,.025) 3px,rgba(0,0,0,.025) 4px);
}

#chips{display:grid;grid-template-columns:repeat(4,1fr);gap:7px;flex-shrink:0}
.chip{
  background:var(--panel);border:.5px solid var(--b1);border-radius:8px;
  padding:7px 11px;position:relative;overflow:hidden;
}
.chip::before{content:'';position:absolute;top:0;left:0;right:0;height:1.5px;
  background:linear-gradient(90deg,transparent,var(--cc,var(--blue)),transparent)}
.chip-lbl{font-size:7.5px;text-transform:uppercase;letter-spacing:.1em;color:var(--t3);margin-bottom:2px}
.chip-val{font-family:var(--mono);font-size:18px;font-weight:700;color:var(--cc,var(--blue));line-height:1.1}
.chip-sub{font-size:8px;color:var(--t2);margin-top:1px}

#mcharts{display:grid;grid-template-columns:1fr 1fr;gap:7px;flex-shrink:0}
.mc{background:var(--panel);border:.5px solid var(--b1);border-radius:8px;padding:9px 11px}
.mc-title{font-size:8px;text-transform:uppercase;letter-spacing:.08em;color:var(--t2);
  margin-bottom:5px;display:flex;align-items:center;gap:4px}
.mc-title .dot{width:5px;height:5px;border-radius:50%;background:var(--cc,var(--blue));
  box-shadow:0 0 4px var(--cc,var(--blue));flex-shrink:0}
.mc canvas{display:block}

#right{
  border-left:.5px solid var(--b1);
  background:linear-gradient(180deg,var(--panel) 0%,var(--bg) 100%);
  display:flex;flex-direction:column;gap:7px;padding:10px 11px;
  overflow-y:auto;min-height:0;
}
.sc{background:var(--panel2);border:.5px solid var(--b1);border-radius:8px;padding:9px 11px}
.sc-title{font-size:7.5px;text-transform:uppercase;letter-spacing:.12em;color:var(--t3);margin-bottom:7px}
.trow{display:flex;justify-content:space-between;align-items:center;padding:3px 0;
  border-bottom:.5px solid rgba(80,120,220,.06)}
.trow:last-child{border-bottom:none}
.tlbl{font-size:9.5px;color:var(--t2)}
.tval{font-family:var(--mono);font-size:10.5px;color:var(--t1)}
.bw{margin:2px 0 5px}
.bt{height:4px;background:rgba(255,255,255,.05);border-radius:2px;overflow:hidden}
.bf{height:100%;border-radius:inherit;transition:width .22s,background .22s}

#mbtn{
  width:100%;padding:7px;border-radius:6px;cursor:pointer;margin-bottom:6px;
  font-family:var(--mono);font-size:9.5px;letter-spacing:.04em;
  border:.5px solid rgba(79,163,232,.5);background:rgba(79,163,232,.08);color:var(--blue);
  transition:all .18s;
}
#mbtn:hover{background:rgba(79,163,232,.15)}
#mbtn.sensor{border-color:rgba(245,166,35,.5);background:rgba(245,166,35,.08);color:var(--orange)}
.adcs-live{font-size:9px;font-family:var(--mono);color:var(--orange);text-align:right}
#mdesc{font-size:9px;color:var(--t2);line-height:1.55}

.sat-grid{display:grid;grid-template-columns:1fr 1fr;gap:4px;margin-bottom:5px}
.sbn{padding:4px 0;border-radius:4px;border:.5px solid var(--b1);background:transparent;
  color:var(--t3);font-family:var(--mono);font-size:8.5px;cursor:pointer;text-align:center;
  letter-spacing:.04em;transition:all .14s}
.sbn:hover{color:var(--t1);border-color:var(--b2)}
.sbn.active{border-color:rgba(76,200,130,.5);color:var(--green);background:rgba(76,200,130,.08)}

.spd{display:flex;gap:3px}
.sb{flex:1;padding:4px 0;border-radius:4px;border:.5px solid var(--b1);background:transparent;
  color:var(--t3);font-family:var(--mono);font-size:9px;cursor:pointer;transition:all .14s}
.sb:hover{color:var(--t1)}
.sb.active{background:rgba(79,163,232,.1);color:var(--blue);border-color:var(--b2)}

.erow{margin-bottom:5px}
.elrow{display:flex;justify-content:space-between;margin-bottom:2px}
.elbl{font-size:9px;color:var(--t2)}
.eval{font-size:9.5px;font-family:var(--mono)}

#gain-big{font-family:var(--mono);font-size:24px;font-weight:700;text-align:center;
  color:var(--green);padding:6px 0 2px;letter-spacing:-.01em}
.gain-sub{font-size:8px;text-align:center;color:var(--t3);letter-spacing:.07em;text-transform:uppercase}

#rbtn{width:100%;padding:6px;border-radius:6px;border:.5px solid var(--b1);background:transparent;
  color:var(--t2);font-size:9.5px;cursor:pointer;font-family:var(--mono);letter-spacing:.04em;
  transition:all .14s}
#rbtn:hover{background:rgba(255,255,255,.04);color:var(--t1)}

.formula{font-family:var(--mono);font-size:8px;color:var(--t3);text-align:center;line-height:1.9;padding:3px 0}
#adcs-wrap{display:none}
/* ── MODE TABS ── */
#modetabs{display:flex;gap:6px;align-items:center;padding:7px 18px;background:rgba(3,4,15,0.92);border-bottom:.5px solid var(--b1);position:relative;z-index:10;flex-shrink:0}
.mtab{flex:1;max-width:280px;padding:7px 14px;border-radius:6px;font-family:var(--mono);font-size:9.5px;letter-spacing:.06em;cursor:pointer;border:.5px solid;transition:all .18s;text-align:center;font-weight:700;line-height:1.3}
.mtab-ml{border-color:rgba(76,200,130,.4);background:rgba(76,200,130,.05);color:rgba(76,200,130,.45)}
.mtab-ml.active{border-color:rgba(76,200,130,.9);background:rgba(76,200,130,.14);color:var(--green);box-shadow:0 0 14px rgba(76,200,130,.2)}
.mtab-sensor{border-color:rgba(245,166,35,.4);background:rgba(245,166,35,.05);color:rgba(245,166,35,.45)}
.mtab-sensor.active{border-color:rgba(245,166,35,.9);background:rgba(245,166,35,.14);color:var(--orange);box-shadow:0 0 14px rgba(245,166,35,.2)}
.mtab-sub{font-size:7.5px;font-family:var(--sans);font-weight:400;opacity:.7;margin-top:2px;letter-spacing:.03em}
.mode-divider{font-size:10px;color:var(--t3);font-family:var(--mono);opacity:.5;padding:0 4px;flex-shrink:0}
.mt-info{font-size:8px;color:var(--t3);font-family:var(--sans);flex:1;text-align:right;line-height:1.6}
.src-chip{font-size:8px;font-family:var(--mono);padding:4px 8px;border-radius:4px;border:.5px solid rgba(167,139,250,.3);background:rgba(167,139,250,.07);color:rgba(167,139,250,.75);margin-bottom:4px;display:block;line-height:1.55}
.src-chip b{color:rgba(200,175,255,.95)}
.cmpbanner{margin-top:6px;padding:7px 10px;border-radius:6px;display:flex;align-items:center;justify-content:space-between;gap:6px}
.cmp-gain{font-family:var(--mono);font-size:18px;font-weight:700;line-height:1}
.cmp-lbl{font-size:7.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--t3);margin-bottom:2px}


#tip{position:fixed;background:rgba(4,6,18,.96);border:.5px solid var(--b2);border-radius:6px;
  padding:6px 10px;font-size:10px;font-family:var(--mono);color:var(--t1);
  pointer-events:none;display:none;z-index:999;white-space:pre;line-height:1.5;
  backdrop-filter:blur(8px)}

@media(max-width:800px){
  #layout{grid-template-columns:1fr}
  #right{border-left:none;border-top:.5px solid var(--b1);max-height:380px}
  #chips{grid-template-columns:repeat(2,1fr)}
  html,body{overflow:auto}
}
</style>
</head>
<body>
<div id="sf"></div>
<div id="tip"></div>

<header id="hdr">
  <div>
    <h1>🛰 Satellite Power ML Simulator</h1>
    <p>MLP trained on 4,366 BIRDS CubeSat samples &nbsp;·&nbsp; R²=0.9994 &nbsp;·&nbsp; ML sun-tracking vs Sensor ADCS · live simulation of temperature, current, battery & power</p>
  </div>
  <div class="badges">
    <span class="badge b-blue"   id="b-mode">ML AUTO</span>
    <span class="badge b-green"  id="b-sat">PANEL POWER</span>
    <span class="badge b-orange" id="b-ecl">☀ SUNLIT</span>
  </div>
</header>

<div id="modetabs">
  <button class="mtab mtab-ml active" id="tab-ml" onclick="setMode('ml')">
    🤖 MODE 1 — ML PREDICTED
    <div class="mtab-sub">MLP cos(θ)=1.0 · always faces sun · R²=0.9994</div>
  </button>
  <span class="mode-divider">VS</span>
  <button class="mtab mtab-sensor" id="tab-sensor" onclick="setMode('sensor')">
    📡 MODE 2 — SENSOR ADCS
    <div class="mtab-sub">BIRDS CSS ±20° · MTQ 1.2°/s · ±8° deadband · 8 s re-acq</div>
  </button>
  <div class="mt-info">
    ML gain vs Sensor: <span id="hdr-gain" style="color:var(--green);font-family:var(--mono);font-weight:700;font-size:10px">+0.0%</span><br>
    Sensor data: <span style="color:rgba(167,139,250,.75)">BIRDS EPS 2022 · MinXSS-1 NASA 2017</span>
  </div>
</div>
<div id="layout">
<div id="left">
  <div id="cw"><canvas id="sim"></canvas></div>

  <div id="chips">
    <div class="chip" style="--cc:var(--orange)">
      <div class="chip-lbl">ML Predicted Power</div>
      <div class="chip-val" id="c-ml">0.000</div>
      <div class="chip-sub">W · perfect sun tracking</div>
    </div>
    <div class="chip" style="--cc:var(--blue)">
      <div class="chip-lbl">Sensor ADCS Power</div>
      <div class="chip-val" id="c-nad">0.000</div>
      <div class="chip-sub">W · imperfect sun tracking</div>
    </div>
    <div class="chip" style="--cc:var(--green)">
      <div class="chip-lbl">ML Efficiency Gain</div>
      <div class="chip-val" id="c-gain">+0.0%</div>
      <div class="chip-sub">cumulative over orbit</div>
    </div>
    <div class="chip" style="--cc:var(--purple)">
      <div class="chip-lbl">Panel Temperature</div>
      <div class="chip-val" id="c-tmp">25°C</div>
      <div class="chip-sub">η(T) = <span id="c-ef">1.000</span></div>
    </div>
  </div>

  <div id="mcharts">
    <div class="mc" style="--cc:var(--orange)">
      <div class="mc-title"><span class="dot"></span>Live Power — ML vs Sensor ADCS</div>
      <canvas id="ch-pw" height="72"></canvas>
    </div>
    <div class="mc" style="--cc:var(--purple)">
      <div class="mc-title"><span class="dot"></span>Panel Temperature</div>
      <canvas id="ch-tmp" height="72"></canvas>
    </div>
    <div class="mc" style="--cc:var(--blue)">
      <div class="mc-title"><span class="dot"></span>Battery State of Charge</div>
      <canvas id="ch-bat" height="72"></canvas>
    </div>
    <div class="mc" style="--cc:var(--blue)">
      <div class="mc-title"><span class="dot"></span>Panel Current (mA)</div>
      <canvas id="ch-cur" height="72"></canvas>
    </div>
  </div>
</div>

<aside id="right">
  <div class="sc">
    <div class="sc-title" id="mode-panel-title">Mode 1 — ML Predicted</div>
    <div id="ml-details">
      <div class="trow"><span class="tlbl">Architecture</span><span class="tval">MLP 4→12→6→1</span></div>
      <div class="trow"><span class="tlbl">cos(θ)</span><span class="tval" style="color:var(--green)">1.000 perfect</span></div>
      <div class="trow"><span class="tlbl">Pointing error</span><span class="tval" style="color:var(--green)">0.0°</span></div>
      <div class="trow"><span class="tlbl">R²</span><span class="tval" style="color:var(--green)">0.9994</span></div>
      <div class="trow"><span class="tlbl">MAE</span><span class="tval">0.014 W</span></div>
      <div class="trow"><span class="tlbl">Training samples</span><span class="tval">4,366</span></div>
      <div class="trow"><span class="tlbl">Live output</span><span id="v-inf" class="tval" style="color:var(--green)">—</span></div>
      <div class="cmpbanner" style="border:.5px solid rgba(76,200,130,.3);background:rgba(76,200,130,.07)">
        <div><div class="cmp-lbl">ML Efficiency Gain</div><div style="font-size:8px;color:var(--t2);margin-top:2px">vs Sensor ADCS mode</div></div>
        <div style="text-align:right">
          <div class="cmp-gain" id="gain-big-mode" style="color:var(--green)">+0.0%</div>
          <div style="font-size:7.5px;color:var(--t3);text-transform:uppercase;letter-spacing:.06em">cumul. energy</div>
        </div>
      </div>
    </div>
    <div id="sensor-details" style="display:none">
      <div class="trow" style="margin-top:2px"><span class="tlbl">ADCS state</span><span id="v-adcs-state" class="tval" style="color:var(--green)">TRACKING</span></div>
      <div class="trow"><span class="tlbl">Sensor angle</span><span id="v-sensor-ang" class="tval" style="color:var(--orange)">—</span></div>
      <div class="trow"><span class="tlbl">Tracking error</span><span id="v-track-err" class="tval" style="color:var(--orange)">—</span></div>
      <div class="trow"><span class="tlbl">Incidence θ</span><span id="v-inc" class="tval" style="color:var(--orange)">—</span></div>
      <div class="trow"><span class="tlbl" style="color:rgba(167,139,250,.8)">CSS noise [BIRDS]</span><span class="tval">±20°</span></div>
      <div class="trow"><span class="tlbl" style="color:rgba(167,139,250,.8)">MTQ slew [BIRDS]</span><span class="tval">1.2°/s</span></div>
      <div class="trow"><span class="tlbl" style="color:rgba(167,139,250,.8)">Deadband [BIRDS]</span><span class="tval">±8°</span></div>
      <div class="trow"><span class="tlbl" style="color:rgba(167,139,250,.8)">Re-acq [MinXSS]</span><span class="tval">8 s</span></div>
      <div class="cmpbanner" style="border:.5px solid rgba(245,166,35,.3);background:rgba(245,166,35,.07)">
        <div><div class="cmp-lbl" style="color:rgba(245,166,35,.8)">Power Lost vs ML</div><div style="font-size:8px;color:var(--t2);margin-top:2px">sensor errors cost</div></div>
        <div style="text-align:right">
          <div class="cmp-gain" id="gain-big2" style="color:var(--orange)">-0.0%</div>
          <div style="font-size:7.5px;color:var(--t3);text-transform:uppercase;letter-spacing:.06em">cumul. loss</div>
        </div>
      </div>
    </div>
  </div>

  <div class="sc" id="sensor-src-panel" style="display:none">
    <div class="sc-title">Open-Source Sensor Data</div>
    <span class="src-chip"><b>BIRDS EPS Dataset</b> · Jara et al. 2022<br>CSS noise ±20° · 1U CubeSat MTQ 1.2°/s<br>NepaliSat · Raavana · Tsuru · Uguisu</span>
    <span class="src-chip"><b>MinXSS-1 Archive</b> · NASA 2016–2017<br>Eclipse re-acq 5–10 s · ADCS telemetry<br>Sun-pointing validated &lt;0.002° fine mode</span>
    <span class="src-chip"><b>Rosetta SA Data</b> · ESA 2004–2016<br>Cosine-law incidence confirmed · ±1° nominal<br>Basis for sensor power loss calculation</span>
    <div style="font-size:7.5px;color:var(--t3);line-height:1.5;margin-top:4px">All sensor params from real on-orbit data, not theoretical estimates.</div>
  </div>

  <div class="sc">
    <div class="sc-title">Live Telemetry</div>
    <div class="trow"><span class="tlbl">Status</span><span id="v-ecl" class="tval" style="color:var(--orange)">☀ Sunlit</span></div>
    <div class="trow"><span class="tlbl">Current power</span><span id="v-pw" class="tval">—</span></div>
    <div class="bw"><div class="bt"><div id="b-pw" class="bf" style="width:0%;background:var(--orange)"></div></div></div>
    <div class="trow"><span class="tlbl">Battery</span><span id="v-bat" class="tval">100%</span></div>
    <div class="bw"><div class="bt"><div id="b-bat" class="bf" style="width:100%;background:var(--blue)"></div></div></div>
    <div class="trow"><span class="tlbl">Orbit position</span><span id="v-orb" class="tval">—</span></div>
    <div class="trow"><span class="tlbl" id="lbl-ang">Sun incidence θ</span><span id="v-ang" class="tval">—</span></div>
  </div>



  <div class="sc">
    <div class="sc-title">Cumulative Energy</div>
    <div class="erow">
      <div class="elrow"><span class="elbl">ML (sun-tracking)</span><span class="eval" id="e-ml" style="color:var(--blue)">0 J</span></div>
      <div class="bt" style="height:5px"><div id="b-eml" class="bf" style="width:50%;background:var(--blue)"></div></div>
    </div>
    <div class="erow">
      <div class="elrow"><span class="elbl">Sensor ADCS</span><span class="eval" id="e-nad" style="color:var(--orange)">0 J</span></div>
      <div class="bt" style="height:5px"><div id="b-enad" class="bf" style="width:50%;background:var(--orange)"></div></div>
    </div>
    <div id="gain-big">+0.0%</div>
    <div class="gain-sub">ML efficiency advantage</div>
  </div>

  <div class="sc">
    <div class="sc-title">Simulation Charts</div>
    <div style="font-size:8.5px;color:var(--t3);line-height:1.5;margin-bottom:5px">
      All 4 charts show live sim data for the hypothetical BIRDS-class CubeSat. Hover any chart for values.
    </div>
    <div class="trow"><span class="tlbl">Orbit period</span><span class="tval">~92 min (20s sim)</span></div>
    <div class="trow"><span class="tlbl">Sunlit fraction</span><span id="v-sun-pct" class="tval" style="color:var(--orange)">—</span></div>
    <div class="trow"><span class="tlbl">Avg ML power</span><span id="v-avg-ml" class="tval" style="color:var(--green)">—</span></div>
    <div class="trow"><span class="tlbl">Avg ADCS power</span><span id="v-avg-nad" class="tval" style="color:var(--orange)">—</span></div>
  </div>

  <div class="sc">
    <div class="sc-title">Simulation Speed</div>
    <div class="spd">
      <button class="sb active" onclick="setSp(1,this)">1×</button>
      <button class="sb"        onclick="setSp(3,this)">3×</button>
      <button class="sb"        onclick="setSp(8,this)">8×</button>
      <button class="sb"        onclick="setSp(20,this)">20×</button>
    </div>
  </div>

  <button id="rbtn" onclick="resetSim()">↺ RESET SIMULATION</button>

  <div class="formula">
    P_ML    = MLP(1.0, η(T), Vbat, φ)<br>
    P_sensor = MLP(cos θ_css, η(T), Vbat, φ)<br>
    η(T) = 1 − 0.004·max(0, T−25)
  </div>
</aside>
</div>

<script>
// ════════════════════════════════════════════════
// EMBEDDED DATA  (ML weights + BIRDS + CSIM)
// ════════════════════════════════════════════════
const MLDATA     = {"weights": {"coefs": [[[0.1408316302348222, 3.998738458580801e-05, 0.6508763590237119, 0.46796951264955217, -0.07671069895056755, -0.3650631546834094, -1.00931786857714, 0.8161414600152179, -4.2854402870002375e-10, 1.4645831470493497e-09, -0.00015200124520859214, 0.4913205451509753], [0.48834306525413024, 7.457380353154238e-09, -0.3460931365399752, -0.3770901476833151, -0.15121533441541932, -0.16000900513566704, 0.2967100739776889, -0.14459800163509035, 4.846594611362706e-10, 7.154425562599812e-08, -1.416351474369608e-09, -0.25225730764796606], [0.15997558492427247, -3.853212036506367e-09, -0.09994636426465772, 0.2256142213991834, 0.3702824447271444, -0.7070611042634591, 0.1558432526741329, -0.1117350066453123, -1.4716282038434705e-05, 3.6081101556523325e-05, 8.462190951033468e-05, 0.28868276671532755], [-0.22168151343083645, 5.098402850484503e-07, 0.15351199761610465, -0.1539879933582498, -0.6199950772303439, -0.19795597170149362, -0.06228873528619024, 0.49231091115578307, 3.905544541628757e-09, -5.059302803120998e-11, 1.2655965567721196e-09, -0.0642512260237566]], [[3.0667580093443314e-10, -0.09868978981849845, 0.5068374832959095, -4.526492683849401e-10, -0.17832297827592533, 0.08716302567943872], [-9.492684292927239e-08, -3.486113035877228e-09, 6.071096445409235e-07, 6.184179014852099e-05, 2.7902552290885945e-09, 2.30371451091532e-09], [-8.683533820228479e-05, 0.6386296353681766, 0.45531678220675537, 2.256247179146288e-09, 0.3085369706141622, -0.47354165205683374], [-2.4080925368305113e-10, 0.0039698052892581746, 0.8323972068327538, 3.4001659345295663e-10, -0.5108511459348567, -0.691370133459474], [-5.95568671046115e-10, 0.2268750478664333, 0.44749312539047886, -2.962646408331132e-10, 0.4810880845180351, -0.11996990217350023], [3.553772527207256e-08, 0.07310961369266333, 0.14245719138363688, -2.9749155634219026e-10, 0.48424284235911236, 0.14646781163004996], [2.907534815789035e-11, -0.35608818108055545, -1.0634907039128207, 3.1390401142864406e-07, -0.1864337166451359, 0.6883417546089788], [-9.995368337759037e-10, 0.24420815562202822, 0.6478857972812309, 3.5123073925552316e-09, -0.13527849176595136, 0.3107927508320637], [-2.1420052691032563e-09, 7.481836765338063e-07, 9.304925604443034e-10, -1.1121179879408394e-08, -2.161893997493837e-07, -1.1667402076989513e-08], [-5.944640976755246e-10, 7.130040125889673e-08, -5.467373464991378e-09, 1.8387766595670206e-08, -3.2735451978393186e-07, -7.577377752348028e-11], [-1.0721800037197018e-08, -4.3743190148143514e-07, -1.1060742363036472e-09, 2.517342232731177e-07, -2.6783928782685305e-09, 2.684367730498738e-10], [-2.220709145221158e-08, 0.578321126748722, -0.4611157303321292, -9.784090161815637e-12, -0.27479276207793196, -0.3998308885711699]], [[-1.0148417774537694e-09], [1.279700285560686], [1.0602281635092046], [5.003102700828382e-07], [-0.13316188732891163], [-0.5242872445208767]]], "intercepts": [[0.13851260201143872, -0.3859728893370207, 0.6186613429404193, 0.34757415865181684, 0.626694992833138, 0.2931431994024437, 0.4999999821664102, 0.6277506532147917, -0.5039916976510964, -0.372343430067303, -0.5569805455556673, -0.3025689979870161], [-0.4389416649963954, -0.10209760055597827, 0.5948524626079219, -0.20414766957950703, 0.10265310240565982, 0.25424218310939783], [-0.3150844055865817]], "n_features": 4, "feature_names": ["cos_theta", "temp_efficiency", "vbat_norm", "cycle_phase"], "stats": {"pmin": 0.01800417096, "pmax": 4.16705181984, "pmean": 0.9536273390244802, "r2": 0.9994, "mae": 0.0145, "n": 4366}}, "sat_curves": {"nepalisat": [{"t": 0.0, "pw": 1.048, "vb": 4.2, "tp": 13.9, "ic": 209.8, "ef": 1.0}, {"t": 30.0, "pw": 2.944, "vb": 4.12, "tp": 13.8, "ic": 615.3, "ef": 1.0}, {"t": 60.0, "pw": 1.304, "vb": 4.2, "tp": 14.4, "ic": 251.7, "ef": 1.0}, {"t": 90.0, "pw": 1.295, "vb": 4.2, "tp": 15.0, "ic": 251.7, "ef": 1.0}, {"t": 120.0, "pw": 1.239, "vb": 4.2, "tp": 15.1, "ic": 247.0, "ef": 1.0}, {"t": 150.0, "pw": 1.275, "vb": 4.2, "tp": 14.9, "ic": 256.4, "ef": 1.0}, {"t": 180.0, "pw": 1.203, "vb": 4.2, "tp": 14.5, "ic": 247.0, "ef": 1.0}, {"t": 210.0, "pw": 1.195, "vb": 4.2, "tp": 14.0, "ic": 242.4, "ef": 1.0}, {"t": 240.0, "pw": 1.29, "vb": 4.2, "tp": 14.0, "ic": 256.3, "ef": 1.0}, {"t": 270.0, "pw": 1.522, "vb": 4.2, "tp": 14.4, "ic": 298.3, "ef": 1.0}, {"t": 300.0, "pw": 1.247, "vb": 4.2, "tp": 15.1, "ic": 242.4, "ef": 1.0}, {"t": 330.0, "pw": 3.465, "vb": 4.1, "tp": 14.6, "ic": 741.1, "ef": 1.0}, {"t": 360.0, "pw": 1.447, "vb": 4.2, "tp": 15.0, "ic": 284.3, "ef": 1.0}, {"t": 390.0, "pw": 1.726, "vb": 4.2, "tp": 14.6, "ic": 344.9, "ef": 1.0}, {"t": 420.0, "pw": 1.789, "vb": 4.2, "tp": 15.1, "ic": 349.6, "ef": 1.0}, {"t": 450.0, "pw": 1.422, "vb": 4.2, "tp": 16.0, "ic": 275.0, "ef": 1.0}, {"t": 480.0, "pw": 1.364, "vb": 4.2, "tp": 16.5, "ic": 265.7, "ef": 1.0}, {"t": 510.0, "pw": 1.31, "vb": 4.2, "tp": 16.9, "ic": 261.0, "ef": 1.0}, {"t": 540.0, "pw": 1.543, "vb": 4.2, "tp": 16.2, "ic": 317.0, "ef": 1.0}, {"t": 570.0, "pw": 1.19, "vb": 4.2, "tp": 15.2, "ic": 251.7, "ef": 1.0}, {"t": 600.0, "pw": 1.252, "vb": 4.2, "tp": 14.2, "ic": 251.7, "ef": 1.0}, {"t": 630.0, "pw": 1.258, "vb": 4.2, "tp": 14.7, "ic": 247.0, "ef": 1.0}, {"t": 660.0, "pw": 1.481, "vb": 4.2, "tp": 15.4, "ic": 293.7, "ef": 1.0}, {"t": 690.0, "pw": 1.174, "vb": 4.2, "tp": 15.5, "ic": 237.7, "ef": 1.0}, {"t": 720.0, "pw": 1.176, "vb": 4.2, "tp": 15.5, "ic": 242.4, "ef": 1.0}, {"t": 750.0, "pw": 1.241, "vb": 4.2, "tp": 14.9, "ic": 256.4, "ef": 1.0}, {"t": 780.0, "pw": 1.212, "vb": 4.2, "tp": 13.7, "ic": 265.7, "ef": 1.0}, {"t": 810.0, "pw": 1.203, "vb": 4.2, "tp": 13.2, "ic": 237.7, "ef": 1.0}, {"t": 840.0, "pw": 1.224, "vb": 4.2, "tp": 14.1, "ic": 237.7, "ef": 1.0}, {"t": 870.0, "pw": 1.112, "vb": 4.2, "tp": 14.7, "ic": 237.7, "ef": 1.0}, {"t": 900.0, "pw": 1.169, "vb": 4.2, "tp": 14.7, "ic": 233.0, "ef": 1.0}, {"t": 930.0, "pw": 1.099, "vb": 4.2, "tp": 14.8, "ic": 228.4, "ef": 1.0}, {"t": 960.0, "pw": 1.096, "vb": 4.2, "tp": 14.1, "ic": 237.7, "ef": 1.0}, {"t": 990.0, "pw": 1.116, "vb": 4.2, "tp": 12.5, "ic": 228.4, "ef": 1.0}, {"t": 1020.0, "pw": 1.177, "vb": 4.2, "tp": 12.6, "ic": 233.1, "ef": 1.0}, {"t": 1050.0, "pw": 1.217, "vb": 4.2, "tp": 13.4, "ic": 237.7, "ef": 1.0}, {"t": 1080.0, "pw": 1.028, "vb": 4.2, "tp": 13.6, "ic": 237.7, "ef": 1.0}, {"t": 1110.0, "pw": 1.366, "vb": 4.2, "tp": 14.0, "ic": 275.0, "ef": 1.0}, {"t": 1140.0, "pw": 1.109, "vb": 4.2, "tp": 14.2, "ic": 233.1, "ef": 1.0}, {"t": 1170.0, "pw": 0.219, "vb": 4.15, "tp": 12.9, "ic": 51.3, "ef": 1.0}, {"t": 1200.0, "pw": 1.17, "vb": 4.2, "tp": 12.0, "ic": 247.0, "ef": 1.0}, {"t": 1230.0, "pw": 1.469, "vb": 4.2, "tp": 12.5, "ic": 298.3, "ef": 1.0}, {"t": 1260.0, "pw": 1.175, "vb": 4.2, "tp": 13.4, "ic": 237.7, "ef": 1.0}, {"t": 1290.0, "pw": 1.02, "vb": 4.2, "tp": 13.4, "ic": 237.7, "ef": 1.0}, {"t": 1320.0, "pw": 0.869, "vb": 4.2, "tp": 14.0, "ic": 223.7, "ef": 1.0}, {"t": 1350.0, "pw": 1.143, "vb": 4.2, "tp": 13.6, "ic": 293.6, "ef": 1.0}, {"t": 1380.0, "pw": 0.772, "vb": 4.15, "tp": 12.0, "ic": 228.4, "ef": 1.0}, {"t": 1410.0, "pw": 0.881, "vb": 4.2, "tp": 11.7, "ic": 247.0, "ef": 1.0}, {"t": 1440.0, "pw": 0.925, "vb": 4.2, "tp": 12.4, "ic": 247.0, "ef": 1.0}, {"t": 1470.0, "pw": 1.142, "vb": 4.2, "tp": 13.0, "ic": 303.0, "ef": 1.0}, {"t": 1500.0, "pw": 0.965, "vb": 4.2, "tp": 13.3, "ic": 242.4, "ef": 1.0}, {"t": 1530.0, "pw": 0.8, "vb": 4.2, "tp": 13.3, "ic": 247.0, "ef": 1.0}, {"t": 1560.0, "pw": 0.665, "vb": 4.2, "tp": 12.5, "ic": 247.0, "ef": 1.0}, {"t": 1590.0, "pw": 0.656, "vb": 4.2, "tp": 11.2, "ic": 228.4, "ef": 1.0}, {"t": 1620.0, "pw": 0.731, "vb": 4.2, "tp": 11.4, "ic": 247.0, "ef": 1.0}, {"t": 1650.0, "pw": 0.89, "vb": 4.2, "tp": 12.1, "ic": 242.4, "ef": 1.0}, {"t": 1680.0, "pw": 0.902, "vb": 4.2, "tp": 12.7, "ic": 247.0, "ef": 1.0}, {"t": 1710.0, "pw": 1.054, "vb": 4.2, "tp": 13.1, "ic": 298.3, "ef": 1.0}, {"t": 1740.0, "pw": 0.069, "vb": 4.15, "tp": 11.9, "ic": 28.0, "ef": 1.0}, {"t": 1770.0, "pw": 0.031, "vb": 4.15, "tp": 10.1, "ic": 23.3, "ef": 1.0}, {"t": 1800.0, "pw": 0.025, "vb": 4.12, "tp": 8.3, "ic": 18.6, "ef": 1.0}, {"t": 1830.0, "pw": 0.031, "vb": 4.1, "tp": 6.7, "ic": 23.3, "ef": 1.0}, {"t": 1860.0, "pw": 0.024, "vb": 4.1, "tp": 5.2, "ic": 18.6, "ef": 1.0}, {"t": 1890.0, "pw": 0.03, "vb": 4.1, "tp": 3.8, "ic": 23.3, "ef": 1.0}, {"t": 1920.0, "pw": 0.024, "vb": 4.07, "tp": 2.4, "ic": 18.6, "ef": 1.0}, {"t": 1950.0, "pw": 0.024, "vb": 4.07, "tp": 1.2, "ic": 18.6, "ef": 1.0}, {"t": 1980.0, "pw": 0.03, "vb": 4.07, "tp": 0.2, "ic": 23.3, "ef": 1.0}, {"t": 2010.0, "pw": 0.024, "vb": 4.07, "tp": -0.7, "ic": 18.6, "ef": 1.0}, {"t": 2040.0, "pw": 0.03, "vb": 4.04, "tp": -1.5, "ic": 23.3, "ef": 1.0}, {"t": 2070.0, "pw": 0.024, "vb": 4.04, "tp": -2.4, "ic": 18.6, "ef": 1.0}, {"t": 2100.0, "pw": 0.03, "vb": 4.04, "tp": -3.2, "ic": 23.3, "ef": 1.0}, {"t": 2130.0, "pw": 0.024, "vb": 4.04, "tp": -4.1, "ic": 18.6, "ef": 1.0}, {"t": 2160.0, "pw": 0.024, "vb": 4.02, "tp": -5.0, "ic": 18.6, "ef": 1.0}, {"t": 2190.0, "pw": 0.024, "vb": 4.02, "tp": -5.6, "ic": 18.6, "ef": 1.0}, {"t": 2220.0, "pw": 0.024, "vb": 4.02, "tp": -6.2, "ic": 18.6, "ef": 1.0}, {"t": 2250.0, "pw": 0.024, "vb": 4.02, "tp": -6.7, "ic": 18.6, "ef": 1.0}, {"t": 2280.0, "pw": 0.024, "vb": 3.99, "tp": -7.4, "ic": 18.6, "ef": 1.0}, {"t": 2310.0, "pw": 0.024, "vb": 3.99, "tp": -8.1, "ic": 18.6, "ef": 1.0}, {"t": 2340.0, "pw": 0.024, "vb": 3.99, "tp": -8.7, "ic": 18.6, "ef": 1.0}, {"t": 2370.0, "pw": 0.024, "vb": 3.99, "tp": -9.3, "ic": 18.6, "ef": 1.0}, {"t": 2400.0, "pw": 0.024, "vb": 3.97, "tp": -9.8, "ic": 18.6, "ef": 1.0}, {"t": 2430.0, "pw": 0.024, "vb": 3.97, "tp": -10.3, "ic": 18.6, "ef": 1.0}, {"t": 2460.0, "pw": 0.024, "vb": 3.99, "tp": -10.8, "ic": 18.6, "ef": 1.0}, {"t": 2490.0, "pw": 0.03, "vb": 3.97, "tp": -11.4, "ic": 23.3, "ef": 1.0}, {"t": 2520.0, "pw": 0.024, "vb": 3.97, "tp": -12.0, "ic": 18.6, "ef": 1.0}, {"t": 2550.0, "pw": 0.024, "vb": 3.97, "tp": -12.6, "ic": 18.6, "ef": 1.0}, {"t": 2580.0, "pw": 0.024, "vb": 3.97, "tp": -13.0, "ic": 18.6, "ef": 1.0}, {"t": 2610.0, "pw": 0.024, "vb": 3.97, "tp": -13.5, "ic": 18.6, "ef": 1.0}, {"t": 2640.0, "pw": 0.03, "vb": 3.97, "tp": -13.9, "ic": 23.3, "ef": 1.0}, {"t": 2670.0, "pw": 0.024, "vb": 3.94, "tp": -14.4, "ic": 18.6, "ef": 1.0}, {"t": 2700.0, "pw": 0.024, "vb": 3.94, "tp": -14.9, "ic": 18.6, "ef": 1.0}, {"t": 2730.0, "pw": 0.024, "vb": 3.94, "tp": -15.4, "ic": 18.6, "ef": 1.0}, {"t": 2760.0, "pw": 0.03, "vb": 3.94, "tp": -15.8, "ic": 23.3, "ef": 1.0}, {"t": 2790.0, "pw": 0.03, "vb": 3.94, "tp": -16.1, "ic": 23.3, "ef": 1.0}, {"t": 2820.0, "pw": 0.03, "vb": 3.94, "tp": -16.3, "ic": 23.3, "ef": 1.0}, {"t": 2850.0, "pw": 0.03, "vb": 3.94, "tp": -16.6, "ic": 23.3, "ef": 1.0}, {"t": 2880.0, "pw": 0.03, "vb": 3.92, "tp": -17.0, "ic": 23.3, "ef": 1.0}, {"t": 2910.0, "pw": 0.024, "vb": 3.92, "tp": -17.4, "ic": 18.6, "ef": 1.0}, {"t": 2940.0, "pw": 0.024, "vb": 3.92, "tp": -18.0, "ic": 18.6, "ef": 1.0}, {"t": 2970.0, "pw": 0.024, "vb": 3.92, "tp": -18.4, "ic": 18.6, "ef": 1.0}, {"t": 3000.0, "pw": 0.024, "vb": 3.92, "tp": -18.9, "ic": 18.6, "ef": 1.0}, {"t": 3030.0, "pw": 0.024, "vb": 3.92, "tp": -19.1, "ic": 18.6, "ef": 1.0}, {"t": 3060.0, "pw": 0.024, "vb": 3.92, "tp": -19.5, "ic": 18.6, "ef": 1.0}, {"t": 3090.0, "pw": 0.03, "vb": 3.92, "tp": -19.8, "ic": 23.3, "ef": 1.0}, {"t": 3120.0, "pw": 0.024, "vb": 3.92, "tp": -20.2, "ic": 18.6, "ef": 1.0}, {"t": 3150.0, "pw": 0.036, "vb": 3.92, "tp": -20.6, "ic": 28.0, "ef": 1.0}, {"t": 3180.0, "pw": 0.024, "vb": 3.92, "tp": -20.8, "ic": 18.6, "ef": 1.0}, {"t": 3210.0, "pw": 0.036, "vb": 3.89, "tp": -21.0, "ic": 28.0, "ef": 1.0}, {"t": 3240.0, "pw": 0.024, "vb": 3.89, "tp": -21.0, "ic": 18.6, "ef": 1.0}, {"t": 3270.0, "pw": 0.03, "vb": 3.89, "tp": -21.1, "ic": 23.3, "ef": 1.0}, {"t": 3300.0, "pw": 0.03, "vb": 3.89, "tp": -21.2, "ic": 23.3, "ef": 1.0}, {"t": 3330.0, "pw": 0.03, "vb": 3.89, "tp": -21.6, "ic": 23.3, "ef": 1.0}, {"t": 3360.0, "pw": 0.03, "vb": 3.89, "tp": -21.8, "ic": 23.3, "ef": 1.0}, {"t": 3390.0, "pw": 0.024, "vb": 3.89, "tp": -22.0, "ic": 18.6, "ef": 1.0}, {"t": 3420.0, "pw": 0.03, "vb": 3.89, "tp": -22.2, "ic": 23.3, "ef": 1.0}, {"t": 3450.0, "pw": 0.024, "vb": 3.89, "tp": -22.2, "ic": 18.6, "ef": 1.0}, {"t": 3480.0, "pw": 0.024, "vb": 3.89, "tp": -22.4, "ic": 18.6, "ef": 1.0}, {"t": 3510.0, "pw": 0.024, "vb": 3.87, "tp": -22.6, "ic": 18.6, "ef": 1.0}, {"t": 3540.0, "pw": 0.024, "vb": 3.87, "tp": -23.0, "ic": 18.6, "ef": 1.0}, {"t": 3570.0, "pw": 0.036, "vb": 3.87, "tp": -23.3, "ic": 28.0, "ef": 1.0}, {"t": 3600.0, "pw": 0.03, "vb": 3.87, "tp": -23.5, "ic": 23.3, "ef": 1.0}, {"t": 3630.0, "pw": 0.03, "vb": 3.87, "tp": -23.6, "ic": 23.3, "ef": 1.0}, {"t": 3660.0, "pw": 0.03, "vb": 3.87, "tp": -23.7, "ic": 23.3, "ef": 1.0}, {"t": 3690.0, "pw": 0.024, "vb": 3.87, "tp": -23.9, "ic": 18.6, "ef": 1.0}, {"t": 3720.0, "pw": 0.03, "vb": 3.87, "tp": -24.2, "ic": 18.6, "ef": 1.0}, {"t": 3750.0, "pw": 1.902, "vb": 3.97, "tp": -23.7, "ic": 568.7, "ef": 1.0}, {"t": 3780.0, "pw": 2.001, "vb": 3.99, "tp": -22.1, "ic": 596.6, "ef": 1.0}, {"t": 3810.0, "pw": 2.414, "vb": 4.02, "tp": -20.5, "ic": 694.5, "ef": 1.0}, {"t": 3840.0, "pw": 1.445, "vb": 4.02, "tp": -19.1, "ic": 536.0, "ef": 1.0}, {"t": 3870.0, "pw": 0.733, "vb": 3.97, "tp": -18.4, "ic": 261.0, "ef": 1.0}, {"t": 3900.0, "pw": 0.611, "vb": 3.94, "tp": -18.6, "ic": 223.7, "ef": 1.0}, {"t": 3930.0, "pw": 1.699, "vb": 4.02, "tp": -17.9, "ic": 629.2, "ef": 1.0}, {"t": 3960.0, "pw": 2.711, "vb": 4.07, "tp": -16.6, "ic": 797.0, "ef": 1.0}, {"t": 3990.0, "pw": 2.495, "vb": 4.04, "tp": -15.7, "ic": 550.0, "ef": 1.0}, {"t": 4020.0, "pw": 2.953, "vb": 4.12, "tp": -14.5, "ic": 755.1, "ef": 1.0}, {"t": 4050.0, "pw": 1.983, "vb": 4.07, "tp": -13.4, "ic": 545.3, "ef": 1.0}, {"t": 4080.0, "pw": 0.262, "vb": 3.99, "tp": -13.4, "ic": 79.2, "ef": 1.0}, {"t": 4110.0, "pw": 1.799, "vb": 4.04, "tp": -13.7, "ic": 452.1, "ef": 1.0}, {"t": 4140.0, "pw": 3.089, "vb": 4.1, "tp": -13.0, "ic": 713.1, "ef": 1.0}, {"t": 4170.0, "pw": 2.969, "vb": 4.12, "tp": -11.9, "ic": 741.1, "ef": 1.0}, {"t": 4200.0, "pw": 3.289, "vb": 4.15, "tp": -11.3, "ic": 703.8, "ef": 1.0}, {"t": 4230.0, "pw": 3.175, "vb": 4.15, "tp": -10.1, "ic": 680.5, "ef": 1.0}, {"t": 4260.0, "pw": 1.879, "vb": 4.12, "tp": -9.6, "ic": 419.5, "ef": 1.0}, {"t": 4290.0, "pw": 0.735, "vb": 4.07, "tp": -10.2, "ic": 158.5, "ef": 1.0}, {"t": 4320.0, "pw": 2.969, "vb": 4.15, "tp": -9.9, "ic": 643.2, "ef": 1.0}, {"t": 4350.0, "pw": 3.523, "vb": 4.2, "tp": -9.1, "ic": 680.5, "ef": 1.0}, {"t": 4380.0, "pw": 2.731, "vb": 4.2, "tp": -8.1, "ic": 624.6, "ef": 1.0}, {"t": 4410.0, "pw": 2.871, "vb": 4.2, "tp": -7.3, "ic": 550.0, "ef": 1.0}, {"t": 4440.0, "pw": 2.597, "vb": 4.2, "tp": -6.4, "ic": 517.4, "ef": 1.0}, {"t": 4470.0, "pw": 1.761, "vb": 4.15, "tp": -6.3, "ic": 377.5, "ef": 1.0}, {"t": 4500.0, "pw": 1.825, "vb": 4.15, "tp": -6.8, "ic": 391.5, "ef": 1.0}, {"t": 4530.0, "pw": 2.422, "vb": 4.2, "tp": -6.5, "ic": 466.1, "ef": 1.0}, {"t": 4560.0, "pw": 2.251, "vb": 4.2, "tp": -5.3, "ic": 428.8, "ef": 1.0}, {"t": 4590.0, "pw": 2.233, "vb": 4.2, "tp": -4.2, "ic": 419.5, "ef": 1.0}, {"t": 4620.0, "pw": 1.987, "vb": 4.2, "tp": -3.2, "ic": 377.6, "ef": 1.0}, {"t": 4650.0, "pw": 2.026, "vb": 4.2, "tp": -2.5, "ic": 391.5, "ef": 1.0}, {"t": 4680.0, "pw": 1.866, "vb": 4.2, "tp": -2.4, "ic": 368.2, "ef": 1.0}, {"t": 4710.0, "pw": 1.776, "vb": 4.2, "tp": -2.5, "ic": 344.9, "ef": 1.0}, {"t": 4740.0, "pw": 1.652, "vb": 4.2, "tp": -2.1, "ic": 316.9, "ef": 1.0}, {"t": 4770.0, "pw": 1.716, "vb": 4.2, "tp": -1.3, "ic": 330.9, "ef": 1.0}, {"t": 4800.0, "pw": 1.824, "vb": 4.2, "tp": 0.2, "ic": 340.3, "ef": 1.0}, {"t": 4830.0, "pw": 1.756, "vb": 4.2, "tp": 1.8, "ic": 330.9, "ef": 1.0}, {"t": 4860.0, "pw": 1.951, "vb": 4.2, "tp": 2.8, "ic": 372.9, "ef": 1.0}, {"t": 4890.0, "pw": 1.591, "vb": 4.2, "tp": 3.3, "ic": 307.6, "ef": 1.0}, {"t": 4920.0, "pw": 1.51, "vb": 4.2, "tp": 3.2, "ic": 293.6, "ef": 1.0}, {"t": 4950.0, "pw": 1.513, "vb": 4.2, "tp": 3.5, "ic": 293.7, "ef": 1.0}, {"t": 4980.0, "pw": 1.518, "vb": 4.2, "tp": 4.0, "ic": 289.0, "ef": 1.0}, {"t": 5010.0, "pw": 1.578, "vb": 4.2, "tp": 5.2, "ic": 298.3, "ef": 1.0}, {"t": 5040.0, "pw": 1.53, "vb": 4.2, "tp": 6.4, "ic": 293.6, "ef": 1.0}, {"t": 5070.0, "pw": 1.496, "vb": 4.2, "tp": 7.0, "ic": 289.0, "ef": 1.0}, {"t": 5100.0, "pw": 1.729, "vb": 4.2, "tp": 7.4, "ic": 340.3, "ef": 1.0}, {"t": 5130.0, "pw": 1.431, "vb": 4.2, "tp": 7.2, "ic": 284.3, "ef": 1.0}, {"t": 5160.0, "pw": 1.396, "vb": 4.2, "tp": 7.1, "ic": 275.0, "ef": 1.0}, {"t": 5190.0, "pw": 1.477, "vb": 4.2, "tp": 7.6, "ic": 284.3, "ef": 1.0}, {"t": 5220.0, "pw": 1.365, "vb": 4.2, "tp": 8.6, "ic": 261.0, "ef": 1.0}, {"t": 5250.0, "pw": 1.448, "vb": 4.2, "tp": 9.5, "ic": 279.6, "ef": 1.0}, {"t": 5280.0, "pw": 1.455, "vb": 4.2, "tp": 10.3, "ic": 284.3, "ef": 1.0}, {"t": 5310.0, "pw": 1.396, "vb": 4.2, "tp": 10.6, "ic": 275.0, "ef": 1.0}, {"t": 5340.0, "pw": 1.682, "vb": 4.2, "tp": 10.7, "ic": 335.6, "ef": 1.0}, {"t": 5370.0, "pw": 1.338, "vb": 4.2, "tp": 10.8, "ic": 265.7, "ef": 1.0}], "raavana": [{"t": 0.0, "pw": 1.047, "vb": 4.17, "tp": 11.8, "ic": 261.0, "ef": 1.0}, {"t": 30.0, "pw": 1.147, "vb": 4.17, "tp": 12.0, "ic": 275.0, "ef": 1.0}, {"t": 60.0, "pw": 1.136, "vb": 4.17, "tp": 12.9, "ic": 275.0, "ef": 1.0}, {"t": 90.0, "pw": 0.917, "vb": 4.15, "tp": 13.3, "ic": 247.0, "ef": 1.0}, {"t": 120.0, "pw": 1.668, "vb": 4.02, "tp": 12.7, "ic": 447.5, "ef": 1.0}, {"t": 150.0, "pw": 1.895, "vb": 4.17, "tp": 13.4, "ic": 475.4, "ef": 1.0}, {"t": 180.0, "pw": 1.625, "vb": 4.17, "tp": 12.8, "ic": 405.5, "ef": 1.0}, {"t": 210.0, "pw": 1.425, "vb": 4.17, "tp": 12.5, "ic": 354.2, "ef": 1.0}, {"t": 240.0, "pw": 1.237, "vb": 4.17, "tp": 12.4, "ic": 307.6, "ef": 1.0}, {"t": 270.0, "pw": 1.321, "vb": 4.17, "tp": 12.7, "ic": 321.6, "ef": 1.0}, {"t": 300.0, "pw": 1.539, "vb": 4.17, "tp": 12.8, "ic": 377.5, "ef": 1.0}, {"t": 330.0, "pw": 1.322, "vb": 4.17, "tp": 12.4, "ic": 335.6, "ef": 1.0}, {"t": 360.0, "pw": 1.208, "vb": 4.17, "tp": 12.4, "ic": 289.0, "ef": 1.0}, {"t": 390.0, "pw": 1.229, "vb": 4.17, "tp": 12.7, "ic": 298.3, "ef": 1.0}, {"t": 420.0, "pw": 1.199, "vb": 4.17, "tp": 13.1, "ic": 293.6, "ef": 1.0}, {"t": 450.0, "pw": 1.172, "vb": 4.17, "tp": 13.8, "ic": 293.6, "ef": 1.0}, {"t": 480.0, "pw": 1.044, "vb": 4.17, "tp": 14.0, "ic": 279.7, "ef": 1.0}, {"t": 510.0, "pw": 1.186, "vb": 4.17, "tp": 14.4, "ic": 293.6, "ef": 1.0}, {"t": 540.0, "pw": 1.184, "vb": 4.17, "tp": 14.6, "ic": 293.6, "ef": 1.0}, {"t": 570.0, "pw": 1.153, "vb": 4.17, "tp": 14.6, "ic": 284.3, "ef": 1.0}, {"t": 600.0, "pw": 1.349, "vb": 4.17, "tp": 14.8, "ic": 335.6, "ef": 1.0}, {"t": 630.0, "pw": 1.11, "vb": 4.17, "tp": 15.0, "ic": 275.0, "ef": 1.0}, {"t": 660.0, "pw": 1.136, "vb": 4.17, "tp": 14.8, "ic": 284.3, "ef": 1.0}, {"t": 690.0, "pw": 1.079, "vb": 4.17, "tp": 13.9, "ic": 275.0, "ef": 1.0}, {"t": 720.0, "pw": 1.002, "vb": 4.17, "tp": 13.6, "ic": 247.0, "ef": 1.0}, {"t": 750.0, "pw": 1.061, "vb": 4.17, "tp": 13.7, "ic": 270.3, "ef": 1.0}, {"t": 780.0, "pw": 1.031, "vb": 4.17, "tp": 13.9, "ic": 256.4, "ef": 1.0}, {"t": 810.0, "pw": 1.013, "vb": 4.17, "tp": 14.6, "ic": 251.7, "ef": 1.0}, {"t": 840.0, "pw": 0.992, "vb": 4.17, "tp": 15.2, "ic": 247.0, "ef": 1.0}, {"t": 870.0, "pw": 0.953, "vb": 4.17, "tp": 16.0, "ic": 256.4, "ef": 1.0}, {"t": 900.0, "pw": 1.114, "vb": 4.17, "tp": 16.4, "ic": 279.7, "ef": 1.0}, {"t": 930.0, "pw": 1.071, "vb": 4.17, "tp": 16.5, "ic": 275.0, "ef": 1.0}, {"t": 960.0, "pw": 1.297, "vb": 4.17, "tp": 16.4, "ic": 326.3, "ef": 1.0}, {"t": 990.0, "pw": 1.048, "vb": 4.17, "tp": 16.4, "ic": 265.7, "ef": 1.0}, {"t": 1020.0, "pw": 1.011, "vb": 4.17, "tp": 16.0, "ic": 270.3, "ef": 1.0}, {"t": 1050.0, "pw": 0.901, "vb": 4.17, "tp": 14.8, "ic": 242.4, "ef": 1.0}, {"t": 1080.0, "pw": 1.305, "vb": 4.17, "tp": 13.7, "ic": 326.3, "ef": 1.0}, {"t": 1110.0, "pw": 1.009, "vb": 4.17, "tp": 13.5, "ic": 261.0, "ef": 1.0}, {"t": 1140.0, "pw": 1.001, "vb": 4.17, "tp": 13.7, "ic": 256.4, "ef": 1.0}, {"t": 1170.0, "pw": 0.951, "vb": 4.17, "tp": 14.3, "ic": 247.0, "ef": 1.0}, {"t": 1200.0, "pw": 0.888, "vb": 4.17, "tp": 14.9, "ic": 228.4, "ef": 1.0}, {"t": 1230.0, "pw": 1.044, "vb": 4.17, "tp": 15.8, "ic": 275.0, "ef": 1.0}, {"t": 1260.0, "pw": 0.753, "vb": 4.15, "tp": 16.0, "ic": 233.0, "ef": 1.0}, {"t": 1290.0, "pw": 0.878, "vb": 4.17, "tp": 16.3, "ic": 293.6, "ef": 1.0}, {"t": 1320.0, "pw": 0.99, "vb": 4.17, "tp": 16.3, "ic": 330.9, "ef": 1.0}, {"t": 1350.0, "pw": 0.907, "vb": 4.17, "tp": 16.5, "ic": 270.3, "ef": 1.0}, {"t": 1380.0, "pw": 0.859, "vb": 4.17, "tp": 16.5, "ic": 270.3, "ef": 1.0}, {"t": 1410.0, "pw": 0.59, "vb": 4.17, "tp": 15.6, "ic": 195.8, "ef": 1.0}, {"t": 1440.0, "pw": 0.695, "vb": 4.17, "tp": 13.8, "ic": 233.0, "ef": 1.0}, {"t": 1470.0, "pw": 0.928, "vb": 4.17, "tp": 12.9, "ic": 298.3, "ef": 1.0}, {"t": 1500.0, "pw": 0.801, "vb": 4.17, "tp": 12.7, "ic": 279.7, "ef": 1.0}, {"t": 1530.0, "pw": 0.759, "vb": 4.17, "tp": 13.0, "ic": 289.0, "ef": 1.0}, {"t": 1560.0, "pw": 0.72, "vb": 4.17, "tp": 13.4, "ic": 289.0, "ef": 1.0}, {"t": 1590.0, "pw": 0.393, "vb": 4.15, "tp": 13.6, "ic": 167.8, "ef": 1.0}, {"t": 1620.0, "pw": 0.783, "vb": 4.17, "tp": 14.1, "ic": 298.3, "ef": 1.0}, {"t": 1650.0, "pw": 0.881, "vb": 4.17, "tp": 14.3, "ic": 335.6, "ef": 1.0}, {"t": 1680.0, "pw": 0.706, "vb": 4.17, "tp": 14.5, "ic": 270.3, "ef": 1.0}, {"t": 1710.0, "pw": 0.711, "vb": 4.17, "tp": 15.1, "ic": 275.0, "ef": 1.0}, {"t": 1740.0, "pw": 0.14, "vb": 4.17, "tp": 14.5, "ic": 69.9, "ef": 1.0}, {"t": 1770.0, "pw": 0.054, "vb": 4.12, "tp": 12.4, "ic": 51.3, "ef": 1.0}, {"t": 1800.0, "pw": 0.054, "vb": 4.12, "tp": 10.3, "ic": 51.3, "ef": 1.0}, {"t": 1830.0, "pw": 0.049, "vb": 4.1, "tp": 8.4, "ic": 46.6, "ef": 1.0}, {"t": 1860.0, "pw": 0.053, "vb": 4.1, "tp": 6.7, "ic": 51.3, "ef": 1.0}, {"t": 1890.0, "pw": 0.053, "vb": 4.07, "tp": 5.2, "ic": 51.3, "ef": 1.0}, {"t": 1920.0, "pw": 0.048, "vb": 4.07, "tp": 3.9, "ic": 46.6, "ef": 1.0}, {"t": 1950.0, "pw": 0.053, "vb": 4.07, "tp": 2.5, "ic": 51.3, "ef": 1.0}, {"t": 1980.0, "pw": 0.048, "vb": 4.07, "tp": 1.3, "ic": 46.6, "ef": 1.0}, {"t": 2010.0, "pw": 0.053, "vb": 4.07, "tp": 0.3, "ic": 51.3, "ef": 1.0}, {"t": 2040.0, "pw": 0.053, "vb": 4.04, "tp": -0.6, "ic": 51.3, "ef": 1.0}, {"t": 2070.0, "pw": 0.053, "vb": 4.04, "tp": -1.4, "ic": 51.3, "ef": 1.0}, {"t": 2100.0, "pw": 0.053, "vb": 4.04, "tp": -2.2, "ic": 51.3, "ef": 1.0}, {"t": 2130.0, "pw": 0.063, "vb": 4.02, "tp": -3.0, "ic": 60.6, "ef": 1.0}, {"t": 2160.0, "pw": 0.053, "vb": 4.02, "tp": -4.0, "ic": 51.3, "ef": 1.0}, {"t": 2190.0, "pw": 0.053, "vb": 4.02, "tp": -4.6, "ic": 51.3, "ef": 1.0}, {"t": 2220.0, "pw": 0.053, "vb": 4.02, "tp": -5.4, "ic": 51.3, "ef": 1.0}, {"t": 2250.0, "pw": 0.053, "vb": 4.02, "tp": -6.1, "ic": 51.3, "ef": 1.0}, {"t": 2280.0, "pw": 0.048, "vb": 4.02, "tp": -6.7, "ic": 46.6, "ef": 1.0}, {"t": 2310.0, "pw": 0.053, "vb": 3.99, "tp": -7.5, "ic": 51.3, "ef": 1.0}, {"t": 2340.0, "pw": 0.053, "vb": 3.99, "tp": -8.1, "ic": 51.3, "ef": 1.0}, {"t": 2370.0, "pw": 0.058, "vb": 3.99, "tp": -8.7, "ic": 55.9, "ef": 1.0}, {"t": 2400.0, "pw": 0.058, "vb": 3.99, "tp": -9.1, "ic": 55.9, "ef": 1.0}, {"t": 2430.0, "pw": 0.053, "vb": 3.99, "tp": -9.6, "ic": 51.3, "ef": 1.0}, {"t": 2460.0, "pw": 0.053, "vb": 3.99, "tp": -10.1, "ic": 51.3, "ef": 1.0}, {"t": 2490.0, "pw": 0.053, "vb": 3.97, "tp": -10.8, "ic": 51.3, "ef": 1.0}, {"t": 2520.0, "pw": 0.053, "vb": 3.97, "tp": -11.3, "ic": 51.3, "ef": 1.0}, {"t": 2550.0, "pw": 0.053, "vb": 3.97, "tp": -11.9, "ic": 51.3, "ef": 1.0}, {"t": 2580.0, "pw": 0.057, "vb": 3.97, "tp": -12.3, "ic": 55.9, "ef": 1.0}, {"t": 2610.0, "pw": 0.057, "vb": 3.97, "tp": -12.8, "ic": 55.9, "ef": 1.0}, {"t": 2640.0, "pw": 0.057, "vb": 3.97, "tp": -13.4, "ic": 55.9, "ef": 1.0}, {"t": 2670.0, "pw": 0.057, "vb": 3.97, "tp": -14.0, "ic": 55.9, "ef": 1.0}, {"t": 2700.0, "pw": 0.053, "vb": 3.97, "tp": -14.5, "ic": 51.3, "ef": 1.0}, {"t": 2730.0, "pw": 0.053, "vb": 3.97, "tp": -14.8, "ic": 51.3, "ef": 1.0}, {"t": 2760.0, "pw": 0.057, "vb": 3.94, "tp": -15.1, "ic": 55.9, "ef": 1.0}, {"t": 2790.0, "pw": 0.053, "vb": 3.94, "tp": -15.3, "ic": 51.3, "ef": 1.0}, {"t": 2820.0, "pw": 0.053, "vb": 3.94, "tp": -15.7, "ic": 51.3, "ef": 1.0}, {"t": 2850.0, "pw": 0.053, "vb": 3.94, "tp": -16.0, "ic": 51.3, "ef": 1.0}, {"t": 2880.0, "pw": 0.053, "vb": 3.94, "tp": -16.4, "ic": 51.3, "ef": 1.0}, {"t": 2910.0, "pw": 0.057, "vb": 3.94, "tp": -17.0, "ic": 55.9, "ef": 1.0}, {"t": 2940.0, "pw": 0.053, "vb": 3.94, "tp": -17.4, "ic": 51.3, "ef": 1.0}, {"t": 2970.0, "pw": 0.053, "vb": 3.94, "tp": -17.7, "ic": 51.3, "ef": 1.0}, {"t": 3000.0, "pw": 0.057, "vb": 3.94, "tp": -18.1, "ic": 55.9, "ef": 1.0}, {"t": 3030.0, "pw": 0.057, "vb": 3.94, "tp": -18.4, "ic": 55.9, "ef": 1.0}, {"t": 3060.0, "pw": 0.057, "vb": 3.94, "tp": -18.8, "ic": 55.9, "ef": 1.0}, {"t": 3090.0, "pw": 0.057, "vb": 3.92, "tp": -19.2, "ic": 55.9, "ef": 1.0}, {"t": 3120.0, "pw": 0.057, "vb": 3.92, "tp": -19.5, "ic": 55.9, "ef": 1.0}, {"t": 3150.0, "pw": 0.057, "vb": 3.92, "tp": -19.7, "ic": 55.9, "ef": 1.0}, {"t": 3180.0, "pw": 0.053, "vb": 3.92, "tp": -19.9, "ic": 51.3, "ef": 1.0}, {"t": 3210.0, "pw": 0.053, "vb": 3.92, "tp": -20.1, "ic": 51.3, "ef": 1.0}, {"t": 3240.0, "pw": 0.057, "vb": 3.92, "tp": -20.5, "ic": 55.9, "ef": 1.0}, {"t": 3270.0, "pw": 0.053, "vb": 3.92, "tp": -20.9, "ic": 51.3, "ef": 1.0}, {"t": 3300.0, "pw": 0.053, "vb": 3.92, "tp": -21.1, "ic": 51.3, "ef": 1.0}, {"t": 3330.0, "pw": 0.057, "vb": 3.92, "tp": -21.2, "ic": 55.9, "ef": 1.0}, {"t": 3360.0, "pw": 0.053, "vb": 3.92, "tp": -21.2, "ic": 51.3, "ef": 1.0}, {"t": 3390.0, "pw": 0.057, "vb": 3.92, "tp": -21.2, "ic": 55.9, "ef": 1.0}, {"t": 3420.0, "pw": 0.062, "vb": 3.92, "tp": -21.5, "ic": 60.6, "ef": 1.0}, {"t": 3450.0, "pw": 0.053, "vb": 3.89, "tp": -21.6, "ic": 51.3, "ef": 1.0}, {"t": 3480.0, "pw": 0.057, "vb": 3.89, "tp": -21.9, "ic": 55.9, "ef": 1.0}, {"t": 3510.0, "pw": 0.053, "vb": 3.89, "tp": -22.2, "ic": 51.3, "ef": 1.0}, {"t": 3540.0, "pw": 0.057, "vb": 3.89, "tp": -22.5, "ic": 55.9, "ef": 1.0}, {"t": 3570.0, "pw": 0.057, "vb": 3.89, "tp": -22.6, "ic": 55.9, "ef": 1.0}, {"t": 3600.0, "pw": 0.057, "vb": 3.89, "tp": -22.7, "ic": 55.9, "ef": 1.0}, {"t": 3630.0, "pw": 0.058, "vb": 3.89, "tp": -23.0, "ic": 55.9, "ef": 1.0}, {"t": 3660.0, "pw": 0.058, "vb": 3.89, "tp": -23.3, "ic": 55.9, "ef": 1.0}, {"t": 3690.0, "pw": 0.059, "vb": 3.89, "tp": -23.6, "ic": 55.9, "ef": 1.0}, {"t": 3720.0, "pw": 0.062, "vb": 3.89, "tp": -23.7, "ic": 55.9, "ef": 1.0}, {"t": 3750.0, "pw": 0.3, "vb": 3.89, "tp": -23.6, "ic": 125.8, "ef": 1.0}, {"t": 3780.0, "pw": 0.938, "vb": 3.94, "tp": -21.8, "ic": 386.9, "ef": 1.0}, {"t": 3810.0, "pw": 0.328, "vb": 3.89, "tp": -20.0, "ic": 135.2, "ef": 1.0}, {"t": 3840.0, "pw": 1.205, "vb": 3.97, "tp": -18.1, "ic": 466.1, "ef": 1.0}, {"t": 3870.0, "pw": 1.391, "vb": 3.99, "tp": -17.2, "ic": 568.7, "ef": 1.0}, {"t": 3900.0, "pw": 1.357, "vb": 3.99, "tp": -16.7, "ic": 559.3, "ef": 1.0}, {"t": 3930.0, "pw": 1.216, "vb": 4.02, "tp": -16.3, "ic": 503.4, "ef": 1.0}, {"t": 3960.0, "pw": 0.911, "vb": 3.99, "tp": -15.9, "ic": 330.9, "ef": 1.0}, {"t": 3990.0, "pw": 1.344, "vb": 4.02, "tp": -15.3, "ic": 536.0, "ef": 1.0}, {"t": 4020.0, "pw": 1.67, "vb": 4.07, "tp": -14.0, "ic": 689.8, "ef": 1.0}, {"t": 4050.0, "pw": 1.201, "vb": 4.02, "tp": -12.5, "ic": 386.9, "ef": 1.0}, {"t": 4080.0, "pw": 1.417, "vb": 4.02, "tp": -11.1, "ic": 391.5, "ef": 1.0}, {"t": 4110.0, "pw": 1.641, "vb": 4.04, "tp": -9.8, "ic": 526.7, "ef": 1.0}, {"t": 4140.0, "pw": 1.891, "vb": 4.07, "tp": -9.2, "ic": 610.6, "ef": 1.0}, {"t": 4170.0, "pw": 1.277, "vb": 4.04, "tp": -8.3, "ic": 410.2, "ef": 1.0}, {"t": 4200.0, "pw": 1.987, "vb": 4.1, "tp": -7.2, "ic": 638.6, "ef": 1.0}, {"t": 4230.0, "pw": 1.886, "vb": 4.1, "tp": -6.4, "ic": 615.3, "ef": 1.0}, {"t": 4260.0, "pw": 1.938, "vb": 4.1, "tp": -6.6, "ic": 517.4, "ef": 1.0}, {"t": 4290.0, "pw": 2.011, "vb": 4.1, "tp": -6.6, "ic": 536.0, "ef": 1.0}, {"t": 4320.0, "pw": 1.92, "vb": 4.1, "tp": -6.5, "ic": 512.7, "ef": 1.0}, {"t": 4350.0, "pw": 1.76, "vb": 4.1, "tp": -6.4, "ic": 480.1, "ef": 1.0}, {"t": 4380.0, "pw": 2.769, "vb": 4.15, "tp": -5.5, "ic": 736.4, "ef": 1.0}, {"t": 4410.0, "pw": 2.243, "vb": 4.15, "tp": -4.4, "ic": 596.6, "ef": 1.0}, {"t": 4440.0, "pw": 1.608, "vb": 4.12, "tp": -3.3, "ic": 428.8, "ef": 1.0}, {"t": 4470.0, "pw": 1.691, "vb": 4.1, "tp": -2.3, "ic": 452.1, "ef": 1.0}, {"t": 4500.0, "pw": 1.638, "vb": 4.12, "tp": -1.7, "ic": 438.1, "ef": 1.0}, {"t": 4530.0, "pw": 2.538, "vb": 4.15, "tp": -0.9, "ic": 675.9, "ef": 1.0}, {"t": 4560.0, "pw": 2.546, "vb": 4.17, "tp": -0.2, "ic": 643.2, "ef": 1.0}, {"t": 4590.0, "pw": 2.084, "vb": 4.17, "tp": -0.4, "ic": 554.7, "ef": 1.0}, {"t": 4620.0, "pw": 2.262, "vb": 4.17, "tp": -0.4, "ic": 554.7, "ef": 1.0}, {"t": 4650.0, "pw": 2.095, "vb": 4.17, "tp": -0.5, "ic": 498.7, "ef": 1.0}, {"t": 4680.0, "pw": 2.012, "vb": 4.17, "tp": 0.1, "ic": 484.8, "ef": 1.0}, {"t": 4710.0, "pw": 1.575, "vb": 4.17, "tp": 0.3, "ic": 424.2, "ef": 1.0}, {"t": 4740.0, "pw": 1.867, "vb": 4.17, "tp": 0.7, "ic": 447.5, "ef": 1.0}, {"t": 4770.0, "pw": 1.805, "vb": 4.17, "tp": 1.7, "ic": 438.1, "ef": 1.0}, {"t": 4800.0, "pw": 1.682, "vb": 4.17, "tp": 2.6, "ic": 452.1, "ef": 1.0}, {"t": 4830.0, "pw": 1.024, "vb": 4.15, "tp": 3.0, "ic": 275.0, "ef": 1.0}, {"t": 4860.0, "pw": 1.787, "vb": 4.17, "tp": 3.8, "ic": 438.1, "ef": 1.0}, {"t": 4890.0, "pw": 1.716, "vb": 4.17, "tp": 4.2, "ic": 410.2, "ef": 1.0}, {"t": 4920.0, "pw": 1.603, "vb": 4.17, "tp": 4.3, "ic": 386.9, "ef": 1.0}, {"t": 4950.0, "pw": 1.805, "vb": 4.17, "tp": 4.3, "ic": 433.5, "ef": 1.0}, {"t": 4980.0, "pw": 1.538, "vb": 4.17, "tp": 4.6, "ic": 363.6, "ef": 1.0}, {"t": 5010.0, "pw": 1.532, "vb": 4.17, "tp": 5.2, "ic": 368.2, "ef": 1.0}, {"t": 5040.0, "pw": 1.45, "vb": 4.17, "tp": 5.1, "ic": 386.9, "ef": 1.0}, {"t": 5070.0, "pw": 1.701, "vb": 4.17, "tp": 4.8, "ic": 410.2, "ef": 1.0}, {"t": 5100.0, "pw": 1.447, "vb": 4.17, "tp": 5.8, "ic": 344.9, "ef": 1.0}, {"t": 5130.0, "pw": 1.325, "vb": 4.17, "tp": 6.8, "ic": 354.2, "ef": 1.0}, {"t": 5160.0, "pw": 1.219, "vb": 4.17, "tp": 7.0, "ic": 326.3, "ef": 1.0}, {"t": 5190.0, "pw": 1.483, "vb": 4.17, "tp": 7.6, "ic": 354.2, "ef": 1.0}, {"t": 5220.0, "pw": 1.465, "vb": 4.17, "tp": 7.9, "ic": 354.2, "ef": 1.0}, {"t": 5250.0, "pw": 1.386, "vb": 4.17, "tp": 7.7, "ic": 335.6, "ef": 1.0}, {"t": 5280.0, "pw": 1.335, "vb": 4.17, "tp": 7.7, "ic": 326.3, "ef": 1.0}, {"t": 5310.0, "pw": 1.271, "vb": 4.17, "tp": 8.4, "ic": 303.0, "ef": 1.0}, {"t": 5340.0, "pw": 1.369, "vb": 4.17, "tp": 8.8, "ic": 330.9, "ef": 1.0}, {"t": 5370.0, "pw": 1.247, "vb": 4.17, "tp": 8.6, "ic": 316.9, "ef": 1.0}], "tsuru": [{"t": 0.0, "pw": 0.036, "vb": 4.1, "tp": 2.9, "ic": 28.0, "ef": 1.0}, {"t": 68.0, "pw": 0.036, "vb": 4.1, "tp": 0.7, "ic": 28.0, "ef": 1.0}, {"t": 136.0, "pw": 0.036, "vb": 4.07, "tp": -1.3, "ic": 28.0, "ef": 1.0}, {"t": 203.0, "pw": 0.036, "vb": 4.1, "tp": -2.8, "ic": 28.0, "ef": 1.0}, {"t": 271.0, "pw": 0.03, "vb": 4.07, "tp": -4.4, "ic": 23.3, "ef": 1.0}, {"t": 339.0, "pw": 0.03, "vb": 4.07, "tp": -5.5, "ic": 23.3, "ef": 1.0}, {"t": 407.0, "pw": 0.03, "vb": 4.04, "tp": -6.8, "ic": 23.3, "ef": 1.0}, {"t": 475.0, "pw": 0.03, "vb": 4.04, "tp": -7.9, "ic": 23.3, "ef": 1.0}, {"t": 542.0, "pw": 0.036, "vb": 4.04, "tp": -9.1, "ic": 28.0, "ef": 1.0}, {"t": 610.0, "pw": 0.03, "vb": 4.04, "tp": -10.2, "ic": 23.3, "ef": 1.0}, {"t": 678.0, "pw": 0.036, "vb": 4.04, "tp": -11.6, "ic": 28.0, "ef": 1.0}, {"t": 746.0, "pw": 0.036, "vb": 4.04, "tp": -12.5, "ic": 28.0, "ef": 1.0}, {"t": 814.0, "pw": 0.03, "vb": 4.04, "tp": -13.4, "ic": 23.3, "ef": 1.0}, {"t": 881.0, "pw": 0.036, "vb": 4.02, "tp": -14.3, "ic": 28.0, "ef": 1.0}, {"t": 949.0, "pw": 0.036, "vb": 4.02, "tp": -14.8, "ic": 28.0, "ef": 1.0}, {"t": 1017.0, "pw": 0.036, "vb": 4.02, "tp": -15.7, "ic": 28.0, "ef": 1.0}, {"t": 1085.0, "pw": 0.036, "vb": 4.02, "tp": -16.1, "ic": 28.0, "ef": 1.0}, {"t": 1153.0, "pw": 0.036, "vb": 4.02, "tp": -16.9, "ic": 28.0, "ef": 1.0}, {"t": 1220.0, "pw": 0.036, "vb": 4.02, "tp": -17.5, "ic": 28.0, "ef": 1.0}, {"t": 1288.0, "pw": 0.036, "vb": 4.02, "tp": -18.1, "ic": 28.0, "ef": 1.0}, {"t": 1356.0, "pw": 0.036, "vb": 3.99, "tp": -19.0, "ic": 28.0, "ef": 1.0}, {"t": 1424.0, "pw": 0.036, "vb": 3.97, "tp": -19.3, "ic": 28.0, "ef": 1.0}, {"t": 1492.0, "pw": 0.03, "vb": 3.97, "tp": -20.2, "ic": 23.3, "ef": 1.0}, {"t": 1559.0, "pw": 0.036, "vb": 3.97, "tp": -20.5, "ic": 28.0, "ef": 1.0}, {"t": 1627.0, "pw": 0.036, "vb": 3.97, "tp": -21.2, "ic": 28.0, "ef": 1.0}, {"t": 1695.0, "pw": 0.036, "vb": 3.94, "tp": -21.8, "ic": 28.0, "ef": 1.0}, {"t": 1763.0, "pw": 0.036, "vb": 3.94, "tp": -22.2, "ic": 28.0, "ef": 1.0}, {"t": 1831.0, "pw": 0.036, "vb": 3.94, "tp": -22.9, "ic": 28.0, "ef": 1.0}, {"t": 1898.0, "pw": 0.036, "vb": 3.94, "tp": -23.3, "ic": 28.0, "ef": 1.0}, {"t": 1966.0, "pw": 2.387, "vb": 4.04, "tp": -22.7, "ic": 717.8, "ef": 1.0}, {"t": 2034.0, "pw": 2.546, "vb": 4.07, "tp": -19.3, "ic": 694.5, "ef": 1.0}, {"t": 2102.0, "pw": 2.254, "vb": 4.1, "tp": -16.5, "ic": 675.9, "ef": 1.0}, {"t": 2170.0, "pw": 2.218, "vb": 4.1, "tp": -16.5, "ic": 647.9, "ef": 1.0}, {"t": 2237.0, "pw": 3.655, "vb": 4.15, "tp": -14.2, "ic": 862.3, "ef": 1.0}, {"t": 2305.0, "pw": 1.71, "vb": 4.07, "tp": -13.7, "ic": 372.9, "ef": 1.0}, {"t": 2373.0, "pw": 3.186, "vb": 4.12, "tp": -11.8, "ic": 685.2, "ef": 1.0}, {"t": 2441.0, "pw": 1.749, "vb": 4.1, "tp": -10.2, "ic": 377.5, "ef": 1.0}, {"t": 2509.0, "pw": 3.904, "vb": 4.17, "tp": -8.9, "ic": 787.7, "ef": 1.0}, {"t": 2576.0, "pw": 2.723, "vb": 4.15, "tp": -6.9, "ic": 587.3, "ef": 1.0}, {"t": 2644.0, "pw": 3.573, "vb": 4.17, "tp": -6.6, "ic": 727.1, "ef": 1.0}, {"t": 2712.0, "pw": 3.197, "vb": 4.2, "tp": -4.0, "ic": 619.9, "ef": 1.0}, {"t": 2780.0, "pw": 2.901, "vb": 4.17, "tp": -3.6, "ic": 624.6, "ef": 1.0}, {"t": 2848.0, "pw": 2.997, "vb": 4.2, "tp": -1.8, "ic": 564.0, "ef": 1.0}, {"t": 2915.0, "pw": 2.751, "vb": 4.2, "tp": -0.2, "ic": 582.6, "ef": 1.0}, {"t": 2983.0, "pw": 2.806, "vb": 4.2, "tp": 0.5, "ic": 536.0, "ef": 1.0}, {"t": 3051.0, "pw": 2.657, "vb": 4.2, "tp": 2.6, "ic": 522.0, "ef": 1.0}, {"t": 3119.0, "pw": 2.625, "vb": 4.2, "tp": 4.4, "ic": 517.4, "ef": 1.0}, {"t": 3187.0, "pw": 2.336, "vb": 4.17, "tp": 4.9, "ic": 503.4, "ef": 1.0}, {"t": 3254.0, "pw": 2.026, "vb": 4.2, "tp": 6.1, "ic": 396.2, "ef": 1.0}, {"t": 3322.0, "pw": 1.899, "vb": 4.2, "tp": 6.7, "ic": 410.2, "ef": 1.0}, {"t": 3390.0, "pw": 1.974, "vb": 4.2, "tp": 7.6, "ic": 386.9, "ef": 1.0}, {"t": 3458.0, "pw": 1.529, "vb": 4.17, "tp": 7.4, "ic": 330.9, "ef": 1.0}, {"t": 3526.0, "pw": 1.879, "vb": 4.2, "tp": 8.2, "ic": 363.6, "ef": 1.0}, {"t": 3593.0, "pw": 2.114, "vb": 4.2, "tp": 8.0, "ic": 442.8, "ef": 1.0}, {"t": 3661.0, "pw": 1.77, "vb": 4.2, "tp": 9.4, "ic": 344.9, "ef": 1.0}, {"t": 3729.0, "pw": 1.798, "vb": 4.2, "tp": 9.8, "ic": 372.9, "ef": 1.0}, {"t": 3797.0, "pw": 2.074, "vb": 4.2, "tp": 9.9, "ic": 405.5, "ef": 1.0}, {"t": 3865.0, "pw": 1.628, "vb": 4.2, "tp": 10.7, "ic": 316.9, "ef": 1.0}, {"t": 3932.0, "pw": 1.703, "vb": 4.2, "tp": 9.2, "ic": 326.3, "ef": 1.0}, {"t": 4000.0, "pw": 1.537, "vb": 4.2, "tp": 10.6, "ic": 298.3, "ef": 1.0}, {"t": 4068.0, "pw": 1.723, "vb": 4.2, "tp": 9.6, "ic": 335.6, "ef": 1.0}, {"t": 4136.0, "pw": 1.572, "vb": 4.2, "tp": 11.0, "ic": 303.0, "ef": 1.0}, {"t": 4204.0, "pw": 1.645, "vb": 4.2, "tp": 10.4, "ic": 316.9, "ef": 1.0}, {"t": 4271.0, "pw": 1.506, "vb": 4.2, "tp": 11.9, "ic": 293.6, "ef": 1.0}, {"t": 4339.0, "pw": 1.5, "vb": 4.2, "tp": 11.5, "ic": 289.0, "ef": 1.0}, {"t": 4407.0, "pw": 1.54, "vb": 4.2, "tp": 12.2, "ic": 293.7, "ef": 1.0}, {"t": 4475.0, "pw": 1.505, "vb": 4.2, "tp": 12.5, "ic": 303.0, "ef": 1.0}, {"t": 4543.0, "pw": 1.462, "vb": 4.2, "tp": 12.2, "ic": 279.7, "ef": 1.0}, {"t": 4610.0, "pw": 1.513, "vb": 4.2, "tp": 13.6, "ic": 303.0, "ef": 1.0}, {"t": 4678.0, "pw": 1.513, "vb": 4.2, "tp": 12.0, "ic": 298.3, "ef": 1.0}, {"t": 4746.0, "pw": 1.421, "vb": 4.2, "tp": 13.7, "ic": 284.3, "ef": 1.0}, {"t": 4814.0, "pw": 1.5, "vb": 4.2, "tp": 11.9, "ic": 307.6, "ef": 1.0}, {"t": 4882.0, "pw": 1.229, "vb": 4.2, "tp": 13.2, "ic": 279.7, "ef": 1.0}, {"t": 4949.0, "pw": 1.263, "vb": 4.2, "tp": 11.8, "ic": 312.3, "ef": 1.0}, {"t": 5017.0, "pw": 1.249, "vb": 4.2, "tp": 12.5, "ic": 293.7, "ef": 1.0}, {"t": 5085.0, "pw": 0.862, "vb": 4.2, "tp": 11.8, "ic": 279.7, "ef": 1.0}, {"t": 5153.0, "pw": 1.079, "vb": 4.2, "tp": 12.2, "ic": 298.3, "ef": 1.0}, {"t": 5221.0, "pw": 0.871, "vb": 4.2, "tp": 12.2, "ic": 312.3, "ef": 1.0}, {"t": 5288.0, "pw": 0.031, "vb": 4.12, "tp": 9.1, "ic": 23.3, "ef": 1.0}, {"t": 5356.0, "pw": 0.036, "vb": 4.12, "tp": 6.0, "ic": 28.0, "ef": 1.0}, {"t": 5424.0, "pw": 0.03, "vb": 4.1, "tp": 3.4, "ic": 23.3, "ef": 1.0}, {"t": 5492.0, "pw": 0.036, "vb": 4.1, "tp": 1.2, "ic": 28.0, "ef": 1.0}, {"t": 5560.0, "pw": 0.03, "vb": 4.1, "tp": -0.8, "ic": 23.3, "ef": 1.0}, {"t": 5627.0, "pw": 0.036, "vb": 4.07, "tp": -2.5, "ic": 28.0, "ef": 1.0}, {"t": 5695.0, "pw": 0.03, "vb": 4.07, "tp": -4.0, "ic": 23.3, "ef": 1.0}, {"t": 5763.0, "pw": 0.03, "vb": 4.07, "tp": -5.2, "ic": 23.3, "ef": 1.0}, {"t": 5831.0, "pw": 0.036, "vb": 4.07, "tp": -6.7, "ic": 28.0, "ef": 1.0}, {"t": 5899.0, "pw": 0.03, "vb": 4.07, "tp": -7.7, "ic": 23.3, "ef": 1.0}, {"t": 5966.0, "pw": 0.036, "vb": 4.04, "tp": -9.0, "ic": 28.0, "ef": 1.0}, {"t": 6034.0, "pw": 0.036, "vb": 4.04, "tp": -9.9, "ic": 28.0, "ef": 1.0}, {"t": 6102.0, "pw": 0.036, "vb": 4.04, "tp": -10.8, "ic": 28.0, "ef": 1.0}, {"t": 6170.0, "pw": 0.036, "vb": 4.04, "tp": -11.8, "ic": 28.0, "ef": 1.0}, {"t": 6238.0, "pw": 0.036, "vb": 4.04, "tp": -12.6, "ic": 28.0, "ef": 1.0}, {"t": 6305.0, "pw": 0.036, "vb": 4.02, "tp": -13.8, "ic": 28.0, "ef": 1.0}, {"t": 6373.0, "pw": 0.036, "vb": 4.02, "tp": -14.4, "ic": 28.0, "ef": 1.0}, {"t": 6441.0, "pw": 0.036, "vb": 4.02, "tp": -15.4, "ic": 28.0, "ef": 1.0}, {"t": 6509.0, "pw": 0.036, "vb": 4.02, "tp": -16.1, "ic": 28.0, "ef": 1.0}, {"t": 6577.0, "pw": 0.036, "vb": 4.02, "tp": -16.9, "ic": 28.0, "ef": 1.0}, {"t": 6644.0, "pw": 0.036, "vb": 4.02, "tp": -17.6, "ic": 28.0, "ef": 1.0}, {"t": 6712.0, "pw": 0.036, "vb": 4.02, "tp": -18.2, "ic": 28.0, "ef": 1.0}, {"t": 6780.0, "pw": 0.036, "vb": 3.99, "tp": -19.0, "ic": 28.0, "ef": 1.0}, {"t": 6848.0, "pw": 0.036, "vb": 3.97, "tp": -19.4, "ic": 28.0, "ef": 1.0}, {"t": 6916.0, "pw": 0.036, "vb": 3.97, "tp": -20.2, "ic": 28.0, "ef": 1.0}, {"t": 6983.0, "pw": 0.036, "vb": 3.97, "tp": -20.6, "ic": 28.0, "ef": 1.0}, {"t": 7051.0, "pw": 0.036, "vb": 3.97, "tp": -21.3, "ic": 28.0, "ef": 1.0}, {"t": 7119.0, "pw": 0.036, "vb": 3.94, "tp": -21.8, "ic": 28.0, "ef": 1.0}, {"t": 7187.0, "pw": 0.036, "vb": 3.94, "tp": -22.2, "ic": 28.0, "ef": 1.0}, {"t": 7255.0, "pw": 0.036, "vb": 3.94, "tp": -22.9, "ic": 28.0, "ef": 1.0}, {"t": 7322.0, "pw": 0.036, "vb": 3.94, "tp": -23.2, "ic": 28.0, "ef": 1.0}, {"t": 7390.0, "pw": 0.535, "vb": 3.97, "tp": -23.9, "ic": 163.1, "ef": 1.0}, {"t": 7458.0, "pw": 0.677, "vb": 3.99, "tp": -20.4, "ic": 237.7, "ef": 1.0}, {"t": 7526.0, "pw": 2.592, "vb": 4.1, "tp": -19.5, "ic": 745.8, "ef": 1.0}, {"t": 7594.0, "pw": 1.538, "vb": 4.07, "tp": -16.3, "ic": 531.4, "ef": 1.0}, {"t": 7661.0, "pw": 2.729, "vb": 4.1, "tp": -16.4, "ic": 694.5, "ef": 1.0}, {"t": 7729.0, "pw": 3.065, "vb": 4.12, "tp": -13.6, "ic": 764.4, "ef": 1.0}, {"t": 7797.0, "pw": 2.302, "vb": 4.1, "tp": -13.7, "ic": 545.3, "ef": 1.0}, {"t": 7865.0, "pw": 3.753, "vb": 4.15, "tp": -11.5, "ic": 806.4, "ef": 1.0}, {"t": 7933.0, "pw": 1.486, "vb": 4.07, "tp": -10.5, "ic": 321.6, "ef": 1.0}, {"t": 8000.0, "pw": 3.135, "vb": 4.17, "tp": -8.9, "ic": 764.4, "ef": 1.0}, {"t": 8068.0, "pw": 2.797, "vb": 4.15, "tp": -7.0, "ic": 601.3, "ef": 1.0}, {"t": 8136.0, "pw": 4.036, "vb": 4.17, "tp": -6.2, "ic": 787.7, "ef": 1.0}, {"t": 8204.0, "pw": 3.3, "vb": 4.2, "tp": -3.8, "ic": 633.9, "ef": 1.0}, {"t": 8272.0, "pw": 2.968, "vb": 4.17, "tp": -3.2, "ic": 638.6, "ef": 1.0}, {"t": 8339.0, "pw": 2.963, "vb": 4.2, "tp": -1.2, "ic": 559.3, "ef": 1.0}, {"t": 8407.0, "pw": 2.312, "vb": 4.17, "tp": -0.3, "ic": 498.7, "ef": 1.0}, {"t": 8475.0, "pw": 2.744, "vb": 4.2, "tp": 0.9, "ic": 517.4, "ef": 1.0}, {"t": 8543.0, "pw": 2.662, "vb": 4.2, "tp": 2.7, "ic": 540.7, "ef": 1.0}, {"t": 8611.0, "pw": 2.8, "vb": 4.2, "tp": 3.0, "ic": 554.7, "ef": 1.0}, {"t": 8678.0, "pw": 2.611, "vb": 4.2, "tp": 4.8, "ic": 526.7, "ef": 1.0}, {"t": 8746.0, "pw": 2.159, "vb": 4.2, "tp": 5.4, "ic": 424.2, "ef": 1.0}, {"t": 8814.0, "pw": 2.376, "vb": 4.2, "tp": 6.9, "ic": 475.4, "ef": 1.0}, {"t": 8882.0, "pw": 1.983, "vb": 4.2, "tp": 7.6, "ic": 386.9, "ef": 1.0}, {"t": 8950.0, "pw": 1.907, "vb": 4.17, "tp": 9.1, "ic": 368.2, "ef": 1.0}, {"t": 9017.0, "pw": 1.831, "vb": 4.2, "tp": 9.7, "ic": 358.9, "ef": 1.0}, {"t": 9085.0, "pw": 1.801, "vb": 4.2, "tp": 10.3, "ic": 354.2, "ef": 1.0}, {"t": 9153.0, "pw": 1.809, "vb": 4.2, "tp": 10.0, "ic": 358.9, "ef": 1.0}, {"t": 9221.0, "pw": 1.8, "vb": 4.2, "tp": 10.6, "ic": 349.6, "ef": 1.0}, {"t": 9289.0, "pw": 1.843, "vb": 4.2, "tp": 9.7, "ic": 368.2, "ef": 1.0}, {"t": 9356.0, "pw": 1.65, "vb": 4.2, "tp": 10.5, "ic": 321.6, "ef": 1.0}, {"t": 9424.0, "pw": 0.835, "vb": 4.15, "tp": 10.6, "ic": 181.8, "ef": 1.0}, {"t": 9492.0, "pw": 1.728, "vb": 4.2, "tp": 10.4, "ic": 335.6, "ef": 1.0}, {"t": 9560.0, "pw": 1.662, "vb": 4.2, "tp": 11.6, "ic": 330.9, "ef": 1.0}, {"t": 9628.0, "pw": 1.674, "vb": 4.2, "tp": 10.6, "ic": 321.6, "ef": 1.0}, {"t": 9695.0, "pw": 1.469, "vb": 4.2, "tp": 12.1, "ic": 289.0, "ef": 1.0}, {"t": 9763.0, "pw": 1.608, "vb": 4.2, "tp": 11.4, "ic": 307.6, "ef": 1.0}, {"t": 9831.0, "pw": 1.592, "vb": 4.2, "tp": 12.8, "ic": 312.3, "ef": 1.0}, {"t": 9899.0, "pw": 1.926, "vb": 4.2, "tp": 12.0, "ic": 368.2, "ef": 1.0}, {"t": 9967.0, "pw": 1.478, "vb": 4.2, "tp": 14.0, "ic": 289.0, "ef": 1.0}, {"t": 10034.0, "pw": 1.568, "vb": 4.2, "tp": 13.0, "ic": 307.6, "ef": 1.0}, {"t": 10102.0, "pw": 1.739, "vb": 4.2, "tp": 14.8, "ic": 344.9, "ef": 1.0}, {"t": 10170.0, "pw": 1.511, "vb": 4.2, "tp": 13.2, "ic": 312.3, "ef": 1.0}, {"t": 10238.0, "pw": 1.397, "vb": 4.2, "tp": 14.2, "ic": 289.0, "ef": 1.0}, {"t": 10306.0, "pw": 1.28, "vb": 4.17, "tp": 13.4, "ic": 298.3, "ef": 1.0}, {"t": 10373.0, "pw": 1.343, "vb": 4.2, "tp": 13.5, "ic": 303.0, "ef": 1.0}, {"t": 10441.0, "pw": 0.352, "vb": 4.12, "tp": 13.6, "ic": 93.2, "ef": 1.0}, {"t": 10509.0, "pw": 1.467, "vb": 4.2, "tp": 13.1, "ic": 321.6, "ef": 1.0}, {"t": 10577.0, "pw": 1.08, "vb": 4.2, "tp": 13.6, "ic": 312.3, "ef": 1.0}, {"t": 10645.0, "pw": 1.142, "vb": 4.2, "tp": 12.2, "ic": 312.3, "ef": 1.0}, {"t": 10712.0, "pw": 0.857, "vb": 4.2, "tp": 13.2, "ic": 289.0, "ef": 1.0}, {"t": 10780.0, "pw": 0.909, "vb": 4.2, "tp": 11.9, "ic": 298.3, "ef": 1.0}, {"t": 10848.0, "pw": 0.037, "vb": 4.12, "tp": 9.2, "ic": 28.0, "ef": 1.0}, {"t": 10916.0, "pw": 0.03, "vb": 4.12, "tp": 6.1, "ic": 23.3, "ef": 1.0}, {"t": 10984.0, "pw": 0.042, "vb": 4.1, "tp": 3.5, "ic": 32.6, "ef": 1.0}, {"t": 11051.0, "pw": 0.036, "vb": 4.1, "tp": 1.3, "ic": 28.0, "ef": 1.0}, {"t": 11119.0, "pw": 0.03, "vb": 4.07, "tp": -0.6, "ic": 23.3, "ef": 1.0}, {"t": 11187.0, "pw": 0.036, "vb": 4.1, "tp": -2.5, "ic": 28.0, "ef": 1.0}, {"t": 11255.0, "pw": 0.03, "vb": 4.07, "tp": -3.9, "ic": 23.3, "ef": 1.0}, {"t": 11323.0, "pw": 0.03, "vb": 4.07, "tp": -5.4, "ic": 23.3, "ef": 1.0}, {"t": 11390.0, "pw": 0.03, "vb": 4.07, "tp": -6.6, "ic": 23.3, "ef": 1.0}, {"t": 11458.0, "pw": 0.042, "vb": 4.04, "tp": -7.8, "ic": 32.6, "ef": 1.0}, {"t": 11526.0, "pw": 0.036, "vb": 4.04, "tp": -9.3, "ic": 28.0, "ef": 1.0}, {"t": 11594.0, "pw": 0.036, "vb": 4.04, "tp": -10.3, "ic": 28.0, "ef": 1.0}, {"t": 11662.0, "pw": 0.036, "vb": 4.04, "tp": -11.7, "ic": 28.0, "ef": 1.0}, {"t": 11729.0, "pw": 0.036, "vb": 4.04, "tp": -13.5, "ic": 28.0, "ef": 1.0}, {"t": 11797.0, "pw": 0.036, "vb": 4.02, "tp": -14.2, "ic": 28.0, "ef": 1.0}, {"t": 11865.0, "pw": 0.036, "vb": 4.02, "tp": -14.9, "ic": 28.0, "ef": 1.0}, {"t": 11933.0, "pw": 0.03, "vb": 4.02, "tp": -15.8, "ic": 23.3, "ef": 1.0}, {"t": 12001.0, "pw": 0.036, "vb": 4.02, "tp": -16.3, "ic": 28.0, "ef": 1.0}, {"t": 12068.0, "pw": 0.036, "vb": 4.02, "tp": -17.4, "ic": 28.0, "ef": 1.0}, {"t": 12136.0, "pw": 0.03, "vb": 4.02, "tp": -18.2, "ic": 23.3, "ef": 1.0}, {"t": 12204.0, "pw": 0.03, "vb": 4.02, "tp": -19.2, "ic": 23.3, "ef": 1.0}, {"t": 12272.0, "pw": 0.03, "vb": 3.99, "tp": -19.8, "ic": 23.3, "ef": 1.0}, {"t": 12340.0, "pw": 0.036, "vb": 3.97, "tp": -20.5, "ic": 28.0, "ef": 1.0}], "uguisu": [{"t": 0.0, "pw": 1.066, "vb": 4.2, "tp": 11.7, "ic": 233.1, "ef": 1.0}, {"t": 30.0, "pw": 1.227, "vb": 4.2, "tp": 11.6, "ic": 265.7, "ef": 1.0}, {"t": 60.0, "pw": 1.188, "vb": 4.2, "tp": 11.8, "ic": 256.4, "ef": 1.0}, {"t": 90.0, "pw": 1.5, "vb": 4.2, "tp": 12.2, "ic": 321.6, "ef": 1.0}, {"t": 120.0, "pw": 1.222, "vb": 4.2, "tp": 12.9, "ic": 261.0, "ef": 1.0}, {"t": 150.0, "pw": 1.194, "vb": 4.2, "tp": 13.6, "ic": 256.3, "ef": 1.0}, {"t": 180.0, "pw": 1.19, "vb": 4.2, "tp": 14.2, "ic": 256.4, "ef": 1.0}, {"t": 210.0, "pw": 1.054, "vb": 4.2, "tp": 14.8, "ic": 223.7, "ef": 1.0}, {"t": 240.0, "pw": 1.176, "vb": 4.2, "tp": 15.9, "ic": 247.0, "ef": 1.0}, {"t": 270.0, "pw": 1.145, "vb": 4.2, "tp": 17.0, "ic": 242.4, "ef": 1.0}, {"t": 300.0, "pw": 1.129, "vb": 4.2, "tp": 17.6, "ic": 242.4, "ef": 1.0}, {"t": 330.0, "pw": 1.109, "vb": 4.2, "tp": 17.5, "ic": 242.4, "ef": 1.0}, {"t": 360.0, "pw": 1.162, "vb": 4.2, "tp": 16.7, "ic": 265.7, "ef": 1.0}, {"t": 390.0, "pw": 0.619, "vb": 4.17, "tp": 15.0, "ic": 149.2, "ef": 1.0}, {"t": 420.0, "pw": 1.271, "vb": 4.2, "tp": 13.6, "ic": 289.0, "ef": 1.0}, {"t": 450.0, "pw": 1.212, "vb": 4.2, "tp": 12.7, "ic": 265.7, "ef": 1.0}, {"t": 480.0, "pw": 1.132, "vb": 4.2, "tp": 12.5, "ic": 251.7, "ef": 1.0}, {"t": 510.0, "pw": 1.144, "vb": 4.2, "tp": 12.2, "ic": 251.7, "ef": 1.0}, {"t": 540.0, "pw": 1.417, "vb": 4.2, "tp": 12.4, "ic": 312.3, "ef": 1.0}, {"t": 570.0, "pw": 1.182, "vb": 4.2, "tp": 12.8, "ic": 265.7, "ef": 1.0}, {"t": 600.0, "pw": 0.345, "vb": 4.17, "tp": 12.8, "ic": 83.9, "ef": 1.0}, {"t": 630.0, "pw": 1.067, "vb": 4.15, "tp": 13.1, "ic": 251.7, "ef": 1.0}, {"t": 660.0, "pw": 1.206, "vb": 4.2, "tp": 13.7, "ic": 256.4, "ef": 1.0}, {"t": 690.0, "pw": 1.271, "vb": 4.2, "tp": 14.4, "ic": 270.3, "ef": 1.0}, {"t": 720.0, "pw": 1.213, "vb": 4.2, "tp": 14.8, "ic": 261.0, "ef": 1.0}, {"t": 750.0, "pw": 1.192, "vb": 4.2, "tp": 14.9, "ic": 261.0, "ef": 1.0}, {"t": 780.0, "pw": 1.419, "vb": 4.2, "tp": 14.2, "ic": 326.3, "ef": 1.0}, {"t": 810.0, "pw": 1.034, "vb": 4.2, "tp": 13.1, "ic": 270.3, "ef": 1.0}, {"t": 840.0, "pw": 1.176, "vb": 4.2, "tp": 11.7, "ic": 265.7, "ef": 1.0}, {"t": 870.0, "pw": 1.11, "vb": 4.2, "tp": 10.9, "ic": 242.4, "ef": 1.0}, {"t": 900.0, "pw": 0.99, "vb": 4.2, "tp": 10.7, "ic": 219.1, "ef": 1.0}, {"t": 930.0, "pw": 1.037, "vb": 4.2, "tp": 10.8, "ic": 237.7, "ef": 1.0}, {"t": 960.0, "pw": 1.079, "vb": 4.2, "tp": 11.1, "ic": 237.7, "ef": 1.0}, {"t": 990.0, "pw": 1.045, "vb": 4.2, "tp": 11.9, "ic": 237.7, "ef": 1.0}, {"t": 1020.0, "pw": 0.844, "vb": 4.2, "tp": 12.8, "ic": 219.1, "ef": 1.0}, {"t": 1050.0, "pw": 0.867, "vb": 4.17, "tp": 13.3, "ic": 205.1, "ef": 1.0}, {"t": 1080.0, "pw": 1.176, "vb": 4.2, "tp": 13.9, "ic": 265.7, "ef": 1.0}, {"t": 1110.0, "pw": 1.135, "vb": 4.2, "tp": 14.4, "ic": 256.4, "ef": 1.0}, {"t": 1140.0, "pw": 0.952, "vb": 4.2, "tp": 14.8, "ic": 219.1, "ef": 1.0}, {"t": 1170.0, "pw": 0.915, "vb": 4.2, "tp": 15.1, "ic": 237.7, "ef": 1.0}, {"t": 1200.0, "pw": 0.798, "vb": 4.2, "tp": 14.9, "ic": 237.7, "ef": 1.0}, {"t": 1230.0, "pw": 0.798, "vb": 4.2, "tp": 14.0, "ic": 265.7, "ef": 1.0}, {"t": 1260.0, "pw": 0.139, "vb": 4.15, "tp": 12.3, "ic": 37.3, "ef": 1.0}, {"t": 1290.0, "pw": 0.711, "vb": 4.15, "tp": 10.7, "ic": 195.8, "ef": 1.0}, {"t": 1320.0, "pw": 1.065, "vb": 4.2, "tp": 9.6, "ic": 307.6, "ef": 1.0}, {"t": 1350.0, "pw": 0.852, "vb": 4.2, "tp": 9.2, "ic": 279.7, "ef": 1.0}, {"t": 1380.0, "pw": 0.85, "vb": 4.2, "tp": 9.2, "ic": 270.3, "ef": 1.0}, {"t": 1410.0, "pw": 0.842, "vb": 4.2, "tp": 9.4, "ic": 270.3, "ef": 1.0}, {"t": 1440.0, "pw": 0.633, "vb": 4.17, "tp": 9.9, "ic": 209.8, "ef": 1.0}, {"t": 1470.0, "pw": 0.067, "vb": 4.15, "tp": 10.2, "ic": 23.3, "ef": 1.0}, {"t": 1500.0, "pw": 0.765, "vb": 4.17, "tp": 10.7, "ic": 261.0, "ef": 1.0}, {"t": 1530.0, "pw": 0.952, "vb": 4.2, "tp": 11.4, "ic": 298.3, "ef": 1.0}, {"t": 1560.0, "pw": 0.87, "vb": 4.2, "tp": 12.2, "ic": 275.0, "ef": 1.0}, {"t": 1590.0, "pw": 0.096, "vb": 4.15, "tp": 11.8, "ic": 37.3, "ef": 1.0}, {"t": 1620.0, "pw": 0.024, "vb": 4.12, "tp": 9.8, "ic": 18.6, "ef": 1.0}, {"t": 1650.0, "pw": 0.024, "vb": 4.12, "tp": 8.1, "ic": 18.6, "ef": 1.0}, {"t": 1680.0, "pw": 0.024, "vb": 4.1, "tp": 6.4, "ic": 18.6, "ef": 1.0}, {"t": 1710.0, "pw": 0.024, "vb": 4.1, "tp": 4.9, "ic": 18.6, "ef": 1.0}, {"t": 1740.0, "pw": 0.03, "vb": 4.1, "tp": 3.4, "ic": 23.3, "ef": 1.0}, {"t": 1770.0, "pw": 0.03, "vb": 4.1, "tp": 2.0, "ic": 23.3, "ef": 1.0}, {"t": 1800.0, "pw": 0.024, "vb": 4.07, "tp": 0.8, "ic": 18.6, "ef": 1.0}, {"t": 1830.0, "pw": 0.024, "vb": 4.07, "tp": -0.4, "ic": 18.6, "ef": 1.0}, {"t": 1860.0, "pw": 0.024, "vb": 4.07, "tp": -1.4, "ic": 18.6, "ef": 1.0}, {"t": 1890.0, "pw": 0.03, "vb": 4.04, "tp": -2.3, "ic": 23.3, "ef": 1.0}, {"t": 1920.0, "pw": 0.03, "vb": 4.04, "tp": -3.1, "ic": 23.3, "ef": 1.0}, {"t": 1950.0, "pw": 0.03, "vb": 4.04, "tp": -3.9, "ic": 23.3, "ef": 1.0}, {"t": 1980.0, "pw": 0.03, "vb": 4.04, "tp": -4.6, "ic": 23.3, "ef": 1.0}, {"t": 2010.0, "pw": 0.024, "vb": 4.04, "tp": -5.4, "ic": 18.6, "ef": 1.0}, {"t": 2040.0, "pw": 0.03, "vb": 4.02, "tp": -6.0, "ic": 23.3, "ef": 1.0}, {"t": 2070.0, "pw": 0.03, "vb": 4.02, "tp": -6.7, "ic": 23.3, "ef": 1.0}, {"t": 2100.0, "pw": 0.03, "vb": 4.02, "tp": -7.3, "ic": 23.3, "ef": 1.0}, {"t": 2130.0, "pw": 0.03, "vb": 4.02, "tp": -7.9, "ic": 23.3, "ef": 1.0}, {"t": 2160.0, "pw": 0.024, "vb": 4.02, "tp": -8.6, "ic": 18.6, "ef": 1.0}, {"t": 2190.0, "pw": 0.03, "vb": 3.99, "tp": -9.2, "ic": 23.3, "ef": 1.0}, {"t": 2220.0, "pw": 0.03, "vb": 3.99, "tp": -9.9, "ic": 23.3, "ef": 1.0}, {"t": 2250.0, "pw": 0.03, "vb": 3.99, "tp": -10.6, "ic": 23.3, "ef": 1.0}, {"t": 2280.0, "pw": 0.03, "vb": 3.99, "tp": -11.3, "ic": 23.3, "ef": 1.0}, {"t": 2310.0, "pw": 0.03, "vb": 3.99, "tp": -11.9, "ic": 23.3, "ef": 1.0}, {"t": 2340.0, "pw": 0.03, "vb": 3.99, "tp": -12.4, "ic": 23.3, "ef": 1.0}, {"t": 2370.0, "pw": 0.03, "vb": 3.99, "tp": -12.9, "ic": 23.3, "ef": 1.0}, {"t": 2400.0, "pw": 0.03, "vb": 3.99, "tp": -13.3, "ic": 23.3, "ef": 1.0}, {"t": 2430.0, "pw": 0.036, "vb": 3.97, "tp": -13.9, "ic": 28.0, "ef": 1.0}, {"t": 2460.0, "pw": 0.03, "vb": 3.97, "tp": -14.1, "ic": 23.3, "ef": 1.0}, {"t": 2490.0, "pw": 0.03, "vb": 3.97, "tp": -14.6, "ic": 23.3, "ef": 1.0}, {"t": 2520.0, "pw": 0.03, "vb": 3.97, "tp": -15.0, "ic": 23.3, "ef": 1.0}, {"t": 2550.0, "pw": 0.03, "vb": 3.97, "tp": -15.3, "ic": 23.3, "ef": 1.0}, {"t": 2580.0, "pw": 0.03, "vb": 3.97, "tp": -15.7, "ic": 23.3, "ef": 1.0}, {"t": 2610.0, "pw": 0.03, "vb": 3.97, "tp": -16.1, "ic": 23.3, "ef": 1.0}, {"t": 2640.0, "pw": 0.036, "vb": 3.94, "tp": -16.6, "ic": 28.0, "ef": 1.0}, {"t": 2670.0, "pw": 0.03, "vb": 3.97, "tp": -17.1, "ic": 23.3, "ef": 1.0}, {"t": 2700.0, "pw": 0.03, "vb": 3.97, "tp": -17.6, "ic": 23.3, "ef": 1.0}, {"t": 2730.0, "pw": 0.03, "vb": 3.97, "tp": -18.1, "ic": 23.3, "ef": 1.0}, {"t": 2760.0, "pw": 0.03, "vb": 3.94, "tp": -18.5, "ic": 23.3, "ef": 1.0}, {"t": 2790.0, "pw": 0.03, "vb": 3.94, "tp": -18.9, "ic": 23.3, "ef": 1.0}, {"t": 2820.0, "pw": 0.03, "vb": 3.94, "tp": -19.2, "ic": 23.3, "ef": 1.0}, {"t": 2850.0, "pw": 0.03, "vb": 3.94, "tp": -19.6, "ic": 23.3, "ef": 1.0}, {"t": 2880.0, "pw": 0.03, "vb": 3.94, "tp": -19.9, "ic": 23.3, "ef": 1.0}, {"t": 2910.0, "pw": 0.03, "vb": 3.94, "tp": -20.2, "ic": 23.3, "ef": 1.0}, {"t": 2940.0, "pw": 0.03, "vb": 3.94, "tp": -20.5, "ic": 23.3, "ef": 1.0}, {"t": 2970.0, "pw": 0.03, "vb": 3.94, "tp": -20.7, "ic": 23.3, "ef": 1.0}, {"t": 3000.0, "pw": 0.083, "vb": 3.94, "tp": -21.0, "ic": 65.2, "ef": 1.0}, {"t": 3030.0, "pw": 0.03, "vb": 3.94, "tp": -21.3, "ic": 23.3, "ef": 1.0}, {"t": 3060.0, "pw": 0.03, "vb": 3.92, "tp": -21.6, "ic": 23.3, "ef": 1.0}, {"t": 3090.0, "pw": 0.03, "vb": 3.92, "tp": -21.9, "ic": 23.3, "ef": 1.0}, {"t": 3120.0, "pw": 0.03, "vb": 3.92, "tp": -22.1, "ic": 23.3, "ef": 1.0}, {"t": 3150.0, "pw": 0.03, "vb": 3.92, "tp": -22.3, "ic": 23.3, "ef": 1.0}, {"t": 3180.0, "pw": 0.03, "vb": 3.92, "tp": -22.4, "ic": 23.3, "ef": 1.0}, {"t": 3210.0, "pw": 0.03, "vb": 3.92, "tp": -22.5, "ic": 23.3, "ef": 1.0}, {"t": 3240.0, "pw": 0.036, "vb": 3.92, "tp": -22.6, "ic": 28.0, "ef": 1.0}, {"t": 3270.0, "pw": 0.03, "vb": 3.92, "tp": -22.7, "ic": 23.3, "ef": 1.0}, {"t": 3300.0, "pw": 0.03, "vb": 3.92, "tp": -22.8, "ic": 23.3, "ef": 1.0}, {"t": 3330.0, "pw": 0.113, "vb": 3.92, "tp": -22.8, "ic": 88.6, "ef": 1.0}, {"t": 3360.0, "pw": 0.036, "vb": 3.92, "tp": -23.0, "ic": 28.0, "ef": 1.0}, {"t": 3390.0, "pw": 0.03, "vb": 3.92, "tp": -23.2, "ic": 23.3, "ef": 1.0}, {"t": 3420.0, "pw": 0.03, "vb": 3.89, "tp": -23.4, "ic": 23.3, "ef": 1.0}, {"t": 3450.0, "pw": 0.03, "vb": 3.89, "tp": -23.7, "ic": 23.3, "ef": 1.0}, {"t": 3480.0, "pw": 0.03, "vb": 3.89, "tp": -24.1, "ic": 23.3, "ef": 1.0}, {"t": 3510.0, "pw": 0.03, "vb": 3.89, "tp": -24.4, "ic": 23.3, "ef": 1.0}, {"t": 3540.0, "pw": 0.03, "vb": 3.89, "tp": -24.8, "ic": 23.3, "ef": 1.0}, {"t": 3570.0, "pw": 0.03, "vb": 3.89, "tp": -25.1, "ic": 23.3, "ef": 1.0}, {"t": 3600.0, "pw": 0.257, "vb": 3.89, "tp": -25.2, "ic": 97.9, "ef": 1.0}, {"t": 3630.0, "pw": 0.966, "vb": 3.94, "tp": -24.5, "ic": 363.6, "ef": 1.0}, {"t": 3660.0, "pw": 1.42, "vb": 3.99, "tp": -23.3, "ic": 536.0, "ef": 1.0}, {"t": 3690.0, "pw": 1.808, "vb": 4.02, "tp": -21.8, "ic": 615.3, "ef": 1.0}, {"t": 3720.0, "pw": 1.674, "vb": 4.02, "tp": -20.0, "ic": 559.3, "ef": 1.0}, {"t": 3750.0, "pw": 1.211, "vb": 4.02, "tp": -18.0, "ic": 400.9, "ef": 1.0}, {"t": 3780.0, "pw": 0.604, "vb": 3.97, "tp": -16.3, "ic": 167.8, "ef": 1.0}, {"t": 3810.0, "pw": 0.806, "vb": 3.97, "tp": -14.9, "ic": 228.4, "ef": 1.0}, {"t": 3840.0, "pw": 1.245, "vb": 3.99, "tp": -13.5, "ic": 344.9, "ef": 1.0}, {"t": 3870.0, "pw": 1.638, "vb": 4.02, "tp": -12.4, "ic": 456.8, "ef": 1.0}, {"t": 3900.0, "pw": 1.837, "vb": 4.04, "tp": -11.9, "ic": 517.4, "ef": 1.0}, {"t": 3930.0, "pw": 1.883, "vb": 4.07, "tp": -11.8, "ic": 564.0, "ef": 1.0}, {"t": 3960.0, "pw": 2.08, "vb": 4.07, "tp": -11.7, "ic": 550.0, "ef": 1.0}, {"t": 3990.0, "pw": 1.796, "vb": 4.07, "tp": -11.6, "ic": 452.1, "ef": 1.0}, {"t": 4020.0, "pw": 1.058, "vb": 4.02, "tp": -11.9, "ic": 256.4, "ef": 1.0}, {"t": 4050.0, "pw": 0.917, "vb": 3.99, "tp": -12.4, "ic": 228.4, "ef": 1.0}, {"t": 4080.0, "pw": 1.523, "vb": 4.04, "tp": -12.5, "ic": 368.2, "ef": 1.0}, {"t": 4110.0, "pw": 2.078, "vb": 4.07, "tp": -12.0, "ic": 498.7, "ef": 1.0}, {"t": 4140.0, "pw": 2.352, "vb": 4.1, "tp": -11.4, "ic": 587.3, "ef": 1.0}, {"t": 4170.0, "pw": 2.582, "vb": 4.12, "tp": -10.5, "ic": 605.9, "ef": 1.0}, {"t": 4200.0, "pw": 2.159, "vb": 4.1, "tp": -9.0, "ic": 503.4, "ef": 1.0}, {"t": 4230.0, "pw": 1.199, "vb": 4.07, "tp": -7.7, "ic": 279.7, "ef": 1.0}, {"t": 4260.0, "pw": 0.358, "vb": 4.02, "tp": -6.8, "ic": 97.9, "ef": 1.0}, {"t": 4290.0, "pw": 1.587, "vb": 4.04, "tp": -5.9, "ic": 377.6, "ef": 1.0}, {"t": 4320.0, "pw": 2.622, "vb": 4.12, "tp": -4.5, "ic": 615.3, "ef": 1.0}, {"t": 4350.0, "pw": 3.063, "vb": 4.15, "tp": -3.5, "ic": 727.1, "ef": 1.0}, {"t": 4380.0, "pw": 2.846, "vb": 4.15, "tp": -3.2, "ic": 680.5, "ef": 1.0}, {"t": 4410.0, "pw": 2.149, "vb": 4.15, "tp": -3.6, "ic": 512.7, "ef": 1.0}, {"t": 4440.0, "pw": 1.406, "vb": 4.12, "tp": -3.9, "ic": 335.6, "ef": 1.0}, {"t": 4470.0, "pw": 0.78, "vb": 4.07, "tp": -4.8, "ic": 186.4, "ef": 1.0}, {"t": 4500.0, "pw": 1.807, "vb": 4.12, "tp": -5.2, "ic": 428.8, "ef": 1.0}, {"t": 4530.0, "pw": 2.921, "vb": 4.17, "tp": -4.8, "ic": 689.8, "ef": 1.0}, {"t": 4560.0, "pw": 2.831, "vb": 4.2, "tp": -3.9, "ic": 596.6, "ef": 1.0}, {"t": 4590.0, "pw": 2.597, "vb": 4.2, "tp": -2.9, "ic": 545.3, "ef": 1.0}, {"t": 4620.0, "pw": 2.42, "vb": 4.2, "tp": -1.7, "ic": 512.7, "ef": 1.0}, {"t": 4650.0, "pw": 2.279, "vb": 4.2, "tp": -0.3, "ic": 484.8, "ef": 1.0}, {"t": 4680.0, "pw": 2.117, "vb": 4.2, "tp": 1.1, "ic": 447.5, "ef": 1.0}, {"t": 4710.0, "pw": 2.008, "vb": 4.2, "tp": 2.5, "ic": 424.2, "ef": 1.0}, {"t": 4740.0, "pw": 1.732, "vb": 4.2, "tp": 3.3, "ic": 372.9, "ef": 1.0}, {"t": 4770.0, "pw": 1.806, "vb": 4.2, "tp": 3.9, "ic": 382.2, "ef": 1.0}, {"t": 4800.0, "pw": 1.765, "vb": 4.2, "tp": 4.5, "ic": 372.9, "ef": 1.0}, {"t": 4830.0, "pw": 1.742, "vb": 4.2, "tp": 5.0, "ic": 368.2, "ef": 1.0}, {"t": 4860.0, "pw": 1.943, "vb": 4.2, "tp": 5.3, "ic": 414.8, "ef": 1.0}, {"t": 4890.0, "pw": 1.651, "vb": 4.2, "tp": 5.2, "ic": 354.2, "ef": 1.0}, {"t": 4920.0, "pw": 1.596, "vb": 4.2, "tp": 4.9, "ic": 344.9, "ef": 1.0}, {"t": 4950.0, "pw": 1.602, "vb": 4.2, "tp": 5.1, "ic": 340.3, "ef": 1.0}, {"t": 4980.0, "pw": 1.5, "vb": 4.2, "tp": 5.7, "ic": 316.9, "ef": 1.0}, {"t": 5010.0, "pw": 1.617, "vb": 4.2, "tp": 6.5, "ic": 340.3, "ef": 1.0}, {"t": 5040.0, "pw": 1.595, "vb": 4.2, "tp": 7.4, "ic": 335.6, "ef": 1.0}, {"t": 5070.0, "pw": 1.526, "vb": 4.2, "tp": 8.4, "ic": 321.6, "ef": 1.0}, {"t": 5100.0, "pw": 1.755, "vb": 4.2, "tp": 9.3, "ic": 372.9, "ef": 1.0}, {"t": 5130.0, "pw": 1.462, "vb": 4.2, "tp": 10.0, "ic": 312.3, "ef": 1.0}, {"t": 5160.0, "pw": 1.419, "vb": 4.2, "tp": 10.4, "ic": 307.6, "ef": 1.0}, {"t": 5190.0, "pw": 1.413, "vb": 4.2, "tp": 10.6, "ic": 303.0, "ef": 1.0}, {"t": 5220.0, "pw": 1.699, "vb": 4.2, "tp": 11.0, "ic": 363.6, "ef": 1.0}, {"t": 5250.0, "pw": 1.419, "vb": 4.2, "tp": 11.7, "ic": 303.0, "ef": 1.0}, {"t": 5280.0, "pw": 1.359, "vb": 4.2, "tp": 11.8, "ic": 293.6, "ef": 1.0}, {"t": 5310.0, "pw": 1.373, "vb": 4.2, "tp": 11.7, "ic": 298.3, "ef": 1.0}, {"t": 5340.0, "pw": 1.376, "vb": 4.2, "tp": 11.9, "ic": 293.6, "ef": 1.0}, {"t": 5370.0, "pw": 1.358, "vb": 4.2, "tp": 12.1, "ic": 289.0, "ef": 1.0}, {"t": 5400.0, "pw": 1.067, "vb": 4.2, "tp": 16.1, "ic": 233.0, "ef": 1.0}, {"t": 5430.0, "pw": 1.123, "vb": 4.2, "tp": 15.1, "ic": 256.4, "ef": 1.0}, {"t": 5460.0, "pw": 1.151, "vb": 4.2, "tp": 14.6, "ic": 247.0, "ef": 1.0}, {"t": 5490.0, "pw": 1.169, "vb": 4.2, "tp": 15.0, "ic": 247.0, "ef": 1.0}, {"t": 5500.0, "pw": 1.175, "vb": 4.2, "tp": 15.5, "ic": 251.7, "ef": 1.0}, {"t": 5500.0, "pw": 1.144, "vb": 4.2, "tp": 16.0, "ic": 247.0, "ef": 1.0}]}, "minxss": [{"lat": -42.23, "lon": -32.71, "alt": 412.2, "ec": 1, "v": 4.948}, {"lat": -39.65, "lon": -125.56, "alt": 411.5, "ec": 1, "v": 4.951}, {"lat": 42.49, "lon": -103.46, "alt": 397.5, "ec": 1, "v": 4.931}, {"lat": 36.35, "lon": -48.16, "alt": 399.6, "ec": 1, "v": 4.969}, {"lat": -24.3, "lon": 106.55, "alt": 408.4, "ec": 1, "v": 4.967}, {"lat": 16.55, "lon": 40.65, "alt": 402.0, "ec": 0, "v": 4.929}, {"lat": 35.61, "lon": 59.85, "alt": 398.0, "ec": 0, "v": 4.924}, {"lat": 48.9, "lon": 88.79, "alt": 395.5, "ec": 0, "v": 4.926}, {"lat": -51.62, "lon": -78.19, "alt": 412.1, "ec": 0, "v": 4.923}, {"lat": -42.18, "lon": -37.07, "alt": 411.3, "ec": 0, "v": 4.923}, {"lat": -23.86, "lon": -13.54, "alt": 409.1, "ec": 0, "v": 4.924}, {"lat": -2.98, "lon": 2.82, "alt": 405.7, "ec": 0, "v": 4.929}, {"lat": 11.44, "lon": 141.44, "alt": 403.4, "ec": 1, "v": 4.926}, {"lat": -9.35, "lon": 156.42, "alt": 407.3, "ec": 1, "v": 4.927}, {"lat": -33.25, "lon": 178.09, "alt": 410.6, "ec": 1, "v": 4.93}, {"lat": 10.55, "lon": 8.66, "alt": 402.2, "ec": 1, "v": 4.964}, {"lat": -12.63, "lon": 175.33, "alt": 408.4, "ec": 1, "v": 4.959}, {"lat": 8.15, "lon": -169.68, "alt": 404.6, "ec": 1, "v": 4.964}, {"lat": 28.19, "lon": -152.81, "alt": 400.3, "ec": 1, "v": 4.97}, {"lat": 45.59, "lon": -125.85, "alt": 396.5, "ec": 1, "v": 4.966}, {"lat": 50.36, "lon": -74.98, "alt": 395.1, "ec": 1, "v": 4.96}, {"lat": -47.41, "lon": -105.38, "alt": 411.8, "ec": 0, "v": 4.974}, {"lat": -51.16, "lon": 141.46, "alt": 411.6, "ec": 0, "v": 4.924}, {"lat": -41.05, "lon": 175.65, "alt": 411.3, "ec": 0, "v": 4.927}, {"lat": -23.8, "lon": -162.89, "alt": 409.8, "ec": 0, "v": 4.928}, {"lat": -2.93, "lon": -146.55, "alt": 406.7, "ec": 0, "v": 4.925}, {"lat": 20.59, "lon": -128.9, "alt": 402.0, "ec": 0, "v": 4.927}, {"lat": 38.94, "lon": -108.15, "alt": 398.0, "ec": 0, "v": 4.928}, {"lat": 50.39, "lon": -76.53, "alt": 395.5, "ec": 0, "v": 4.929}, {"lat": 48.9, "lon": -36.58, "alt": 395.3, "ec": 0, "v": 4.929}, {"lat": 35.2, "lon": -7.06, "alt": 397.4, "ec": 1, "v": 4.928}, {"lat": 15.07, "lon": 12.76, "alt": 401.2, "ec": 1, "v": 4.928}, {"lat": -5.19, "lon": 27.5, "alt": 405.0, "ec": 1, "v": 4.927}, {"lat": -25.44, "lon": 43.77, "alt": 408.2, "ec": 1, "v": 4.929}, {"lat": -50.75, "lon": 176.17, "alt": 411.5, "ec": 0, "v": 4.924}, {"lat": -26.74, "lon": -134.64, "alt": 410.0, "ec": 0, "v": 4.926}, {"lat": -6.6, "lon": -118.12, "alt": 407.3, "ec": 0, "v": 4.927}, {"lat": 14.16, "lon": -103.07, "alt": 403.3, "ec": 0, "v": 4.925}, {"lat": 33.12, "lon": -85.19, "alt": 399.3, "ec": 0, "v": 4.926}, {"lat": 48.02, "lon": -56.4, "alt": 396.1, "ec": 0, "v": 4.926}, {"lat": 51.01, "lon": -17.77, "alt": 395.1, "ec": 0, "v": 4.932}, {"lat": 38.92, "lon": 18.57, "alt": 396.7, "ec": 0, "v": 4.924}, {"lat": -51.62, "lon": 138.23, "alt": 411.3, "ec": 1, "v": 4.926}, {"lat": -45.08, "lon": 174.75, "alt": 411.4, "ec": 0, "v": 4.924}, {"lat": -28.41, "lon": -159.83, "alt": 410.2, "ec": 0, "v": 4.924}, {"lat": 20.71, "lon": -121.23, "alt": 402.0, "ec": 0, "v": 4.93}, {"lat": 43.09, "lon": -93.06, "alt": 397.1, "ec": 0, "v": 4.931}, {"lat": 51.26, "lon": -43.93, "alt": 395.0, "ec": 0, "v": 4.927}, {"lat": -45.79, "lon": 34.54, "alt": 410.4, "ec": 1, "v": 4.928}, {"lat": -45.12, "lon": 104.15, "alt": 411.4, "ec": 0, "v": 4.928}, {"lat": -24.75, "lon": 133.3, "alt": 409.9, "ec": 0, "v": 4.926}, {"lat": -0.89, "lon": 151.97, "alt": 406.4, "ec": 0, "v": 4.928}, {"lat": 23.58, "lon": 170.83, "alt": 401.4, "ec": 0, "v": 4.925}, {"lat": 45.01, "lon": -159.22, "alt": 396.7, "ec": 0, "v": 4.926}, {"lat": -46.93, "lon": -32.7, "alt": 410.4, "ec": 1, "v": 4.929}, {"lat": -51.39, "lon": 5.14, "alt": 411.4, "ec": 0, "v": 4.929}, {"lat": -42.15, "lon": 40.17, "alt": 411.3, "ec": 0, "v": 4.929}, {"lat": -25.25, "lon": 62.35, "alt": 410.0, "ec": 0, "v": 4.926}, {"lat": -4.99, "lon": 78.57, "alt": 407.2, "ec": 0, "v": 4.929}, {"lat": 15.74, "lon": 93.7, "alt": 403.2, "ec": 0, "v": 4.926}, {"lat": 35.34, "lon": 113.18, "alt": 398.9, "ec": 0, "v": 4.926}, {"lat": 51.44, "lon": 159.97, "alt": 395.1, "ec": 0, "v": 4.929}, {"lat": 20.97, "lon": -105.85, "alt": 402.2, "ec": 0, "v": 4.93}, {"lat": 45.32, "lon": -26.58, "alt": 395.1, "ec": 0, "v": 4.977}, {"lat": -51.62, "lon": 107.57, "alt": 409.8, "ec": 1, "v": 4.981}, {"lat": 45.63, "lon": -98.79, "alt": 395.0, "ec": 0, "v": 4.925}, {"lat": 37.48, "lon": -107.39, "alt": 395.9, "ec": 0, "v": 4.925}, {"lat": -39.34, "lon": -106.93, "alt": 404.2, "ec": 0, "v": 4.929}, {"lat": 33.07, "lon": 117.51, "alt": 396.5, "ec": 0, "v": 4.927}, {"lat": 47.79, "lon": -5.57, "alt": 395.6, "ec": 0, "v": 4.925}, {"lat": 51.01, "lon": 33.93, "alt": 394.7, "ec": 0, "v": 4.926}, {"lat": 40.79, "lon": 67.11, "alt": 395.7, "ec": 0, "v": 4.927}, {"lat": 22.43, "lon": 89.35, "alt": 398.0, "ec": 0, "v": 4.925}, {"lat": 2.44, "lon": 104.8, "alt": 400.5, "ec": 0, "v": 4.928}, {"lat": -18.73, "lon": 120.53, "alt": 402.7, "ec": 0, "v": 4.926}, {"lat": -37.41, "lon": 140.49, "alt": 404.0, "ec": 0, "v": 4.926}, {"lat": 9.54, "lon": -78.37, "alt": 401.4, "ec": 1, "v": 4.926}, {"lat": 29.46, "lon": -61.18, "alt": 398.5, "ec": 0, "v": 4.923}, {"lat": 45.22, "lon": -36.52, "alt": 396.0, "ec": 0, "v": 4.926}, {"lat": 51.62, "lon": 0.29, "alt": 394.8, "ec": 0, "v": 4.926}, {"lat": 43.02, "lon": 39.36, "alt": 395.4, "ec": 0, "v": 4.926}, {"lat": 24.43, "lon": -170.74, "alt": 397.6, "ec": 0, "v": 4.923}, {"lat": 3.55, "lon": -154.26, "alt": 400.2, "ec": 0, "v": 4.931}, {"lat": -16.67, "lon": -139.42, "alt": 402.4, "ec": 0, "v": 4.929}, {"lat": 16.48, "lon": 28.68, "alt": 400.5, "ec": 1, "v": 4.926}, {"lat": 36.38, "lon": 49.0, "alt": 397.4, "ec": 0, "v": 4.924}, {"lat": 49.48, "lon": 79.45, "alt": 395.3, "ec": 0, "v": 4.927}, {"lat": 49.76, "lon": 120.43, "alt": 394.7, "ec": 0, "v": 4.932}, {"lat": 37.42, "lon": 150.81, "alt": 396.0, "ec": 0, "v": 4.928}, {"lat": 12.74, "lon": 175.54, "alt": 399.1, "ec": 0, "v": 4.934}, {"lat": -22.89, "lon": -157.63, "alt": 402.9, "ec": 0, "v": 4.927}, {"lat": 51.62, "lon": -101.58, "alt": 393.8, "ec": 0, "v": 4.927}, {"lat": 20.5, "lon": -34.17, "alt": 397.7, "ec": 0, "v": 4.93}, {"lat": -29.7, "lon": 5.62, "alt": 403.6, "ec": 0, "v": 4.929}, {"lat": -50.16, "lon": 83.09, "alt": 405.2, "ec": 1, "v": 4.929}, {"lat": -12.35, "lon": 140.63, "alt": 403.3, "ec": 1, "v": 4.927}, {"lat": 34.85, "lon": 179.98, "alt": 396.7, "ec": 0, "v": 4.926}, {"lat": 46.9, "lon": -95.47, "alt": 394.1, "ec": 0, "v": 4.93}, {"lat": 4.67, "lon": -45.48, "alt": 400.0, "ec": 0, "v": 4.929}, {"lat": -49.17, "lon": 19.38, "alt": 405.0, "ec": 0, "v": 4.928}, {"lat": 46.5, "lon": -85.5, "alt": 393.9, "ec": 0, "v": 4.925}, {"lat": -30.4, "lon": -8.28, "alt": 402.6, "ec": 0, "v": 4.926}, {"lat": -51.49, "lon": 56.07, "alt": 402.5, "ec": 0, "v": 4.93}, {"lat": -25.61, "lon": 114.78, "alt": 400.8, "ec": 1, "v": 4.928}, {"lat": 15.44, "lon": 146.25, "alt": 396.7, "ec": 1, "v": 4.926}, {"lat": 48.17, "lon": -167.53, "alt": 393.0, "ec": 0, "v": 4.932}, {"lat": 39.79, "lon": -94.52, "alt": 394.9, "ec": 0, "v": 4.927}, {"lat": 2.12, "lon": -58.32, "alt": 400.2, "ec": 0, "v": 4.925}, {"lat": -32.63, "lon": -115.07, "alt": 402.6, "ec": 0, "v": 4.926}, {"lat": -47.48, "lon": -87.56, "alt": 402.7, "ec": 0, "v": 4.929}, {"lat": -51.13, "lon": -48.33, "alt": 402.3, "ec": 0, "v": 4.929}, {"lat": -39.81, "lon": -12.19, "alt": 401.6, "ec": 0, "v": 4.927}, {"lat": 47.45, "lon": 33.68, "alt": 392.7, "ec": 1, "v": 4.928}, {"lat": 51.13, "lon": 73.02, "alt": 392.8, "ec": 0, "v": 4.924}, {"lat": 37.8, "lon": 112.35, "alt": 395.1, "ec": 0, "v": 4.926}, {"lat": 11.71, "lon": 138.43, "alt": 399.0, "ec": 0, "v": 4.925}, {"lat": -20.05, "lon": 162.01, "alt": 402.1, "ec": 0, "v": 4.925}, {"lat": -14.08, "lon": 133.7, "alt": 401.7, "ec": 0, "v": 4.926}, {"lat": 50.0, "lon": -2.68, "alt": 392.5, "ec": 0, "v": 4.923}, {"lat": 49.4, "lon": 37.38, "alt": 393.2, "ec": 0, "v": 4.926}, {"lat": 35.37, "lon": 68.85, "alt": 395.5, "ec": 0, "v": 4.925}, {"lat": 15.27, "lon": 88.75, "alt": 398.5, "ec": 0, "v": 4.925}, {"lat": -9.55, "lon": 106.82, "alt": 401.3, "ec": 0, "v": 4.923}, {"lat": -37.2, "lon": 133.63, "alt": 402.7, "ec": 0, "v": 4.926}, {"lat": -46.84, "lon": -144.95, "alt": 402.0, "ec": 0, "v": 4.931}, {"lat": 50.58, "lon": -110.09, "alt": 392.9, "ec": 0, "v": 4.926}, {"lat": -13.41, "lon": -31.08, "alt": 401.7, "ec": 0, "v": 4.926}, {"lat": 44.49, "lon": -111.26, "alt": 394.0, "ec": 0, "v": 4.928}, {"lat": -5.89, "lon": -60.11, "alt": 401.0, "ec": 0, "v": 4.93}, {"lat": -27.05, "lon": -42.77, "alt": 402.4, "ec": 0, "v": 4.927}, {"lat": -50.72, "lon": 5.94, "alt": 402.6, "ec": 0, "v": 4.929}, {"lat": -47.71, "lon": 48.02, "alt": 402.0, "ec": 0, "v": 4.926}, {"lat": -31.26, "lon": 77.91, "alt": 400.9, "ec": 0, "v": 4.929}, {"lat": 51.28, "lon": -78.62, "alt": 392.3, "ec": 0, "v": 4.931}, {"lat": 43.66, "lon": -30.99, "alt": 394.0, "ec": 0, "v": 4.921}, {"lat": 49.85, "lon": 27.66, "alt": 392.8, "ec": 0, "v": 4.928}, {"lat": -3.24, "lon": 94.79, "alt": 400.8, "ec": 0, "v": 4.926}, {"lat": -23.17, "lon": 110.34, "alt": 402.3, "ec": 0, "v": 4.925}, {"lat": -40.96, "lon": 132.22, "alt": 402.8, "ec": 0, "v": 4.92}, {"lat": -51.14, "lon": 166.42, "alt": 402.6, "ec": 0, "v": 4.928}, {"lat": -47.49, "lon": -154.43, "alt": 401.9, "ec": 0, "v": 4.926}, {"lat": -31.31, "lon": -125.34, "alt": 400.8, "ec": 0, "v": 4.925}, {"lat": -11.1, "lon": -107.27, "alt": 399.1, "ec": 0, "v": 4.932}, {"lat": 24.7, "lon": 26.29, "alt": 397.0, "ec": 0, "v": 4.926}, {"lat": -26.05, "lon": 66.11, "alt": 402.5, "ec": 0, "v": 4.929}, {"lat": -42.78, "lon": 88.76, "alt": 402.8, "ec": 0, "v": 4.927}, {"lat": -45.54, "lon": 164.27, "alt": 401.8, "ec": 0, "v": 4.926}, {"lat": 13.42, "lon": -73.54, "alt": 398.7, "ec": 0, "v": 4.924}, {"lat": 6.18, "lon": 108.9, "alt": 396.9, "ec": 0, "v": 4.931}, {"lat": 36.74, "lon": -120.23, "alt": 394.9, "ec": 0, "v": 4.923}, {"lat": -51.52, "lon": 1.61, "alt": 402.4, "ec": 0, "v": 4.926}, {"lat": 17.26, "lon": 93.82, "alt": 395.5, "ec": 1, "v": 4.926}, {"lat": 33.85, "lon": -139.83, "alt": 395.4, "ec": 0, "v": 4.926}, {"lat": -50.26, "lon": -43.52, "alt": 402.6, "ec": 0, "v": 4.926}, {"lat": -16.6, "lon": 21.83, "alt": 399.4, "ec": 1, "v": 4.927}, {"lat": 12.75, "lon": 43.35, "alt": 396.1, "ec": 1, "v": 4.929}, {"lat": 39.34, "lon": 71.06, "alt": 392.8, "ec": 1, "v": 4.926}, {"lat": 51.56, "lon": 121.9, "alt": 392.0, "ec": 1, "v": 4.927}, {"lat": 36.42, "lon": 169.83, "alt": 395.0, "ec": 1, "v": 4.927}, {"lat": 6.97, "lon": -162.6, "alt": 399.6, "ec": 0, "v": 4.927}, {"lat": -25.05, "lon": -138.04, "alt": 402.5, "ec": 0, "v": 4.928}, {"lat": -51.36, "lon": -66.0, "alt": 402.3, "ec": 0, "v": 4.927}, {"lat": -28.1, "lon": -66.32, "alt": 400.3, "ec": 0, "v": 4.93}, {"lat": 4.69, "lon": -40.38, "alt": 396.8, "ec": 0, "v": 4.926}, {"lat": 31.94, "lon": -16.9, "alt": 393.2, "ec": 0, "v": 4.932}, {"lat": 46.83, "lon": 9.41, "alt": 391.6, "ec": 0, "v": 4.93}, {"lat": 41.01, "lon": 84.74, "alt": 393.8, "ec": 0, "v": 4.929}, {"lat": 19.8, "lon": 109.66, "alt": 397.5, "ec": 0, "v": 4.931}, {"lat": -5.41, "lon": 128.41, "alt": 400.9, "ec": 0, "v": 4.928}, {"lat": -19.98, "lon": -82.23, "alt": 399.5, "ec": 0, "v": 4.929}, {"lat": 12.82, "lon": -57.87, "alt": 395.7, "ec": 0, "v": 4.931}, {"lat": 51.04, "lon": 5.79, "alt": 391.4, "ec": 1, "v": 4.93}, {"lat": 47.68, "lon": 45.26, "alt": 392.5, "ec": 0, "v": 4.934}, {"lat": 32.06, "lon": 74.14, "alt": 395.4, "ec": 0, "v": 4.927}, {"lat": 9.92, "lon": 93.96, "alt": 399.0, "ec": 0, "v": 4.932}, {"lat": 15.73, "lon": -79.08, "alt": 395.3, "ec": 0, "v": 4.931}, {"lat": 35.35, "lon": -59.56, "alt": 392.7, "ec": 0, "v": 4.927}, {"lat": 48.99, "lon": -29.89, "alt": 391.4, "ec": 0, "v": 4.932}, {"lat": 50.32, "lon": 10.1, "alt": 392.0, "ec": 1, "v": 4.929}, {"lat": 38.77, "lon": 41.59, "alt": 394.2, "ec": 0, "v": 4.926}, {"lat": 19.86, "lon": 62.68, "alt": 397.5, "ec": 0, "v": 4.931}, {"lat": -0.15, "lon": 77.74, "alt": 400.3, "ec": 0, "v": 4.924}, {"lat": -21.21, "lon": 93.74, "alt": 402.2, "ec": 0, "v": 4.928}, {"lat": -39.81, "lon": 115.36, "alt": 402.9, "ec": 1, "v": 4.928}, {"lat": 19.7, "lon": 77.48, "alt": 392.9, "ec": 1, "v": 4.965}, {"lat": -0.45, "lon": 92.61, "alt": 396.4, "ec": 1, "v": 4.963}, {"lat": -39.23, "lon": 129.07, "alt": 400.4, "ec": 1, "v": 4.971}, {"lat": -49.55, "lon": -162.77, "alt": 400.3, "ec": 1, "v": 4.967}, {"lat": -16.66, "lon": -111.76, "alt": 397.2, "ec": 1, "v": 4.97}, {"lat": 4.61, "lon": -96.17, "alt": 394.2, "ec": 1, "v": 4.965}, {"lat": 26.86, "lon": -78.09, "alt": 390.5, "ec": 1, "v": 4.966}, {"lat": 46.04, "lon": -72.03, "alt": 387.5, "ec": 1, "v": 4.964}, {"lat": 51.62, "lon": -62.13, "alt": 386.9, "ec": 1, "v": 4.962}, {"lat": 44.74, "lon": -25.6, "alt": 388.3, "ec": 1, "v": 4.966}, {"lat": 28.73, "lon": -1.32, "alt": 391.2, "ec": 1, "v": 4.967}, {"lat": 7.68, "lon": 16.46, "alt": 395.0, "ec": 1, "v": 4.965}, {"lat": -12.64, "lon": 31.12, "alt": 398.0, "ec": 1, "v": 4.965}, {"lat": 45.5, "lon": -41.72, "alt": 387.4, "ec": 1, "v": 4.974}, {"lat": -18.88, "lon": -2.53, "alt": 398.5, "ec": 1, "v": 4.968}, {"lat": -40.33, "lon": 21.95, "alt": 400.2, "ec": 1, "v": 4.952}, {"lat": -15.11, "lon": 125.37, "alt": 396.7, "ec": 1, "v": 4.952}, {"lat": 40.12, "lon": 151.26, "alt": 388.0, "ec": 1, "v": 4.953}, {"lat": 50.81, "lon": -176.05, "alt": 386.6, "ec": 1, "v": 4.953}, {"lat": -51.32, "lon": -26.14, "alt": 400.3, "ec": 1, "v": 4.957}, {"lat": -47.17, "lon": 11.95, "alt": 399.8, "ec": 1, "v": 4.957}, {"lat": -21.19, "lon": 50.02, "alt": 397.4, "ec": 1, "v": 4.961}, {"lat": 0.16, "lon": 66.22, "alt": 394.5, "ec": 1, "v": 4.963}, {"lat": 51.09, "lon": 139.61, "alt": 386.6, "ec": 1, "v": 4.956}, {"lat": 47.3, "lon": 97.24, "alt": 387.0, "ec": 1, "v": 4.952}, {"lat": 9.32, "lon": 25.91, "alt": 393.1, "ec": 1, "v": 4.957}, {"lat": 28.39, "lon": 42.13, "alt": 389.9, "ec": 1, "v": 4.957}, {"lat": 44.51, "lon": 66.21, "alt": 387.3, "ec": 1, "v": 4.957}, {"lat": -50.85, "lon": -101.19, "alt": 400.2, "ec": 1, "v": 4.965}, {"lat": -48.36, "lon": -62.48, "alt": 399.8, "ec": 1, "v": 4.958}, {"lat": -18.85, "lon": -18.33, "alt": 397.1, "ec": 1, "v": 4.957}, {"lat": -36.7, "lon": -60.62, "alt": 398.9, "ec": 1, "v": 4.96}, {"lat": -44.08, "lon": -97.14, "alt": 399.5, "ec": 1, "v": 4.97}, {"lat": 47.75, "lon": 61.1, "alt": 387.3, "ec": 1, "v": 4.967}, {"lat": 20.74, "lon": 101.47, "alt": 392.2, "ec": 1, "v": 4.964}, {"lat": -47.97, "lon": 173.99, "alt": 400.2, "ec": 1, "v": 4.955}, {"lat": 38.38, "lon": 11.39, "alt": 388.9, "ec": 0, "v": 4.989}, {"lat": -15.22, "lon": 133.58, "alt": 396.6, "ec": 1, "v": 4.983}, {"lat": -3.6, "lon": 118.76, "alt": 395.0, "ec": 1, "v": 4.971}, {"lat": -33.7, "lon": 68.92, "alt": 398.5, "ec": 0, "v": 4.959}, {"lat": -50.72, "lon": 4.15, "alt": 399.9, "ec": 1, "v": 4.954}, {"lat": 14.11, "lon": 84.72, "alt": 392.2, "ec": 1, "v": 4.953}, {"lat": 32.68, "lon": 102.12, "alt": 389.0, "ec": 1, "v": 4.952}, {"lat": 34.24, "lon": -146.92, "alt": 389.6, "ec": 1, "v": 4.956}, {"lat": -50.93, "lon": -20.99, "alt": 400.0, "ec": 1, "v": 4.954}, {"lat": 41.94, "lon": 92.53, "alt": 387.6, "ec": 1, "v": 4.952}, {"lat": -23.6, "lon": -122.5, "alt": 398.5, "ec": 1, "v": 4.955}, {"lat": -2.03, "lon": 26.09, "alt": 394.7, "ec": 1, "v": 4.954}, {"lat": 31.08, "lon": 169.99, "alt": 390.2, "ec": 1, "v": 4.954}, {"lat": -50.58, "lon": -65.15, "alt": 399.9, "ec": 1, "v": 4.948}, {"lat": 42.04, "lon": 45.83, "alt": 387.5, "ec": 1, "v": 4.951}, {"lat": -36.88, "lon": -52.56, "alt": 398.8, "ec": 0, "v": 4.973}, {"lat": 8.19, "lon": -60.39, "alt": 393.1, "ec": 0, "v": 4.951}, {"lat": 47.86, "lon": -56.71, "alt": 386.7, "ec": 0, "v": 4.951}, {"lat": -0.16, "lon": 31.82, "alt": 395.5, "ec": 1, "v": 4.955}, {"lat": 46.69, "lon": -44.47, "alt": 387.3, "ec": 1, "v": 4.962}, {"lat": 2.94, "lon": 178.61, "alt": 393.9, "ec": 1, "v": 4.963}, {"lat": -49.51, "lon": 47.93, "alt": 400.0, "ec": 1, "v": 4.971}, {"lat": -20.45, "lon": 137.62, "alt": 397.1, "ec": 1, "v": 4.965}, {"lat": -0.85, "lon": 152.47, "alt": 394.5, "ec": 1, "v": 4.964}, {"lat": -24.74, "lon": -19.33, "alt": 398.5, "ec": 1, "v": 4.97}, {"lat": 39.68, "lon": -99.6, "alt": 388.5, "ec": 0, "v": 4.958}, {"lat": -42.42, "lon": -43.03, "alt": 399.8, "ec": 1, "v": 4.958}, {"lat": 14.5, "lon": 69.9, "alt": 392.0, "ec": 1, "v": 4.952}, {"lat": 33.28, "lon": 175.72, "alt": 389.6, "ec": 1, "v": 4.949}, {"lat": -10.34, "lon": -171.86, "alt": 396.9, "ec": 1, "v": 4.949}, {"lat": 38.12, "lon": 23.99, "alt": 388.0, "ec": 1, "v": 4.95}, {"lat": -42.61, "lon": -159.88, "alt": 399.7, "ec": 1, "v": 4.952}, {"lat": 51.04, "lon": 38.45, "alt": 386.2, "ec": 1, "v": 4.957}, {"lat": -51.27, "lon": -150.73, "alt": 400.0, "ec": 1, "v": 4.954}, {"lat": 49.03, "lon": 49.41, "alt": 386.7, "ec": 1, "v": 4.957}, {"lat": -46.14, "lon": -132.53, "alt": 399.4, "ec": 1, "v": 4.964}, {"lat": 49.56, "lon": 23.55, "alt": 386.6, "ec": 1, "v": 4.965}, {"lat": -51.61, "lon": 169.65, "alt": 399.9, "ec": 1, "v": 4.964}, {"lat": 12.41, "lon": 54.47, "alt": 393.3, "ec": 1, "v": 4.961}, {"lat": 40.27, "lon": -89.74, "alt": 387.6, "ec": 1, "v": 4.965}, {"lat": -39.03, "lon": 171.83, "alt": 398.9, "ec": 1, "v": 4.95}, {"lat": -12.06, "lon": 25.31, "alt": 397.0, "ec": 1, "v": 4.946}, {"lat": 51.14, "lon": -101.16, "alt": 386.2, "ec": 1, "v": 4.951}, {"lat": -33.57, "lon": 132.61, "alt": 398.4, "ec": 1, "v": 4.947}, {"lat": -18.23, "lon": -16.72, "alt": 397.7, "ec": 1, "v": 4.947}, {"lat": 51.62, "lon": -137.32, "alt": 386.2, "ec": 0, "v": 4.957}, {"lat": -12.81, "lon": 105.2, "alt": 396.1, "ec": 1, "v": 4.949}, {"lat": 41.95, "lon": 156.09, "alt": 387.4, "ec": 1, "v": 4.951}, {"lat": 51.3, "lon": -169.67, "alt": 386.1, "ec": 1, "v": 4.953}, {"lat": 40.34, "lon": -115.85, "alt": 388.2, "ec": 1, "v": 4.952}, {"lat": -34.28, "lon": -47.52, "alt": 399.1, "ec": 1, "v": 4.953}, {"lat": 21.75, "lon": -117.22, "alt": 391.6, "ec": 1, "v": 4.95}, {"lat": 19.24, "lon": 82.05, "alt": 391.1, "ec": 0, "v": 4.958}, {"lat": -51.59, "lon": -37.5, "alt": 399.8, "ec": 1, "v": 4.956}, {"lat": 15.68, "lon": -159.06, "alt": 392.7, "ec": 1, "v": 4.962}, {"lat": 38.0, "lon": 55.59, "alt": 387.9, "ec": 1, "v": 4.964}, {"lat": -47.88, "lon": -59.22, "alt": 399.5, "ec": 1, "v": 4.96}, {"lat": 27.7, "lon": 143.38, "alt": 390.4, "ec": 1, "v": 4.962}, {"lat": -51.47, "lon": -115.94, "alt": 399.8, "ec": 1, "v": 4.958}, {"lat": -43.47, "lon": -70.81, "alt": 399.1, "ec": 1, "v": 4.957}, {"lat": -7.03, "lon": -31.18, "alt": 395.3, "ec": 1, "v": 4.941}, {"lat": 7.17, "lon": -91.37, "alt": 393.1, "ec": 1, "v": 4.949}, {"lat": 50.3, "lon": -19.03, "alt": 386.3, "ec": 1, "v": 4.949}, {"lat": 44.66, "lon": -96.03, "alt": 386.9, "ec": 0, "v": 4.947}, {"lat": 7.25, "lon": -161.64, "alt": 393.0, "ec": 1, "v": 4.956}, {"lat": -27.51, "lon": 147.73, "alt": 397.7, "ec": 1, "v": 4.952}, {"lat": -45.97, "lon": 95.61, "alt": 399.3, "ec": 1, "v": 4.958}, {"lat": -25.0, "lon": 103.31, "alt": 397.4, "ec": 0, "v": 4.959}, {"lat": 30.42, "lon": 124.5, "alt": 389.1, "ec": 1, "v": 4.952}, {"lat": 46.41, "lon": -167.64, "alt": 387.0, "ec": 1, "v": 4.946}, {"lat": -16.06, "lon": -127.36, "alt": 397.2, "ec": 1, "v": 4.951}, {"lat": -3.37, "lon": 3.24, "alt": 394.6, "ec": 1, "v": 4.946}, {"lat": 2.99, "lon": -39.13, "alt": 393.6, "ec": 1, "v": 4.953}, {"lat": 44.07, "lon": 57.6, "alt": 387.3, "ec": 1, "v": 4.957}, {"lat": 43.89, "lon": -42.56, "alt": 386.8, "ec": 1, "v": 4.957}, {"lat": 51.62, "lon": -28.54, "alt": 385.9, "ec": 1, "v": 4.959}, {"lat": 49.4, "lon": -29.35, "alt": 386.3, "ec": 1, "v": 4.956}, {"lat": 48.31, "lon": -48.26, "alt": 386.5, "ec": 1, "v": 4.952}, {"lat": -2.12, "lon": -12.11, "alt": 395.3, "ec": 0, "v": 4.946}, {"lat": 7.47, "lon": 136.54, "alt": 392.8, "ec": 0, "v": 4.942}, {"lat": -12.95, "lon": -97.98, "alt": 396.6, "ec": 1, "v": 4.948}, {"lat": -48.41, "lon": -44.45, "alt": 399.3, "ec": 1, "v": 4.957}, {"lat": 16.11, "lon": -21.02, "alt": 391.5, "ec": 1, "v": 4.957}, {"lat": 29.56, "lon": 64.35, "alt": 389.6, "ec": 1, "v": 4.95}, {"lat": -24.19, "lon": -145.46, "alt": 397.3, "ec": 1, "v": 4.943}, {"lat": -1.24, "lon": -127.55, "alt": 394.3, "ec": 1, "v": 4.946}, {"lat": 19.71, "lon": -111.85, "alt": 390.8, "ec": 1, "v": 4.947}, {"lat": 6.94, "lon": 36.67, "alt": 393.6, "ec": 1, "v": 4.947}, {"lat": 11.45, "lon": -165.27, "alt": 392.1, "ec": 0, "v": 4.948}, {"lat": -42.38, "lon": 97.15, "alt": 398.7, "ec": 1, "v": 4.954}, {"lat": 7.3, "lon": -57.36, "alt": 393.6, "ec": 1, "v": 4.956}, {"lat": -16.41, "lon": -40.03, "alt": 397.0, "ec": 1, "v": 4.959}, {"lat": -37.22, "lon": -18.45, "alt": 398.8, "ec": 1, "v": 4.964}, {"lat": 48.36, "lon": 174.37, "alt": 386.0, "ec": 1, "v": 4.955}, {"lat": 49.56, "lon": 156.04, "alt": 385.8, "ec": 0, "v": 4.922}, {"lat": 38.06, "lon": -133.97, "alt": 388.1, "ec": 0, "v": 4.926}, {"lat": 0.82, "lon": -99.61, "alt": 394.6, "ec": 0, "v": 4.926}, {"lat": -38.32, "lon": -63.68, "alt": 398.9, "ec": 1, "v": 4.927}, {"lat": -48.16, "lon": 11.72, "alt": 399.1, "ec": 1, "v": 4.925}, {"lat": -11.56, "lon": 60.88, "alt": 395.5, "ec": 0, "v": 4.926}, {"lat": 34.17, "lon": 98.77, "alt": 388.1, "ec": 0, "v": 4.926}, {"lat": 47.33, "lon": -177.16, "alt": 386.5, "ec": 0, "v": 4.924}, {"lat": -1.52, "lon": -121.39, "alt": 395.0, "ec": 0, "v": 4.925}, {"lat": 28.87, "lon": -178.49, "alt": 388.4, "ec": 0, "v": 4.926}, {"lat": 32.24, "lon": -60.79, "alt": 388.5, "ec": 0, "v": 4.923}, {"lat": 10.66, "lon": 142.34, "alt": 391.6, "ec": 0, "v": 4.929}, {"lat": -19.0, "lon": 101.77, "alt": 395.1, "ec": 0, "v": 4.925}, {"lat": -12.65, "lon": 128.1, "alt": 389.9, "ec": 0, "v": 4.925}, {"lat": 27.39, "lon": 159.18, "alt": 383.1, "ec": 1, "v": 4.926}, {"lat": 51.59, "lon": -141.4, "alt": 379.0, "ec": 1, "v": 4.926}, {"lat": 19.55, "lon": -69.09, "alt": 384.8, "ec": 0, "v": 4.925}, {"lat": -33.64, "lon": -25.53, "alt": 392.5, "ec": 0, "v": 4.924}, {"lat": -50.75, "lon": 43.37, "alt": 393.6, "ec": 0, "v": 4.925}, {"lat": -7.42, "lon": 108.57, "alt": 389.1, "ec": 0, "v": 4.934}, {"lat": -2.06, "lon": 26.13, "alt": 388.5, "ec": 0, "v": 4.927}, {"lat": -23.07, "lon": 42.43, "alt": 391.3, "ec": 0, "v": 4.926}, {"lat": -40.92, "lon": 64.33, "alt": 392.9, "ec": 0, "v": 4.925}, {"lat": -51.23, "lon": 99.56, "alt": 393.5, "ec": 0, "v": 4.926}, {"lat": -46.65, "lon": 140.35, "alt": 393.2, "ec": 0, "v": 4.93}, {"lat": 0.12, "lon": -166.96, "alt": 387.9, "ec": 1, "v": 4.929}, {"lat": 37.23, "lon": -55.87, "alt": 381.3, "ec": 0, "v": 4.928}, {"lat": 17.92, "lon": -35.49, "alt": 384.9, "ec": 0, "v": 4.924}, {"lat": -2.84, "lon": -20.14, "alt": 388.5, "ec": 0, "v": 4.933}, {"lat": -50.36, "lon": 22.23, "alt": 393.4, "ec": 0, "v": 4.922}, {"lat": 46.23, "lon": -120.36, "alt": 379.7, "ec": 1, "v": 4.926}, {"lat": -23.82, "lon": 80.86, "alt": 391.2, "ec": 0, "v": 4.929}, {"lat": 48.68, "lon": 158.8, "alt": 379.3, "ec": 1, "v": 4.926}, {"lat": -2.22, "lon": -90.8, "alt": 388.4, "ec": 0, "v": 4.927}, {"lat": -47.63, "lon": 20.24, "alt": 393.2, "ec": 0, "v": 4.93}, {"lat": 1.03, "lon": -139.93, "alt": 387.8, "ec": 0, "v": 4.922}, {"lat": 51.56, "lon": -106.98, "alt": 376.8, "ec": 1, "v": 4.928}, {"lat": 42.01, "lon": -120.78, "alt": 378.8, "ec": 0, "v": 4.923}, {"lat": 42.71, "lon": -63.56, "alt": 378.5, "ec": 0, "v": 4.925}, {"lat": -34.27, "lon": 24.24, "alt": 381.7, "ec": 1, "v": 4.928}, {"lat": -49.78, "lon": -75.3, "alt": 380.9, "ec": 1, "v": 4.926}, {"lat": 45.36, "lon": -117.46, "alt": 369.4, "ec": 0, "v": 4.93}, {"lat": 25.21, "lon": -153.56, "alt": 364.5, "ec": 1, "v": 4.929}, {"lat": 51.29, "lon": -47.14, "alt": 362.0, "ec": 1, "v": 4.928}, {"lat": 43.14, "lon": -165.86, "alt": 361.8, "ec": 1, "v": 4.93}, {"lat": -45.15, "lon": 79.87, "alt": 374.3, "ec": 0, "v": 4.926}, {"lat": -29.28, "lon": 104.57, "alt": 372.3, "ec": 0, "v": 4.924}, {"lat": -9.22, "lon": 121.82, "alt": 369.1, "ec": 0, "v": 4.926}, {"lat": 12.77, "lon": 137.71, "alt": 364.9, "ec": 0, "v": 4.926}, {"lat": 31.95, "lon": 155.29, "alt": 361.1, "ec": 0, "v": 4.931}, {"lat": 47.45, "lon": -176.46, "alt": 358.6, "ec": 1, "v": 4.927}, {"lat": -10.41, "lon": -172.26, "alt": 371.4, "ec": 1, "v": 4.931}, {"lat": -51.62, "lon": -95.99, "alt": 375.2, "ec": 0, "v": 4.924}, {"lat": -48.61, "lon": -143.85, "alt": 375.2, "ec": 0, "v": 4.926}, {"lat": 22.89, "lon": -87.08, "alt": 362.8, "ec": 0, "v": 4.924}, {"lat": 51.17, "lon": -30.44, "alt": 358.0, "ec": 1, "v": 4.926}, {"lat": 32.55, "lon": 36.13, "alt": 362.4, "ec": 1, "v": 4.925}, {"lat": -8.11, "lon": 69.48, "alt": 370.9, "ec": 1, "v": 4.926}, {"lat": -44.71, "lon": 111.16, "alt": 375.0, "ec": 0, "v": 4.925}, {"lat": -43.47, "lon": -172.67, "alt": 374.0, "ec": 0, "v": 4.925}, {"lat": -6.06, "lon": -132.32, "alt": 368.4, "ec": 0, "v": 4.929}, {"lat": 35.19, "lon": -97.12, "alt": 360.4, "ec": 0, "v": 4.927}, {"lat": 50.86, "lon": -31.06, "alt": 358.3, "ec": 1, "v": 4.924}, {"lat": -37.77, "lon": -9.01, "alt": 368.3, "ec": 1, "v": 4.926}, {"lat": 31.82, "lon": -95.49, "alt": 355.6, "ec": 0, "v": 4.934}, {"lat": 43.19, "lon": -107.88, "alt": 353.4, "ec": 0, "v": 4.927}, {"lat": 25.92, "lon": -84.23, "alt": 355.4, "ec": 0, "v": 4.93}, {"lat": 44.91, "lon": -118.67, "alt": 351.2, "ec": 1, "v": 4.923}, {"lat": 25.61, "lon": -111.45, "alt": 354.2, "ec": 0, "v": 4.926}, {"lat": 43.16, "lon": -88.19, "alt": 351.0, "ec": 1, "v": 4.928}, {"lat": 48.36, "lon": -88.55, "alt": 346.7, "ec": 1, "v": 4.926}, {"lat": 45.1, "lon": -121.97, "alt": 346.2, "ec": 1, "v": 4.93}, {"lat": 18.7, "lon": 30.19, "alt": 350.3, "ec": 1, "v": 4.925}, {"lat": 43.12, "lon": -126.74, "alt": 345.7, "ec": 1, "v": 4.926}, {"lat": 2.5, "lon": -73.76, "alt": 352.6, "ec": 1, "v": 4.929}, {"lat": 30.67, "lon": -40.84, "alt": 347.3, "ec": 0, "v": 4.931}, {"lat": 51.6, "lon": -100.45, "alt": 344.2, "ec": 1, "v": 4.932}, {"lat": 45.24, "lon": 110.28, "alt": 344.8, "ec": 1, "v": 4.927}, {"lat": -25.13, "lon": 179.86, "alt": 354.9, "ec": 0, "v": 4.926}, {"lat": -32.42, "lon": 68.87, "alt": 354.7, "ec": 0, "v": 4.926}, {"lat": -49.24, "lon": -104.99, "alt": 355.5, "ec": 0, "v": 4.926}, {"lat": 7.15, "lon": -177.33, "alt": 350.0, "ec": 0, "v": 4.928}, {"lat": -39.84, "lon": -22.68, "alt": 355.1, "ec": 0, "v": 4.928}, {"lat": 45.23, "lon": -97.63, "alt": 343.8, "ec": 1, "v": 4.927}, {"lat": -51.54, "lon": -108.21, "alt": 354.9, "ec": 0, "v": 4.929}, {"lat": 50.29, "lon": -113.79, "alt": 339.7, "ec": 0, "v": 4.926}, {"lat": 51.09, "lon": -125.2, "alt": 336.5, "ec": 0, "v": 4.925}, {"lat": -42.39, "lon": 54.62, "alt": 337.9, "ec": 0, "v": 4.928}, {"lat": 23.57, "lon": -98.6, "alt": 330.2, "ec": 0, "v": 4.922}, {"lat": 48.23, "lon": 142.43, "alt": 323.5, "ec": 0, "v": 4.923}, {"lat": -23.38, "lon": -41.33, "alt": 331.2, "ec": 0, "v": 4.927}, {"lat": -40.99, "lon": -19.57, "alt": 332.9, "ec": 0, "v": 4.925}, {"lat": -51.29, "lon": 16.3, "alt": 333.2, "ec": 0, "v": 4.927}, {"lat": -46.85, "lon": 55.81, "alt": 332.3, "ec": 0, "v": 4.923}, {"lat": -30.83, "lon": 83.45, "alt": 330.3, "ec": 0, "v": 4.928}, {"lat": -11.26, "lon": 100.89, "alt": 327.2, "ec": 0, "v": 4.923}, {"lat": 9.4, "lon": 115.79, "alt": 323.3, "ec": 0, "v": 4.926}, {"lat": 29.67, "lon": 133.34, "alt": 319.1, "ec": 1, "v": 4.93}, {"lat": 46.12, "lon": 160.17, "alt": 316.2, "ec": 1, "v": 4.928}, {"lat": 51.45, "lon": -160.58, "alt": 315.7, "ec": 1, "v": 4.928}, {"lat": 39.89, "lon": -120.43, "alt": 318.5, "ec": 1, "v": 4.928}, {"lat": 20.93, "lon": -98.38, "alt": 322.9, "ec": 1, "v": 4.928}, {"lat": -0.0, "lon": -82.5, "alt": 327.3, "ec": 0, "v": 4.932}, {"lat": -20.9, "lon": -66.63, "alt": 330.8, "ec": 0, "v": 4.929}, {"lat": -39.82, "lon": -44.7, "alt": 332.7, "ec": 0, "v": 4.924}, {"lat": -51.11, "lon": -8.86, "alt": 333.2, "ec": 0, "v": 4.921}, {"lat": -47.14, "lon": 31.82, "alt": 332.3, "ec": 0, "v": 4.927}, {"lat": -31.9, "lon": 59.12, "alt": 330.4, "ec": 0, "v": 4.928}, {"lat": -11.44, "lon": 77.65, "alt": 327.3, "ec": 0, "v": 4.927}, {"lat": 9.72, "lon": 92.94, "alt": 323.2, "ec": 0, "v": 4.929}, {"lat": -48.62, "lon": -167.47, "alt": 322.0, "ec": 0, "v": 4.923}, {"lat": 25.04, "lon": -88.53, "alt": 313.2, "ec": 0, "v": 4.93}, {"lat": 31.17, "lon": 34.36, "alt": 308.4, "ec": 1, "v": 4.927}, {"lat": -45.12, "lon": 108.87, "alt": 320.2, "ec": 1, "v": 4.925}, {"lat": -47.72, "lon": 11.46, "alt": 321.3, "ec": 0, "v": 4.926}, {"lat": -25.28, "lon": 47.63, "alt": 320.6, "ec": 0, "v": 4.923}, {"lat": 12.97, "lon": 76.91, "alt": 315.2, "ec": 0, "v": 4.923}, {"lat": 36.35, "lon": 99.97, "alt": 310.2, "ec": 0, "v": 4.931}, {"lat": 50.95, "lon": 139.69, "alt": 306.5, "ec": 0, "v": 4.923}, {"lat": -25.13, "lon": -21.37, "alt": 320.3, "ec": 0, "v": 4.925}, {"lat": -3.41, "lon": -4.09, "alt": 317.8, "ec": 0, "v": 4.929}, {"lat": 17.69, "lon": 11.5, "alt": 314.0, "ec": 0, "v": 4.925}, {"lat": 43.08, "lon": 42.22, "alt": 308.4, "ec": 0, "v": 4.928}, {"lat": 51.56, "lon": 86.36, "alt": 305.8, "ec": 0, "v": 4.926}, {"lat": -39.87, "lon": -131.72, "alt": 320.7, "ec": 0, "v": 4.926}, {"lat": 22.0, "lon": -77.0, "alt": 312.9, "ec": 0, "v": 4.925}, {"lat": 47.39, "lon": 19.72, "alt": 305.5, "ec": 1, "v": 4.925}, {"lat": -10.65, "lon": 82.34, "alt": 313.9, "ec": 1, "v": 4.928}, {"lat": -51.35, "lon": 166.61, "alt": 320.2, "ec": 0, "v": 4.921}, {"lat": 32.95, "lon": -88.82, "alt": 310.5, "ec": 0, "v": 4.926}, {"lat": 51.26, "lon": -89.55, "alt": 295.4, "ec": 0, "v": 4.929}], "csim": [{"wl": 210.0, "ir": 0.0243}, {"wl": 212.0, "ir": 0.0364}, {"wl": 213.0, "ir": 0.0288}, {"wl": 215.0, "ir": 0.038}, {"wl": 217.0, "ir": 0.0288}, {"wl": 219.0, "ir": 0.039}, {"wl": 221.0, "ir": 0.0431}, {"wl": 223.0, "ir": 0.0487}, {"wl": 225.0, "ir": 0.0611}, {"wl": 227.0, "ir": 0.0296}, {"wl": 229.0, "ir": 0.0466}, {"wl": 232.0, "ir": 0.0489}, {"wl": 234.0, "ir": 0.0321}, {"wl": 237.0, "ir": 0.0502}, {"wl": 240.0, "ir": 0.0386}, {"wl": 243.0, "ir": 0.067}, {"wl": 246.0, "ir": 0.0457}, {"wl": 250.0, "ir": 0.0595}, {"wl": 253.0, "ir": 0.0427}, {"wl": 257.0, "ir": 0.1043}, {"wl": 260.0, "ir": 0.0847}, {"wl": 264.0, "ir": 0.2489}, {"wl": 269.0, "ir": 0.2461}, {"wl": 273.0, "ir": 0.2058}, {"wl": 278.0, "ir": 0.18}, {"wl": 283.0, "ir": 0.322}, {"wl": 289.0, "ir": 0.386}, {"wl": 295.0, "ir": 0.5221}, {"wl": 301.0, "ir": 0.446}, {"wl": 308.0, "ir": 0.626}, {"wl": 316.0, "ir": 0.6391}, {"wl": 324.0, "ir": 0.7484}, {"wl": 333.0, "ir": 0.9575}, {"wl": 343.0, "ir": 0.9568}, {"wl": 354.0, "ir": 1.0866}, {"wl": 367.0, "ir": 1.2117}, {"wl": 380.0, "ir": 1.1615}, {"wl": 396.0, "ir": 1.0739}, {"wl": 414.0, "ir": 1.8144}, {"wl": 435.0, "ir": 1.7606}, {"wl": 460.0, "ir": 2.0918}, {"wl": 489.0, "ir": 1.9603}, {"wl": 525.0, "ir": 1.9056}, {"wl": 570.0, "ir": 1.8607}, {"wl": 627.0, "ir": 1.6644}, {"wl": 701.0, "ir": 1.4194}, {"wl": 799.0, "ir": 1.1453}, {"wl": 933.0, "ir": 0.8315}, {"wl": 1087.0, "ir": 0.6005}, {"wl": 1257.0, "ir": 0.436}, {"wl": 1429.0, "ir": 0.3232}, {"wl": 1598.0, "ir": 0.2413}, {"wl": 1765.0, "ir": 0.177}, {"wl": 1921.0, "ir": 0.1331}, {"wl": 2066.0, "ir": 0.1041}, {"wl": 2202.0, "ir": 0.0824}, {"wl": 2330.0, "ir": 0.0665}, {"wl": 2450.0, "ir": 0.0548}, {"wl": 2564.0, "ir": 0.0482}]};
const ML_W       = MLDATA.weights;
const SAT_CURVES = MLDATA.sat_curves;
const CSIM       = MLDATA.csim;

// ════════════════════════════════════════════════
// STARFIELD
// ════════════════════════════════════════════════
(function(){
  const sf = document.getElementById('sf');
  for(let i=0;i<150;i++){
    const d=document.createElement('div'); d.className='st';
    const s=(Math.random()*1.5+0.3).toFixed(1);
    d.style.cssText=`width:${s}px;height:${s}px;left:${(Math.random()*100).toFixed(1)}%;top:${(Math.random()*100).toFixed(1)}%;--a0:${(Math.random()*.25+.05).toFixed(2)};--a1:${(Math.random()*.45+.25).toFixed(2)};--d:${(Math.random()*3+2).toFixed(1)}s;animation-delay:${(Math.random()*5).toFixed(1)}s`;
    sf.appendChild(d);
  }
})();

// ════════════════════════════════════════════════
// ML INFERENCE  — 4→12→6→1  ReLU
// Features: [cos_theta, temp_efficiency, vbat_norm, cycle_phase]
//   cos_theta    : 1.0 for ML (perfect tracking), cos(nadir_incidence) for nadir mode
//   temp_efficiency : max(0.5, 1 - 0.004*max(0, T-25))
//   vbat_norm    : (vbat - 3.8) / 0.5
//   cycle_phase  : orbital angle / 2π  →  0..1
// ════════════════════════════════════════════════
function mlInfer(cosT, tEf, vbat, phi){
  let a = [ cosT, tEf, (vbat-3.8)/0.5, phi ];
  const C=ML_W.coefs, B=ML_W.intercepts;
  for(let L=0;L<C.length;L++){
    const W=C[L],b=B[L],o=new Array(b.length);
    for(let j=0;j<b.length;j++){
      let s=b[j]; for(let i=0;i<a.length;i++) s+=a[i]*W[i][j];
      o[j]=(L<C.length-1)?(s>0?s:0):s;
    }
    a=o;
  }
  return a[0]>0?a[0]:0;
}

// ════════════════════════════════════════════════
// ORBITAL CANVAS
// ════════════════════════════════════════════════
const CV=document.getElementById('sim');
const CTX=CV.getContext('2d');
// All layout variables — set by resizeSim()
let W=0,H=0,CX=0,CY=0,ER=0,OR=0,SX=0,SY=0;

function resizeSim(){
  const wrap=document.getElementById('cw');
  const dpr=window.devicePixelRatio||1;
  const dw=wrap.clientWidth||600;
  const dh=Math.round(dw*0.46);
  CV.width=dw*dpr; CV.height=dh*dpr;
  CV.style.width=dw+'px'; CV.style.height=dh+'px';
  CTX.setTransform(dpr,0,0,dpr,0,0);
  W=dw; H=dh;
  CX=W*0.37; CY=H*0.5;
  ER=Math.min(W,H)*0.125;
  OR=ER*2.4;
  SX=W*0.94; SY=H*0.5;
}
resizeSim();

// ════════════════════════════════════════════════
// SIM STATE
// ════════════════════════════════════════════════
let ANG=-Math.PI/2;   // satellite orbital angle
let BAT=1.0;           // battery 0-1, start full
let eML=0, eNad=0;     // cumulative energy
let SPEED=1;
let LAST=null;
let ML_ON=true;        // true=ML tracking, false=sensor ADCS
let activeParam='pw';  // parameter shown in BIRDS chart

// Sensor ADCS state
// Realistic CubeSat magnetic torquer ADCS:
//   CSS noise ±8° (cheap coarse sun sensors)
//   Slew rate 3°/s  (magnetic torquers, slow)
//   Deadband ±5°    (control hysteresis)
//   Re-acq delay 6s after eclipse exit
const CSS_NOISE  = 20 * Math.PI/180;  // ±20° coarse sun sensor noise
const SLEW_RATE  = 1.2 * Math.PI/180;  // 1.2°/s magnetic torquer (slow!)
const DEADBAND   = 8  * Math.PI/180;   // ±8° deadband
const REACQ_TIME = 8.0;               // 8s re-acquisition after eclipse
let sensorAng = -Math.PI/2;           // sensor-estimated sun angle
let reacqTimer = 0;
let adcsState  = 'TRACKING';          // TRACKING | SLEWING | DEADBAND | RE-ACQ

// Rolling history for mini-charts (NOT resized every frame)
const NH=180;
const mlBuf  = new Float32Array(NH);
const nadBuf = new Float32Array(NH);
const batBuf = new Float32Array(NH).fill(1.0);
const tmpBuf = new Float32Array(NH).fill(25);   // panel temperature °C
const curBuf = new Float32Array(NH).fill(0);    // panel current mA
// For running averages (used in sidebar stats)
let sunFrames=0, totalFrames=0;
let sumML=0, sumNad=0;
let hI=0,bI=0;

const SPD0=(2*Math.PI)/20;  // one orbit per 20 real-seconds at 1×

// Starfield dots for canvas background
const SDOTS=Array.from({length:200},()=>({
  x:Math.random(),y:Math.random(),
  r:Math.random()*1.1+0.25,
  a:Math.random()*.4+.1
}));

// ════════════════════════════════════════════════
// PHYSICS HELPERS
// ════════════════════════════════════════════════
function isEcl(a){ return Math.cos(a) < -(ER/OR); }
function getT(a,ecl){ return ecl ? -5+Math.sin(a)*8 : 25+Math.cos(a)*18; }
function tEff(T){ return Math.max(0.5, 1-0.004*Math.max(0,T-25)); }
function phi(a){ return (((a%(2*Math.PI))+(2*Math.PI))%(2*Math.PI))/(2*Math.PI); }

// True sun direction angle as seen from satellite
function sunDir(a){
  const sx=CX+Math.cos(a)*OR, sy=CY+Math.sin(a)*OR;
  return Math.atan2(SY-sy,SX-sx);
}

// ── Sensor ADCS simulation ──────────────────────
// Models a realistic CubeSat with coarse sun sensors + magnetic torquers
// CSS = coarse sun sensor (noisy), MTQ = magnetic torquer rods (slow)
function stepADCS(dt, ecl){
  if(ecl){
    // Eclipse: sensors blind, spin to nadir as fallback
    reacqTimer = REACQ_TIME;
    adcsState  = 'RE-ACQ';
    // Slowly drift toward a fixed angle
    let diff = 0 - sensorAng;
    while(diff>Math.PI)diff-=2*Math.PI; while(diff<-Math.PI)diff+=2*Math.PI;
    sensorAng += Math.sign(diff)*Math.min(Math.abs(diff), SLEW_RATE*dt);
    return;
  }
  if(reacqTimer > 0){
    // Just exited eclipse — re-acquiring sun, large angle error likely
    reacqTimer -= dt;
    adcsState   = 'RE-ACQ';
    // Sensor sees sun + large noise during re-acquisition
    const trueSun = sunDir(ANG);
    const noisyMeas = trueSun + CSS_NOISE*(Math.random()*2-1)*2.5; // extra noisy
    let err = noisyMeas - sensorAng;
    while(err>Math.PI)err-=2*Math.PI; while(err<-Math.PI)err+=2*Math.PI;
    sensorAng += Math.sign(err)*Math.min(Math.abs(err), SLEW_RATE*dt);
    return;
  }
  // Normal operation: CSS measurement with noise
  const trueSun   = sunDir(ANG);
  const noisyMeas = trueSun + CSS_NOISE*(Math.random()*2-1);
  let err = noisyMeas - sensorAng;
  while(err>Math.PI)err-=2*Math.PI; while(err<-Math.PI)err+=2*Math.PI;
  const errDeg = Math.abs(err)*180/Math.PI;
  if(errDeg < DEADBAND*180/Math.PI){
    adcsState = 'DEADBAND';  // within dead zone, no actuation
    return;
  }
  adcsState = 'SLEWING';
  sensorAng += Math.sign(err)*Math.min(Math.abs(err), SLEW_RATE*dt);
}

// Incidence angle for sensor ADCS: angle between sensor-pointed direction and true sun
function sensorIncidence(){
  const trueSun = sunDir(ANG);
  // Panel normal faces sensorAng direction
  let inc = trueSun - sensorAng;
  while(inc>Math.PI)inc-=2*Math.PI; while(inc<-Math.PI)inc+=2*Math.PI;
  return inc;
}

// ════════════════════════════════════════════════
// DRAW FUNCTIONS
// ════════════════════════════════════════════════
function drawBg(){
  CTX.fillStyle='#02030e'; CTX.fillRect(0,0,W,H);
  SDOTS.forEach(s=>{
    CTX.beginPath(); CTX.arc(s.x*W,s.y*H,s.r,0,Math.PI*2);
    CTX.fillStyle=`rgba(200,220,255,${s.a})`; CTX.fill();
  });
}

function drawSun(t){
  const p=1+Math.sin(t*1.3)*.025;
  [[125,.012],[88,.027],[60,.058],[38,.13],[22,.72]].forEach(([r,a])=>{
    CTX.beginPath(); CTX.arc(SX,SY,r*p,0,Math.PI*2);
    CTX.fillStyle=`rgba(255,210,50,${a})`; CTX.fill();
  });
  CTX.beginPath(); CTX.arc(SX,SY,16*p,0,Math.PI*2);
  CTX.fillStyle='#fffcee'; CTX.fill();
  CTX.font=Math.round(W*.01)+'px sans-serif';
  CTX.fillStyle='rgba(255,195,50,.5)'; CTX.textAlign='center';
  CTX.fillText('SUN',SX,SY+29);
}

function drawEclShadow(){
  const len=W*.5;
  const g=CTX.createLinearGradient(CX,0,CX-len,0);
  g.addColorStop(0,'rgba(0,1,14,.93)'); g.addColorStop(.5,'rgba(0,1,14,.5)'); g.addColorStop(1,'rgba(0,1,14,0)');
  CTX.save(); CTX.beginPath();
  CTX.moveTo(CX,CY-ER); CTX.lineTo(CX-len,CY-ER*1.5);
  CTX.lineTo(CX-len,CY+ER*1.5); CTX.lineTo(CX,CY+ER);
  CTX.closePath(); CTX.fillStyle=g; CTX.fill(); CTX.restore();
  CTX.font=Math.round(W*.009)+'px sans-serif';
  CTX.fillStyle='rgba(55,100,150,.38)'; CTX.textAlign='center';
  CTX.fillText('eclipse zone',CX-OR*.53,CY+ER+15);
}

function drawOrbit(){
  CTX.save(); CTX.beginPath(); CTX.arc(CX,CY,OR,0,Math.PI*2);
  CTX.strokeStyle='rgba(79,130,200,.16)'; CTX.lineWidth=.8;
  CTX.setLineDash([4,10]); CTX.stroke(); CTX.setLineDash([]); CTX.restore();
}

function drawEarth(){
  const ag=CTX.createRadialGradient(CX,CY,ER,CX,CY,ER+26);
  ag.addColorStop(0,'rgba(40,100,220,.34)'); ag.addColorStop(1,'rgba(10,30,100,0)');
  CTX.beginPath(); CTX.arc(CX,CY,ER+26,0,Math.PI*2); CTX.fillStyle=ag; CTX.fill();
  const eg=CTX.createRadialGradient(CX-ER*.2,CY-ER*.2,0,CX,CY,ER);
  eg.addColorStop(0,'#1a5298'); eg.addColorStop(1,'#0d2f5e');
  CTX.beginPath(); CTX.arc(CX,CY,ER,0,Math.PI*2); CTX.fillStyle=eg; CTX.fill();
  CTX.save(); CTX.beginPath(); CTX.arc(CX,CY,ER,0,Math.PI*2); CTX.clip();
  CTX.fillStyle='rgba(28,108,50,.52)';
  [[-.22,-.21,.27,.18],[.27,.1,.2,.25],[-.32,.27,.16,.12],[.09,-.37,.11,.1]]
    .forEach(([dx,dy,rx,ry])=>{
      CTX.beginPath(); CTX.ellipse(CX+dx*ER,CY+dy*ER,rx*ER,ry*ER,0,0,Math.PI*2); CTX.fill();
    });
  CTX.restore();
  CTX.beginPath(); CTX.arc(CX,CY,ER,0,Math.PI*2);
  CTX.strokeStyle='rgba(100,180,255,.28)'; CTX.lineWidth=1; CTX.stroke();
  CTX.font=Math.round(W*.009)+'px sans-serif';
  CTX.fillStyle='rgba(100,160,255,.55)'; CTX.textAlign='center';
  CTX.fillText('EARTH',CX,CY+ER+13);
}

function drawSat(mlP, nadP, ecl, nadInc){
  const sx=CX+Math.cos(ANG)*OR, sy=CY+Math.sin(ANG)*OR;
  // trail
  for(let i=1;i<=6;i++){
    const ta=ANG-i*.09;
    CTX.beginPath(); CTX.arc(CX+Math.cos(ta)*OR,CY+Math.sin(ta)*OR,1.2-i*.15,0,Math.PI*2);
    CTX.fillStyle=`rgba(100,200,255,${.22-i*.03})`; CTX.fill();
  }
  CTX.save(); CTX.translate(sx,sy);
  // body — aligned with orbit tangent
  CTX.save(); CTX.rotate(ANG+Math.PI/2);
  CTX.fillStyle='#bccedd'; CTX.fillRect(-7,-5,14,10);
  CTX.fillStyle='rgba(70,120,175,.42)'; CTX.fillRect(-5,-3,3,6); CTX.fillRect(2,-3,3,6);
  CTX.strokeStyle='rgba(80,140,200,.38)'; CTX.lineWidth=.5; CTX.strokeRect(-7,-5,14,10);
  CTX.restore();

  const PH=Math.round(OR*.185), PW=Math.round(OR*.05);
  const sd=sunDir(ANG);

  if(ML_ON){
    // ML: panel faces sun perfectly
    const panelAng=sd+Math.PI/2;
    const cf=1.0;
    CTX.save(); CTX.rotate(panelAng);
    const r2=Math.round(135+cf*120), g2=Math.round(75+cf*115);
    CTX.fillStyle=ecl?'#0e1a28':`rgb(${r2},${g2},10)`;
    if(!ecl){CTX.shadowColor=`rgba(255,165,0,.65)`;CTX.shadowBlur=8+cf*10;}
    CTX.fillRect(-PW/2,-6-PH,PW,PH); CTX.fillRect(-PW/2,6,PW,PH);
    CTX.shadowBlur=0;
    // cell lines
    CTX.strokeStyle='rgba(0,0,0,.2)'; CTX.lineWidth=.5;
    for(let i=1;i<4;i++){
      const y1=-6-PH+(PH/4)*i,y2=6+(PH/4)*i;
      CTX.beginPath();CTX.moveTo(-PW/2,y1);CTX.lineTo(PW/2,y1);CTX.stroke();
      CTX.beginPath();CTX.moveTo(-PW/2,y2);CTX.lineTo(PW/2,y2);CTX.stroke();
    }
    CTX.restore();
    // sun ray arrow
    if(!ecl){
      CTX.beginPath();CTX.moveTo(Math.cos(sd)*22,Math.sin(sd)*22);CTX.lineTo(Math.cos(sd)*40,Math.sin(sd)*40);
      CTX.strokeStyle='rgba(255,200,50,.45)';CTX.lineWidth=1;CTX.stroke();
      CTX.beginPath();
      CTX.moveTo(Math.cos(sd)*40,Math.sin(sd)*40);
      CTX.lineTo(Math.cos(sd+2.6)*34,Math.sin(sd+2.6)*34);
      CTX.lineTo(Math.cos(sd-2.6)*34,Math.sin(sd-2.6)*34);
      CTX.closePath();CTX.fillStyle='rgba(255,200,50,.45)';CTX.fill();
    }
    // ML power label
    if(!ecl){
      CTX.fillStyle='rgba(76,200,130,.75)';
      CTX.font='bold '+Math.round(W*.009)+'px monospace';
      CTX.textAlign='center';
      CTX.fillText(mlP.toFixed(2)+'W',0,-PH-12);
    }
  } else {
    // Sensor ADCS: panel angle driven by sensorAng (with CSS noise + slew lag)
    const panelAng = sensorAng + Math.PI/2;
    const cf = Math.max(0, Math.cos(nadInc));  // nadInc = sInc from caller
    const r2 = Math.round(80+cf*175), g2 = Math.round(40+cf*150);
    CTX.save(); CTX.rotate(panelAng);
    CTX.fillStyle = ecl ? '#0e1a28' : `rgb(${r2},${g2},10)`;
    if(!ecl && cf>.05){ CTX.shadowColor=`rgba(245,166,35,${cf*.5})`; CTX.shadowBlur=5+cf*8; }
    CTX.fillRect(-PW/2,-6-PH,PW,PH); CTX.fillRect(-PW/2,6,PW,PH);
    CTX.shadowBlur=0;
    CTX.strokeStyle='rgba(0,0,0,.2)'; CTX.lineWidth=.5;
    for(let i=1;i<4;i++){
      const y1=-6-PH+(PH/4)*i, y2=6+(PH/4)*i;
      CTX.beginPath(); CTX.moveTo(-PW/2,y1); CTX.lineTo(PW/2,y1); CTX.stroke();
      CTX.beginPath(); CTX.moveTo(-PW/2,y2); CTX.lineTo(PW/2,y2); CTX.stroke();
    }
    CTX.restore();
    if(!ecl){
      // Arc showing tracking error between sensor-pointed panel and true sun
      let diff = sd - sensorAng;
      while(diff>Math.PI)diff-=2*Math.PI; while(diff<-Math.PI)diff+=2*Math.PI;
      const adeg = Math.abs(diff)*180/Math.PI;
      CTX.beginPath();
      CTX.arc(0,0,22,Math.min(sensorAng,sensorAng+diff),Math.max(sensorAng,sensorAng+diff));
      CTX.strokeStyle = adeg<10 ? 'rgba(76,200,130,.8)' : adeg<25 ? 'rgba(245,166,35,.85)' : 'rgba(232,90,90,.85)';
      CTX.lineWidth=1.8; CTX.stroke();
      // True sun arrow
      CTX.beginPath(); CTX.moveTo(Math.cos(sd)*22,Math.sin(sd)*22); CTX.lineTo(Math.cos(sd)*40,Math.sin(sd)*40);
      CTX.strokeStyle='rgba(255,200,50,.4)'; CTX.lineWidth=1; CTX.stroke();
      // ADCS state label
      const stateColor = {TRACKING:'rgba(76,200,130,.8)',SLEWING:'rgba(245,166,35,.85)',DEADBAND:'rgba(79,163,232,.8)','RE-ACQ':'rgba(232,90,90,.85)'}[adcsState]||'rgba(245,166,35,.8)';
      CTX.fillStyle = stateColor;
      CTX.font = 'bold '+Math.round(W*.008)+'px monospace';
      CTX.textAlign = 'center';
      CTX.fillText(adcsState, 0, PH+22);
      // Sensor power label
      CTX.fillStyle='rgba(245,166,35,.75)';
      CTX.font='bold '+Math.round(W*.009)+'px monospace';
      CTX.fillText(nadP.toFixed(2)+'W', 0, -PH-12);
    }
  }
  CTX.restore();
}

function drawPwGraph(){
  const gx=6,gy=H-44,gw=Math.round(W*.7),gh=32;
  CTX.fillStyle='rgba(0,0,0,.22)'; CTX.fillRect(gx,gy,gw,gh);
  const pmax=ML_W.stats.pmax||4;
  // ML line
  CTX.beginPath();
  for(let i=0;i<NH;i++){
    const idx=(hI+i)%NH;
    const x=gx+(i/NH)*gw, y=gy+gh-(mlBuf[idx]/pmax)*gh;
    i===0?CTX.moveTo(x,y):CTX.lineTo(x,y);
  }
  CTX.strokeStyle='rgba(76,200,130,.85)'; CTX.lineWidth=1.5; CTX.stroke();
  // Nadir line
  CTX.beginPath();
  for(let i=0;i<NH;i++){
    const idx=(hI+i)%NH;
    const x=gx+(i/NH)*gw, y=gy+gh-(nadBuf[idx]/pmax)*gh;
    i===0?CTX.moveTo(x,y):CTX.lineTo(x,y);
  }
  CTX.strokeStyle='rgba(245,166,35,.65)'; CTX.lineWidth=1; CTX.stroke();
  const fs=Math.round(W*.009);
  CTX.font=fs+'px monospace';
  CTX.fillStyle='rgba(76,200,130,.6)'; CTX.textAlign='left'; CTX.fillText('ML',gx+3,gy+10);
  CTX.fillStyle='rgba(245,166,35,.6)';                        CTX.fillText('Nadir',gx+22,gy+10);
  CTX.fillStyle='rgba(130,155,200,.4)'; CTX.textAlign='right'; CTX.fillText(pmax.toFixed(1)+'W',gx+gw-3,gy+10);
}

// ════════════════════════════════════════════════
// MINI CHARTS  — contexts cached, no resize each frame
// ════════════════════════════════════════════════
const MC = {};  // cached: { el, ctx, w, h }

function setupMC(id){
  const el=document.getElementById(id);
  const dpr=window.devicePixelRatio||1;
  const pw=el.parentElement.clientWidth-22;
  const ph=parseInt(el.getAttribute('height')||72);
  el.width=pw*dpr; el.height=ph*dpr;
  el.style.width=pw+'px'; el.style.height=ph+'px';
  const c=el.getContext('2d'); c.scale(dpr,dpr);
  MC[id]={el,ctx:c,w:pw,h:ph};
}

function setupAllMC(){
  ['ch-pw','ch-tmp','ch-bat','ch-cur'].forEach(setupMC);
}

// Grid helper — no canvas resize inside
function miniGrid(id, yMax, yDec){
  const {ctx:c,w,h}=MC[id];
  const pad={t:3,r:6,b:14,l:28};
  c.clearRect(0,0,w,h);
  c.fillStyle='rgba(0,0,12,.3)'; c.fillRect(pad.l,pad.t,w-pad.l-pad.r,h-pad.t-pad.b);
  const cw=w-pad.l-pad.r, ch=h-pad.t-pad.b;
  for(let i=0;i<=3;i++){
    const y=pad.t+ch*(1-i/3);
    c.strokeStyle='rgba(80,120,200,.09)'; c.lineWidth=.5;
    c.beginPath(); c.moveTo(pad.l,y); c.lineTo(w-pad.r,y); c.stroke();
    c.fillStyle='rgba(120,150,200,.38)'; c.font='7px monospace'; c.textAlign='right';
    c.fillText((yMax*i/3).toFixed(yDec),pad.l-3,y+2.5);
  }
  return pad;
}

// Draw a line on a mini chart using pre-computed pad
function mcLine(id, pad, xs, ys, color, lw, fill){
  const {ctx:c,w,h}=MC[id];
  const cw=w-pad.l-pad.r, ch=h-pad.t-pad.b;
  const xMin=xs[0]||0, xMax=xs[xs.length-1]||1, xR=xMax-xMin||1;
  const yMin=Math.min(...ys), yMax=Math.max(...ys)||.001, yR=yMax-yMin||.001;
  c.beginPath();
  xs.forEach((xv,i)=>{
    const px=pad.l+(xv-xMin)/xR*cw, py=pad.t+ch-((ys[i]-yMin)/yR)*ch;
    i===0?c.moveTo(px,py):c.lineTo(px,py);
  });
  if(fill){
    c.lineTo(pad.l+cw,pad.t+ch); c.lineTo(pad.l,pad.t+ch); c.closePath();
    c.fillStyle=fill; c.fill(); c.beginPath();
    xs.forEach((xv,i)=>{
      const px=pad.l+(xv-xMin)/xR*cw, py=pad.t+ch-((ys[i]-yMin)/yR)*ch;
      i===0?c.moveTo(px,py):c.lineTo(px,py);
    });
  }
  c.strokeStyle=color; c.lineWidth=lw; c.stroke();
}

// Power history — called each frame but uses cached ctx
function drawPwChart(){
  if(!MC['ch-pw']) return;
  const {ctx:c,w,h}=MC['ch-pw'];
  const pad=miniGrid('ch-pw', ML_W.stats.pmax||4, 1);
  const cw=w-pad.l-pad.r, ch2=h-pad.t-pad.b;
  const pmax=ML_W.stats.pmax||4;
  // ML fill
  c.beginPath();
  for(let i=0;i<NH;i++){
    const idx=(hI+i)%NH;
    const x=pad.l+(i/NH)*cw, y=pad.t+ch2-(mlBuf[idx]/pmax)*ch2;
    i===0?c.moveTo(x,y):c.lineTo(x,y);
  }
  c.lineTo(pad.l+cw,pad.t+ch2); c.lineTo(pad.l,pad.t+ch2); c.closePath();
  c.fillStyle='rgba(76,200,130,.09)'; c.fill();
  // ML line
  c.beginPath();
  for(let i=0;i<NH;i++){const idx=(hI+i)%NH;c.lineTo(pad.l+(i/NH)*cw, pad.t+ch2-(mlBuf[idx]/pmax)*ch2);}
  c.strokeStyle='rgba(76,200,130,.9)'; c.lineWidth=1.5; c.stroke();
  // Nadir line
  c.beginPath();
  for(let i=0;i<NH;i++){const idx=(hI+i)%NH;c.lineTo(pad.l+(i/NH)*cw, pad.t+ch2-(nadBuf[idx]/pmax)*ch2);}
  c.strokeStyle='rgba(245,166,35,.7)'; c.lineWidth=1.2; c.stroke();
  // legend
  c.fillStyle='rgba(76,200,130,.6)'; c.font='7px monospace'; c.textAlign='left'; c.fillText('ML',pad.l+2,pad.t+9);
  c.fillStyle='rgba(245,166,35,.6)'; c.fillText('Nadir',pad.l+18,pad.t+9);
  c.fillStyle='rgba(120,150,200,.35)'; c.font='7px sans-serif'; c.textAlign='center'; c.fillText('time →',pad.l+cw/2,h-1);
}

// Battery — called each frame
function drawBatChart(){
  if(!MC['ch-bat']) return;
  const {ctx:c,w,h}=MC['ch-bat'];
  const pad=miniGrid('ch-bat',100,0);
  const cw=w-pad.l-pad.r, ch2=h-pad.t-pad.b;
  c.beginPath();
  for(let i=0;i<NH;i++){const idx=(bI+i)%NH;c.lineTo(pad.l+(i/NH)*cw, pad.t+ch2-batBuf[idx]*ch2);}
  c.lineTo(pad.l+cw,pad.t+ch2); c.lineTo(pad.l,pad.t+ch2); c.closePath();
  c.fillStyle='rgba(79,163,232,.08)'; c.fill();
  c.beginPath();
  for(let i=0;i<NH;i++){const idx=(bI+i)%NH;c.lineTo(pad.l+(i/NH)*cw, pad.t+ch2-batBuf[idx]*ch2);}
  c.strokeStyle='rgba(79,163,232,.9)'; c.lineWidth=1.5; c.stroke();
  c.fillStyle='rgba(120,150,200,.35)'; c.font='7px sans-serif'; c.textAlign='center'; c.fillText('time →',pad.l+cw/2,h-1);
}

// Temperature chart — sim-driven
function drawTmpChart(){
  if(!MC['ch-tmp']) return;
  const {ctx:cc,w,h}=MC['ch-tmp'];
  const tMin=-10, tMax=50;
  const pad=miniGrid('ch-tmp', tMax, 0);
  const cw=w-pad.l-pad.r, ch2=h-pad.t-pad.b;

  // Shade eclipse zones (where T dips below 0)
  for(let i=0;i<NH;i++){
    const idx=(hI+i)%NH;
    if(tmpBuf[idx]<5){
      const x=pad.l+(i/NH)*cw;
      cc.fillStyle='rgba(79,163,232,0.07)';
      cc.fillRect(x,pad.t,(cw/NH)+1,ch2);
    }
  }

  // Zero line
  const zeroY=pad.t+ch2-((0-tMin)/(tMax-tMin))*ch2;
  cc.beginPath(); cc.moveTo(pad.l,zeroY); cc.lineTo(pad.l+cw,zeroY);
  cc.strokeStyle='rgba(79,163,232,0.2)'; cc.lineWidth=0.5; cc.stroke();

  // ML mode temp (orange — hotter because more power absorbed)
  // Sensor ADCS temp (blue — slightly cooler)
  cc.beginPath();
  for(let i=0;i<NH;i++){
    const idx=(hI+i)%NH;
    const x=pad.l+(i/NH)*cw;
    const y=pad.t+ch2-((tmpBuf[idx]-tMin)/(tMax-tMin))*ch2;
    i===0?cc.moveTo(x,y):cc.lineTo(x,y);
  }
  cc.strokeStyle='rgba(167,139,250,0.9)'; cc.lineWidth=1.5; cc.stroke();

  // Fill under
  cc.beginPath();
  for(let i=0;i<NH;i++){
    const idx=(hI+i)%NH;
    cc.lineTo(pad.l+(i/NH)*cw, pad.t+ch2-((tmpBuf[idx]-tMin)/(tMax-tMin))*ch2);
  }
  cc.lineTo(pad.l+cw,pad.t+ch2); cc.lineTo(pad.l,pad.t+ch2); cc.closePath();
  cc.fillStyle='rgba(167,139,250,0.07)'; cc.fill();

  // Min label
  cc.fillStyle='rgba(120,150,200,0.38)'; cc.font='7px monospace'; cc.textAlign='right';
  cc.fillText(tMin+'°',pad.l-3,pad.t+ch2+2.5);
  cc.fillStyle='rgba(120,150,200,0.35)'; cc.font='7px sans-serif'; cc.textAlign='center';
  cc.fillText('time → (°C)',pad.l+cw/2,h-1);

  // Hover
  MC['ch-tmp'].el.onmousemove=function(e){
    const rect=MC['ch-tmp'].el.getBoundingClientRect();
    const mx=(e.clientX-rect.left)*(w/rect.width);
    const i=Math.round((mx-pad.l)/cw*NH);
    const idx=(hI+Math.max(0,Math.min(NH-1,i)))%NH;
    const T=tmpBuf[idx];
    const ef=Math.max(0.5,1-0.004*Math.max(0,T-25));
    showTip(e,'Panel Temperature\n'+T.toFixed(1)+'°C\nη(T) = '+ef.toFixed(4)+'\n'+(T<5?'🌑 Eclipse zone':'☀ Sunlit'));
  };
  MC['ch-tmp'].el.onmouseleave=hideTip;
}

// Current chart — sim-driven, shows ML vs sensor ADCS
function drawCurChart(){
  if(!MC['ch-cur']) return;
  const {ctx:cc,w,h}=MC['ch-cur'];
  // Current range: 0 to ~800mA (P_max/5V * 1000)
  const cMax=Math.max(800,Math.max(...curBuf)*1.1)||800;
  const pad=miniGrid('ch-cur', Math.round(cMax), 0);
  const cw=w-pad.l-pad.r, ch2=h-pad.t-pad.b;

  // ML current (from mlBuf: I = P/5V * 1000)
  cc.beginPath();
  for(let i=0;i<NH;i++){
    const idx=(hI+i)%NH;
    const cur=mlBuf[idx]/5.0*1000;
    const x=pad.l+(i/NH)*cw;
    const y=pad.t+ch2-(cur/cMax)*ch2;
    i===0?cc.moveTo(x,y):cc.lineTo(x,y);
  }
  cc.lineTo(pad.l+cw,pad.t+ch2); cc.lineTo(pad.l,pad.t+ch2); cc.closePath();
  cc.fillStyle='rgba(76,200,130,0.08)'; cc.fill();
  cc.beginPath();
  for(let i=0;i<NH;i++){
    const idx=(hI+i)%NH;
    const x=pad.l+(i/NH)*cw, y=pad.t+ch2-(mlBuf[idx]/5.0*1000/cMax)*ch2;
    i===0?cc.moveTo(x,y):cc.lineTo(x,y);
  }
  cc.strokeStyle='rgba(76,200,130,0.9)'; cc.lineWidth=1.5; cc.stroke();

  // Sensor ADCS current (orange)
  cc.beginPath();
  for(let i=0;i<NH;i++){
    const idx=(hI+i)%NH;
    const x=pad.l+(i/NH)*cw, y=pad.t+ch2-(nadBuf[idx]/5.0*1000/cMax)*ch2;
    i===0?cc.moveTo(x,y):cc.lineTo(x,y);
  }
  cc.strokeStyle='rgba(245,166,35,0.75)'; cc.lineWidth=1.2; cc.stroke();

  // Legend
  cc.fillStyle='rgba(76,200,130,0.7)'; cc.font='7px monospace'; cc.textAlign='left'; cc.fillText('ML',pad.l+2,pad.t+9);
  cc.fillStyle='rgba(245,166,35,0.7)'; cc.fillText('Sensor',pad.l+20,pad.t+9);
  cc.fillStyle='rgba(120,150,200,0.35)'; cc.font='7px sans-serif'; cc.textAlign='center';
  cc.fillText('time → (mA)',pad.l+cw/2,h-1);

  // Hover
  MC['ch-cur'].el.onmousemove=function(e){
    const rect=MC['ch-cur'].el.getBoundingClientRect();
    const mx=(e.clientX-rect.left)*(w/rect.width);
    const i=Math.round((mx-pad.l)/cw*NH);
    const idx=(hI+Math.max(0,Math.min(NH-1,i)))%NH;
    const mlC=(mlBuf[idx]/5.0*1000), nadC=(nadBuf[idx]/5.0*1000);
    showTip(e,'Panel Current\nML:     '+mlC.toFixed(1)+' mA\nSensor: '+nadC.toFixed(1)+' mA\nΔ = '+(mlC-nadC).toFixed(1)+' mA');
  };
  MC['ch-cur'].el.onmouseleave=hideTip;
}

// ════════════════════════════════════════════════
// UI UPDATE
// ════════════════════════════════════════════════
function fmtE(j){ return j<1000?Math.round(j)+' J':(j/1000).toFixed(2)+' kJ'; }

function updateUI(mlP, nadP, T, ecl, tE, nadInc){
  // header badges
  document.getElementById('b-ecl').textContent = ecl?'🌑 ECLIPSE':'☀ SUNLIT';
  document.getElementById('b-ecl').className   = 'badge '+(ecl?'b-blue':'b-orange');
  // telemetry
  document.getElementById('v-ecl').textContent = ecl?'🌑 Eclipse':'☀ Sunlit';
  document.getElementById('v-ecl').style.color = ecl?'var(--blue)':'var(--orange)';
  const disp=ML_ON?mlP:nadP;
  const pmax=ML_W.stats.pmax||4;
  const pPct=disp/pmax*100;
  document.getElementById('v-pw').textContent = disp.toFixed(3)+' W';
  document.getElementById('v-pw').style.color = ML_ON?'var(--green)':'var(--orange)';
  document.getElementById('b-pw').style.width = pPct+'%';
  document.getElementById('b-pw').style.background = pPct>65?'var(--green)':pPct>30?'var(--orange)':'var(--red)';
  const bp=Math.round(BAT*100);
  document.getElementById('v-bat').textContent=bp+'%';
  document.getElementById('b-bat').style.width=bp+'%';
  document.getElementById('b-bat').style.background=bp<20?'var(--red)':bp<50?'var(--orange)':'var(--blue)';
  document.getElementById('v-orb').textContent=Math.round((ANG+Math.PI)*180/Math.PI%360)+'°';
  const incDeg=Math.round(Math.abs(nadInc)*180/Math.PI);
  document.getElementById('v-ang').textContent=incDeg+'°';
  // ADCS live telemetry (only visible in sensor mode)
  const stEl=document.getElementById('v-adcs-state');
  if(stEl){
    stEl.textContent=adcsState;
    stEl.style.color={TRACKING:'var(--green)',SLEWING:'var(--orange)',DEADBAND:'var(--blue)','RE-ACQ':'var(--red)'}[adcsState]||'var(--orange)';
  }
  const saEl=document.getElementById('v-sensor-ang');
  if(saEl) saEl.textContent=Math.round(sensorAng*180/Math.PI)+'°';
  const teEl=document.getElementById('v-track-err');
  if(teEl){
    teEl.textContent=incDeg+'°';
    teEl.style.color=incDeg<10?'var(--green)':incDeg<20?'var(--orange)':'var(--red)';
  }
  const incEl=document.getElementById('v-inc');
  if(incEl) incEl.textContent=incDeg+'°';
  // chips
  document.getElementById('c-ml').textContent  = mlP.toFixed(3);
  document.getElementById('c-nad').textContent = nadP.toFixed(3);
  document.getElementById('c-tmp').textContent = Math.round(T)+'°C';
  document.getElementById('c-ef').textContent  = tE.toFixed(3);
  document.getElementById('v-inf').textContent = mlP.toFixed(4)+' W';
  // Simulation stats sidebar
  const spEl=document.getElementById('v-sun-pct');
  if(spEl && totalFrames>0) spEl.textContent=(sunFrames/totalFrames*100).toFixed(0)+'%';
  const amEl=document.getElementById('v-avg-ml');
  if(amEl && sunFrames>0) amEl.textContent=(sumML/sunFrames).toFixed(3)+' W';
  const anEl=document.getElementById('v-avg-nad');
  if(anEl && sunFrames>0) anEl.textContent=(sumNad/sunFrames).toFixed(3)+' W';
  // energy
  document.getElementById('e-ml').textContent  = fmtE(eML);
  document.getElementById('e-nad').textContent = fmtE(eNad);
  const maxE=Math.max(eML,eNad,1);
  document.getElementById('b-eml').style.width  = (eML/maxE*100)+'%';
  document.getElementById('b-enad').style.width = (eNad/maxE*100)+'%';
  const gain=eNad>1?(eML-eNad)/eNad*100:0;
  const gs=(gain>=0?'+':'')+gain.toFixed(1)+'%';
  document.getElementById('c-gain').textContent  = gs;
  document.getElementById('c-gain').style.color  = gain>=0?'var(--green)':'var(--red)';
  document.getElementById('gain-big').textContent = gs;
  document.getElementById('gain-big').style.color = gain>=0?'var(--green)':'var(--red)';
  const gbm = document.getElementById('gain-big-mode');
  if(gbm){ gbm.textContent = gs; gbm.style.color = gain>=0?'var(--green)':'var(--red)'; }
  const gb2 = document.getElementById('gain-big2');
  if(gb2){ const absG=Math.abs(gain).toFixed(1); gb2.textContent = gain>=0?'-'+absG+'%':'+'+absG+'%'; gb2.style.color = gain>=0?'var(--orange)':'var(--green)'; }
  const hg = document.getElementById('hdr-gain');
  if(hg){ hg.textContent = gs; hg.style.color = gain>=0?'var(--green)':'var(--red)'; }
}

// ════════════════════════════════════════════════
// CONTROLS
// ════════════════════════════════════════════════
function setMode(m){
  ML_ON = (m === 'ml');
  document.getElementById('tab-ml').classList.toggle('active', ML_ON);
  document.getElementById('tab-sensor').classList.toggle('active', !ML_ON);
  document.getElementById('b-mode').textContent = ML_ON ? 'ML AUTO' : 'SENSOR ADCS';
  document.getElementById('b-mode').className   = 'badge '+(ML_ON ? 'b-blue' : 'b-orange');
  document.getElementById('mode-panel-title').textContent = ML_ON ? 'Mode 1 — ML Predicted' : 'Mode 2 — Sensor ADCS';
  document.getElementById('ml-details').style.display     = ML_ON ? '' : 'none';
  document.getElementById('sensor-details').style.display = ML_ON ? 'none' : '';
  const srcPanel = document.getElementById('sensor-src-panel');
  if(srcPanel) srcPanel.style.display = ML_ON ? 'none' : '';
  document.getElementById('lbl-ang').textContent = ML_ON ? 'Sun incidence θ' : 'CSS tracking err';
}
function toggleMode(){ setMode(ML_ON ? 'sensor' : 'ml'); }

function setSp(m,btn){
  SPEED=m;
  document.querySelectorAll('.sb').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
}


function resetSim(){
  ANG=-Math.PI/2; BAT=1.0; eML=0; eNad=0;
  mlBuf.fill(0); nadBuf.fill(0); batBuf.fill(1.0);
  tmpBuf.fill(25); curBuf.fill(0);
  hI=0; bI=0; LAST=null;
  sunFrames=0; totalFrames=0; sumML=0; sumNad=0;
  sensorAng=-Math.PI/2; reacqTimer=0; adcsState='TRACKING';
}

// ════════════════════════════════════════════════
// TOOLTIP
// ════════════════════════════════════════════════
const TIP=document.getElementById('tip');
function showTip(e,t){ TIP.textContent=t; TIP.style.display='block'; TIP.style.left=(e.clientX+14)+'px'; TIP.style.top=(e.clientY-8)+'px'; }
function hideTip(){ TIP.style.display='none'; }

// ════════════════════════════════════════════════
// INIT
// ════════════════════════════════════════════════
requestAnimationFrame(()=>requestAnimationFrame(()=>{
  setupAllMC();
}));
window.addEventListener('resize',()=>{
  setTimeout(()=>{ CTX.setTransform(1,0,0,1,0,0); resizeSim(); setupAllMC(); }, 80);
});

// ════════════════════════════════════════════════
// MAIN LOOP  — lean, no canvas resize inside
// ════════════════════════════════════════════════
function frame(ts){
  if(!LAST) LAST=ts;
  const dt=Math.min((ts-LAST)/1000,.1); LAST=ts;
  const sdt=dt*SPEED;

  ANG=(ANG+SPD0*dt)%(2*Math.PI);

  const ecl=isEcl(ANG);
  const T=getT(ANG,ecl);
  const tE=tEff(T);
  const p=phi(ANG);

  // Step sensor ADCS (runs every frame, physics-based)
  stepADCS(sdt, ecl);

  // Sensor incidence: angle between sensor-pointed panel and true sun
  const sInc   = ecl ? Math.PI/2 : sensorIncidence();
  const cosSens = ecl ? 0 : Math.max(0, Math.cos(sInc));

  // ML power: cos_theta = 1.0 — always faces sun perfectly
  const pw_ml  = ecl ? 0 : mlInfer(1.0,    tE, BAT, p);
  // Sensor ADCS power: cos_theta = cos(actual incidence after CSS noise + slew lag)
  const pw_nad = ecl ? 0 : mlInfer(cosSens, tE, BAT, p);

  // Accumulate both always (for cumulative comparison)
  eML  += pw_ml  * sdt;
  eNad += pw_nad * sdt;

  // Battery follows whichever mode is displayed
  const pw_disp = ML_ON ? pw_ml : pw_nad;
  // Battery: charges when panel power > subsystem quiescent load (~0.8W)
  // Drains during eclipse (no generation) and when pw < load
  const QUIESCENT_W = 0.8;   // satellite subsystem consumption
  const CHARGE_RATE = 0.003; // normalised charge/discharge rate (scaled for visibility)
  if(ecl){
    // Eclipse: pure drain
    BAT = Math.min(1, Math.max(0, BAT - 0.03*sdt));
  } else {
    // Sunlit: net = panel power minus quiescent load
    const net = (pw_disp - QUIESCENT_W) * CHARGE_RATE;
    BAT = Math.min(1, Math.max(0, BAT + net*sdt));
  }

  // Sim-derived current: P = V*I → I = P/V (use ~5V bus)
  const busCurrent = pw_disp > 0 ? (pw_disp / 5.0) * 1000 : 0; // mA

  // Buffers — all written to same slot before incrementing
  mlBuf[hI]=pw_ml; nadBuf[hI]=pw_nad;
  tmpBuf[hI]=T;    curBuf[hI]=busCurrent;
  hI=(hI+1)%NH;
  batBuf[bI]=BAT;  bI=(bI+1)%NH;

  // Running stats for sidebar
  totalFrames++;
  if(!ecl){ sunFrames++; sumML+=pw_ml; sumNad+=pw_nad; }

  // Draw orbital canvas
  drawBg(); drawOrbit(); drawEclShadow(); drawSun(ts/1000); drawEarth();
  drawSat(pw_ml, pw_nad, ecl, sInc);
  drawPwGraph();

  // Update DOM + mini-charts
  updateUI(pw_ml, pw_nad, T, ecl, tE, sInc);
  drawPwChart();
  drawBatChart();
  drawTmpChart();
  drawCurChart();

  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
</script>
</body>
</html>
