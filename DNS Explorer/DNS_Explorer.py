import aiohttp
import asyncio
import dns.resolver
import pyfiglet
import click
from functools import lru_cache
import concurrent.futures

@lru_cache(maxsize=128)  # Cache DNS query results
async def perform_dns_lookup(target, record_types=None):
    try:
        if record_types is None:
            record_types = ["A", "AAAA", "MX", "CNAME", "NS", "TXT", "SOA"]

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://dns.google/resolve?name={target}") as response:
                data = await response.json()
                if "Answer" in data:
                    results = []
                    for record in data["Answer"]:
                        if record["type"] in record_types:
                            results.append(f"{record['type']} Record: {record['data']}")
                    return results
                else:
                    return [f"No DNS records found for {target}"]

    except aiohttp.ClientError as e:
        return [f"DNS lookup failed: {e}"]
    except dns.resolver.NXDOMAIN:
        return [f"DNS lookup failed: Domain '{target}' not found."]
    except Exception as e:
        return [f"An error occurred: {e}"]

@click.command()
def dns_explorer():
    loop = asyncio.get_event_loop()
    
    ascii_banner = pyfiglet.figlet_format("DNS Explorer")
    click.echo(ascii_banner)

    domain = input("Enter a domain name or IP address (separate multiple domains with spaces): ").split()
    record_types = input("Enter DNS record types separated by spaces (e.g., 'A AAAA MX'): ").split()
    reverse = input("Perform reverse DNS lookup (IP to domain)? (yes/no): ").lower() == "yes"
    output_file = input("Specify an output file to save results (leave empty to skip): ").strip()

    if not domain:
        click.echo("Please provide at least one domain or IP address to perform DNS lookup.")
        return

    results = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_domain = {executor.submit(perform_dns_lookup, target, record_types): target for target in domain}
        for future in concurrent.futures.as_completed(future_to_domain):
            target = future_to_domain[future]
            try:
                result = future.result()
                results.extend([f"{target}:"] + result)
            except Exception as exc:
                click.echo(f"An error occurred while performing DNS lookup for {target}: {exc}")

    for result in results:
        click.echo(result)

    if output_file:
        try:
            with open(output_file, "w") as file:
                file.write("\n".join(results))
            click.echo(f"Results saved to {output_file}")
        except Exception as e:
            click.echo(f"Error while writing to {output_file}: {e}")

if __name__ == "__main__":
    dns_explorer()
