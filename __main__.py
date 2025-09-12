import sys
import os
from pathlib import Path
from typing import List, NoReturn, Optional, Tuple
import pytest
import time
from makcu import create_controller, MakcuConnectionError, MakcuController
import json
import re
import subprocess

makcu_version = "v2.1.3"

def debug_console():
    controller = create_controller()
    transport = controller.transport

    print("🔧 Makcu Debug Console")
    print("Type a raw command (e.g., km.version()) and press Enter.")
    print("Type 'exit' or 'quit' to leave.")

    command_counter = 0

    while True:
        try:
            cmd = input(">>> ").strip()
            if cmd.lower() in {"exit", "quit"}:
                break
            if not cmd:
                continue

            command_counter += 1
            
            response = transport.send_command(cmd, expect_response=True)
            
            if response and response.strip():
                if response.strip() == cmd:
                    print(f"{cmd}")
                else:
                    print(f"{response}")
            else:
                print("(no response)")

        except Exception as e:
            print(f"⚠️ Error: {e}")

    controller.disconnect()
    print("Disconnected.")

def test_port(port: str) -> None:
    try:
        print(f"Trying to connect to {port}...")
        makcu = MakcuController(fallback_com_port=port, send_init=False, override_port=True)
        makcu.connect()
        if makcu.is_connected:
            print(f"✅ Successfully connected to {port}.")
        makcu.disconnect()
    except MakcuConnectionError as e:
        if "FileNotFoundError" in str(e):
            print(f"❌ Port {port} does not exist. Please check the port name.")
        else:
            print(f"❌ Failed to connect to {port}: ") 
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def check_pytest_html_installed() -> bool:
    """Check if pytest-html is installed."""
    try:
        import pytest_html
        return True
    except ImportError:
        return False

def find_writable_directory() -> Path:
    """Find a writable directory for the HTML report."""
    # Try current working directory first
    cwd = Path.cwd()
    if os.access(cwd, os.W_OK):
        return cwd
    
    # Try user's home directory
    home = Path.home()
    if os.access(home, os.W_OK):
        return home
    
    # Try temp directory as last resort
    import tempfile
    return Path(tempfile.gettempdir())

def parse_html_results(html_file: Path) -> Tuple[List[Tuple[str, str, int]], int]:
    if not html_file.exists():
        raise FileNotFoundError(f"HTML report not found: {html_file}")
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    match = re.search(r'data-jsonblob="([^"]*)"', content)
    if not match:
        raise ValueError("Could not find JSON data in HTML report")
    
    json_str = match.group(1)
    json_str = json_str.replace('&#34;', '"').replace('&amp;#x27;', "'").replace('&amp;', '&')
    
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON data: {e}")
    
    test_results = []
    total_ms = 0
    
    skip_tests = {'test_connect_to_port'}
    
    for test_id, test_data_list in data.get('tests', {}).items():
        test_name = test_id.split('::')[-1]
        if test_name in skip_tests:
            continue
            
        for test_data in test_data_list:
            status = test_data.get('result', 'UNKNOWN')
            duration_str = test_data.get('duration', '0 ms')
            
            duration_match = re.search(r'(\d+)\s*ms', duration_str)
            duration_ms = int(duration_match.group(1)) if duration_match else 0
            total_ms += duration_ms
            
            test_results.append((test_name, status, duration_ms))
    
    return test_results, total_ms

