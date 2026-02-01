import git
from colorama import Fore, Style
import click

def check_pr_safety(branch=None):
    """Check PR safety - commits behind, conflicts, and who modified files."""
    try:
        repo = git.Repo('.')
        
        # Get current branch if not specified
        if branch is None:
            current_branch = repo.active_branch.name
        else:
            current_branch = branch
        
        click.echo(f"Branch: {Fore.YELLOW}{current_branch}{Style.RESET_ALL}")
        click.echo(f"Target: {Fore.YELLOW}main{Style.RESET_ALL}\n")
        
        # 1. Check commits behind
        commits_behind = check_commits_behind(repo, current_branch)
        
        # 2. Check for conflicts
        has_conflicts = check_merge_conflicts(repo, current_branch)
        
        # 3. Calculate risk level
        risk_level = calculate_risk(commits_behind, has_conflicts)
        
        # 4. Show recommendation
        show_recommendation(risk_level)
        
    except git.exc.InvalidGitRepositoryError:
        click.echo(f"{Fore.RED}❌ Not a git repository{Style.RESET_ALL}")
    except Exception as e:
        click.echo(f"{Fore.RED}❌ Error: {str(e)}{Style.RESET_ALL}")

def check_commits_behind(repo, branch):
    """Check how many commits behind main."""
    try:
        # Fetch latest
        repo.remotes.origin.fetch()
        
        # Count commits
        commits = repo.git.rev_list('--count', f'{branch}..origin/main')
        commits_behind = int(commits)
        
        if commits_behind == 0:
            click.echo(f"{Fore.GREEN}✅ Up to date (0 commits behind){Style.RESET_ALL}")
        else:
            click.echo(f"{Fore.RED}❌ {commits_behind} commits behind main{Style.RESET_ALL}")
        
        return commits_behind
        
    except Exception as e:
        click.echo(f"{Fore.YELLOW}⚠️  Could not check commits behind: {str(e)}{Style.RESET_ALL}")
        return 0

def check_merge_conflicts(repo, branch):
    """Predict merge conflicts using git merge-tree."""
    try:
        # Find merge base
        merge_base = repo.git.merge_base(branch, 'origin/main')
        
        # Simulate merge
        merge_output = repo.git.merge_tree(merge_base, branch, 'origin/main')
        
        # Check for conflict markers
        has_conflicts = '<<<<<<<' in merge_output
        
        if has_conflicts:
            click.echo(f"{Fore.RED}❌ Conflicts detected{Style.RESET_ALL}")
        else:
            click.echo(f"{Fore.GREEN}✅ No conflicts detected{Style.RESET_ALL}")
        
        return has_conflicts
        
    except Exception as e:
        click.echo(f"{Fore.YELLOW}⚠️  Could not check conflicts: {str(e)}{Style.RESET_ALL}")
        return False

def calculate_risk(commits_behind, has_conflicts):
    """Calculate risk level based on checks."""
    if has_conflicts or commits_behind > 20:
        return "HIGH"
    elif commits_behind > 5:
        return "MEDIUM"
    else:
        return "LOW"

def show_recommendation(risk_level):
    """Show final recommendation."""
    click.echo()
    
    if risk_level == "LOW":
        click.echo(f"Risk Level: {Fore.GREEN}{risk_level} 🟢{Style.RESET_ALL}")
        click.echo(f"Recommendation: {Fore.GREEN}Safe to merge{Style.RESET_ALL}")
    elif risk_level == "MEDIUM":
        click.echo(f"Risk Level: {Fore.YELLOW}{risk_level} 🟡{Style.RESET_ALL}")
        click.echo(f"Recommendation: {Fore.YELLOW}Review carefully before merging{Style.RESET_ALL}")
    else:
        click.echo(f"Risk Level: {Fore.RED}{risk_level} 🔴{Style.RESET_ALL}")
        click.echo(f"Recommendation: {Fore.RED}Sync with main before merging{Style.RESET_ALL}")