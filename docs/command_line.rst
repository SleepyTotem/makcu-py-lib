Command Line Interface
======================

The Makcu Python Library provides several command-line tools for testing, debugging, and development. These tools are accessible through Python's module execution syntax.

Overview
--------

All command-line tools are accessed via:

.. code-block:: bash

   python -m makcu [OPTION]

Available Options
-----------------

``--debug``
^^^^^^^^^^^

Launches an interactive debug console where you can send raw commands directly to your Makcu device and see live responses.

**Usage:**

.. code-block:: bash

   python -m makcu --debug

**Features:**
- Real-time command execution
- Live response monitoring
- Connection status display
- Error handling and reporting
- Exit with ``quit`` or ``exit``

**Example Session:**

.. code-block:: text

   🔧 Makcu Debug Console
   Type a raw command (e.g., km.version()) and press Enter.
   Type 'exit' or 'quit' to leave
   
   > km.version()
   Response: km.MAKCU
   
   > km.move(100,50)
   Response: km.move(100,50)

   > km.click(1)
   Response: km.click(1)

   > quit
   Disconnecting...

``--testPort``
^^^^^^^^^^^^^^

Tests connection to a specific COM port and reports success or failure.

**Usage:**

.. code-block:: bash

   python -m makcu --testPort COM3
   python -m makcu --testPort /dev/ttyUSB0  # Linux/macOS

**Output Examples:**

*Successful connection:*

.. code-block:: text

   Trying to connect to COM1...
   ✅ Successfully connected to COM1.

*Failed connection:*

.. code-block:: text

   Testing connection to COM2...
   ❌ Port COM2 does not exist. Please check the port name.

**Use Cases:**
- Verify device connectivity
- Troubleshoot connection issues
- Identify correct COM port
- Automated testing scripts

``--runtest``
^^^^^^^^^^^^^

Executes the complete test suite using pytest and generates a detailed HTML report.

**Usage:**

.. code-block:: bash

   python -m makcu --runtest

**What it does:**
1. Runs ``test_suite.py`` with pytest
2. Generates ``latest_pytest.html`` report
3. Automatically opens the report in your default browser
4. Provides comprehensive test results

**Test Categories:**
- Port connection tests
- Mouse movement accuracy
- Button control verification
- Locking mechanism tests
- Performance benchmarks

**Example Output:**

.. code-block:: text

   Running Makcu Test Suite...
   ============================
   
   test_suite.py::test_connect_to_port PASSED          [ 10%]
   test_suite.py::test_firmware_version PASSED         [ 20%]
   test_suite.py::test_mouse_movement PASSED           [ 30%]
   test_suite.py::test_button_control PASSED           [ 40%]
   test_suite.py::test_button_locking PASSED           [ 50%]
   test_suite.py::test_performance_timing PASSED       [ 60%]
   test_suite.py::test_batch_commands PASSED           [ 70%]
   test_suite.py::test_human_like_clicking PASSED      [ 80%]
   test_suite.py::test_auto_reconnection PASSED        [ 90%]
   test_suite.py::test_async_operations PASSED         [100%]
   
   ==================== 10 passed, 0 failed ====================
   
   HTML report generated: latest_pytest.html
   Opening report in browser...

Error Handling
--------------

All command-line tools include comprehensive error handling:

**Device Not Found:**

.. code-block:: text

   Error: No Makcu device found
   Solutions:
   - Check USB connection
   - Verify device is powered on
   - Try different USB port
   - Check device manager (Windows)
   - Install device drivers (Makcu Discord Server)

**Permission Errors:**

.. code-block:: text

   Error: Permission denied accessing COM port
   Solutions:
   - Run as administrator (Windows)
   - Add user to dialout group (Linux)
   - Check port permissions

**Invalid Arguments:**

.. code-block:: text

   Unknown command: --invalid
   
   Usage: python -m makcu [OPTION]
   Options:
     --debug      Interactive debug console
     --testPort   Test specific port connection
     --runtest    Run complete test suite

Integration with Scripts
------------------------

The command-line tools can be integrated into automated workflows:

**Batch Testing:**

.. code-block:: bash

   #!/bin/bash
   # test_makcu.sh
   
   echo "Testing Makcu device..."
   python -m makcu --testPort COM3
   
   if [ $? -eq 0 ]; then
       echo "Running full test suite..."
       python -m makcu --runtest
   else
       echo "Device not ready, skipping tests"
   fi

**CI/CD Integration:**

.. code-block:: yaml

   # .github/workflows/test.yml
   name: Test Makcu Library
   
   steps:
     - name: Install dependencies
       run: pip install makcu pytest
       
     - name: Test device connection
       run: python -m makcu --testPort COM3
       
     - name: Run test suite
       run: python -m makcu --runtest

**Python Script Integration:**

.. code-block:: python

   import subprocess
   import sys
   
   def test_device_ready():
       """Test if Makcu device is ready"""
       result = subprocess.run([
           sys.executable, '-m', 'makcu', '--testPort', 'COM3'
       ], capture_output=True, text=True)
       
       return result.returncode == 0
   
   if test_device_ready():
       print("Device ready")
   else:
       print("Device not available")

Advanced Usage
--------------

**Debug Console with Logging:**

.. code-block:: bash

   python -m makcu --debug

**Automated Port Testing:**

.. code-block:: bash

   # Test multiple ports
   for port in COM3 COM4 COM5; do
       echo "Testing $port..."
       python -m makcu --testPort $port
   done

Performance Monitoring
----------------------

The command-line tools provide performance insights:

**Test Suite Benchmarks:**

The ``--runtest`` option includes performance benchmarks that compare current performance against baseline metrics, helping identify performance regressions.

**Port Testing:**

The ``--testPort`` option measures connection establishment, useful for optimizing connection parameters.

Troubleshooting
---------------

**Common Issues:**

1. **"Module not found" error:**
   
   .. code-block:: bash
   
      pip install makcu

2. **"No device found" repeatedly:**
   
   - Check device manager
   - Try different USB ports
   - Restart device
   - Update drivers

3. **Permission denied on Linux/macOS:**
   
   .. code-block:: bash
   
      sudo usermod -a -G dialout $USER
      # Then log out and back in

4. **Tests fail intermittently:**
   
   - Check USB cable quality
   - Reduce USB hub usage
   - Close other serial applications

Exit Codes
-----------

All command-line tools return standard exit codes:

- ``0``: Success
- ``1``: General error
- ``2``: Device not found
- ``3``: Permission denied
- ``4``: Timeout
- ``5``: Invalid arguments