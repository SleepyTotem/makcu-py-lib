Advanced Features
=================

This guide covers advanced functionality and customization options in the Makcu Python Library.

Serial Spoofing
---------------

The Makcu device supports serial number spoofing for advanced use cases:

**Spoofing Device Serial:**

.. code-block:: python

   from makcu import create_controller

   with create_controller() as makcu:
       # Spoof device serial number
       makcu.spoof_serial("CUSTOM123456")
       
       # Verify the change
       info = makcu.get_device_info()
       print(f"New serial: {info}")

**Resetting Serial:**

.. code-block:: python

   # Reset to factory default serial
   makcu.reset_serial()
   
   # Reconnect to see changes
   makcu.disconnect()
   makcu.connect()

Low-Level Command Interface
--------------------------

For advanced users who need direct device communication:

**Raw Command Execution:**

.. code-block:: python

   # Send raw commands directly to device
   response = makcu.transport.send_command(
       "km.version()", 
       expect_response=True,
       timeout=0.5
   )
   print(f"Firmware version: {response}")

**Custom Command Building:**

.. code-block:: python

   # Build custom commands using the device protocol
   def custom_rapid_click(makcu, count=10):
       """Custom rapid clicking implementation."""
       commands = []
       for i in range(count):
           commands.append(f"km.click(0)#{i}")  # Track with ID
       
       # Send all commands rapidly
       for cmd in commands:
           makcu.transport.send_command(cmd, expect_response=False)

Batch Command Processing
-----------------------

Execute multiple operations efficiently:

**Simple Batch Execution:**

.. code-block:: python

   def batch_demo(makcu):
       # Define batch of operations
       operations = [
           lambda: makcu.move(50, 0),
           lambda: makcu.click(MouseButton.LEFT),
           lambda: makcu.move(-50, 0),
           lambda: makcu.click(MouseButton.RIGHT),
           lambda: makcu.scroll(-2)
       ]
       
       # Execute as batch
       makcu.batch_execute(operations)

**Async Batch Operations:**

.. code-block:: python

   async def async_batch_demo(makcu):
       # Parallel batch execution
       await asyncio.gather(
           makcu.move(100, 0),
           makcu.click(MouseButton.LEFT),
           makcu.scroll(-1),
           makcu.move(-100, 0)
       )

**Custom Batch Processor:**

.. code-block:: python

   def advanced_batch_processor(makcu, commands, delay=0.001):
       """Advanced batch processor with timing control."""
       import time
       
       results = []
       for i, command in enumerate(commands):
           start_time = time.time()
           
           try:
               result = command()
               execution_time = time.time() - start_time
               results.append({
                   'command': i,
                   'success': True,
                   'time': execution_time
               })
           except Exception as e:
               results.append({
                   'command': i,
                   'success': False,
                   'error': str(e),
                   'time': time.time() - start_time
               })
           
           time.sleep(delay)
       
       return results

Connection Event Handling
-------------------------

**Async Connection Monitoring:**

.. code-block:: python

   async def connection_monitor():
       async with await create_async_controller(auto_reconnect=True) as makcu:
           @makcu.on_connection_change
           async def handle_connection_change(connected: bool):
               if connected:
                   print("Reconnected - resuming operations")
                   await makcu.move(1, 1)  # Test movement
               else:
                   print("Lost connection - waiting for reconnect")
           
           # Your main application logic here
           while True:
               if makcu.is_connected():
                   await makcu.click(MouseButton.LEFT)
               await asyncio.sleep(1)

Custom Movement Algorithms
--------------------------

Implement custom mouse movement patterns:

**Spiral Movement:**

.. code-block:: python

   import math

   def spiral_movement(makcu, radius=100, rotations=3, segments=50):
       """Create a spiral mouse movement pattern."""
       for i in range(segments * rotations):
           angle = (i / segments) * 2 * math.pi
           current_radius = radius * (i / (segments * rotations))
           
           x = int(current_radius * math.cos(angle))
           y = int(current_radius * math.sin(angle))
           
           makcu.move(x - prev_x if i > 0 else x, y - prev_y if i > 0 else y)
           prev_x, prev_y = x, y

**Random Walk:**

.. code-block:: python

   import random

   def random_walk(makcu, steps=20, max_distance=50):
       """Random mouse movement pattern."""
       for _ in range(steps):
           dx = random.randint(-max_distance, max_distance)
           dy = random.randint(-max_distance, max_distance)
           makcu.move(dx, dy)

**Sine Wave Movement:**

.. code-block:: python

   def sine_wave_movement(makcu, amplitude=50, frequency=2, duration=100):
       """Create sine wave movement pattern."""
       for i in range(duration):
           x = i * 2  # Horizontal progression
           y = int(amplitude * math.sin(frequency * i * math.pi / 180))
           
           if i == 0:
               makcu.move(x, y)
           else:
               makcu.move(2, y - prev_y)
           prev_y = y

Custom Error Handling
---------------------

Advanced error handling and recovery mechanisms:

**Retry Mechanism:**

.. code-block:: python

   import time
   from functools import wraps

   def retry_on_failure(max_attempts=3, delay=0.1):
       """Decorator for retrying failed operations."""
       def decorator(func):
           @wraps(func)
           def wrapper(*args, **kwargs):
               last_exception = None
               
               for attempt in range(max_attempts):
                   try:
                       return func(*args, **kwargs)
                   except (MakcuConnectionError, MakcuTimeoutError) as e:
                       last_exception = e
                       if attempt < max_attempts - 1:
                           time.sleep(delay * (attempt + 1))  # Exponential backoff
                       
               raise last_exception
           return wrapper
       return decorator

   # Usage
   @retry_on_failure(max_attempts=5, delay=0.05)
   def reliable_click(makcu, button):
       makcu.click(button)

Next Steps
----------

* :doc:`api/controller` - Complete API reference