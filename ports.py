import psutil
from colorama import Fore, Style
import click
from tabulate import tabulate

def check_ports():
    """Show all ports in use with process details."""
    try:
        ports_info = []
        
        # Get all network connections
        connections = psutil.net_connections(kind='inet')
        
        for conn in connections:
            # Only show listening ports
            if conn.status == 'LISTEN' and conn.laddr:
                try:
                    # Get process info
                    process = psutil.Process(conn.pid) if conn.pid else None
                    
                    port_data = {
                        'Port': conn.laddr.port,
                        'Process': process.name() if process else 'Unknown',
                        'PID': conn.pid if conn.pid else 'N/A',
                        'Status': conn.status
                    }
                    
                    ports_info.append(port_data)
                    
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    # Process ended or no permission
                    ports_info.append({
                        'Port': conn.laddr.port,
                        'Process': 'No access',
                        'PID': conn.pid if conn.pid else 'N/A',
                        'Status': conn.status
                    })
        
        if not ports_info:
            click.echo(f"{Fore.GREEN}✅ No ports currently in use{Style.RESET_ALL}")
            return
        
        # Sort by port number
        ports_info = sorted(ports_info, key=lambda x: x['Port'])
        
        # Display table
        click.echo(f"{Fore.CYAN}Ports in use:{Style.RESET_ALL}\n")
        
        table_data = []
        for info in ports_info:
            table_data.append([
                f"{Fore.YELLOW}{info['Port']}{Style.RESET_ALL}",
                info['Process'],
                info['PID'],
                f"{Fore.GREEN}{info['Status']}{Style.RESET_ALL}"
            ])
        
        headers = [
            f"{Fore.CYAN}Port{Style.RESET_ALL}",
            f"{Fore.CYAN}Process{Style.RESET_ALL}",
            f"{Fore.CYAN}PID{Style.RESET_ALL}",
            f"{Fore.CYAN}Status{Style.RESET_ALL}"
        ]
        
        print(tabulate(table_data, headers=headers, tablefmt='simple'))
        
        # Ask if user wants to kill any process
        click.echo(f"\n{Fore.CYAN}Want to kill a process? Use: kill <PID>{Style.RESET_ALL}")
        
    except PermissionError:
        click.echo(f"{Fore.RED}❌ Permission denied. Try running with sudo/admin rights{Style.RESET_ALL}")
    except Exception as e:
        click.echo(f"{Fore.RED}❌ Error: {str(e)}{Style.RESET_ALL}")