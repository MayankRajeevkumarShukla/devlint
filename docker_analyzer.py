import docker
from colorama import Fore, Style
import click
from tabulate import tabulate

def analyze_image(image_name):
    """Analyze Docker image size and layers."""
    try:
        # Connect to Docker
        client = docker.from_env()
        
        # Get image
        try:
            image = client.images.get(image_name)
        except docker.errors.ImageNotFound:
            click.echo(f"{Fore.RED}❌ Image '{image_name}' not found{Style.RESET_ALL}")
            click.echo(f"{Fore.CYAN}Tip: Run 'docker images' to see available images{Style.RESET_ALL}")
            return
        
        # Get image details
        total_size = image.attrs['Size']
        layers = image.history()
        
        click.echo(f"{Fore.CYAN}Image: {Fore.YELLOW}{image_name}{Style.RESET_ALL}")
        click.echo(f"{Fore.CYAN}Total Size: {Fore.YELLOW}{format_bytes(total_size)}{Style.RESET_ALL}\n")
        
        # Analyze layers
        click.echo(f"{Fore.CYAN}Layer breakdown:{Style.RESET_ALL}\n")
        
        layer_data = []
        total_layer_size = 0
        
        for i, layer in enumerate(layers):
            size = layer.get('Size', 0)
            total_layer_size += size
            
            # Get command (truncate if too long)
            command = layer.get('CreatedBy', 'Unknown')
            if len(command) > 60:
                command = command[:57] + '...'
            
            layer_data.append([
                i + 1,
                format_bytes(size),
                command
            ])
        
        headers = [
            f"{Fore.CYAN}Layer{Style.RESET_ALL}",
            f"{Fore.CYAN}Size{Style.RESET_ALL}",
            f"{Fore.CYAN}Command{Style.RESET_ALL}"
        ]
        
        print(tabulate(layer_data, headers=headers, tablefmt='simple'))
        
        # Find largest layers
        click.echo(f"\n{Fore.CYAN}Analysis:{Style.RESET_ALL}\n")
        
        sorted_layers = sorted(enumerate(layers), key=lambda x: x[1].get('Size', 0), reverse=True)
        large_layers = [l for l in sorted_layers if l[1].get('Size', 0) > 10_000_000][:3]  # Top 3 > 10MB
        
        if large_layers:
            click.echo(f"{Fore.YELLOW}⚠️  Largest layers:{Style.RESET_ALL}")
            for idx, layer in large_layers:
                size = layer.get('Size', 0)
                click.echo(f"   Layer {idx + 1}: {Fore.RED}{format_bytes(size)}{Style.RESET_ALL}")
        
        # Suggestions
        click.echo(f"\n{Fore.CYAN}💡 Optimization tips:{Style.RESET_ALL}")
        
        suggestions = []
        
        # Check for common issues
        if any('apt-get' in layer.get('CreatedBy', '') and 'rm -rf /var/lib/apt' not in layer.get('CreatedBy', '') for layer in layers):
            suggestions.append("Combine apt-get commands and clean cache: RUN apt-get update && apt-get install -y pkg && rm -rf /var/lib/apt/lists/*")
        
        if any('pip install' in layer.get('CreatedBy', '') and '--no-cache-dir' not in layer.get('CreatedBy', '') for layer in layers):
            suggestions.append("Use pip --no-cache-dir to reduce image size")
        
        if len(layers) > 20:
            suggestions.append(f"Too many layers ({len(layers)}). Combine RUN commands to reduce layers")
        
        if any(layer.get('Size', 0) > 100_000_000 for layer in layers):
            suggestions.append("Some layers are very large (>100MB). Consider multi-stage builds")
        
        if suggestions:
            for suggestion in suggestions:
                click.echo(f"   • {suggestion}")
        else:
            click.echo(f"   {Fore.GREEN}✅ Image looks well optimized!{Style.RESET_ALL}")
        
        # Potential savings
        if large_layers:
            potential_savings = sum(l[1].get('Size', 0) for l in large_layers) * 0.3  # Estimate 30% reduction
            click.echo(f"\n{Fore.GREEN}Potential savings: ~{format_bytes(int(potential_savings))}{Style.RESET_ALL}")
        
    except docker.errors.DockerException as e:
        click.echo(f"{Fore.RED}❌ Docker error: {str(e)}{Style.RESET_ALL}")
        click.echo(f"{Fore.CYAN}Tip: Make sure Docker is running{Style.RESET_ALL}")
    except Exception as e:
        click.echo(f"{Fore.RED}❌ Error: {str(e)}{Style.RESET_ALL}")

def format_bytes(bytes_size):
    """Convert bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"