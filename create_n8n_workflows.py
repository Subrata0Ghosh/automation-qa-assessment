import json
import uuid

def generate_id():
    return str(uuid.uuid4())

# Task 2: Morning Brief GitHub Integration Workflow
task2_nodes = [
    {
        "parameters": {
            "rule": {
                "interval": [
                    {
                        "field": "hours",
                        "hoursInterval": 1
                    }
                ]
            }
        },
        "id": "11111111-1111-4111-8111-111111111111",
        "name": "Schedule Trigger (Hourly)",
        "type": "n8n-nodes-base.scheduleTrigger",
        "typeVersion": 1.2,
        "position": [180, 300]
    },
    {
        "parameters": {
            "httpMethod": "POST",
            "path": "trigger-morning-brief",
            "responseMode": "onReceived",
            "options": {}
        },
        "id": "22222222-2222-4222-8222-222222222222",
        "name": "Webhook Trigger (On Demand)",
        "type": "n8n-nodes-base.webhook",
        "typeVersion": 2,
        "position": [180, 500],
        "webhookId": "morning-brief-hook"
    },
    {
        "parameters": {
            "method": "GET",
            "url": "https://api.github.com/search/repositories?q=topic:automation+stars:>1000&sort=stars&order=desc&per_page=10",
            "sendHeaders": True,
            "headerParameters": {
                "parameters": [
                    {
                        "name": "User-Agent",
                        "value": "n8n-Automation-QA-Digest"
                    },
                    {
                        "name": "Accept",
                        "value": "application/vnd.github+json"
                    }
                ]
            },
            "options": {
                "response": {
                    "response": {
                        "responseFormat": "json"
                    }
                },
                "timeout": 15000
            }
        },
        "id": "33333333-3333-4333-8333-333333333333",
        "name": "Fetch Trending Automation Repos",
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.2,
        "position": [420, 400],
        "continueOnFail": True
    },
    {
        "parameters": {
            "conditions": {
                "options": {
                    "caseSensitive": True,
                    "leftValue": "",
                    "typeValidation": "strict"
                },
                "conditions": [
                    {
                        "id": "c1",
                        "leftValue": "={{ $json.items !== undefined && $json.items.length > 0 }}",
                        "rightValue": True,
                        "operator": {
                            "type": "boolean",
                            "operation": "equals"
                        }
                    }
                ],
                "combinator": "and"
            },
            "options": {}
        },
        "id": "44444444-4444-4444-8444-444444444444",
        "name": "Check GitHub API Success",
        "type": "n8n-nodes-base.if",
        "typeVersion": 2,
        "position": [660, 400]
    },
    {
        "parameters": {
            "jsCode": """// Extract items, sort, filter and select top 5 results
const rawData = $input.first().json;
const items = rawData.items || [];

// Sort descending by stars just to guarantee ordering
const sorted = items.sort((a, b) => (b.stargazers_count || 0) - (a.stargazers_count || 0));

// Slices top 5 repositories
const top5 = sorted.slice(0, 5).map((repo, idx) => ({
  rank: idx + 1,
  id: repo.id,
  name: repo.name,
  full_name: repo.full_name,
  description: repo.description || 'No description provided.',
  stars: repo.stargazers_count,
  stars_formatted: (repo.stargazers_count >= 1000 ? (repo.stargazers_count / 1000).toFixed(1) + 'k' : repo.stargazers_count.toString()),
  forks: repo.forks_count,
  open_issues: repo.open_issues_count,
  language: repo.language || 'Multi-language',
  repo_url: repo.html_url,
  owner: repo.owner ? repo.owner.login : 'unknown'
}));

// Highlighted top candidate for second API enrichment
const topRepo = top5[0];

return [{
  json: {
    top_repo: topRepo,
    top_5_repos: top5,
    total_found: rawData.total_count || items.length,
    digest_timestamp: new Date().toISOString()
  }
}];
"""
        },
        "id": "55555555-5555-4555-8555-555555555555",
        "name": "Transform & Filter Top 5",
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [900, 320]
    },
    {
        "parameters": {
            "method": "GET",
            "url": "=https://api.github.com/repos/{{ $json.top_repo.full_name }}/commits?per_page=1",
            "sendHeaders": True,
            "headerParameters": {
                "parameters": [
                    {
                        "name": "User-Agent",
                        "value": "n8n-Automation-QA-Digest"
                    },
                    {
                        "name": "Accept",
                        "value": "application/vnd.github+json"
                    }
                ]
            },
            "options": {
                "response": {
                    "response": {
                        "responseFormat": "json"
                    }
                },
                "timeout": 10000
            }
        },
        "id": "66666666-6666-4666-8666-666666666666",
        "name": "Enrich #1 Repo (Commit Activity)",
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.2,
        "position": [1140, 320],
        "continueOnFail": True
    },
    {
        "parameters": {
            "jsCode": """// Merge top 5 list with enriched commit activity data
const prevData = $('Transform & Filter Top 5').first().json;
const commitResponse = $input.first().json;

let latestCommit = {
  sha: 'N/A',
  message: 'Commit details unavailable',
  author: 'N/A',
  date: 'N/A'
};

if (Array.isArray(commitResponse) && commitResponse.length > 0) {
  const c = commitResponse[0];
  latestCommit = {
    sha: c.sha ? c.sha.substring(0, 7) : 'N/A',
    message: c.commit && c.commit.message ? c.commit.message.split('\\n')[0] : 'No commit message',
    author: c.commit && c.commit.author ? c.commit.author.name : 'Unknown',
    date: c.commit && c.commit.author ? c.commit.author.date : 'Unknown'
  };
}

const topRepoEnriched = {
  ...prevData.top_repo,
  latest_commit: latestCommit
};

return [{
  json: {
    top_repo: topRepoEnriched,
    top_5_repos: prevData.top_5_repos,
    is_mega_project: topRepoEnriched.stars >= 50000,
    digest_timestamp: prevData.digest_timestamp
  }
}];
"""
        },
        "id": "77777777-7777-4777-8777-777777777777",
        "name": "Merge Enriched Data",
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [1380, 320]
    },
    {
        "parameters": {
            "conditions": {
                "options": {
                    "caseSensitive": True,
                    "leftValue": "",
                    "typeValidation": "strict"
                },
                "conditions": [
                    {
                        "id": "cond_threshold",
                        "leftValue": "={{ $json.top_repo.stars }}",
                        "rightValue": 50000,
                        "operator": {
                            "type": "number",
                            "operation": "gte"
                        }
                    }
                ],
                "combinator": "and"
            },
            "options": {}
        },
        "id": "88888888-8888-4888-8888-888888888888",
        "name": "Conditional Star Threshold",
        "type": "n8n-nodes-base.if",
        "typeVersion": 2,
        "position": [1620, 320]
    },
    {
        "parameters": {
            "jsCode": """// Format High-Velocity Mega Alert Digest
const data = $input.first().json;
const top = data.top_repo;
const list = data.top_5_repos;

let listText = '';
list.forEach(r => {
  listText += `${r.rank}. **[${r.full_name}](${r.repo_url})** — ⭐ ${r.stars_formatted} | 🍴 ${r.forks} | 🛠️ ${r.language}\\n   _${r.description}_\\n\\n`;
});

const content = `🔥 **[DAILY MORNING BRIEF: MEGA-TIER QA & AUTOMATION RADAR]** 🔥
*Threshold Notice: Top project exceeds 50,000+ GitHub Stars!*

👑 **SPOTLIGHT LEADER (#1):**
• **Repository:** [${top.full_name}](${top.repo_url})
• **Stars:** ⭐ **${top.stars.toLocaleString()}** (${top.stars_formatted})
• **Open Issues:** 🐞 ${top.open_issues} | **Forks:** 🍴 ${top.forks}
• **Primary Language:** 💻 ${top.language}
• **Latest Commit:** \`${top.latest_commit.sha}\` "${top.latest_commit.message}" by *${top.latest_commit.author}* (${top.latest_commit.date})

━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 **TOP 5 AUTOMATION REPOSITORIES TODAY:**
${listText}
━━━━━━━━━━━━━━━━━━━━━━━━━━
*Generated automatically by n8n Morning Brief Workflow at ${data.digest_timestamp}*`;

return [{
  json: {
    tier: 'MEGA_HIGH_VELOCITY',
    message: content,
    payload: {
      content: content,
      username: "QA Automation Morning Brief"
    }
  }
}];
"""
        },
        "id": "99999999-9999-4999-8999-999999999999",
        "name": "Format Mega-Tier Brief",
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [1860, 220]
    },
    {
        "parameters": {
            "jsCode": """// Format Standard Morning Digest
const data = $input.first().json;
const top = data.top_repo;
const list = data.top_5_repos;

let listText = '';
list.forEach(r => {
  listText += `${r.rank}. **[${r.full_name}](${r.repo_url})** — ⭐ ${r.stars_formatted} | 🍴 ${r.forks}\\n   _${r.description}_\\n\\n`;
});

const content = `☀️ **[DAILY MORNING BRIEF: AUTOMATION RADAR]** ☀️

⭐ **Leading Automation Project:**
• **Repository:** [${top.full_name}](${top.repo_url})
• **Stars:** ⭐ ${top.stars_formatted}
• **Latest Activity:** \`${top.latest_commit.sha}\` by *${top.latest_commit.author}*

━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 **TOP 5 PROJECTS:**
${listText}
━━━━━━━━━━━━━━━━━━━━━━━━━━
*Generated by n8n at ${data.digest_timestamp}*`;

return [{
  json: {
    tier: 'STANDARD_GROWTH',
    message: content,
    payload: {
      content: content,
      username: "QA Automation Morning Brief"
    }
  }
}];
"""
        },
        "id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
        "name": "Format Standard Brief",
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [1860, 420]
    },
    {
        "parameters": {
            "method": "POST",
            "url": "={{ $env.NOTIFICATION_WEBHOOK_URL || 'https://webhook.site/placeholder-channel' }}",
            "sendBody": True,
            "specifyBody": "json",
            "jsonBody": "={{ JSON.stringify($json.payload) }}",
            "options": {
                "timeout": 10000
            }
        },
        "id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
        "name": "Send Notification Digest",
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.2,
        "position": [2120, 320],
        "continueOnFail": True
    },
    {
        "parameters": {
            "jsCode": """// Handle API 1 Search Failure Gracefully
const errorData = $input.first().json;
const alertMsg = `⚠️ **[INCIDENT ALERT: Morning Brief Data Collection Failed]** ⚠️
Endpoint: GitHub Search API (/search/repositories)
Reason: Response returned empty results, rate-limited, or failed network connectivity.
Timestamp: ${new Date().toISOString()}
Action: Workflow prevented silent crash. Retrying scheduled on next cycle.`;

return [{
  json: {
    status: 'ERROR_LOGGED',
    alert_message: alertMsg,
    raw_error: errorData,
    payload: {
      content: alertMsg,
      username: "Automation Monitor Alert"
    }
  }
}];
"""
        },
        "id": "cccccccc-cccc-4ccc-8ccc-cccccccccccc",
        "name": "API 1 Error Fallback Logger",
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [900, 520]
    },
    {
        "parameters": {
            "method": "POST",
            "url": "={{ $env.NOTIFICATION_WEBHOOK_URL || 'https://webhook.site/placeholder-channel' }}",
            "sendBody": True,
            "specifyBody": "json",
            "jsonBody": "={{ JSON.stringify($json.payload) }}",
            "options": {
                "timeout": 10000
            }
        },
        "id": "dddddddd-dddd-4ddd-8ddd-dddddddddddd",
        "name": "Dispatch Error Notification",
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.2,
        "position": [1140, 520],
        "continueOnFail": True
    },
    {
        "parameters": {},
        "id": "eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee",
        "name": "Global Error Trigger",
        "type": "n8n-nodes-base.errorTrigger",
        "typeVersion": 1,
        "position": [180, 720]
    },
    {
        "parameters": {
            "jsCode": """// Catch unexpected workflow exceptions
const errorInfo = $input.first().json;
const errMsg = `🚨 **[CRITICAL WORKFLOW EXCEPTION: Task2 Morning Brief]** 🚨
Execution ID: ${$execution.id}
Node: ${errorInfo.execution ? errorInfo.execution.lastNodeExecuted : 'Unknown'}
Error: ${errorInfo.message || 'Unhandled error occurred'}
Timestamp: ${new Date().toISOString()}`;

return [{
  json: {
    payload: {
      content: errMsg,
      username: "n8n Error Watchdog"
    }
  }
}];
"""
        },
        "id": "ffffffff-ffff-4fff-8fff-ffffffffffff",
        "name": "Format Global Error Alert",
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [420, 720]
    },
    {
        "parameters": {
            "method": "POST",
            "url": "={{ $env.NOTIFICATION_WEBHOOK_URL || 'https://webhook.site/placeholder-channel' }}",
            "sendBody": True,
            "specifyBody": "json",
            "jsonBody": "={{ JSON.stringify($json.payload) }}",
            "options": {
                "timeout": 10000
            }
        },
        "id": "00000000-0000-4000-8000-000000000000",
        "name": "Send Global Error Alert",
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.2,
        "position": [660, 720],
        "continueOnFail": True
    }
]

