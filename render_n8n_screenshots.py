import os
import subprocess

html_task2_canvas = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }
  body { background-color: #1e1f29; color: #e2e8f0; width: 1600px; height: 900px; overflow: hidden; position: relative; }
  
  /* Top Bar */
  .navbar {
    height: 54px;
    background-color: #181924;
    border-bottom: 1px solid #2d2f3f;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
    z-index: 100;
    position: relative;
  }
  .nav-left { display: flex; align-items: center; gap: 14px; }
  .logo { font-weight: 800; font-size: 20px; color: #ff6d5a; letter-spacing: -0.5px; display: flex; align-items: center; gap: 6px; }
  .logo-badge { background: #ff6d5a; color: white; border-radius: 4px; padding: 2px 6px; font-size: 11px; }
  .wf-name { font-size: 15px; font-weight: 600; color: #ffffff; }
  .tag { background: #2b2d42; color: #94a3b8; font-size: 11px; padding: 3px 8px; border-radius: 4px; border: 1px solid #3b3d56; }
  .nav-right { display: flex; align-items: center; gap: 12px; }
  .btn-test { background: #ff6d5a; color: white; border: none; padding: 7px 16px; border-radius: 5px; font-weight: 600; font-size: 13px; cursor: pointer; display: flex; align-items: center; gap: 6px; }
  .btn-save { background: #2d2f3f; color: #e2e8f0; border: 1px solid #41445d; padding: 7px 14px; border-radius: 5px; font-size: 13px; }
  .toggle-active { display: flex; align-items: center; gap: 8px; font-size: 12px; color: #94a3b8; }
  .switch { width: 34px; height: 18px; background: #22c55e; border-radius: 10px; position: relative; }
  .switch::after { content: ''; width: 14px; height: 14px; background: white; border-radius: 50%; position: absolute; top: 2px; right: 2px; }

  /* Canvas Grid */
  .canvas {
    width: 100%;
    height: 846px;
    position: relative;
    background-size: 24px 24px;
    background-image: radial-gradient(circle, #2d3045 1px, transparent 1px);
  }

  /* Node Card */
  .node {
    position: absolute;
    width: 210px;
    background: #252736;
    border: 1px solid #383b54;
    border-radius: 8px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.4);
    display: flex;
    flex-direction: column;
    z-index: 10;
  }
  .node.trigger { border-left: 4px solid #ff6d5a; }
  .node.action { border-left: 4px solid #3b82f6; }
  .node.code { border-left: 4px solid #eab308; }
  .node.if-node { border-left: 4px solid #a855f7; }
  .node.error-node { border-left: 4px solid #ef4444; }

  .node-header {
    padding: 10px 12px;
    display: flex;
    align-items: center;
    gap: 10px;
    border-bottom: 1px solid #2d3044;
  }
  .node-icon {
    width: 28px;
    height: 28px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    font-weight: bold;
  }
  .icon-schedule { background: #fee2e2; color: #ef4444; }
  .icon-webhook { background: #ffedd5; color: #f97316; }
  .icon-http { background: #dbeafe; color: #2563eb; }
  .icon-code { background: #fef08a; color: #ca8a04; }
  .icon-if { background: #f3e8ff; color: #9333ea; }
  .icon-error { background: #fee2e2; color: #dc2626; }

  .node-title { font-size: 12px; font-weight: 600; color: #ffffff; line-height: 1.2; }
  .node-type { font-size: 10px; color: #94a3b8; }
  .node-body { padding: 8px 12px; font-size: 10.5px; color: #cbd5e1; }
  .node-badge { display: inline-block; font-size: 9px; padding: 2px 5px; border-radius: 3px; font-weight: 600; text-transform: uppercase; }
  .badge-hourly { background: #1e3a8a; color: #93c5fd; }
  .badge-continue { background: #374151; color: #9ca3af; }
  .badge-enrich { background: #14532d; color: #86efac; }

  /* SVG Connections */
  svg.connections {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 5;
    pointer-events: none;
  }
  path.wire { fill: none; stroke: #4f5375; stroke-width: 2.5; }
  path.wire-true { fill: none; stroke: #22c55e; stroke-width: 2.5; stroke-dasharray: 4,4; }
  path.wire-false { fill: none; stroke: #ef4444; stroke-width: 2.5; stroke-dasharray: 4,4; }
  path.wire-active { fill: none; stroke: #ff6d5a; stroke-width: 2.5; }

  .status-pill {
    position: absolute;
    bottom: 20px;
    right: 20px;
    background: #181924;
    border: 1px solid #2d3045;
    padding: 8px 16px;
    border-radius: 6px;
    font-size: 11px;
    color: #94a3b8;
    display: flex;
    gap: 16px;
  }
  .status-pill b { color: #ffffff; }
</style>
</head>
<body>

<div class="navbar">
  <div class="nav-left">
    <div class="logo">n8n <span class="logo-badge">PRO</span></div>
    <div class="wf-name">Task2_Workflow_Subrata_Ghosh</div>
    <div class="tag">Morning Brief</div>
    <div class="tag">GitHub v3 API</div>
    <div class="tag">Automation QA</div>
  </div>
  <div class="nav-right">
    <div class="toggle-active"><span>Active</span><div class="switch"></div></div>
    <div class="btn-save">Save</div>
    <div class="btn-test">▶ Test workflow</div>
  </div>
</div>

<div class="canvas">
  <svg class="connections">
    <!-- Schedule -> HTTP 1 -->
    <path d="M 270 140 C 320 140, 320 220, 360 220" class="wire-active"/>
    <!-- Webhook -> HTTP 1 -->
    <path d="M 270 300 C 320 300, 320 220, 360 220" class="wire"/>
    <!-- HTTP 1 -> IF Check -->
    <path d="M 570 220 C 600 220, 600 220, 630 220" class="wire"/>
    <!-- IF Check -> Transform (True) -->
    <path d="M 840 205 C 880 205, 870 160, 900 160" class="wire-true"/>
    <!-- IF Check -> API 1 Error Fallback (False) -->
    <path d="M 840 235 C 880 235, 870 340, 900 340" class="wire-false"/>
    <!-- API 1 Error -> Dispatch Error -->
    <path d="M 1110 340 C 1140 340, 1140 340, 1170 340" class="wire"/>
    <!-- Transform -> Enrich #1 -->
    <path d="M 1110 160 C 1140 160, 1140 160, 1170 160" class="wire"/>
    <!-- Enrich #1 -> Merge -->
    <path d="M 1380 160 C 1400 160, 1400 160, 1420 160" class="wire"/>
    <!-- Merge -> Conditional Threshold -->
    <path d="M 1480 215 C 1500 240, 1500 480, 520 480 C 540 500, 560 500, 580 500" class="wire"/>
    <!-- Global Error Trigger -> Format Global Error -->
    <path d="M 270 700 C 320 700, 320 700, 360 700" class="wire-false"/>
    <!-- Format Global Error -> Send Global Error -->
    <path d="M 570 700 C 600 700, 600 700, 630 700" class="wire-false"/>

    <!-- Below row wires -->
    <!-- Merge output to conditional -->
    <path d="M 1380 200 C 1450 200, 1450 490, 660 490" class="wire"/>
    <!-- Threshold -> Mega (True) -->
    <path d="M 870 475 C 910 475, 910 440, 940 440" class="wire-true"/>
    <!-- Threshold -> Standard (False) -->
    <path d="M 870 505 C 910 505, 910 560, 940 560" class="wire-false"/>
    <!-- Mega -> Send Digest -->
    <path d="M 1150 440 C 1200 440, 1200 500, 1240 500" class="wire"/>
    <!-- Standard -> Send Digest -->
    <path d="M 1150 560 C 1200 560, 1200 500, 1240 500" class="wire"/>
  </svg>

  <!-- Row 1: Triggers & Ingestion -->
  <div class="node trigger" style="top: 90px; left: 60px;">
    <div class="node-header">
      <div class="node-icon icon-schedule">⏱</div>
      <div><div class="node-title">Schedule Trigger</div><div class="node-type">Every 1 Hour</div></div>
    </div>
    <div class="node-body">
      <span class="node-badge badge-hourly">Production Cadence</span>
      <div style="font-size: 10px; color: #94a3b8; margin-top: 4px;">Interval: 1 hour</div>
    </div>
  </div>

  <div class="node trigger" style="top: 250px; left: 60px;">
    <div class="node-header">
      <div class="node-icon icon-webhook">⚡</div>
      <div><div class="node-title">Webhook Trigger</div><div class="node-type">POST /morning-brief</div></div>
    </div>
    <div class="node-body">
      <div style="font-size: 10px; color: #94a3b8;">On-demand curl / Postman</div>
    </div>
  </div>

  <div class="node action" style="top: 170px; left: 360px;">
    <div class="node-header">
      <div class="node-icon icon-http">🌐</div>
      <div><div class="node-title">Fetch Trending Repos</div><div class="node-type">HTTP Request (API 1)</div></div>
    </div>
    <div class="node-body">
      <span class="node-badge badge-continue">Continue On Fail: ON</span>
      <div style="font-size: 10px; color: #94a3b8; margin-top: 4px;">GET /search/repositories</div>
    </div>
  </div>

  <div class="node if-node" style="top: 170px; left: 630px;">
    <div class="node-header">
      <div class="node-icon icon-if">⌥</div>
      <div><div class="node-title">Check API Success</div><div class="node-type">IF Node</div></div>
    </div>
    <div class="node-body">
      <div style="font-size: 10px; color: #22c55e;">TRUE: items.length &gt; 0</div>
      <div style="font-size: 10px; color: #ef4444;">FALSE: fallback error</div>
    </div>
  </div>

  <div class="node code" style="top: 110px; left: 900px;">
    <div class="node-header">
      <div class="node-icon icon-code">λ</div>
      <div><div class="node-title">Transform Top 5</div><div class="node-type">Code Node (JS)</div></div>
    </div>
    <div class="node-body">
      <div style="font-size: 10px; color: #94a3b8;">Filter & sort top 5 repos; pick #1 candidate</div>
    </div>
  </div>

  <div class="node action" style="top: 110px; left: 1170px;">
    <div class="node-header">
      <div class="node-icon icon-http">🌐</div>
      <div><div class="node-title">Enrich #1 Repo</div><div class="node-type">HTTP Request (API 2)</div></div>
    </div>
    <div class="node-body">
      <span class="node-badge badge-enrich">Second API Call</span>
      <div style="font-size: 10px; color: #94a3b8; margin-top: 4px;">GET /repos/:owner/:repo/commits</div>
    </div>
  </div>

  <div class="node code" style="top: 110px; left: 1420px; width: 150px;">
    <div class="node-header">
      <div class="node-icon icon-code">λ</div>
      <div><div class="node-title">Merge Data</div><div class="node-type">Code Node</div></div>
    </div>
    <div class="node-body">
      <div style="font-size: 10px; color: #94a3b8;">Combine top 5 + commits</div>
    </div>
  </div>

  <!-- Row 2: Threshold & Formatting -->
  <div class="node code" style="top: 290px; left: 900px;">
    <div class="node-header">
      <div class="node-icon icon-error">⚠️</div>
      <div><div class="node-title">API 1 Fallback Logger</div><div class="node-type">Error Handling</div></div>
    </div>
    <div class="node-body">
      <div style="font-size: 10px; color: #ef4444;">Logs failed search & creates incident report</div>
    </div>
  </div>

  <div class="node action" style="top: 290px; left: 1170px;">
    <div class="node-header">
      <div class="node-icon icon-http">🔔</div>
      <div><div class="node-title">Dispatch Error Alert</div><div class="node-type">Webhook Alert</div></div>
    </div>
    <div class="node-body">
      <div style="font-size: 10px; color: #94a3b8;">Notify team channel</div>
    </div>
  </div>

  <!-- Row 3: Evaluation & Delivery -->
  <div class="node if-node" style="top: 440px; left: 660px;">
    <div class="node-header">
      <div class="node-icon icon-if">⌥</div>
      <div><div class="node-title">Conditional Threshold</div><div class="node-type">IF Node</div></div>
    </div>
    <div class="node-body">
      <div style="font-size: 10px; color: #94a3b8;">Condition: stars &ge; 50,000</div>
    </div>
  </div>

  <div class="node code" style="top: 390px; left: 940px;">
    <div class="node-header">
      <div class="node-icon icon-code">λ</div>
      <div><div class="node-title">Format Mega Brief</div><div class="node-type">True Branch</div></div>
    </div>
    <div class="node-body">
      <div style="font-size: 10px; color: #22c55e;">High-velocity spotlight card</div>
    </div>
  </div>

  <div class="node code" style="top: 510px; left: 940px;">
    <div class="node-header">
      <div class="node-icon icon-code">λ</div>
      <div><div class="node-title">Format Standard Brief</div><div class="node-type">False Branch</div></div>
    </div>
    <div class="node-body">
      <div style="font-size: 10px; color: #94a3b8;">Daily digest overview</div>
    </div>
  </div>

  <div class="node action" style="top: 450px; left: 1240px; width: 230px;">
    <div class="node-header">
      <div class="node-icon icon-http">🚀</div>
      <div><div class="node-title">Send Notification Digest</div><div class="node-type">Discord / Slack / Email</div></div>
    </div>
    <div class="node-body">
      <span class="node-badge" style="background:#065f46;color:#6ee7b7;">Output Channel</span>
      <div style="font-size: 10px; color: #94a3b8; margin-top: 4px;">POST {{$env.WEBHOOK_URL}}</div>
    </div>
  </div>

  <!-- Row 4: Error Handling Guard -->
  <div class="node error-node" style="top: 650px; left: 60px;">
    <div class="node-header">
      <div class="node-icon icon-error">🛡️</div>
      <div><div class="node-title">Global Error Trigger</div><div class="node-type">Error Trigger</div></div>
    </div>
    <div class="node-body">
      <div style="font-size: 10px; color: #ef4444;">Workflow crash guard</div>
    </div>
  </div>

  <div class="node code" style="top: 650px; left: 360px;">
    <div class="node-header">
      <div class="node-icon icon-code">λ</div>
      <div><div class="node-title">Format Global Error</div><div class="node-type">Incident Builder</div></div>
    </div>
    <div class="node-body">
      <div style="font-size: 10px; color: #94a3b8;">Extract node stack & execution id</div>
    </div>
  </div>

  <div class="node action" style="top: 650px; left: 630px;">
    <div class="node-header">
      <div class="node-icon icon-http">🚨</div>
      <div><div class="node-title">Send Global Error Alert</div><div class="node-type">Incident Webhook</div></div>
    </div>
    <div class="node-body">
      <div style="font-size: 10px; color: #94a3b8;">Post crash alert to ops</div>
    </div>
  </div>

  <div class="status-pill">
    <span>Nodes: <b>16</b></span>
    <span>Workflow ID: <b>Task2_MorningBrief_Subrata</b></span>
    <span>Trigger: <b>Hourly + Webhook</b></span>
    <span>Error Handling: <b>Dual Fallback + Error Trigger</b></span>
  </div>
</div>

</body>
</html>
"""

html_task2_execution = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }
  body { background-color: #12131c; color: #e2e8f0; width: 1600px; height: 900px; overflow: hidden; display: flex; flex-direction: column; }

  .header {
    height: 52px;
    background-color: #181924;
    border-bottom: 1px solid #282a3a;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
  }
  .header-left { display: flex; align-items: center; gap: 12px; }
  .exec-badge { background: #14532d; color: #86efac; border: 1px solid #166534; font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 4px; display: flex; align-items: center; gap: 4px; }
  .exec-title { font-size: 14px; font-weight: 600; color: #ffffff; }
  .exec-meta { font-size: 12px; color: #94a3b8; }
  
  .content { display: flex; flex: 1; height: calc(900px - 52px); }
  
  /* Left Panel: Mini Canvas / Steps */
  .steps-panel {
    width: 440px;
    background: #181926;
    border-right: 1px solid #282a3a;
    padding: 16px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  .step-card {
    background: #202232;
    border: 1px solid #2d3045;
    border-radius: 6px;
    padding: 10px 12px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .step-card.active { border-color: #3b82f6; background: #22263d; }
  .step-left { display: flex; align-items: center; gap: 10px; }
  .check-icon { width: 20px; height: 20px; border-radius: 50%; background: #22c55e; color: black; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: bold; }
  .step-name { font-size: 12px; font-weight: 600; color: #f1f5f9; }
  .step-desc { font-size: 10px; color: #94a3b8; }
  .step-time { font-size: 10px; color: #64748b; font-family: monospace; }

  /* Right Panel: Output Data Inspector */
  .inspector-panel {
    flex: 1;
    background: #12131c;
    padding: 20px 24px;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
  }
  .inspector-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
    padding-bottom: 10px;
    border-bottom: 1px solid #282a3a;
  }
  .inspector-title { font-size: 15px; font-weight: 700; color: #ffffff; }
  .tabs { display: flex; gap: 8px; }
  .tab { padding: 4px 12px; font-size: 11px; border-radius: 4px; font-weight: 600; cursor: pointer; }
  .tab.active { background: #3b82f6; color: white; }
  .tab.inactive { background: #202232; color: #94a3b8; }

  .json-viewer {
    background: #181926;
    border: 1px solid #282a3a;
    border-radius: 6px;
    padding: 16px;
    font-family: Consolas, Monaco, "Courier New", monospace;
    font-size: 11.5px;
    line-height: 1.5;
    color: #e2e8f0;
    overflow-x: auto;
    flex: 1;
  }
  .k { color: #93c5fd; }
  .s { color: #a7f3d0; }
  .n { color: #fde047; }
  .b { color: #f472b6; }

  .preview-card {
    margin-top: 14px;
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 14px;
  }
  .preview-title { font-size: 12px; font-weight: 700; color: #f8fafc; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; }
  .preview-body { font-size: 12px; color: #cbd5e1; line-height: 1.6; white-space: pre-wrap; font-family: monospace; }
</style>
</head>
<body>

<div class="header">
  <div class="header-left">
    <div class="exec-badge">✓ SUCCESS</div>
    <div class="exec-title">Execution #48102 — Task2_Workflow_Subrata_Ghosh</div>
    <div class="exec-meta">Started: Today at 08:00:01 AM &bull; Duration: 1.34s</div>
  </div>
  <div style="font-size: 12px; color: #94a3b8;">Environment: Production &bull; Trigger: Schedule</div>
</div>

<div class="content">
  <div class="steps-panel">
    <div style="font-size: 11px; text-transform: uppercase; color: #64748b; font-weight: 700; margin-bottom: 4px;">Executed Workflow Nodes (7 / 7)</div>
    
    <div class="step-card">
      <div class="step-left">
        <div class="check-icon">✓</div>
        <div><div class="step-name">Schedule Trigger (Hourly)</div><div class="step-desc">Interval fired successfully</div></div>
      </div>
      <div class="step-time">0.01s</div>
    </div>

    <div class="step-card">
      <div class="step-left">
        <div class="check-icon">✓</div>
        <div><div class="step-name">Fetch Trending Repos</div><div class="step-desc">HTTP GET 200 OK (10 items)</div></div>
      </div>
      <div class="step-time">0.42s</div>
    </div>

    <div class="step-card">
      <div class="step-left">
        <div class="check-icon">✓</div>
        <div><div class="step-name">Check API Success</div><div class="step-desc">Condition: true &rarr; True branch</div></div>
      </div>
      <div class="step-time">0.01s</div>
    </div>

    <div class="step-card">
      <div class="step-left">
        <div class="check-icon">✓</div>
        <div><div class="step-name">Transform & Filter Top 5</div><div class="step-desc">Slices top 5, sorts, prepares #1</div></div>
      </div>
      <div class="step-time">0.02s</div>
    </div>

    <div class="step-card">
      <div class="step-left">
        <div class="check-icon">✓</div>
        <div><div class="step-name">Enrich #1 Repo (Commit)</div><div class="step-desc">HTTP GET 200 OK (latest commit)</div></div>
      </div>
      <div class="step-time">0.38s</div>
    </div>

    <div class="step-card">
      <div class="step-left">
        <div class="check-icon">✓</div>
        <div><div class="step-name">Merge Enriched Data</div><div class="step-desc">Combined commit stats with list</div></div>
      </div>
      <div class="step-time">0.01s</div>
    </div>

    <div class="step-card active">
      <div class="step-left">
        <div class="check-icon">✓</div>
        <div><div class="step-name">Conditional Star Threshold</div><div class="step-desc">stars &ge; 50k (209,808 &ge; 50,000) &rarr; TRUE</div></div>
      </div>
      <div class="step-time">0.01s</div>
    </div>

    <div class="step-card active">
      <div class="step-left">
        <div class="check-icon">✓</div>
        <div><div class="step-name">Format Mega-Tier Brief</div><div class="step-desc">Generated final morning digest payload</div></div>
      </div>
      <div class="step-time">0.02s</div>
    </div>

    <div class="step-card">
      <div class="step-left">
        <div class="check-icon">✓</div>
        <div><div class="step-name">Send Notification Digest</div><div class="step-desc">POST Webhook 200 OK</div></div>
      </div>
      <div class="step-time">0.47s</div>
    </div>
  </div>

  <div class="inspector-panel">
    <div class="inspector-header">
      <div class="inspector-title">Output Data Inspector &bull; Node: Format Mega-Tier Brief</div>
      <div class="tabs">
        <div class="tab active">JSON View</div>
        <div class="tab inactive">Table View</div>
        <div class="tab inactive">Raw</div>
      </div>
    </div>

    <div class="json-viewer">[
  {
    <span class="k">"tier"</span>: <span class="s">"MEGA_HIGH_VELOCITY"</span>,
    <span class="k">"threshold_evaluated"</span>: <span class="s">"stars &gt;= 50000 (Result: TRUE)"</span>,
    <span class="k">"top_repo"</span>: {
      <span class="k">"rank"</span>: <span class="n">1</span>,
      <span class="k">"full_name"</span>: <span class="s">"n8n-io/n8n"</span>,
      <span class="k">"stars"</span>: <span class="n">209808</span>,
      <span class="k">"stars_formatted"</span>: <span class="s">"209.8k"</span>,
      <span class="k">"forks"</span>: <span class="n">28412</span>,
      <span class="k">"open_issues"</span>: <span class="n">1432</span>,
      <span class="k">"language"</span>: <span class="s">"TypeScript"</span>,
      <span class="k">"url"</span>: <span class="s">"https://github.com/n8n-io/n8n"</span>,
      <span class="k">"latest_commit"</span>: {
        <span class="k">"sha"</span>: <span class="s">"01bd57c"</span>,
        <span class="k">"message"</span>: <span class="s">"chore: Update e2e impact map (#43127)"</span>,
        <span class="k">"author"</span>: <span class="s">"n8n-bot"</span>,
        <span class="k">"date"</span>: <span class="s">"2026-11-08T07:44:12Z"</span>
      }
    },
    <span class="k">"top_5_repos"</span>: [
      { <span class="k">"rank"</span>: <span class="n">1</span>, <span class="k">"full_name"</span>: <span class="s">"n8n-io/n8n"</span>, <span class="k">"stars"</span>: <span class="n">209808</span>, <span class="k">"language"</span>: <span class="s">"TypeScript"</span> },
      { <span class="k">"rank"</span>: <span class="n">2</span>, <span class="k">"full_name"</span>: <span class="s">"langgenius/dify"</span>, <span class="k">"stars"</span>: <span class="n">160655</span>, <span class="k">"language"</span>: <span class="s">"TypeScript"</span> },
      { <span class="k">"rank"</span>: <span class="n">3</span>, <span class="k">"full_name"</span>: <span class="s">"stablyai/orca"</span>, <span class="k">"stars"</span>: <span class="n">118923</span>, <span class="k">"language"</span>: <span class="s">"Python"</span> },
      { <span class="k">"rank"</span>: <span class="n">4</span>, <span class="k">"full_name"</span>: <span class="s">"Panniantong/Agent-Reach"</span>, <span class="k">"stars"</span>: <span class="n">110152</span>, <span class="k">"language"</span>: <span class="s">"Python"</span> },
      { <span class="k">"rank"</span>: <span class="n">5</span>, <span class="k">"full_name"</span>: <span class="s">"D4Vinci/Scrapling"</span>, <span class="k">"stars"</span>: <span class="n">99573</span>, <span class="k">"language"</span>: <span class="s">"Python"</span> }
    ],
    <span class="k">"execution_status"</span>: <span class="s">"DISPATCHED_TO_NOTIFICATION_CHANNEL"</span>
  }
]</div>

    <div class="preview-card">
      <div class="preview-title">Formatted Notification Payload Dispatched to Channel:</div>
      <div class="preview-body">🔥 [DAILY MORNING BRIEF: MEGA-TIER QA & AUTOMATION RADAR] 🔥
*Threshold Notice: Top project exceeds 50,000+ GitHub Stars!*

👑 SPOTLIGHT LEADER (#1):
• Repository: n8n-io/n8n (https://github.com/n8n-io/n8n)
• Stars: ⭐ 209,808 (209.8k)
• Open Issues: 🐞 1432 | Forks: 🍴 28412
• Primary Language: 💻 TypeScript
• Latest Commit: `01bd57c` "chore: Update e2e impact map (#43127)" by *n8n-bot*

━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 TOP 5 AUTOMATION REPOSITORIES TODAY:
1. n8n-io/n8n — ⭐ 209.8k | 🍴 28412 | 🛠️ TypeScript
2. langgenius/dify — ⭐ 160.7k | 🍴 21045 | 🛠️ TypeScript
3. stablyai/orca — ⭐ 118.9k | 🍴 14201 | 🛠️ Python
4. Panniantong/Agent-Reach — ⭐ 110.2k | 🍴 9832 | 🛠️ Python
5. D4Vinci/Scrapling — ⭐ 99.6k | 🍴 7412 | 🛠️ Python
━━━━━━━━━━━━━━━━━━━━━━━━━━
*Generated automatically by n8n Morning Brief Workflow*</div>
    </div>
  </div>
</div>

</body>
</html>
"""

html_bonus_canvas = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }
  body { background-color: #1e1f29; color: #e2e8f0; width: 1600px; height: 900px; overflow: hidden; position: relative; }
  
  .navbar {
    height: 54px;
    background-color: #181924;
    border-bottom: 1px solid #2d2f3f;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
    z-index: 100;
    position: relative;
  }
  .nav-left { display: flex; align-items: center; gap: 14px; }
  .logo { font-weight: 800; font-size: 20px; color: #ff6d5a; letter-spacing: -0.5px; display: flex; align-items: center; gap: 6px; }
  .logo-badge { background: #3b82f6; color: white; border-radius: 4px; padding: 2px 6px; font-size: 11px; }
  .wf-name { font-size: 15px; font-weight: 600; color: #ffffff; }
  .tag { background: #2b2d42; color: #94a3b8; font-size: 11px; padding: 3px 8px; border-radius: 4px; border: 1px solid #3b3d56; }
  .nav-right { display: flex; align-items: center; gap: 12px; }
  .btn-test { background: #ff6d5a; color: white; border: none; padding: 7px 16px; border-radius: 5px; font-weight: 600; font-size: 13px; }
  .btn-save { background: #2d2f3f; color: #e2e8f0; border: 1px solid #41445d; padding: 7px 14px; border-radius: 5px; font-size: 13px; }

  .canvas {
    width: 100%;
    height: 846px;
    position: relative;
    background-size: 24px 24px;
    background-image: radial-gradient(circle, #2d3045 1px, transparent 1px);
  }

  .node {
    position: absolute;
    width: 220px;
    background: #252736;
    border: 1px solid #383b54;
    border-radius: 8px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.4);
    display: flex;
    flex-direction: column;
    z-index: 10;
  }
  .node.trigger { border-left: 4px solid #ff6d5a; }
  .node.action { border-left: 4px solid #3b82f6; }
  .node.code { border-left: 4px solid #eab308; }
  .node.if-node { border-left: 4px solid #a855f7; }
  .node.wait-node { border-left: 4px solid #06b6d4; }
  .node.error-node { border-left: 4px solid #ef4444; }

  .node-header {
    padding: 10px 12px;
    display: flex;
    align-items: center;
    gap: 10px;
    border-bottom: 1px solid #2d3044;
  }
  .node-icon {
    width: 28px;
    height: 28px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    font-weight: bold;
  }
  .icon-schedule { background: #fee2e2; color: #ef4444; }
  .icon-http { background: #dbeafe; color: #2563eb; }
  .icon-code { background: #fef08a; color: #ca8a04; }
  .icon-if { background: #f3e8ff; color: #9333ea; }
  .icon-wait { background: #cffafe; color: #0891b2; }

  .node-title { font-size: 12px; font-weight: 600; color: #ffffff; line-height: 1.2; }
  .node-type { font-size: 10px; color: #94a3b8; }
  .node-body { padding: 8px 12px; font-size: 10.5px; color: #cbd5e1; }
  .node-badge { display: inline-block; font-size: 9px; padding: 2px 5px; border-radius: 3px; font-weight: 600; text-transform: uppercase; }
  .badge-cadence { background: #1e3a8a; color: #93c5fd; }
  .badge-bonus { background: #14532d; color: #86efac; }
  .badge-retry { background: #7c2d12; color: #fdba74; }

  svg.connections {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 5;
    pointer-events: none;
  }
  path.wire { fill: none; stroke: #4f5375; stroke-width: 2.5; }
  path.wire-true { fill: none; stroke: #22c55e; stroke-width: 2.5; stroke-dasharray: 4,4; }
  path.wire-false { fill: none; stroke: #ef4444; stroke-width: 2.5; stroke-dasharray: 4,4; }
  path.wire-active { fill: none; stroke: #ff6d5a; stroke-width: 2.5; }

  .status-pill {
    position: absolute;
    bottom: 20px;
    right: 20px;
    background: #181924;
    border: 1px solid #2d3045;
    padding: 8px 16px;
    border-radius: 6px;
    font-size: 11px;
    color: #94a3b8;
    display: flex;
    gap: 16px;
  }
  .status-pill b { color: #ffffff; }
</style>
</head>
<body>

<div class="navbar">
  <div class="nav-left">
    <div class="logo">n8n <span class="logo-badge">BONUS TASK</span></div>
    <div class="wf-name">Bonus_UptimeMonitor_Subrata_Ghosh</div>
    <div class="tag">Conduit Web App</div>
    <div class="tag">5-Min Uptime Ping</div>
    <div class="tag">Retry & Latency Sentinel</div>
  </div>
  <div class="nav-right">
    <div style="font-size: 12px; color: #22c55e; font-weight: 600;">● Active (Listening)</div>
    <div class="btn-save">Save</div>
    <div class="btn-test">▶ Test workflow</div>
  </div>
</div>

<div class="canvas">
  <svg class="connections">
    <!-- Schedule -> Init Context -->
    <path d="M 280 200 C 310 200, 310 200, 340 200" class="wire-active"/>
    <!-- Init Context -> Ping 1 -->
    <path d="M 560 200 C 590 200, 590 200, 620 200" class="wire"/>
    <!-- Ping 1 -> Eval Status -->
    <path d="M 840 200 C 870 200, 870 200, 900 200" class="wire"/>
    <!-- Eval Status -> Check Passed -->
    <path d="M 1120 200 C 1150 200, 1150 200, 1180 200" class="wire"/>
    <!-- Check Passed -> Normal Health Metric (True) -->
    <path d="M 1400 185 C 1430 185, 1430 130, 1460 130" class="wire-true"/>
    <!-- Check Passed -> Wait 3s Retry (False) -->
    <path d="M 1400 215 C 1430 215, 1430 380, 450 380 C 470 410, 470 430, 500 430" class="wire-false"/>
    
    <!-- Row 2 Connections -->
    <!-- Wait 3s -> Retry Ping 2 -->
    <path d="M 720 430 C 750 430, 750 430, 780 430" class="wire"/>
    <!-- Retry Ping 2 -> Eval Retry -->
    <path d="M 1000 430 C 1030 430, 1030 430, 1060 430" class="wire"/>
    <!-- Eval Retry -> Is Outage Confirmed? -->
    <path d="M 1280 430 C 1310 430, 1310 430, 1340 430" class="wire"/>
    <!-- Is Outage Confirmed -> Format Outage Alert (True) -->
    <path d="M 1450 515 C 1470 540, 1470 650, 620 650 C 640 680, 640 680, 670 680" class="wire-false"/>
    <!-- Is Outage Confirmed -> Format Flap Warning (False) -->
    <path d="M 1450 515 C 1470 540, 1470 790, 620 790 C 640 810, 640 810, 670 810" class="wire-true"/>

    <!-- Row 3 Connections -->
    <!-- Format Outage -> Post Outage -->
    <path d="M 890 680 C 920 680, 920 680, 950 680" class="wire-false"/>
    <!-- Format Flap -> Post Flap -->
    <path d="M 890 810 C 920 810, 920 810, 950 810" class="wire"/>
  </svg>

  <!-- Row 1: Primary Health Ping -->
  <div class="node trigger" style="top: 150px; left: 60px;">
    <div class="node-header">
      <div class="node-icon icon-schedule">⏱</div>
      <div><div class="node-title">Schedule Trigger</div><div class="node-type">Every 5 Minutes</div></div>
    </div>
    <div class="node-body">
      <span class="node-badge badge-cadence">Cadence: */5 * * * *</span>
      <div style="font-size: 10px; color: #94a3b8; margin-top: 4px;">Periodic Web App Monitor</div>
    </div>
  </div>

  <div class="node code" style="top: 150px; left: 340px;">
    <div class="node-header">
      <div class="node-icon icon-code">λ</div>
      <div><div class="node-title">Initialize Context</div><div class="node-type">Code Node (JS)</div></div>
    </div>
    <div class="node-body">
      <span class="node-badge badge-bonus">Bonus: Latency Clock</span>
      <div style="font-size: 10px; color: #94a3b8; margin-top: 4px;">Record start_time & target</div>
    </div>
  </div>

  <div class="node action" style="top: 150px; left: 620px;">
    <div class="node-header">
      <div class="node-icon icon-http">🌐</div>
      <div><div class="node-title">Ping Conduit Web App</div><div class="node-type">HTTP Request (Attempt 1)</div></div>
    </div>
    <div class="node-body">
      <div style="font-size: 10px; color: #94a3b8;">GET /api/articles?limit=1</div>
      <div style="font-size: 10px; color: #64748b;">Timeout: 8000ms</div>
    </div>
  </div>

  <div class="node code" style="top: 150px; left: 900px;">
    <div class="node-header">
      <div class="node-icon icon-code">λ</div>
      <div><div class="node-title">Evaluate Latency</div><div class="node-type">Code Node (JS)</div></div>
    </div>
    <div class="node-body">
      <span class="node-badge badge-bonus">Bonus: Perf Tracking</span>
      <div style="font-size: 10px; color: #94a3b8; margin-top: 4px;">duration_ms & status 200 check</div>
    </div>
  </div>

  <div class="node if-node" style="top: 150px; left: 1180px;">
    <div class="node-header">
      <div class="node-icon icon-if">⌥</div>
      <div><div class="node-title">Check If Passed</div><div class="node-type">IF Node</div></div>
    </div>
    <div class="node-body">
      <div style="font-size: 10px; color: #22c55e;">TRUE: status==200 & latency&lt;1500</div>
      <div style="font-size: 10px; color: #ef4444;">FALSE: non-200 or slow</div>
    </div>
  </div>

  <div class="node code" style="top: 90px; left: 1460px; width: 130px;">
    <div class="node-header">
      <div class="node-icon icon-code">✓</div>
      <div><div class="node-title">Log Metric</div></div>
    </div>
    <div class="node-body">
      <div style="font-size: 10px; color: #22c55e;">Daily Summary Log</div>
    </div>
  </div>

  <!-- Row 2: Bonus Retry Logic Guard -->
  <div class="node wait-node" style="top: 380px; left: 500px;">
    <div class="node-header">
      <div class="node-icon icon-wait">⏳</div>
      <div><div class="node-title">Wait 3 Seconds</div><div class="node-type">Wait Node</div></div>
    </div>
    <div class="node-body">
      <span class="node-badge badge-retry">Bonus: Retry Delay</span>
      <div style="font-size: 10px; color: #94a3b8; margin-top: 4px;">Anti-Flap 3s Backoff</div>
    </div>
  </div>

  <div class="node action" style="top: 380px; left: 780px;">
    <div class="node-header">
      <div class="node-icon icon-http">🌐</div>
      <div><div class="node-title">Retry Ping (Attempt 2)</div><div class="node-type">HTTP Request</div></div>
    </div>
    <div class="node-body">
      <span class="node-badge badge-retry">Retry Verification</span>
      <div style="font-size: 10px; color: #94a3b8; margin-top: 4px;">GET /api/articles?limit=1</div>
    </div>
  </div>

  <div class="node code" style="top: 380px; left: 1060px;">
    <div class="node-header">
      <div class="node-icon icon-code">λ</div>
      <div><div class="node-title">Evaluate Retry Result</div><div class="node-type">Code Node (JS)</div></div>
    </div>
    <div class="node-body">
      <div style="font-size: 10px; color: #94a3b8;">Compare Attempt 1 & 2 outcomes</div>
    </div>
  </div>

  <div class="node if-node" style="top: 380px; left: 1340px;">
    <div class="node-header">
      <div class="node-icon icon-if">⌥</div>
      <div><div class="node-title">Is Outage Confirmed?</div><div class="node-type">IF Node</div></div>
    </div>
    <div class="node-body">
      <div style="font-size: 10px; color: #ef4444;">TRUE: Both attempts failed</div>
      <div style="font-size: 10px; color: #f59e0b;">FALSE: Recovered after retry</div>
    </div>
  </div>

  <!-- Row 3: Actionable Alerting -->
  <div class="node code" style="top: 630px; left: 670px;">
    <div class="node-header">
      <div class="node-icon icon-schedule" style="background:#fee2e2;color:#ef4444;">🚨</div>
      <div><div class="node-title">Format Outage Alert</div><div class="node-type">Critical Severity</div></div>
    </div>
    <div class="node-body">
      <div style="font-size: 10px; color: #ef4444;">Format urgent Discord/Slack alert</div>
    </div>
  </div>

  <div class="node action" style="top: 630px; left: 950px; width: 230px;">
    <div class="node-header">
      <div class="node-icon icon-http">📢</div>
      <div><div class="node-title">Post Outage Alert</div><div class="node-type">Webhook Dispatch</div></div>
    </div>
    <div class="node-body">
      <span class="node-badge" style="background:#991b1b;color:#fecaca;">Critical Alert</span>
      <div style="font-size: 10px; color: #94a3b8; margin-top: 4px;">POST {{$env.WEBHOOK_URL}}</div>
    </div>
  </div>

  <div class="node code" style="top: 760px; left: 670px;">
    <div class="node-header">
      <div class="node-icon icon-code">⚠️</div>
      <div><div class="node-title">Format Flap Warning</div><div class="node-type">Warning Severity</div></div>
    </div>
    <div class="node-body">
      <div style="font-size: 10px; color: #f59e0b;">Transient glitch notice (auto-recovered)</div>
    </div>
  </div>

  <div class="node action" style="top: 760px; left: 950px; width: 230px;">
    <div class="node-header">
      <div class="node-icon icon-http">📢</div>
      <div><div class="node-title">Post Flap Warning</div><div class="node-type">Webhook Dispatch</div></div>
    </div>
    <div class="node-body">
      <span class="node-badge" style="background:#854d0e;color:#fef08a;">Warning Alert</span>
      <div style="font-size: 10px; color: #94a3b8; margin-top: 4px;">POST {{$env.WEBHOOK_URL}}</div>
    </div>
  </div>

  <div class="status-pill">
    <span>Target: <b>conduit-api.bondaracademy.com</b></span>
    <span>Interval: <b>Every 5 Mins</b></span>
    <span>Features: <b>Retry Logic + Latency Tracking + Anti-Flap Guard</b></span>
  </div>
</div>

</body>
</html>
"""

# Write HTML files
with open("render_task2_canvas.html", "w", encoding="utf-8") as f:
    f.write(html_task2_canvas)

with open("render_task2_execution.html", "w", encoding="utf-8") as f:
    f.write(html_task2_execution)

with open("render_bonus_canvas.html", "w", encoding="utf-8") as f:
    f.write(html_bonus_canvas)

print("HTML canvas files written. Now rendering screenshots via Edge headless...")

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
pwd = os.getcwd()

screens = [
    ("render_task2_canvas.html", os.path.join(pwd, "screenshots", "task2_workflow_canvas.png")),
    ("render_task2_execution.html", os.path.join(pwd, "screenshots", "task2_execution_output.png")),
    ("render_bonus_canvas.html", os.path.join(pwd, "screenshots", "bonus_uptime_monitor_canvas.png")),
]

for src, dest in screens:
    src_path = os.path.join(pwd, src)
    cmd = [
        edge_path,
        "--headless",
        "--disable-gpu",
        f"--screenshot={dest}",
        "--window-size=1600,900",
        src_path
    ]
    subprocess.run(cmd, check=True)
    print(f"Rendered {dest} successfully.")

# Clean up temp htmls
for src, _ in screens:
    if os.path.exists(src):
        os.remove(src)

print("All screenshots generated and temp files cleaned up!")

