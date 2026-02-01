# DevLint 🛡️

**Stop secrets, stale PRs, and Docker bloat before they reach production.**

<p align="center">
  <img src="https://res.cloudinary.com/ds1dhvevo/image/upload/v1769977780/Screenshot_2026-02-02_004045_t6edq4.png" alt="DevLint Secret Detection" width="800"/>
</p>

<p align="center">
  <a href="#-installation">Installation</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-features">Features</a> •
  <a href="#-github-action">GitHub Action</a> •
  <a href="#-contributing">Contributing</a>
</p>

---

## 💭 Why DevLint?

I pushed a Stripe API key to production once. Spent 2 hours rotating keys, checking logs, and explaining to my team how it happened.

That's when I realized: **developers need prevention, not just debugging.**

DevLint catches mistakes **before** they become incidents. It's the pre-flight checklist you wish you had.

---

## 🎯 Real Problems It Solves

| Problem | Solution |
|---------|----------|
| 🔒 **Accidentally committed AWS keys** | Detects 15+ secret types before commit |
| ⚠️ **Merged stale PR (50 commits behind)** | Shows conflicts & risk before merge |
| 🐛 **"Port 3000 already in use"** | Finds process instantly, one-click kill |
| 📦 **5GB Docker image (should be 500MB)** | Layer analysis + optimization tips |

---

## 📦 Installation

### From GitHub (Recommended)

```bash
pip install git+https://github.com/MayankRajeevkumarShukla/devlint.git
```

### Or Clone & Install Locally

```bash
git clone https://github.com/MayankRajeevkumarShukla/devlint.git
cd devlint
pip install -e .
```

### Verify Installation

```bash
devlint --version
```

---

## 🚀 Quick Start

```bash
# Before committing - catch secrets
devlint secrets

# Before creating PR - check if branch is safe
devlint pre-pr

# Port conflict? Find what's using it
devlint ports

# Optimize Docker images
devlint docker my-app:latest
```

---

## ✨ Features

### 🔒 Secret Detection

Catches API keys, tokens, and passwords **before** you commit them.

```bash
devlint secrets
```

**Detects:**
- AWS Access Keys (`AKIA...`)
- GitHub Personal Tokens (`ghp_...`)
- Stripe API Keys (`sk_live_...`)
- Slack Tokens (`xoxb-...`)
- Private SSH Keys
- Generic API keys and passwords
- Environment variables leaked in code

<p align="center">
  <img src="https://res.cloudinary.com/ds1dhvevo/image/upload/v1769977780/Screenshot_2026-02-02_004045_t6edq4.png" alt="Secret Detection Example" width="700"/>
</p>

**Real-world impact:**
- ✅ Prevents credential leaks to public repos
- ✅ Stops secrets from entering git history
- ✅ Saves hours of key rotation and incident response

---

### ⚠️ PR Safety Check

Know **before** merging if your PR will cause problems.

```bash
devlint pre-pr
```

**Checks:**
- How many commits behind `main`
- Predicts merge conflicts (file + line numbers)
- Shows who else modified the same files
- Calculates risk level (LOW/MEDIUM/HIGH)
- Gives actionable recommendations

<p align="center">
  <img src="https://res.cloudinary.com/ds1dhvevo/image/upload/v1769977766/Screenshot_2026-02-02_005651_nkdslc.png" alt="PR Safety Check" width="700"/>
</p>

**Example Output:**

```
╔════════════════════════════════════════╗
║         PR SAFETY CHECK                ║
╚════════════════════════════════════════╝

Branch: feature-login
Target: main

✅ Up to date (0 commits behind)
✅ No conflicts detected
✅ All checks passed

Risk Level: LOW 🟢
Recommendation: Safe to merge
```

**Real-world impact:**
- ✅ Prevents merge conflicts and rework
- ✅ Reduces "it worked on my machine" incidents
- ✅ Saves teams hours of conflict resolution

---

### 🔌 Port Checker

Stop wasting time with `lsof` and `kill`.

```bash
devlint ports
```

**Shows:**
- All ports currently in use
- Process name (e.g., `node`, `postgres`, `redis`)
- PID for easy killing
- Port number

<p align="center">
  <img src="https://res.cloudinary.com/ds1dhvevo/image/upload/v1769977873/Screenshot_2026-02-02_020058_qvrjls.png" alt="Port Checker" width="700"/>
