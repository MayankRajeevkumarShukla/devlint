# DevLint 🛡️

**Stop secrets, stale PRs, and common mistakes before they reach production.**

<p align="center">
  <img src="https://res.cloudinary.com/ds1dhvevo/image/upload/v1769977780/Screenshot_2026-02-02_004045_t6edq4.png" alt="DevLint Secret Detection" width="800"/>
</p>

---

## 🎯 Why DevLint?

Ever pushed an API key by accident? Merged a PR 50 commits behind main? DevLint catches these mistakes **before** they cause problems.

### Real Problems It Solves

- 🔒 **Accidentally committed AWS keys, API tokens, or passwords**
- ⚠️ **Merged stale branches causing production conflicts**
- 🐛 **Forgot which process is using port 3000**
- 📦 **Docker images bloated to 5GB when they should be 500MB**

---

## 📦 Installation

### From GitHub

```bash
pip install git+https://github.com/MayankRajeevkumarShukla/devlint.git
```

### Or Install Locally

```bash
git clone https://github.com/MayankRajeevkumarShukla/devlint.git
cd devlint
pip install -e .
```

---

## 🚀 Quick Start

```bash
# Check before creating a PR
devlint pre-pr

# Scan for secrets in your code
devlint secrets

# See what's using your ports
devlint ports

# Analyze Docker image size
devlint docker my-app:latest
```

---

## ✨ Features

### 🔒 Secret Detection

Catches API keys, tokens, and passwords before you commit them.

```bash
devlint secrets
```

**Detects:**
- AWS keys, GitHub tokens, Stripe keys
- Leaked `.env` values in code
- Hardcoded passwords and API keys
- Private keys and certificates

<p align="center">
  <img src="https://res.cloudinary.com/ds1dhvevo/image/upload/v1769977780/Screenshot_2026-02-02_004045_t6edq4.png" alt="Secret Detection Example" width="700"/>
</p>

---

### ⚠️ PR Safety Check

Know if your branch is safe to merge.

```bash
devlint pre-pr
```

**Checks:**
- How many commits behind main
- Potential merge conflicts
- Risk level (LOW/MEDIUM/HIGH)

<p align="center">
  <img src="https://res.cloudinary.com/ds1dhvevo/image/upload/v1769977766/Screenshot_2026-02-02_005651_nkdslc.png" alt="PR Safety Check" width="700"/>
</p>

---

### 🔌 Port Checker

Find what's using your ports instantly.

```bash
devlint ports
```

**Shows:**
- Port number
- Process name
- PID for easy killing

<p align="center">
  <img src="https://res.cloudinary.com/ds1dhvevo/image/upload/v1769977873/Screenshot_2026-02-02_020058_qvrjls.png" alt="Port Checker" width="700"/>
</p>

---

### 🐳 Docker Analyzer

Optimize your Docker images.

```bash
devlint docker my-app:latest
```

**Provides:**
- Layer-by-layer breakdown
- Largest layers identified
- Optimization suggestions
- Potential size savings

<p align="center">
  <img src="https://res.cloudinary.com/ds1dhvevo/image/upload/v1769977794/Screenshot_2026-02-02_002511_snzcr1.png" alt="Docker Analysis" width="700"/>
</p>

---

## 🤖 GitHub Action (Auto-Block Secrets)

Automatically check every PR and block merges if secrets are detected.

### Setup

```bash
cd your-repo
devlint setup-github
git add .github/workflows/devlint.yml
git commit -m 'Add DevLint checks'
git push
```

### What It Does

- ✅ Runs on every PR automatically
- ❌ Blocks merge if secrets found
- 💬 Comments on PR with warnings
- 🚫 Prevents secrets from reaching main

<p align="center">
  <img src="https://res.cloudinary.com/ds1dhvevo/image/upload/v1769977751/Screenshot_2026-02-02_015403_iz8q2x.png" alt="GitHub Action Blocking PR" width="700"/>
</p>

---

## 💡 Examples

### Before Committing

```bash
git add .
devlint secrets  # Check for leaked secrets
```

### Before Creating a PR

```bash
devlint pre-pr  # Check if branch is safe to merge
```

### When Port Is In Use

```bash
devlint ports  # Find what's using port 3000
kill <PID>     # Kill the process
```

### Optimizing Docker

```bash
devlint docker my-app:latest  # Get optimization tips
```

---

## 👥 Use Cases

| Role | Use Case |
|------|----------|
| **Solo Developer** | Catch mistakes before pushing |
| **Team Lead** | Enforce checks via GitHub Actions |
| **DevOps** | Audit Docker images and catch secrets |
| **Open Source** | Protect your repo from accidental leaks |

---

## ⚙️ How It Works

DevLint uses:
- **Git internals** (merge-tree, rev-list) for PR checks
- **Regex + smart detection** for secrets
- **psutil** for port monitoring
- **Docker API** for image analysis

**Cross-platform:** Works on Linux, macOS, and Windows

---

## 📚 Commands Reference

| Command | Description |
|---------|-------------|
| `devlint pre-pr` | Check if branch is safe to merge |
| `devlint check-pr <branch>` | Check specific branch |
| `devlint secrets` | Scan for secrets in staged files |
| `devlint ports` | Show all ports in use |
| `devlint docker <image>` | Analyze Docker image size |
| `devlint setup-github` | Setup GitHub Action workflow |

---

## 🤝 Contributing

Found a bug? Have an idea? Open an issue or PR!

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---

<p align="center">
  <b>Built because I pushed an API key to production once. Never again.</b> 🛡️
</p>

<p align="center">
  Made with ❤️ by <a href="https://github.com/MayankRajeevkumarShukla">Mayank Rajeevkumar Shukla</a>
</p>