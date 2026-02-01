import click
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

@click.group()
@click.version_option(version="0.1.0")
def cli():
    """DevLint - Prevent common developer workflow mistakes."""
    pass

@cli.command()
def check():
    """Run all checks."""
    click.echo(f"{Fore.CYAN}Running all DevLint checks...{Style.RESET_ALL}\n")
    
    # We'll call other commands here later
    click.echo(f"{Fore.GREEN}✅ All checks completed!{Style.RESET_ALL}")

@cli.command("pre-pr")
def pre_pr():
    """Check before creating a PR."""
    from .pr_check import check_pr_safety
    
    click.echo(f"{Fore.CYAN}╔════════════════════════════════════════╗{Style.RESET_ALL}")
    click.echo(f"{Fore.CYAN}║         PR SAFETY CHECK                ║{Style.RESET_ALL}")
    click.echo(f"{Fore.CYAN}╚════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    check_pr_safety()

@cli.command("check-pr")
@click.argument("branch")
def check_pr_branch(branch):
    """Check a specific branch before merging."""
    from .pr_check import check_pr_safety
    
    click.echo(f"{Fore.CYAN}Checking branch: {branch}{Style.RESET_ALL}\n")
    check_pr_safety(branch)

@cli.command()
def secrets():
    """Scan for secrets in staged files."""
    from .secrets import scan_secrets
    
    click.echo(f"{Fore.CYAN}Scanning for secrets...{Style.RESET_ALL}\n")
    scan_secrets()

@cli.command()
def ports():
    """Show all ports in use."""
    from .ports import check_ports
    
    click.echo(f"{Fore.CYAN}Checking ports...{Style.RESET_ALL}\n")
    check_ports()

@cli.command()
@click.argument("image")
def docker(image):
    """Analyze Docker image size."""
    from .docker_analyzer import analyze_image
    
    click.echo(f"{Fore.CYAN}Analyzing Docker image: {image}{Style.RESET_ALL}\n")
    analyze_image(image)

@cli.command("setup-github")
def setup_github():
    """Setup GitHub Action integration."""
    from .github_integration import setup_github_action
    
    click.echo(f"{Fore.CYAN}Setting up GitHub integration...{Style.RESET_ALL}\n")
    setup_github_action()

@cli.command("check-gh-pr")
@click.argument("pr_number", type=int)
def check_github_pr(pr_number):
    """Check a GitHub PR by number."""
    from .github_integration import check_github_pr
    
    click.echo(f"{Fore.CYAN}Checking GitHub PR #{pr_number}...{Style.RESET_ALL}\n")
    check_github_pr(pr_number)

if __name__ == "__main__":
    cli()