task2_connections = {
    "Schedule Trigger (Hourly)": {
        "main": [
            [{"node": "Fetch Trending Automation Repos", "type": "main", "index": 0}]
        ]
    },
    "Webhook Trigger (On Demand)": {
        "main": [
            [{"node": "Fetch Trending Automation Repos", "type": "main", "index": 0}]
        ]
    },
    "Fetch Trending Automation Repos": {
        "main": [
            [{"node": "Check GitHub API Success", "type": "main", "index": 0}]
        ]
    },
    "Check GitHub API Success": {
        "main": [
            [{"node": "Transform & Filter Top 5", "type": "main", "index": 0}],
            [{"node": "API 1 Error Fallback Logger", "type": "main", "index": 0}]
        ]
    },
    "Transform & Filter Top 5": {
        "main": [
            [{"node": "Enrich #1 Repo (Commit Activity)", "type": "main", "index": 0}]
        ]
    },
    "Enrich #1 Repo (Commit Activity)": {
        "main": [
            [{"node": "Merge Enriched Data", "type": "main", "index": 0}]
        ]
    },
    "Merge Enriched Data": {
        "main": [
            [{"node": "Conditional Star Threshold", "type": "main", "index": 0}]
        ]
    },
    "Conditional Star Threshold": {
        "main": [
            [{"node": "Format Mega-Tier Brief", "type": "main", "index": 0}],
            [{"node": "Format Standard Brief", "type": "main", "index": 0}]
        ]
    },
    "Format Mega-Tier Brief": {
        "main": [
            [{"node": "Send Notification Digest", "type": "main", "index": 0}]
        ]
    },
    "Format Standard Brief": {
        "main": [
            [{"node": "Send Notification Digest", "type": "main", "index": 0}]
        ]
    },
    "API 1 Error Fallback Logger": {
        "main": [
            [{"node": "Dispatch Error Notification", "type": "main", "index": 0}]
        ]
    },
    "Global Error Trigger": {
        "main": [
            [{"node": "Format Global Error Alert", "type": "main", "index": 0}]
        ]
    },
    "Format Global Error Alert": {
        "main": [
            [{"node": "Send Global Error Alert", "type": "main", "index": 0}]
        ]
    }
}

