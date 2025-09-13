Connection and Transport API Reference
=====================================

The Makcu library handles device connections and communication through its controller classes. This document covers the connection-related features available in the Makcu Python library v2.2.0.

.. currentmodule:: makcu

Connection Management
--------------------

Creating Controllers
^^^^^^^^^^^^^^^^^^^

The library provides two main ways to create and connect to Makcu devices:

**Synchronous Controller:**

.. code-block:: python

   from makcu import create_controller
   
   # Create controller with auto-discovery
   makcu = create_controller(debug=True, auto_reconnect=True)
   
   # Controller automatically connects to first available device
   # No manual connection step required

**Asynchronous Controller:**

.. code-block:: python

   from makcu import create_async_controller
   
   # Create async controller
   makcu = await create_async_controller(debug=True, auto_reconnect=True)
   
   # Use with context manager for automatic cleanup
   async with await create_async_controller(debug=True) as makcu:
       await makcu.click(MouseButton.LEFT)

Device Discovery
^^^^^^^^^^^^^^^

The library automatically discovers Makcu devices using their hardware identifiers:

* **Vendor ID (VID)**: 1A86
* **Product ID (PID)**: 55D3  
* **Protocol**: CH343 USB serial at 4Mbps

.. code-block:: python

   # Auto-discovery happens automatically when creating controllers
   makcu = create_controller()  # Finds and connects to first available device

Connection Status
^^^^^^^^^^^^^^^

.. code-block:: python

   # Check if device is connected
   if makcu.is_connected():
       print("Device is ready for commands")
   else:
       print("Device not connected")

.. code-block:: python

   # Manual disconnection (cleanup)
   makcu.disconnect()

Auto-Reconnection
^^^^^^^^^^^^^^^^

The library includes automatic reconnection capabilities:

.. code-block:: python

   # Enable auto-reconnection when creating controller
   makcu = create_controller(auto_reconnect=True)
   
   # Device will automatically reconnect if unplugged and reconnected
   # No manual intervention required

Connection callbacks can be registered to monitor connection status:

.. code-block:: python

   @makcu.on_connection_change
   async def handle_connection(connected: bool):
       if connected:
           print("Device reconnected!")
       else:
           print("Device disconnected!")

.. code-block:: python

   # Manual reconnection if needed
   if not makcu.is_connected():
       await makcu.connect()

Device Information
-----------------

Device Details
^^^^^^^^^^^^^

.. code-block:: python

   # Get comprehensive device information
   info = await makcu.get_device_info()
   print(info)
   
   # Returns dictionary with device details:
   # {'port': 'COM3', 'vid': '0x1a86', 'pid': '0x55d3', ...}

Firmware Version
^^^^^^^^^^^^^^^

.. code-block:: python

   # Get device firmware version
   version = await makcu.get_firmware_version()
   print(f"Firmware version: {version}")

Context Managers
---------------

Automatic Connection Management
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Synchronous context manager
   with makcu:  # Ensures connection for the block
       makcu.click(MouseButton.LEFT)
       # Automatic cleanup when exiting block

.. code-block:: python

   # Asynchronous context manager  
   async with await create_async_controller() as makcu:
       await makcu.click(MouseButton.LEFT)
       # Automatic cleanup and disconnection

Low-Level Transport Access
-------------------------

Advanced users can access the underlying transport layer:

.. code-block:: python

   # Send raw commands with tracked responses
   response = await makcu.transport.async_send_command(
       "km.version()", 
       expect_response=True,
       timeout=0.1  # Optimized for gaming performance
   )

Communication Protocol
---------------------

The Makcu device uses an ASCII-based command protocol:

**Command Format:**
.. code-block:: text

   Basic commands: command_name(parameters)
   Tracked commands: command_name(parameters)#ID

**Response Format:**  
.. code-block:: text

   Basic responses: response_data
   Tracked responses: >>> #ID:response_data

**Technical Details:**
- **Baudrate**: 4Mbps (4,000,000 baud)
- **Format**: 8 data bits, no parity, 1 stop bit (8N1)
- **Buffer Size**: 4KB read buffer, 256B line buffer
- **Timeouts**: 100ms default (gaming-optimized)
- **Command Tracking**: Unique ID system for command/response matching