</p>

**Quick kill:**
```bash
devlint ports
# See port 3000 is used by PID 12345
kill 12345
```

**Real-world impact:**
- ✅ Instantly find what's blocking your port
- ✅ No more cryptic "EADDRINUSE" errors
- ✅ Works across all platforms

---

### 🐳 Docker Image Analyzer

Find out **why** your Docker image is 5GB.

```bash
devlint docker my-app:latest
```

**Provides:**
- Layer-by-layer size breakdown
- Identifies largest layers
- Shows what's consuming space
- Suggests optimizations
- Estimates potential savings

<p align="center">
  <img src="https://res.cloudinary.com/ds1dhvevo/image/upload/v1769977794/Screenshot_2026-02-02_002511_snzcr1.png" alt="Docker Analysis" width="700"/>
</p>

**Example insights:**
```
📦 Layer Analysis:

Layer 1: 800MB - apt-get install (consider multi-stage build)
Layer 2: 400MB - npm install (use .dockerignore)
Layer 3: 200MB - /var/cache (can be deleted)

💡 Potential savings: 1.2GB (60% reduction)
```

**Real-world impact:**
- ✅ Faster CI/CD (smaller images = faster builds)
- ✅ Reduced storage costs
- ✅ Quicker deployments

---

## 🤖 GitHub Action (Auto-Block Secrets)

**Automatically check every PR and block merges if secrets are detected.**

### Setup (30 seconds)

```bash
cd your-repo
devlint setup-github
git add .github/workflows/devlint.yml
git commit -m 'Add DevLint security checks'
git push
```

### What It Does

- ✅ Runs on every pull request automatically
- ❌ **Blocks merge** if secrets found
- 💬 Comments on PR with detailed warnings
- 🚫 Prevents secrets from reaching `main`
- 📊 Shows risk level and recommendations

<p align="center">
  <img src="https://res.cloudinary.com/ds1dhvevo/image/upload/v1769977751/Screenshot_2026-02-02_015403_iz8q2x.png" alt="GitHub Action Blocking PR" width="700"/>
</p>

**Example PR Comment:**
```
🚨 DevLint Security Check Failed

❌ Secrets detected:
  - AWS Access Key in config.py (line 23)
  - GitHub Token in .env (line 5)

⚠️ This PR cannot be merged until secrets are removed.

💡 Tip: Use environment variables instead of hardcoding secrets.
```

**Real-world impact:**
- ✅ Zero-config security for your entire team
- ✅ Prevents accidental credential leaks
- ✅ Enforces best practices automatically

---

## 📊 Impact

DevLint has already prevented:
- ✅ **15+ types of secrets** from leaking
- ⚡ **PR checks in < 2 seconds** (faster than manual review)
- 🔍 **Cross-platform support** (Linux, macOS, Windows)
- 🌍 **Works with any git repo** (GitHub, GitLab, Bitbucket)

---

## 💡 Real-World Examples

### Example 1: Before Committing

```bash
# You've been coding all day...
git add .

# Quick check before commit
devlint secrets

# Output:
🚨 SECRETS DETECTED

File: src/config.py
Line 23: AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"

❌ Commit blocked. Remove secrets first.
```

### Example 2: Before Creating a PR

```bash
# You're ready to merge...
devlint pre-pr

# Output:
⚠️  WARNING

Your branch is 47 commits behind main
Conflicts expected in:
  - src/api/users.js (Alice changed it 2 days ago)
  - src/db/schema.sql

Risk Level: HIGH 🔴
Recommendation: Sync with main before creating PR
```

### Example 3: Port Conflict

```bash
# Error: Port 3000 already in use
devlint ports

# Output:
Port 3000: node server.js (PID 12345)
Port 5432: postgres (PID 67890)
Port 6379: redis-server (PID 11223)

# Now you know exactly what to kill
kill 12345
```

### Example 4: Optimizing Docker

```bash
devlint docker myapp:latest

# Output:
📦 Image Size: 2.3GB

Largest Layers:
1. 800MB - RUN apt-get install
2. 400MB - COPY node_modules
3. 300MB - RUN pip install

💡 Suggestions:
- Use multi-stage builds
- Add .dockerignore for node_modules
- Clear apt cache after install

Potential savings: 1.5GB
```

---

## 👥 Who Should Use DevLint?

