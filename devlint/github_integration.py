"""GitHub integration for DevLint - creates GitHub Actions workflow."""

import os
from pathlib import Path
from colorama import Fore, Style
import click
from .utils import find_git_root, ensure_directory


def setup_github_action():
    """Create GitHub Action workflow file for DevLint."""
    try:
        # Find git root
        git_root = find_git_root()
        
        if not git_root:
            click.echo(f"{Fore.RED}❌ Not a git repository{Style.RESET_ALL}")
            click.echo(f"{Fore.CYAN}Tip: Run this command from inside a git repository{Style.RESET_ALL}")
            return
        
        # Create .github/workflows directory
        workflows_dir = git_root / '.github' / 'workflows'
        ensure_directory(workflows_dir)
        
        # Create devlint.yml workflow file
        workflow_file = workflows_dir / 'devlint.yml'
        
        if workflow_file.exists():
            click.echo(f"{Fore.YELLOW}⚠️  GitHub Action already exists: {workflow_file}{Style.RESET_ALL}")
            
            if not click.confirm('Overwrite existing workflow?'):
                click.echo(f"{Fore.CYAN}Setup cancelled{Style.RESET_ALL}")
                return
        
        # Create workflow content
        workflow_content = create_workflow_yaml()
        
        # Write file
        with open(workflow_file, 'w') as f:
            f.write(workflow_content)
        
        click.echo(f"{Fore.GREEN}✅ GitHub Action created successfully!{Style.RESET_ALL}\n")
        click.echo(f"File: {Fore.YELLOW}{workflow_file}{Style.RESET_ALL}\n")
        
        click.echo(f"{Fore.CYAN}Next steps:{Style.RESET_ALL}")
        click.echo(f"1. Commit and push the workflow file:")
        click.echo(f"   {Fore.YELLOW}git add .github/workflows/devlint.yml{Style.RESET_ALL}")
        click.echo(f"   {Fore.YELLOW}git commit -m 'Add DevLint GitHub Action'{Style.RESET_ALL}")
        click.echo(f"   {Fore.YELLOW}git push{Style.RESET_ALL}\n")
        click.echo(f"2. Create a new PR to test it")
        click.echo(f"3. DevLint will automatically check your PRs! 🎉\n")
        
    except Exception as e:
        click.echo(f"{Fore.RED}❌ Error: {str(e)}{Style.RESET_ALL}")


def create_workflow_yaml():
    """Generate the GitHub Actions workflow YAML content."""
    return """name: DevLint Check

on:
  pull_request:
    branches:
      - main
      - master
      - develop
  push:
    branches:
      - main
      - master
      - develop

jobs:
  devlint:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Fetch all history for proper PR checks
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install DevLint
        run: |
          pip install git+https://github.com/MayankRajeevkumarShukla/devlint.git
      
      - name: Run DevLint - Secret Scan
        id: secrets
        run: |
          # Stage all files for secret scanning
          git add -A
          
          # Run secret scan and capture exit code
          if devlint secrets; then
            echo "secrets_passed=true" >> $GITHUB_OUTPUT
          else
            echo "secrets_passed=false" >> $GITHUB_OUTPUT
            exit 1
          fi
      
      - name: Run DevLint - PR Safety Check
        if: github.event_name == 'pull_request'
        id: pr_check
        run: |
          # Get the branch name
          BRANCH_NAME="${{ github.head_ref }}"
          
          # Run PR check
          if devlint check-pr "$BRANCH_NAME"; then
            echo "pr_check_passed=true" >> $GITHUB_OUTPUT
          else
            echo "pr_check_passed=false" >> $GITHUB_OUTPUT
          fi
      
      - name: Comment PR with Results
        if: github.event_name == 'pull_request' && failure()
        uses: actions/github-script@v7
        with:
          script: |
            const output = `## 🚨 DevLint Check Failed
            
            **Secret Scan:** ${{ steps.secrets.outputs.secrets_passed == 'true' && '✅ Passed' || '❌ Failed - Secrets detected!' }}
            **PR Safety:** ${{ steps.pr_check.outputs.pr_check_passed == 'true' && '✅ Passed' || '⚠️ Warning - Review needed' }}
            
            ### ⚠️ Action Required
            
            Secrets were detected in your code. Please:
            1. Remove all secrets from your code
            2. Use environment variables instead
            3. Add sensitive files to \`.gitignore\`
            4. Run \`devlint secrets\` locally to check
            
            **DO NOT MERGE until secrets are removed!**
            `;
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: output
            });
      
      - name: Fail if secrets found
        if: steps.secrets.outputs.secrets_passed == 'false'
        run: |
          echo "❌ Secrets detected! Blocking merge."
          exit 1
"""


def check_github_pr(pr_number):
    """Check a specific GitHub PR (future feature - requires GitHub API token)."""
    click.echo(f"{Fore.YELLOW}⚠️  This feature requires GitHub API integration{Style.RESET_ALL}")
    click.echo(f"{Fore.CYAN}For now, use GitHub Actions to auto-check PRs{Style.RESET_ALL}")
    click.echo(f"\nRun: {Fore.YELLOW}devlint setup-github{Style.RESET_ALL} to set up automation")