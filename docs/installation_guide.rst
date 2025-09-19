Installation Guide
==================

This guide covers all the ways to install the Makcu Python library and get started with controlling your Makcu device.

Requirements
------------

**System Requirements:**

* Python 3.7 or higher
* Windows, macOS, or Linux
* USB port for device connection

**Python Dependencies:**

The Makcu library automatically installs these dependencies:

* ``pyserial`` - Serial communication
* ``asyncio`` - Async support (Python 3.7+)

Installation Methods
--------------------

PyPI Installation (Recommended)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The easiest way to install Makcu is from PyPI using pip:

.. code-block:: bash

    pip install makcu

This installs the latest stable version with all dependencies.

**Verify Installation:**

.. code-block:: python

    import makcu
    print(f"Makcu version: {makcu.__version__}")

Install Specific Version
^^^^^^^^^^^^^^^^^^^^^^^^

To install a specific version:

.. code-block:: bash

    # Install latest v2.x
    pip install "makcu>=2.0.0,<3.0.0"
    
    # Install exact version
    pip install makcu==2.2.1

From Source (Development)
^^^^^^^^^^^^^^^^^^^^^^^^^^

For development or the latest features:

.. code-block:: bash

    # Clone the repository
    git clone https://github.com/SleepyTotem/makcu-py-lib
    cd makcu-py-lib
    
    # Install in development mode
    pip install -e .

**Development Installation with Dependencies:**

.. code-block:: bash

    # Install with development dependencies
    pip install -e .[dev]
    
    # Or install test dependencies
    pip install -e .[test]

Virtual Environment Setup
--------------------------

Using venv (Recommended)
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # Create virtual environment
    python -m venv makcu-env
    
    # Activate (Windows)
    makcu-env\Scripts\activate
    
    # Activate (macOS/Linux)
    source makcu-env/bin/activate
    
    # Install makcu
    pip install makcu

Using conda
^^^^^^^^^^^

.. code-block:: bash

    # Create conda environment
    conda create -n makcu-env python=3.9
    conda activate makcu-env
    
    # Install makcu
    pip install makcu

Docker Installation
-------------------

For containerized applications:

.. code-block:: dockerfile

    FROM python:3.9-slim

    # Install makcu
    RUN pip install makcu

    # Your application code
    COPY . /app
    WORKDIR /app

    CMD ["python", "your_app.py"]

**Note:** USB device access in Docker requires additional configuration:

.. code-block:: bash

    # Run with device access
    docker run --device=/dev/ttyUSB0 your-image

Post-Installation Setup
-----------------------

Device Connection
^^^^^^^^^^^^^^^^^

After installation, connect your Makcu device:

1. Plug in your Makcu device via USB
2. Windows will automatically install drivers
3. The device appears as a COM port (Windows) or /dev/tty* (Linux/macOS)

**Verify Device Connection:**

.. code-block:: python

    from makcu import create_controller

    try:
        makcu = create_controller()
        print("✅ Device connected successfully!")
        print(f"Device info: {makcu.get_device_info()}")
        makcu.disconnect()
    except Exception as e:
        print(f"❌ Connection failed: {e}")

Command-Line Tools
^^^^^^^^^^^^^^^^^^

Test your installation with built-in tools:

.. code-block:: bash

    # Interactive debug console
    python -m makcu --debug
    
    # Test specific port
    python -m makcu --testPort COM3
    
    # Run test suite
    python -m makcu --runtest

Troubleshooting Installation
----------------------------

Common Issues
^^^^^^^^^^^^^

**Permission Errors (Linux/macOS):**

.. code-block:: bash

    # Add user to dialout group (Linux)
    sudo usermod -a -G dialout $USER
    
    # Log out and back in, or run:
    sudo chmod 666 /dev/ttyUSB0

**Driver Issues (Windows):**

1. Download CH343 drivers from manufacturer
2. Install drivers manually if Windows doesn't auto-install
3. Check Device Manager for COM port assignment

**Python Version Issues:**