Performance Optimization
-----------------------

The connection system is optimized for high-frequency gaming operations:

**Key Optimizations:**
- Pre-computed commands at initialization
- Gaming-optimized timeouts (100ms default)
- Zero-delay command execution
- Cached connection states
- High-priority listener thread

**Performance Targets Met:**
- **144Hz Gaming**: 7ms frame time - ✅ Easily met (avg 1-3ms per operation)
- **240Hz Gaming**: 4.2ms frame time - ✅ Consistently met (most ops ≤ 2ms)  
- **360Hz Gaming**: 2.8ms frame time - ⚡ Achievable for atomic operations

Error Handling
-------------

Connection Errors
^^^^^^^^^^^^^^^^

.. code-block:: python

   from makcu import MakcuConnectionError, MakcuTimeoutError
   
   try:
       makcu = await create_async_controller()
   except MakcuConnectionError as e:
       print(f"Connection failed: {e}")
       # Device not found, port in use, or driver issues
   
   try:
       response = await makcu.get_firmware_version()
   except MakcuTimeoutError as e:
       print(f"Command timed out: {e}")
       # Device busy, connection lost, or command failed

Debug Mode
---------

Enable debug mode for detailed connection and command logging:

.. code-block:: python

   # Enable debug logging
   makcu = await create_async_controller(debug=True)
   
   # Debug output shows:
   # [123.456] [INFO] Sent command #42: km.move(100,50)
   # [123.458] [DEBUG] Command #42 completed in 0.002s

Migration Notes
--------------

**From v1.x to v2.0:**

Most connection code works without changes. Key differences:

.. code-block:: python

   # v1.x (still supported)
   makcu = create_controller()
   makcu.move(100, 100)

.. code-block:: python

   # v2.0 async (recommended)
   makcu = await create_async_controller()
   await makcu.move(100, 100)

.. code-block:: python

   # v2.0 with context manager (best practice)
   async with await create_async_controller() as makcu:
       await makcu.click(MouseButton.LEFT)

Examples
-------

**Basic Connection Example:**

.. code-block:: python

   from makcu import create_controller, MouseButton
   
   # Create and auto-connect
   makcu = create_controller(debug=True, auto_reconnect=True)
   
   # Use device
   makcu.click(MouseButton.LEFT)
   makcu.move(100, 50)
   
   # Clean disconnect
   makcu.disconnect()

**Async Connection Example:**

.. code-block:: python

   import asyncio
   from makcu import create_async_controller, MouseButton
   
   async def main():
       async with await create_async_controller(debug=True) as makcu:
           # Check device info
           info = await makcu.get_device_info()
           version = await makcu.get_firmware_version()
           
           print(f"Connected to {info['port']}")
           print(f"Firmware: {version}")
           
           # Perform operations
           await makcu.click(MouseButton.LEFT)
           await makcu.move(100, 50)
   
   asyncio.run(main())

**Connection Monitoring Example:**

.. code-block:: python

   from makcu import create_async_controller
   
   async def main():
       makcu = await create_async_controller(auto_reconnect=True)
       
       @makcu.on_connection_change
       async def on_connection(connected: bool):
           if connected:
               print("Device connected and ready!")
               version = await makcu.get_firmware_version()
               print(f"Firmware: {version}")
           else:
               print("Device disconnected!")
       
       # Your main application loop
       while True:
           if makcu.is_connected():
               await makcu.click(MouseButton.LEFT)
           await asyncio.sleep(1)

**Performance-Optimized Example:**

.. code-block:: python

   from makcu import create_controller, MouseButton
   
   # Disable debug mode for maximum performance
   makcu = create_controller(debug=False, auto_reconnect=True)
   
   # Use cached connection checks
   with makcu:  # Context manager ensures connection
       for _ in range(1000):
           if makcu.is_connected():  # Cached, no serial check
               makcu.move(10, 0)  # No connection check per call

See Also
--------

* :doc:`../quick_start` - Getting started with the library
* :doc:`mouse` - Mouse control operations  
* :doc:`../debugging` - Debugging connection issues
* :doc:`../performance` - Performance optimization tips