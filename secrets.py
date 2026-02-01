import re
import os
import git
from colorama import Fore, Style
import click

def scan_secrets():
    """Scan staged files for secrets - both .env leaks and hardcoded secrets."""
    try:
        repo = git.Repo('.')
        
        # Get staged files
        staged_files = [item.a_path for item in repo.index.diff("HEAD")]
        
        if not staged_files:
            click.echo(f"{Fore.YELLOW}⚠️  No staged files to scan{Style.RESET_ALL}")
            click.echo(f"{Fore.CYAN}Tip: Use 'git add' to stage files{Style.RESET_ALL}")
            return
        
        click.echo(f"Scanning {len(staged_files)} staged file(s)...\n")
        
        secrets_found = []
        
        # Step 1: Check for .env leaks
        env_secrets = check_env_leaks(staged_files)
        secrets_found.extend(env_secrets)
        
        # Step 2: Check for hardcoded secrets (smart detection)
        hardcoded_secrets = check_hardcoded_secrets(staged_files)
        secrets_found.extend(hardcoded_secrets)
        
        # Report results
        if secrets_found:
            click.echo(f"{Fore.RED}❌ Found {len(secrets_found)} potential secret(s):{Style.RESET_ALL}\n")
            
            for secret in secrets_found:
                click.echo(f"{Fore.RED}⚠️  {secret['type']}{Style.RESET_ALL}")
                click.echo(f"   File: {Fore.YELLOW}{secret['file']}{Style.RESET_ALL}")
                click.echo(f"   Line: {secret['line']}")
                click.echo(f"   Preview: {secret['preview']}\n")
            
            click.echo(f"{Fore.RED}🚨 DO NOT COMMIT THESE FILES!{Style.RESET_ALL}")
            return False
        else:
            click.echo(f"{Fore.GREEN}✅ No secrets detected{Style.RESET_ALL}")
            click.echo(f"{Fore.GREEN}Safe to commit{Style.RESET_ALL}")
            return True
            
    except git.exc.InvalidGitRepositoryError:
        click.echo(f"{Fore.RED}❌ Not a git repository{Style.RESET_ALL}")
        return False
    except Exception as e:
        click.echo(f"{Fore.RED}❌ Error: {str(e)}{Style.RESET_ALL}")
        return False

def check_env_leaks(staged_files):
    """Check if .env values are leaked in code files."""
    secrets = []
    
    # Check if .env exists
    if not os.path.exists('.env'):
        return secrets
    
    # Read .env file
    try:
        with open('.env', 'r') as f:
            env_content = f.read()
        
        # Extract key=value pairs
        env_values = {}
        for line in env_content.split('\n'):
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                value = value.strip().strip('"').strip("'")
                if len(value) > 5:  # Ignore short values
                    env_values[key.strip()] = value
        
        if not env_values:
            return secrets
        
        # Scan staged files for these values
        for filepath in staged_files:
            # Skip .env itself
            if filepath.endswith('.env'):
                continue
                
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Check each .env value
                for key, value in env_values.items():
                    if value in content:
                        line_num = find_line_number(content, value)
                        secrets.append({
                            'file': filepath,
                            'line': line_num,
                            'type': f'.env leak: {key}',
                            'preview': value[:30] + '...' if len(value) > 30 else value
                        })
            except:
                pass
                
    except Exception as e:
        pass
    
    return secrets

def check_hardcoded_secrets(staged_files):
    """Detect hardcoded secrets using smart patterns."""
    secrets = []
    
    # Patterns for known secret formats
    KNOWN_PATTERNS = {
        'AWS Access Key': r'AKIA[0-9A-Z]{16}',
        'GitHub Token': r'gh[ps]_[0-9a-zA-Z]{36}',
        'Stripe Key': r'sk_(live|test)_[0-9a-zA-Z]{24,}',
        'OpenAI Key': r'sk-[A-Za-z0-9]{48}',
        'JWT Token': r'eyJ[A-Za-z0-9_-]*\.eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*',
        'Private Key': r'-----BEGIN [A-Z]+ PRIVATE KEY-----',
        'Generic API Key': r'api[_-]?key["\s:=]+["\']([a-zA-Z0-9_\-]{20,})["\']',
    }
    
    # Secret-like variable names
    SECRET_VAR_NAMES = [
        'password', 'passwd', 'pwd', 'secret', 'token', 'api_key', 'apikey',
        'access_key', 'private_key', 'auth', 'credentials', 'api_secret'
    ]
    
    for filepath in staged_files:
        # Skip non-code files
        if not is_code_file(filepath):
            continue
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            for line_num, line in enumerate(lines, 1):
                line_lower = line.lower()
                
                # Skip comments and imports
                if is_comment_or_import(line, filepath):
                    continue
                
                # Check known patterns
                for secret_type, pattern in KNOWN_PATTERNS.items():
                    if re.search(pattern, line):
                        secrets.append({
                            'file': filepath,
                            'line': line_num,
                            'type': secret_type,
                            'preview': line.strip()[:50] + '...' if len(line.strip()) > 50 else line.strip()
                        })
                
                # Check for secret variable assignments
                for var_name in SECRET_VAR_NAMES:
                    if var_name in line_lower and '=' in line:
                        # Extract the value
                        value = extract_assigned_value(line)
                        if value and looks_like_secret(value):
                            secrets.append({
                                'file': filepath,
                                'line': line_num,
                                'type': f'Hardcoded {var_name}',
                                'preview': line.strip()[:50] + '...' if len(line.strip()) > 50 else line.strip()
                            })
        except:
            pass
    
    return secrets

def is_code_file(filepath):
    """Check if file is a code file."""
    code_extensions = ['.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.rb', '.php', '.cs', '.cpp', '.c', '.h']
    return any(filepath.endswith(ext) for ext in code_extensions)

def is_comment_or_import(line, filepath):
    """Check if line is a comment or import."""
    line = line.strip()
    
    # Python
    if filepath.endswith('.py'):
        return line.startswith('#') or line.startswith('import ') or line.startswith('from ')
    
    # JavaScript/TypeScript
    if filepath.endswith(('.js', '.ts', '.jsx', '.tsx')):
        return line.startswith('//') or line.startswith('/*') or line.startswith('import ')
    
    return False

def extract_assigned_value(line):
    """Extract value from assignment line."""
    try:
        if '=' in line:
            value = line.split('=', 1)[1].strip()
            # Remove quotes and semicolons
            value = value.strip('"').strip("'").strip(';').strip()
            return value
    except:
        pass
    return None

def looks_like_secret(value):
    """Check if a value looks like a secret."""
    if not value or len(value) < 15:
        return False
    
    # Check for random-looking strings
    has_upper = any(c.isupper() for c in value)
    has_lower = any(c.islower() for c in value)
    has_digit = any(c.isdigit() for c in value)
    has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in value)
    
    # Long random string with mixed case/numbers
    if len(value) > 20 and has_upper and has_lower and has_digit:
        return True
    
    # Base64-like pattern
    if re.match(r'^[A-Za-z0-9+/]{20,}={0,2}$', value):
        return True
    
    # Hex string
    if re.match(r'^[a-fA-F0-9]{32,}$', value):
        return True
    
    return False

def find_line_number(content, value):
    """Find line number of a value in content."""
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        if value in line:
            return i
    return 1