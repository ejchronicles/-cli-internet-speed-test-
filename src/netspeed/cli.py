import click
from .speed_test import InternetSpeedTest
from .exporters import ResultExporter
import sys

@click.command()
@click.option('--json', 'output_format', flag_value='json', help='Output in JSON format')
@click.option('--csv', 'output_format', flag_value='csv', help='Output in CSV format')
@click.option('--text', 'output_format', flag_value='text', default=True, help='Output in text format (default)')
@click.option('--output-file', '-o', help='Save results to file')
@click.option('--server', '-s', help='Specific server ID to use')
@click.option('--list-servers', is_flag=True, help='List available servers')
def main(output_format, output_file, server, list_servers):
    """CLI Internet Speed Test Tool - Measure your internet connection speed"""
    
    try:
        tester = InternetSpeedTest()
        
        if list_servers:
            click.echo("Fetching server list...")
            tester.speedtester.get_servers()
            for s in tester.speedtester.servers[:10]:  # Show first 10
                click.echo(f"{s['id']}: {s['name']} - {s['country']}")
            return
        
        click.echo("Starting internet speed test...")
        results = tester.run_speed_test(server_id=server)
        
        # Export based on format
        if output_format == 'json':
            output = ResultExporter.to_json(results, output_file)
        elif output_format == 'csv':
            output = ResultExporter.to_csv(results, output_file)
        else:
            output = ResultExporter.to_text(results)
            if output_file:
                with open(output_file, 'w') as f:
                    f.write(output)
        
        if not output_file or output_format == 'text':
            click.echo(output)
            
    except KeyboardInterrupt:
        click.echo("\nTest cancelled by user")
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
