# GitHub Setup Guide

This guide explains how to connect your XT Shipping Governance Demo to your personal GitHub account and push the code to a new repository.

## 📋 Prerequisites

- Git installed on your computer
- A GitHub account (create one at https://github.com if you don't have one)
- Terminal/Command Prompt access

## 🚀 Step-by-Step Instructions

### Step 1: Verify Git Installation

Open your terminal and check if Git is installed:

```bash
git --version
```

If not installed, download from: https://git-scm.com/downloads

### Step 2: Configure Git (First Time Only)

If you haven't configured Git before, set your name and email:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

**Note:** Use the same email associated with your GitHub account.

### Step 3: Initialize Local Git Repository

Navigate to the project directory:

```bash
cd /Users/nivbardas/Desktop/BOB_session/xt-shipping-governance-demo
```

Initialize Git repository:

```bash
git init
```

You should see: `Initialized empty Git repository in ...`

### Step 4: Add Files to Git

Add all project files to Git:

```bash
git add .
```

Check what will be committed:

```bash
git status
```

You should see all your files listed in green (ready to commit).

### Step 5: Create Initial Commit

Commit the files with a message:

```bash
git commit -m "Initial commit: XT Shipping Governance Demo with intentional issues"
```

### Step 6: Create GitHub Repository

1. **Go to GitHub:** Open https://github.com in your browser
2. **Sign in** to your GitHub account
3. **Click the "+" icon** in the top right corner
4. **Select "New repository"**

5. **Configure the repository:**
   - **Repository name:** `xt-shipping-governance-demo`
   - **Description:** "XT Group Shipping Management System - Governance Demo with intentional issues for training"
   - **Visibility:** Choose **Private** (recommended) or Public
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)

6. **Click "Create repository"**

### Step 7: Connect Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
# Add the remote repository
git remote add origin https://github.com/YOUR_USERNAME/xt-shipping-governance-demo.git

# Verify the remote was added
git remote -v
```

**Replace `YOUR_USERNAME`** with your actual GitHub username.

### Step 8: Push Code to GitHub

Push your code to GitHub:

```bash
# Push to main branch
git branch -M main
git push -u origin main
```

**If prompted for credentials:**
- **Username:** Your GitHub username
- **Password:** Use a Personal Access Token (not your GitHub password)

### Step 9: Create Personal Access Token (If Needed)

If you need to create a Personal Access Token:

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name: "XT Shipping Demo"
4. Select scopes: Check **repo** (full control of private repositories)
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again!)
7. Use this token as your password when pushing

### Step 10: Verify Upload

1. Go to your GitHub repository: `https://github.com/YOUR_USERNAME/xt-shipping-governance-demo`
2. You should see all your files
3. Check that README.md displays properly

## 🔄 Making Future Changes

After making changes to your code:

```bash
# Check what changed
git status

# Add changed files
git add .

# Commit with a message
git commit -m "Description of changes"

# Push to GitHub
git push
```

## 📝 Common Git Commands

| Command | Description |
|---------|-------------|
| `git status` | Check current status and changes |
| `git add <file>` | Add specific file to staging |
| `git add .` | Add all changes to staging |
| `git commit -m "message"` | Commit staged changes |
| `git push` | Push commits to GitHub |
| `git pull` | Pull latest changes from GitHub |
| `git log` | View commit history |
| `git branch` | List branches |
| `git checkout -b <branch>` | Create and switch to new branch |

## 🌿 Working with Branches

To work on fixes without affecting the main code:

```bash
# Create a new branch for fixes
git checkout -b fix-governance-issues

# Make your changes...

# Commit changes
git add .
git commit -m "Fixed RBAC violations"

# Push branch to GitHub
git push -u origin fix-governance-issues
```

Then create a Pull Request on GitHub to merge changes.

## 🔐 Repository Settings

### Recommended Settings

1. **Go to repository Settings**
2. **Branches:**
   - Add branch protection rule for `main`
   - Require pull request reviews before merging
   - Require status checks to pass

3. **Collaborators:**
   - Add team members if working collaboratively
   - Settings → Collaborators → Add people

4. **Security:**
   - Enable Dependabot alerts
   - Enable secret scanning

## 📊 Repository Structure on GitHub

Your repository will look like this:

```
xt-shipping-governance-demo/
├── .gitignore
├── README.md
├── GOVERNANCE_ISSUES.md
├── GITHUB_SETUP.md (this file)
├── requirements.txt
├── app.py
├── database/
│   ├── init_db.py
│   └── schema.sql
├── static/
│   └── css/
│       └── maritime-theme.css
└── templates/
    ├── base.html
    ├── login.html
    ├── dashboard.html
    └── ... (other templates)
```

## ⚠️ Important Notes

### What NOT to Commit

The `.gitignore` file already excludes:
- `*.db` - Database files (contain data)
- `__pycache__/` - Python cache
- `.env` - Environment variables
- `venv/` - Virtual environment

### Security Considerations

- **Never commit:**
  - Real passwords or API keys
  - Database files with real data
  - `.env` files with secrets
  
- **This demo contains intentional vulnerabilities:**
  - Mark repository as "Demo/Training" in description
  - Consider making it private
  - Add security disclaimer in README

## 🆘 Troubleshooting

### Problem: "Permission denied (publickey)"

**Solution:** Use HTTPS instead of SSH, or set up SSH keys:
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/xt-shipping-governance-demo.git
```

### Problem: "Updates were rejected"

**Solution:** Pull first, then push:
```bash
git pull origin main --rebase
git push
```

### Problem: "Authentication failed"

**Solution:** Use Personal Access Token instead of password

### Problem: Large files rejected

**Solution:** Check `.gitignore` and remove large files:
```bash
git rm --cached large-file.db
git commit -m "Remove large file"
```

## 📚 Additional Resources

- **Git Documentation:** https://git-scm.com/doc
- **GitHub Guides:** https://guides.github.com
- **Git Cheat Sheet:** https://education.github.com/git-cheat-sheet-education.pdf
- **GitHub Desktop:** https://desktop.github.com (GUI alternative)

## ✅ Verification Checklist

- [ ] Git installed and configured
- [ ] Local repository initialized
- [ ] All files committed locally
- [ ] GitHub repository created
- [ ] Remote repository connected
- [ ] Code pushed to GitHub
- [ ] Repository visible on GitHub
- [ ] README displays correctly
- [ ] .gitignore working (no .db files uploaded)

## 🎯 Next Steps

After pushing to GitHub:

1. **Share the repository** with your team
2. **Create issues** for each governance problem to fix
3. **Create branches** for different fixes
4. **Use Pull Requests** for code review
5. **Document fixes** as you implement them

---

**Need Help?**

If you encounter issues:
1. Check the troubleshooting section above
2. Search GitHub documentation
3. Ask your project administrator

---

**© 2025 XT Group**  
*This guide is part of the XT Shipping Governance Demo project*