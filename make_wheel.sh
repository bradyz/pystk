# Usage: source make_wheel.sh 3.10
# Check if a Python version argument was provided
if [[ -z "$1"  ]]; then
      echo "Usage: $0 <python-version>"
        exit 1
fi

# Set the Python version and environment name
PYTHON_VERSION=$1
ENV_NAME="new_temp_env_$PYTHON_VERSION"

# Create the Anaconda environment
echo "Creating Anaconda environment $ENV_NAME with Python $PYTHON_VERSION..."
conda create --name $ENV_NAME python=$PYTHON_VERSION -y

# Activate the environment
echo "Activating environment..."
conda activate $ENV_NAME

# Run the command
echo "Running setup.py bdist_wheel..."

export CMAKE_BUILD_PARALLEL_LEVEL=16
python setup.py bdist_wheel

# Install the built wheel, check if it's the right path
WHEEL_PATH=$(ls -t dist/*.whl | head -n 1)

echo "Installing wheel $WHEEL_PATH"
pip install --force-reinstall $WHEEL_PATH

# Some basic tests
pip install numpy
python examples/benchmark.py
python examples/test_pickle.py

# Done
echo "You might want to clean up $ENV_NAME"
echo "# conda deactivate"
echo "# conda env remove --name $ENV_NAME -y"