.. code-block:: bash

    # Check Python version
    python --version
    
    # Must be 3.7 or higher
    # Upgrade if needed
    python -m pip install --upgrade pip

Dependency Conflicts
^^^^^^^^^^^^^^^^^^^^

If you encounter dependency conflicts:

.. code-block:: bash

    # Create clean environment
    python -m venv clean-env
    source clean-env/bin/activate  # or activate.bat on Windows
    
    # Install only makcu
    pip install makcu

**Specific Conflict Resolution:**

.. code-block:: bash

    # Force reinstall
    pip install --force-reinstall makcu
    
    # Install with no dependencies (advanced)
    pip install --no-deps makcu
    pip install pyserial  # Install dependencies manually

Offline Installation
--------------------

For systems without internet access:

**Download Packages:**

.. code-block:: bash

    # On internet-connected machine
    pip download makcu -d makcu-packages/
    
    # Transfer makcu-packages/ to offline machine
    
    # Install offline
    pip install makcu --find-links makcu-packages/ --no-index

Verification Tests
------------------

Quick Test
^^^^^^^^^^

.. code-block:: python

    #!/usr/bin/env python3
    """Quick installation test"""
    
    import sys
    import makcu
    from makcu import create_controller, MouseButton

    def test_installation():
        print(f"✅ Makcu imported successfully")
        print(f"📦 Version: {makcu.__version__}")
        
        try:
            # Test controller creation
            controller = create_controller()
            print(f"✅ Controller created")
            
            # Test device info
            info = controller.get_device_info()
            print(f"📱 Device: {info}")
            
            controller.disconnect()
            print(f"✅ All tests passed!")
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            return False
        
        return True

    if __name__ == "__main__":
        success = test_installation()
        sys.exit(0 if success else 1)

Full Test Suite
^^^^^^^^^^^^^^^

Run the comprehensive test suite:

.. code-block:: bash

    # Run all tests
    python -m makcu --runtest
    
    # This will:
    # 1. Test device connection
    # 2. Verify all mouse functions
    # 3. Check button states and locking
    # 4. Generate HTML report

Upgrading
---------

Upgrade to Latest Version
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # Upgrade to latest
    pip install --upgrade makcu
    
    # Check new version
    python -c "import makcu; print(makcu.__version__)"

Migration Between Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^

**From v1.x to v2.x:**

Most code remains compatible, but v2.x adds async support:

.. code-block:: python

    # v1.x code (still works)
    from makcu import create_controller
    makcu = create_controller()
    makcu.click(MouseButton.LEFT)

    # v2.x async code (new)
    import asyncio
    from makcu import create_async_controller
    
    async def main():
        async with await create_async_controller() as makcu:
            await makcu.click(MouseButton.LEFT)
    
    asyncio.run(main())

Uninstallation
--------------

To remove Makcu completely:

.. code-block:: bash

    # Uninstall makcu
    pip uninstall makcu
    
    # Remove configuration (if any)
    # Location varies by OS

Getting Help
------------

If installation fails:

1. **Check Requirements**: Python 3.7+, pip up-to-date
2. **Try Virtual Environment**: Isolate from other packages  
3. **Update pip**: ``python -m pip install --upgrade pip``
4. **Check Issues**: `GitHub Issues <https://github.com/SleepyTotem/makcu-py-lib/issues>`_
5. **Ask for Help**: `GitHub Discussions <https://github.com/SleepyTotem/makcu-py-lib/discussions>`_

**System Information for Bug Reports:**

.. code-block:: python

    import sys
    import platform
    
    print(f"Python: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Architecture: {platform.architecture()}")
    
    try:
        import makcu
        print(f"Makcu: {makcu.__version__}")
    except ImportError as e:
        print(f"Makcu import failed: {e}")

Next Steps
----------

After successful installation:

1. 📖 Read the :doc:`getting_started` guide
2. 🚀 Try the :doc:`async_usage` examples  
3. 📚 Explore the :doc:`api/index` reference
4. 🎮 Check out :doc:`examples/index` for your use case