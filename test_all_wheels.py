import os
import sys
import subprocess
import glob
import platform

def find_wheels():
    """Find all wheel files in the wheelhouse directory."""
    wheels = glob.glob("./wheelhouse/*.whl")
    if not wheels:
        print("No wheels found in ./wheelhouse/")
        return []
    return wheels

def install_wheel(wheel_path):
    """Try to install the wheel."""
    print(f"Installing wheel: {wheel_path}")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--force-reinstall", wheel_path])
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install wheel: {e}")
        return False

def run_benchmark():
    """Run the benchmark script."""
    print("Running benchmark...")
    try:
        result = subprocess.run(
            [sys.executable, "examples/benchmark.py", "--track", "abyss"],
            capture_output=True,
            text=True,
            timeout=180
        )
        print(f"Benchmark stdout:\n{result.stdout}")
        if result.stderr:
            print(f"Benchmark stderr:\n{result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"Error running benchmark: {e}")
        return False

def main():
    wheels = find_wheels()
    if not wheels:
        sys.exit(1)
    
    # Filter wheels for current platform
    current_platform = platform.system().lower()
    platform_markers = {
        'linux': 'linux',
        'darwin': 'macosx',
        'windows': 'win'
    }
    
    marker = platform_markers.get(current_platform)
    compatible_wheels = [w for w in wheels if marker in w.lower()]
    
    if not compatible_wheels:
        print(f"No compatible wheels found for {current_platform}")
        sys.exit(1)
    
    failures = []
    
    for wheel in compatible_wheels:
        print(f"\n\nTesting wheel: {wheel}")
        # Create virtual environment for isolation
        venv_dir = f"venv_{os.path.basename(wheel)}"
        subprocess.call([sys.executable, "-m", "venv", venv_dir])
        
        # Get path to Python in venv
        if current_platform == 'windows':
            venv_python = os.path.join(venv_dir, "Scripts", "python.exe")
        else:
            venv_python = os.path.join(venv_dir, "bin", "python")
        
        # Install wheel and test
        try:
            subprocess.check_call([venv_python, "-m", "pip", "install", wheel])
            # Copy benchmark script to venv directory
            test_script = os.path.join(venv_dir, "benchmark.py")
            with open("examples/benchmark.py", "r") as src, open(test_script, "w") as dst:
                dst.write(src.read())
                
            result = subprocess.run(
                [venv_python, test_script, "--track", "abyss"],
                capture_output=True,
                text=True,
                timeout=180
            )
            
            if result.returncode != 0:
                print(f"Benchmark failed for {wheel}")
                print(f"Output: {result.stdout}")
                print(f"Error: {result.stderr}")
                failures.append(wheel)
            else:
                print(f"Successfully tested {wheel}")
        except Exception as e:
            print(f"Error testing {wheel}: {e}")
            failures.append(wheel)
    
    if failures:
        print(f"\n\nThe following wheels failed: {failures}")
        sys.exit(1)
    else:
        print("\n\nAll wheels were tested successfully!")
        sys.exit(0)

if __name__ == "__main__":
    main()