| Role | Use Case |
|------|----------|
| **Solo Developer** | Catch mistakes before they become issues |
| **Team Lead** | Enforce checks via GitHub Actions |
| **DevOps Engineer** | Audit Docker images and prevent leaks |
| **Open Source Maintainer** | Protect your repo from contributor mistakes |
| **Security Team** | Automated secret scanning in CI/CD |

---

## ⚙️ How It Works

DevLint uses proven, battle-tested approaches:

- **Git internals** (`merge-tree`, `rev-list`, `diff`) for PR safety checks
- **Regex + entropy analysis** for secret detection
- **psutil** for cross-platform port monitoring
- **Docker SDK** for image layer analysis
- **GitHub API** for automated PR comments

**No magic. No black boxes. Just solid engineering.**

---

## 📚 Commands Reference

| Command | Description |
|---------|-------------|
| `devlint pre-pr` | Check if your branch is safe to merge |
| `devlint check-pr <branch>` | Check a specific branch against main |
| `devlint secrets` | Scan staged files for leaked secrets |
| `devlint ports` | Show all ports currently in use |
| `devlint docker <image>` | Analyze Docker image size and layers |
| `devlint setup-github` | Create GitHub Action workflow file |
| `devlint --help` | Show all available commands |
| `devlint --version` | Show DevLint version |

---

## 🛠️ Configuration (Optional)

Create a `.devlint.yml` in your project root:

```yaml
# Custom secret patterns
secrets:
  patterns:
    - name: "Custom API Key"
      regex: "api_key_[a-zA-Z0-9]{32}"
  
  # Files to ignore
  ignore:
    - "*.test.js"
    - "mock_data.py"

# PR check settings
pr_check:
  max_commits_behind: 10  # Warn if more than 10 commits behind
  block_on_conflicts: true

# Docker settings
docker:
  warn_size_mb: 500  # Warn if image > 500MB
```

---

## 🚀 Roadmap

- [ ] **GitLab/Bitbucket support** - Expand beyond GitHub
- [ ] **Slack/Discord notifications** - Real-time alerts
- [ ] **Custom secret patterns** - Add your own detection rules
- [ ] **Performance profiling** - Find slow code paths
- [ ] **Dependency vulnerability scanning** - Check for CVEs
- [ ] **VS Code extension** - In-editor warnings

---

## 🤝 Contributing

Found a bug? Have an idea? Contributions welcome!

### How to Contribute

1. **Fork the repo**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Add tests** (if applicable)
5. **Commit with clear message**
   ```bash
   git commit -m 'Add amazing feature'
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

### Development Setup

```bash
git clone https://github.com/MayankRajeevkumarShukla/devlint.git
cd devlint

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest
```

---

## 🐛 Troubleshooting

### "Command not found: devlint"

```bash
# Make sure you installed it correctly
pip install git+https://github.com/MayankRajeevkumarShukla/devlint.git

# Or if using a virtual environment, activate it first
source venv/bin/activate
```

### "Permission denied" on ports check

```bash
# On Linux/Mac, you might need sudo for some ports
sudo devlint ports
```

### Docker daemon not running

```bash
# Make sure Docker is running
docker ps

# If not, start Docker Desktop or daemon
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

**TL;DR:** Use it, modify it, ship it. Just keep the license notice.

---

## 🙏 Acknowledgments

Built with:
- [GitPython](https://github.com/gitpython-developers/GitPython) - Git operations
- [Click](https://click.palletsprojects.com/) - Beautiful CLI framework
- [psutil](https://github.com/giampaolo/psutil) - Cross-platform system utilities
- [Docker SDK](https://docker-py.readthedocs.io/) - Docker API client
- [colorama](https://github.com/tartley/colorama) - Terminal colors

Inspired by real production incidents and late-night debugging sessions.

---

<p align="center">
  <b>Built because I pushed an API key to production once.</b><br>
  <b>Never again.</b> 🛡️
</p>

<p align="center">
  Made with ❤️ by <a href="https://github.com/MayankRajeevkumarShukla">Mayank Rajeevkumar Shukla</a>
</p>

<p align="center">
  <a href="https://github.com/MayankRajeevkumarShukla/devlint/issues">Report Bug</a> •
  <a href="https://github.com/MayankRajeevkumarShukla/devlint/issues">Request Feature</a> •
  <a href="https://github.com/MayankRajeevkumarShukla">Follow Me</a>
</p>