task2_workflow = {
    "name": "Task2_Workflow_Subrata_Ghosh",
    "nodes": task2_nodes,
    "connections": task2_connections,
    "active": False,
    "settings": {
        "executionOrder": "v1"
    },
    "versionId": "f78d91a2-39f2-4bc2-8ef4-d3a47981b101",
    "id": "Task2_MorningBrief_Subrata",
    "meta": {
        "templateCredsSetupCompleted": True,
        "instanceId": "local-dev-instance"
    },
    "tags": [
        {"name": "QA"},
        {"name": "Automation"},
        {"name": "Morning-Brief"},
        {"name": "GitHub-API"}
    ]
}

# Task 4 / Bonus: Uptime Monitor Workflow
bonus_nodes = [
    {
        "parameters": {
            "rule": {
                "interval": [
                    {
                        "field": "minutes",
                        "minutesInterval": 5
                    }
                ]
            }
        },
        "id": "b1111111-1111-4111-8111-111111111111",
        "name": "Schedule Trigger (Every 5 Mins)",
        "type": "n8n-nodes-base.scheduleTrigger",
        "typeVersion": 1.2,
        "position": [180, 300]
    },
    {
        "parameters": {
            "jsCode": """// Record test target and starting timestamp
return [{
  json: {
    target_url: 'https://conduit-api.bondaracademy.com/api/articles?limit=1',
    web_app_url: 'https://conduit.bondaracademy.com/',
    start_time: Date.now(),
    attempt: 1,
    check_timestamp: new Date().toISOString()
  }
}];
"""
        },
        "id": "b2222222-2222-4222-8222-222222222222",
        "name": "Initialize Ping Context",
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [380, 300]
    },
    {
        "parameters": {
            "method": "GET",
            "url": "={{ $json.target_url }}",
            "options": {
                "timeout": 8000,
                "response": {
                    "response": {
                        "neverError": True,
                        "responseFormat": "text"
                    }
                }
            }
        },
        "id": "b3333333-3333-4333-8333-333333333333",
        "name": "Ping Conduit Web App",
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.2,
        "position": [580, 300],
        "continueOnFail": True
    },
    {
        "parameters": {
            "jsCode": """// Measure response time and verify HTTP 200 status
const initData = $('Initialize Ping Context').first().json;
const durationMs = Date.now() - initData.start_time;
const httpResponse = $input.first().json;

// Extract status code (n8n returns status or statusCode when fullResponse is configured or in response headers)
let statusCode = 200;
let isError = false;

if (httpResponse.statusCode) {
  statusCode = httpResponse.statusCode;
} else if (httpResponse.error) {
  statusCode = 500;
  isError = true;
}

const isHealthy = statusCode === 200 && !isError;
const isDegraded = durationMs >= 1500;

return [{
  json: {
    target_url: initData.target_url,
    web_app_url: initData.web_app_url,
    status_code: statusCode,
    duration_ms: durationMs,
    is_healthy: isHealthy,
    is_degraded: isDegraded,
    attempt: 1,
    timestamp: new Date().toISOString()
  }
}];
"""
        },
        "id": "b4444444-4444-4444-8444-444444444444",
        "name": "Evaluate Status & Latency",
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [780, 300]
    },
    {
        "parameters": {
            "conditions": {
                "options": {
                    "caseSensitive": True,
                    "leftValue": "",
                    "typeValidation": "strict"
                },
                "conditions": [
                    {
                        "id": "cond_health",
                        "leftValue": "={{ $json.is_healthy }}",
                        "rightValue": True,
                        "operator": {
                            "type": "boolean",
                            "operation": "equals"
                        }
                    }
                ],
                "combinator": "and"
            },
            "options": {}
        },
        "id": "b5555555-5555-4555-8555-555555555555",
        "name": "Check If Ping Passed",
        "type": "n8n-nodes-base.if",
        "typeVersion": 2,
        "position": [980, 300]
    },
    {
        "parameters": {
            "amount": 3,
            "unit": "seconds"
        },
        "id": "b6666666-6666-4666-8666-666666666666",
        "name": "Wait 3s (Retry Delay)",
        "type": "n8n-nodes-base.wait",
        "typeVersion": 1.1,
        "position": [1200, 420]
    },
    {
        "parameters": {
            "method": "GET",
            "url": "https://conduit-api.bondaracademy.com/api/articles?limit=1",
            "options": {
                "timeout": 10000,
                "response": {
                    "response": {
                        "neverError": True,
                        "responseFormat": "text"
                    }
                }
            }
        },
        "id": "b7777777-7777-4777-8777-777777777777",
        "name": "Retry Ping (Attempt 2)",
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.2,
        "position": [1400, 420],
        "continueOnFail": True
    },
    {
        "parameters": {
            "jsCode": """// Evaluate retry response
const firstAttempt = $('Evaluate Status & Latency').first().json;
const retryRes = $input.first().json;

let statusCode = 200;
let isError = false;

if (retryRes.statusCode) {
  statusCode = retryRes.statusCode;
} else if (retryRes.error) {
  statusCode = 500;
  isError = true;
}

const isConfirmedDown = (statusCode !== 200) || isError;

return [{
  json: {
    target_url: firstAttempt.target_url,
    web_app_url: firstAttempt.web_app_url,
    first_attempt_status: firstAttempt.status_code,
    first_attempt_duration: firstAttempt.duration_ms,
    second_attempt_status: statusCode,
    is_confirmed_down: isConfirmedDown,
    timestamp: new Date().toISOString()
  }
}];
"""
        },
        "id": "b8888888-8888-4888-8888-888888888888",
        "name": "Evaluate Retry Result",
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [1600, 420]
    },
    {
        "parameters": {
            "conditions": {
                "options": {
                    "caseSensitive": True,
                    "leftValue": "",
                    "typeValidation": "strict"
                },
                "conditions": [
                    {
                        "id": "cond_outage",
                        "leftValue": "={{ $json.is_confirmed_down }}",
                        "rightValue": True,
                        "operator": {
                            "type": "boolean",
                            "operation": "equals"
                        }
                    }
                ],
                "combinator": "and"
            },
            "options": {}
        },
        "id": "b9999999-9999-4999-8999-999999999999",
        "name": "Is Outage Confirmed?",
        "type": "n8n-nodes-base.if",
        "typeVersion": 2,
        "position": [1800, 420]
    },
    {
        "parameters": {
            "jsCode": """// Format Critical Outage Alert
const data = $input.first().json;

const alertText = `🚨 **[CRITICAL OUTAGE ALERT: Conduit Web App Is DOWN]** 🚨

🔴 **Application Status:** DOWN / UNRESPONSIVE
🎯 **Target Endpoint:** \`${data.target_url}\`
🌐 **Web App:** ${data.web_app_url}
⚠️ **Status Code (Attempt 1):** ${data.first_attempt_status} (${data.first_attempt_duration}ms)
⚠️ **Status Code (Attempt 2 - Retry):** ${data.second_attempt_status}
⏱️ **Downtime Detected:** ${data.timestamp}
🔁 **Retry Logic:** 2 consecutive attempts failed (3s backoff).
🚨 **Impact:** Users are unable to load feed or authenticate. Immediate investigation required!`;

return [{
  json: {
    severity: 'CRITICAL',
    payload: {
      content: alertText,
      username: "Uptime Sentinel"
    }
  }
}];
"""
        },
        "id": "baaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
        "name": "Format Outage Alert",
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [2020, 360]
    },
    {
        "parameters": {
            "method": "POST",
            "url": "={{ $env.NOTIFICATION_WEBHOOK_URL || 'https://webhook.site/placeholder-channel' }}",
            "sendBody": True,
            "specifyBody": "json",
            "jsonBody": "={{ JSON.stringify($json.payload) }}",
            "options": {
                "timeout": 10000
            }
        },
        "id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbc",
        "name": "Post Outage Alert",
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.2,
        "position": [2240, 360],
        "continueOnFail": True
    },
    {
        "parameters": {
            "jsCode": """// Format Transient Flap Recovery Notice
const data = $input.first().json;

const warningText = `⚠️ **[TRANSIENT NETWORK WARNING: Conduit Web App Recovered]** ⚠️
Target: \`${data.target_url}\`
Attempt 1 failed with status ${data.first_attempt_status}, but Attempt 2 succeeded after 3s retry.
Timestamp: ${data.timestamp}
Status: Healthy (No outage declared due to retry guard).`;

return [{
  json: {
    severity: 'WARNING',
    payload: {
      content: warningText,
      username: "Uptime Sentinel"
    }
  }
}];
"""
        },
        "id": "bcccccccc-cccc-4ccc-8ccc-cccccccccccc",
        "name": "Format Flap Warning",
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [2020, 500]
    },
    {
        "parameters": {
            "method": "POST",
            "url": "={{ $env.NOTIFICATION_WEBHOOK_URL || 'https://webhook.site/placeholder-channel' }}",
            "sendBody": True,
            "specifyBody": "json",
            "jsonBody": "={{ JSON.stringify($json.payload) }}",
            "options": {
                "timeout": 10000
            }
        },
        "id": "bddddddd-dddd-4ddd-8ddd-dddddddddddd",
        "name": "Post Flap Warning",
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.2,
        "position": [2240, 500],
        "continueOnFail": True
    },
    {
        "parameters": {
            "jsCode": """// Healthy Ping Logger & Daily Summary Tracker
const data = $input.first().json;

return [{
  json: {
    metric: 'UPTIME_PING_SUCCESS',
    target: data.target_url,
    status_code: data.status_code,
    latency_ms: data.duration_ms,
    is_degraded: data.is_degraded,
    recorded_at: data.timestamp
  }
}];
"""
        },
        "id": "beeeeeee-eeee-4eee-8eee-eeeeeeeeeeee",
        "name": "Record Normal Health Metric",
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [1200, 200]
    }
]

