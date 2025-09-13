Debugging Guide
===============

This guide covers debugging techniques, common issues, and troubleshooting steps for the Makcu Python Library.

Enable Debug Mode
-----------------

Debug mode provides detailed logging and helps identify issues:

**Synchronous API:**

.. code-block:: python

   from makcu import create_controller
   
   # Enable debug mode
   makcu = create_controller(debug=True)

**Asynchronous API:**

.. code-block:: python

   from makcu import create_async_controller
   
   # Enable debug mode
   makcu = await create_async_controller(debug=True)

Debug Output Examples
---------------------

With debug mode enabled, you'll see detailed command flow:

.. code-block:: text

   [2025.123.456] [INFO] Makcu Controller v2.1.3 starting...
   [2025.123.457] [DEBUG] Scanning for devices (VID:1A86, PID:55D3)
   [2025.123.458] [INFO] Found device on COM3
   [2025.123.459] [DEBUG] Opening serial connection: COM3 @ 4000000 baud
   [2025.123.461] [INFO] Connected successfully
   [2025.123.462] [DEBUG] Sent command #42: km.move(100,50)
   [2025.123.464] [DEBUG] Command #42 completed in 0.002s
   [2025.123.465] [DEBUG] Response: OK

Interactive Debug Console
--------------------------

Use the command-line debug console for real-time troubleshooting:

.. code-block:: bash

   python -m makcu --debug

**Console Features:**

- Real-time command execution
- Live response monitoring  
- Connection status display
- Performance timing
- Error reporting

**Example Debug Session:**

.. code-block:: text

   Makcu Debug Console v2.1.3
   ===========================
   Connecting to device...
   Connected to Makcu device on COM3
   
   > km.version()
   km.MAKCU
   
   > km.move(50,25)
   km.move(50,25)

Common Issues & Solutions
-------------------------

Device Not Found
^^^^^^^^^^^^^^^^^

**Symptoms:**
- ``MakcuConnectionError: No Makcu device found``
- ``Device not detected on any port``

**Solutions:**

1. **Check Physical Connection:**
   
   .. code-block:: bash
   
      # Test specific port
      python -m makcu --testPort COM3

2. **Verify Device Manager (Windows):**
   - Open Device Manager
   - Look for "USB Serial Device" under "Ports (COM & LPT)"
   - Note the COM port number
   - Check for driver issues (yellow warning icons)

3. **Check USB Cable:**
   - Try different USB cable
   - Ensure cable supports data (not power-only)
   - Test with different USB port

4. **Device Power Cycle:**
   
   .. code-block:: python
   
      # In code - retry with delay
      import time
      from makcu import create_controller, MakcuConnectionError
      
      for attempt in range(3):
          try:
              makcu = create_controller(debug=True)
              break
          except MakcuConnectionError:
              print(f"Attempt {attempt + 1} failed, retrying...")
              time.sleep(2)

Permission Denied
^^^^^^^^^^^^^^^^^

**Symptoms:**
- ``PermissionError: [Errno 13] Permission denied``
- ``Access is denied`` (Windows)

**Solutions:**

**Linux/macOS:**

.. code-block:: bash

   # Add user to dialout group
   sudo usermod -a -G dialout $USER
   
   # Or run with sudo (not recommended)
   sudo python your_script.py
   
   # Check port permissions
   ls -l /dev/ttyUSB*

**Windows:**

- Run command prompt/IDE as Administrator
- Check if another application is using the port
- Close Arduino IDE, PuTTY, or other serial applications

Command Timeouts
^^^^^^^^^^^^^^^^

**Symptoms:**
- ``MakcuTimeoutError: Command timed out after 0.1s``
- Intermittent command failures

**Solutions:**

1. **Increase Timeout:**
   
   .. code-block:: python
   
      # Default timeout is 0.1s (100ms)
      makcu = create_controller(timeout=0.5)  # 500ms timeout

2. **Check USB Connection:**
   - Use high-quality USB cable
   - Avoid USB hubs when possible
   - Try different USB ports