def run_tests() -> NoReturn:
    # Check if pytest-html is installed
    if not check_pytest_html_installed():
        print("❌ pytest-html is not installed. Please install it via:")
        print("   pip install pytest-html")
        sys.exit(1)
    
    try:
        from rich.console import Console
        from rich.table import Table
        from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
        from rich.panel import Panel
        from rich.align import Align
        from rich import print as rprint
        from rich.text import Text

        console = Console()

        header = Panel.fit(
            f"[bold cyan]Makcu Test Suite {makcu_version}[/bold cyan]\n[dim]High-Performance Python Library[/dim]",
            border_style="bright_blue"
        )
        console.print(Align.center(header))
        console.print()

        package_dir: Path = Path(__file__).resolve().parent
        test_file: Path = package_dir / "test_suite.py"
        
        # Find writable directory and create HTML path
        writable_dir = find_writable_directory()
        html_file: Path = writable_dir / "latest_pytest.html"
        
        # Clean up old report if it exists
        if html_file.exists():
            try:
                html_file.unlink()
            except Exception:
                pass

        console.print(f"[dim]Running pytest to generate: {html_file}[/dim]")
        console.print(f"[dim]Working directory: {Path.cwd()}[/dim]")

        start_time = time.time()

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task("[cyan]Running tests...", total=100)

            # Run pytest with explicit output capturing
            result = subprocess.run(
                [
                    sys.executable, "-m", "pytest",
                    str(test_file),
                    "--rootdir", str(package_dir),
                    "-q",
                    "--tb=no",
                    "--html", str(html_file),
                    "--self-contained-html",
                    "-v"  # Add verbose to help debug
                ],
                capture_output=True,
                text=True
            )

            progress.update(task, completed=100)

        # Check if HTML file was created
        if not html_file.exists():
            console.print(f"[red]❌ HTML report was not created at: {html_file}[/red]")
            console.print(f"[yellow]pytest exit code: {result.returncode}[/yellow]")
            if result.stdout:
                console.print("[yellow]stdout:[/yellow]")
                console.print(result.stdout)
            if result.stderr:
                console.print("[red]stderr:[/red]")
                console.print(result.stderr)
            
            # Try to run tests without HTML report
            console.print("\n[yellow]Running tests without HTML report...[/yellow]")
            result2 = subprocess.run(
                [sys.executable, "-m", "pytest", str(test_file), "-v"],
                capture_output=True,
                text=True
            )
            console.print(result2.stdout)
            sys.exit(1)

        try:
            test_results, total_ms = parse_html_results(html_file)
        except (FileNotFoundError, ValueError) as e:
            console.print(f"[red]❌ Failed to parse test results: {e}[/red]")
            console.print(f"[yellow]⚠️ pytest exit code: {result.returncode}[/yellow]")
            sys.exit(1)

        elapsed_time = time.time() - start_time

        table = Table(title="[bold]Test Results[/bold]", show_header=True, header_style="bold magenta")
        table.add_column("Test", style="cyan", no_wrap=True)
        table.add_column("Status", justify="center")
        table.add_column("Time", justify="right", style="yellow")
        table.add_column("Performance", justify="center")

        passed = failed = skipped = 0

        for test_name, status, duration_ms in test_results:
            display_name = test_name.replace("test_", "").replace("_", " ").title()

            if status.upper() == "PASSED":
                status_text = "[green]✅ PASSED[/green]"
                passed += 1
            elif status.upper() == "FAILED":
                status_text = "[red]❌ FAILED[/red]"
                failed += 1
            elif status.upper() == "SKIPPED":
                status_text = "[yellow]⏭️ SKIPPED[/yellow]"
                skipped += 1
            else:
                status_text = status

            time_str = f"{duration_ms}ms" if duration_ms else "-"
            if duration_ms <= 3:
                perf = "[green]Excellent[/green]"
            elif duration_ms <= 5:
                perf = "[cyan]Great[/cyan]"
            elif duration_ms <= 10:
                perf = "[yellow]Good[/yellow]"
            elif duration_ms > 0:
                perf = "[red]🐌 Needs work[/red]"
            else:
                perf = "-"

            table.add_row(display_name, status_text, time_str, perf)

        console.print("\n")
        console.print(table)
        console.print()

        summary = Table.grid(padding=1)
        summary.add_column(style="bold cyan", justify="right")
        summary.add_column(justify="left")
        summary.add_row("Total Tests:", str(len(test_results)))
        summary.add_row("Passed:", f"[green]{passed}[/green]")
        summary.add_row("Failed:", f"[red]{failed}[/red]" if failed else str(failed))
        summary.add_row("Skipped:", f"[yellow]{skipped}[/yellow]" if skipped else str(skipped))
        summary.add_row("Total Time:", f"{elapsed_time:.2f}s")
        summary.add_row("Avg Time/Test:", f"{total_ms/len(test_results):.1f}ms" if test_results else "0ms")

        console.print(Align.center(Panel(summary, title="[bold]Summary[/bold]", border_style="blue", expand=False)))
        console.print()

        if test_results:
            avg_time = total_ms / len(test_results)
            if avg_time < 3:
                perf_text = Text("Performance: ELITE - Ready for 360Hz+ gaming!", style="bold bright_green")
            elif avg_time < 5:
                perf_text = Text("Performance: EXCELLENT - Ready for 240Hz+ gaming!", style="bold green")
            elif avg_time < 10:
                perf_text = Text("Performance: GREAT - Ready for 144Hz gaming!", style="bold cyan")
            else:
                perf_text = Text("Performance: GOOD - Suitable for standard gaming", style="bold yellow")
        else:
            perf_text = Text("⚠️ No test results parsed. Check your test suite.", style="bold red")

        console.print(Align.center(Panel(perf_text, border_style="green")))
        
        # Print the location of the HTML report
        console.print(f"\n[dim]HTML report saved to: {html_file}[/dim]")
        
        sys.exit(0 if failed == 0 else 1)

    except ImportError:
        print("📦 Rich not installed. Install it via `pip install rich` for enhanced output.")
        print("\nFallback to raw pytest output...\n")

        package_dir: Path = Path(__file__).resolve().parent
        test_file: Path = package_dir / "test_suite.py"
        
        # Find writable directory
        writable_dir = find_writable_directory()
        html_file: Path = writable_dir / "latest_pytest.html"
        
        print(f"HTML report will be saved to: {html_file}")

        # Use subprocess instead of pytest.main for better control
        result = subprocess.run(
            [
                sys.executable, "-m", "pytest",
                str(test_file),
                "--rootdir", str(package_dir),
                "-q",
                "--tb=no",
                "--html", str(html_file),
                "--self-contained-html"
            ],
            capture_output=True,
            text=True
        )

        if not html_file.exists():
            print(f"\n❌ HTML report was not created. pytest exit code: {result.returncode}")
            if result.stdout:
                print("stdout:", result.stdout)
            if result.stderr:
                print("stderr:", result.stderr)
            sys.exit(1)

        try:
            test_results, total_ms = parse_html_results(html_file)
            passed = sum(1 for _, status, _ in test_results if status.upper() == "PASSED")
            failed = sum(1 for _, status, _ in test_results if status.upper() == "FAILED")
            skipped = sum(1 for _, status, _ in test_results if status.upper() == "SKIPPED")
            
            print(f"\n📊 Results: {passed} passed, {failed} failed, {skipped} skipped")
            if test_results:
                avg_time = total_ms / len(test_results)
                print(f"⏱️ Average time per test: {avg_time:.1f}ms")
        except (FileNotFoundError, ValueError):
            print("\n⚠️ Could not parse HTML results for summary")

        if result.returncode != 0:
            print("\n❌ Some tests failed.")
        else:
            print("\n✅ All tests passed.")

        sys.exit(result.returncode)
    
def main() -> None:
    args: List[str] = sys.argv[1:]

    if not args:
        print("Usage:")
        print("  python -m makcu --debug")
        print("  python -m makcu --testPort COM3")
        print("  python -m makcu --runtest")
        return

    if args[0] == "--debug":
        debug_console()
    elif args[0] == "--testPort" and len(args) == 2:
        test_port(args[1])
    elif args[0] == "--runtest":
        run_tests()
    else:
        print(f"Unknown command: {' '.join(args)}")
        print("Usage:")
        print("  python -m makcu --debug")
        print("  python -m makcu --testPort COM3")
        print("  python -m makcu --runtest")

if __name__ == "__main__":
    main()