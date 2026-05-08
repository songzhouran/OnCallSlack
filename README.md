# OnCallSlack

AI-powered Slack assistant for automated incident triage and on-call response.

---

## Overview

OnCallSlack is a lightweight AI automation tool designed to assist operational Slack channels by acting as a first-line on-call responder.

The system monitors selected Slack channels through browser automation, detects trigger messages, generates contextual AI responses using LLMs, and replies directly inside Slack.

This project is intended for internal operational workflows, alert triage, and engineering support automation where official Slack App permissions are unavailable.

---

## Features

* Automated Slack message monitoring
* AI-generated contextual responses
* Trigger-based alert handling
* Persistent Slack login sessions
* Configurable channel targeting
* Configurable trigger keywords
* Human-like typing simulation
* Duplicate message protection
* Lightweight browser-based architecture
* Groq / OpenAI compatible APIs

---

## Architecture

```text
Slack Channel
      ↓
Playwright Listener
      ↓
Message Filtering
      ↓
LLM Processing
      ↓
AI Response Generation
      ↓
Slack Auto Reply
```

---

## Tech Stack

* Python 3.12+
* Playwright
* Groq API / OpenAI-compatible APIs
* Chromium Persistent Context
* dotenv

---

## Installation

### Clone Repository

```bash
git clone <repository-url>

cd opspilot
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Install Playwright Browser

```bash
playwright install
```

---

## Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=gsk_xxx

CHANNEL_URL=https://app.slack.com/client/TXXXX/CXXXX

TRIGGER_WORDS=@jack,bot,urgent
```

---

## Running

```bash
python main.py
```

On first launch:

1. Log into Slack manually
2. Open the target channel
3. Session data will persist locally in `./slack_profile`

Subsequent launches reuse the existing authenticated session automatically.

---

## Example Workflow

```text
User:
@jack database latency increased

↓
OnCallSlack detects trigger word

↓
LLM generates contextual response

↓
Bot replies in Slack channel
```

---

## Configuration

### Trigger Keywords

Configured through:

```env
TRIGGER_WORDS=@jack,bot,urgent
```

### Slack Channel

Configured through:

```env
CHANNEL_URL=https://app.slack.com/client/TXXXX/CXXXX
```

---

## Current Limitations

* Browser automation based
* Single-channel optimized
* No official Slack Events API integration
* Requires persistent Chromium session
* Intended for low-frequency operational workflows

---

## Roadmap

* Thread replies
* Context-aware memory
* Runbook retrieval
* Incident summarization
* Jira integration
* PagerDuty integration
* Multi-channel support
* Knowledge base retrieval
* RAG-based operational assistance

---

## Security Notes

This project uses browser automation instead of official Slack APIs.

Recommended usage:

* Internal environments only
* Low-frequency operational workflows
* Dedicated Slack account/profile
* Non-production experimentation before broader rollout