3. **Reduce Command Frequency:**
   
   .. code-block:: python
   
      import asyncio
      
      # Add small delays for stability
      async def stable_clicking():
          for _ in range(10):
              await makcu.click(MouseButton.LEFT)
              await asyncio.sleep(0.01)  # 10ms between clicks

Intermittent Disconnections
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Symptoms:**
- Device randomly disconnects
- ``MakcuConnectionError`` during operation

**Solutions:**

1. **Enable Auto-Reconnection:**
   
   .. code-block:: python
   
      makcu = create_controller(auto_reconnect=True, debug=True)
      
      # Or with custom retry settings
      makcu = create_controller(
          auto_reconnect=True,
          reconnect_attempts=5,
          reconnect_delay=1.0
      )

2. **Connection Status Monitoring:**
   
   .. code-block:: python
   
      @makcu.on_connection_change
      def handle_connection(connected: bool):
          if connected:
              print("Device reconnected!")
          else:
              print("Device disconnected - attempting reconnection...")

3. **Robust Error Handling:**
   
   .. code-block:: python
   
      from makcu import MakcuConnectionError
      
      async def robust_operation():
          max_retries = 3
          for attempt in range(max_retries):
              try:
                  await makcu.click(MouseButton.LEFT)
                  return  # Success
              except MakcuConnectionError:
                  if attempt < max_retries - 1:
                      print(f"Retry {attempt + 1}/{max_retries}")
                      await asyncio.sleep(0.5)
                  else:
                      raise  # Final attempt failed

Performance Issues
^^^^^^^^^^^^^^^^^^

**Symptoms:**
- Commands take longer than expected
- High CPU usage
- Memory leaks

**Solutions:**

1. **Disable Debug Mode in Production:**
   
   .. code-block:: python
   
      # Debug mode adds logging overhead
      makcu = create_controller(debug=False)

2. **Use Batch Operations:**
   
   .. code-block:: python
   
      # Instead of individual commands
      for i in range(100):
          makcu.move(1, 0)  # Slow
      
      # Use batch execution
      commands = [lambda: makcu.move(1, 0) for _ in range(100)]
      makcu.batch_execute(commands)  # Fast

3. **Optimize Connection Checks:**
   
   .. code-block:: python
   
      # Use cached connection status
      if makcu.is_connected():  # Fast - cached
          makcu.click(MouseButton.LEFT)
      
      # Avoid repeated connection attempts
      with makcu:  # Context manager ensures connection
          for _ in range(1000):
              makcu.move(1, 0)  # No connection check per call

Memory Usage
^^^^^^^^^^^^

**Monitor Memory Usage:**

.. code-block:: python

   import psutil
   import gc
   
   def monitor_memory():
       process = psutil.Process()
       memory_mb = process.memory_info().rss / 1024 / 1024
       print(f"Memory usage: {memory_mb:.1f} MB")
   
   # Check before and after operations
   monitor_memory()
   # ... your Makcu operations ...
   gc.collect()  # Force garbage collection
   monitor_memory()

**Memory Optimization:**

.. code-block:: python

   # Use context managers for automatic cleanup
   async with await create_async_controller() as makcu:
       # Operations here
       pass  # Automatic cleanup when exiting

   # Explicit cleanup for long-running applications
   makcu.disconnect()
   del makcu

Advanced Debugging
------------------

Custom Logging
^^^^^^^^^^^^^^

Set up custom logging for detailed troubleshooting:

.. code-block:: python

   import logging
   
   # Configure detailed logging
   logging.basicConfig(
       level=logging.DEBUG,
       format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
       handlers=[
           logging.FileHandler('makcu_debug.log'),
           logging.StreamHandler()
       ]
   )
   
   # Create controller with debug enabled
   makcu = create_controller(debug=True)

Raw Command Monitoring
^^^^^^^^^^^^^^^^^^^^^^

Monitor raw serial communication:

.. code-block:: python

   # Access low-level transport
   response = await makcu.transport.async_send_command(
       "km.version()", 
       expect_response=True,
       timeout=0.1
   )
   print(f"Raw response: {response}")

Performance Profiling
^^^^^^^^^^^^^^^^^^^^^^

Profile command execution times:

.. code-block:: python

   import time
   import statistics
   
   # Measure command performance
   timings = []
   for _ in range(100):
       start = time.perf_counter()
       makcu.click(MouseButton.LEFT)
       end = time.perf_counter()
       timings.append((end - start) * 1000)  # Convert to ms
   
   print(f"Average: {statistics.mean(timings):.2f}ms")
   print(f"Min: {min(timings):.2f}ms")
   print(f"Max: {max(timings):.2f}ms")
   print(f"Std Dev: {statistics.stdev(timings):.2f}ms")

Network Debugging (if applicable)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For remote debugging or networked applications:

.. code-block:: python

   import socket
   import json
   
   # Simple debug server
   class MakcuDebugServer:
       def __init__(self, port=8888):
           self.sock = socket.socket()
           self.sock.bind(('localhost', port))
           self.sock.listen(1)
           print(f"Debug server listening on port {port}")
       
       def handle_commands(self, makcu):
           conn, addr = self.sock.accept()
           try:
               while True:
                   data = conn.recv(1024).decode()
                   if not data:
                       break
                   
                   # Execute command and return result
                   try:
                       result = eval(f"makcu.{data}")
                       response = {"status": "ok", "result": str(result)}
                   except Exception as e:
                       response = {"status": "error", "error": str(e)}
                   
                   conn.send(json.dumps(response).encode())
           finally:
               conn.close()

Test Suite Analysis
-------------------

Run comprehensive tests to identify issues:

.. code-block:: bash

   python -m makcu --runtest

**Test Categories:**

1. **Connection Tests:**
   - Port detection
   - Device recognition

2. **Functionality Tests:**
   - Mouse movement accuracy
   - Button control
   - Scrolling behavior

3. **Performance Tests:**
   - Command execution speed
   - Memory usage
   - CPU utilization

4. **Reliability Tests:**
   - Auto-reconnection
   - Error recovery
   - Long-running stability

**Interpreting Test Results:**

.. code-block:: text

   test_connect_to_port PASSED (0.046s)     ✓ Good performance
   test_mouse_movement FAILED               ❌ Check USB connection
   test_button_control PASSED (0.001s)     ✓ Excellent timing
   test_performance SLOW (0.150s)          ⚠️ Performance regression

Debugging Checklist
--------------------

When encountering issues, work through this checklist:

**Hardware:**
- [ ] USB cable connected securely
- [ ] Device powered on
- [ ] Try different USB port
- [ ] Test with different USB cable

**Software:**
- [ ] Latest Makcu library version installed
- [ ] Python version 3.8+ 
- [ ] No conflicting serial applications running
- [ ] Proper permissions (Linux/macOS)

**Connection:**
- [ ] Device appears in Device Manager (Windows)
- [ ] Correct COM port identified
- [ ] Port not in use by other applications
- [ ] Baud rate properly configured

**Code:**
- [ ] Debug mode enabled
- [ ] Proper error handling implemented
- [ ] Timeouts configured appropriately
- [ ] Auto-reconnection enabled if needed

**Performance:**
- [ ] Debug mode disabled in production
- [ ] Batch operations used where possible
- [ ] Memory usage monitored
- [ ] Connection checks optimized

Getting Help
------------

If you're still experiencing issues:

1. **Check GitHub Issues:**
   - Search existing issues: https://github.com/SleepyTotem/makcu-py-lib/issues
   - Create new issue with debug logs

2. **Enable Comprehensive Logging:**
   
   .. code-block:: python
   
      import logging
      logging.basicConfig(level=logging.DEBUG)
      makcu = create_controller(debug=True)

3. **Include System Information:**
   - Operating system and version
   - Python version
   - Makcu library version
   - Device firmware version
   - Full error traceback

4. **Provide Minimal Reproducible Example:**
   
   .. code-block:: python
   
      from makcu import create_controller, MouseButton
      
      # Minimal code that reproduces the issue
      makcu = create_controller(debug=True)
      makcu.click(MouseButton.LEFT)  # Fails here

5. **Community Resources:**
   - GitHub Discussions: https://github.com/SleepyTotem/makcu-py-lib/discussions
   - Stack Overflow with tag `makcu`