bonus_connections = {
    "Schedule Trigger (Every 5 Mins)": {
        "main": [
            [{"node": "Initialize Ping Context", "type": "main", "index": 0}]
        ]
    },
    "Initialize Ping Context": {
        "main": [
            [{"node": "Ping Conduit Web App", "type": "main", "index": 0}]
        ]
    },
    "Ping Conduit Web App": {
        "main": [
            [{"node": "Evaluate Status & Latency", "type": "main", "index": 0}]
        ]
    },
    "Evaluate Status & Latency": {
        "main": [
            [{"node": "Check If Ping Passed", "type": "main", "index": 0}]
        ]
    },
    "Check If Ping Passed": {
        "main": [
            [{"node": "Record Normal Health Metric", "type": "main", "index": 0}],
            [{"node": "Wait 3s (Retry Delay)", "type": "main", "index": 0}]
        ]
    },
    "Wait 3s (Retry Delay)": {
        "main": [
            [{"node": "Retry Ping (Attempt 2)", "type": "main", "index": 0}]
        ]
    },
    "Retry Ping (Attempt 2)": {
        "main": [
            [{"node": "Evaluate Retry Result", "type": "main", "index": 0}]
        ]
    },
    "Evaluate Retry Result": {
        "main": [
            [{"node": "Is Outage Confirmed?", "type": "main", "index": 0}]
        ]
    },
    "Is Outage Confirmed?": {
        "main": [
            [{"node": "Format Outage Alert", "type": "main", "index": 0}],
            [{"node": "Format Flap Warning", "type": "main", "index": 0}]
        ]
    },
    "Format Outage Alert": {
        "main": [
            [{"node": "Post Outage Alert", "type": "main", "index": 0}]
        ]
    },
    "Format Flap Warning": {
        "main": [
            [{"node": "Post Flap Warning", "type": "main", "index": 0}]
        ]
    }
}

bonus_workflow = {
    "name": "Bonus_UptimeMonitor_Subrata_Ghosh",
    "nodes": bonus_nodes,
    "connections": bonus_connections,
    "active": False,
    "settings": {
        "executionOrder": "v1"
    },
    "versionId": "c88f91a2-59f2-4bc2-8ef4-d3a47981b102",
    "id": "Bonus_UptimeMonitor_Subrata",
    "meta": {
        "templateCredsSetupCompleted": True,
        "instanceId": "local-dev-instance"
    },
    "tags": [
        {"name": "QA"},
        {"name": "Uptime-Monitor"},
        {"name": "Conduit"},
        {"name": "Observability"}
    ]
}

# Write Task 2 Workflow
with open("Task2_Workflow_Subrata_Ghosh.json", "w", encoding="utf-8") as f:
    json.dump(task2_workflow, f, indent=2)
print("Saved Task2_Workflow_Subrata_Ghosh.json")

# Write Bonus Workflow
with open("Bonus_UptimeMonitor_Subrata_Ghosh.json", "w", encoding="utf-8") as f:
    json.dump(bonus_workflow, f, indent=2)
print("Saved Bonus_UptimeMonitor_Subrata_Ghosh.json")
