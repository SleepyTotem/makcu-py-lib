MakcuController API Reference
=============================

The ``MakcuController`` is the main class you'll use for synchronous (non-async) mouse control. It provides all the core functionality for clicking, moving, scrolling, and advanced features.

.. currentmodule:: makcu

Class Overview
--------------

.. autoclass:: makcu.MakcuController
   :no-members:

The MakcuController handles:

* **Mouse Operations**: Clicks, movement, scrolling, dragging
* **Button Management**: Press/release, state tracking, locking
* **Connection Handling**: Auto-detection, reconnection, device info
* **Advanced Features**: Human-like behavior, smooth movement, batch operations

Creating a Controller
--------------------

**Simple Creation:**

.. code-block:: python

   from makcu import create_controller
   
   # Auto-detect device
   makcu = create_controller()

**With Options:**

.. code-block:: python

   makcu = create_controller(
       fallback_com_port="COM3",    # Use this port if auto-detect fails
       debug=True,                  # Show detailed logging
       send_init=True,              # Send initialization commands
       auto_reconnect=True,         # Auto-reconnect on disconnect
       override_port=False          # Force use of fallback_com_port
   )

**Using Context Manager (Recommended):**

.. code-block:: python

   with create_controller() as makcu:
       makcu.click(MouseButton.LEFT)
   # Automatically disconnects

Core Mouse Operations
--------------------

Basic Clicking
^^^^^^^^^^^^^

.. automethod:: makcu.MakcuController.click

.. code-block:: python

   from makcu import MouseButton
   
   # Single clicks
   makcu.click(MouseButton.LEFT)
   makcu.click(MouseButton.RIGHT)
   makcu.click(MouseButton.MIDDLE)
   
   # Side buttons (gaming mice)
   makcu.click(MouseButton.MOUSE4)
   makcu.click(MouseButton.MOUSE5)

.. automethod:: makcu.MakcuController.double_click

.. code-block:: python

   # Double click with default timing
   makcu.double_click(MouseButton.LEFT)

Press and Release
^^^^^^^^^^^^^^^^

.. automethod:: makcu.MakcuController.press
.. automethod:: makcu.MakcuController.release

.. code-block:: python

   # Hold down a button
   makcu.press(MouseButton.LEFT)
   
   # Do something while button is held...
   
   # Release the button
   makcu.release(MouseButton.LEFT)

Mouse Movement
^^^^^^^^^^^^^

.. automethod:: makcu.MakcuController.move

.. code-block:: python

   # Basic movement (relative to current position)
   makcu.move(100, 50)   # Move right 100, down 50
   makcu.move(-50, 0)    # Move left 50
   makcu.move(0, -25)    # Move up 25

.. automethod:: makcu.MakcuController.move_smooth

.. code-block:: python

   # Smooth movement in multiple steps
   makcu.move_smooth(200, 100, segments=20)
   
   # More segments = smoother but slower
   makcu.move_smooth(300, 150, segments=50)

.. automethod:: makcu.MakcuController.move_bezier

.. code-block:: python

   # Curved movement using Bezier curves
   makcu.move_bezier(
       x=200, y=100,           # Destination
       segments=30,            # Smoothness
       ctrl_x=100, ctrl_y=200  # Control point for curve shape
   )

Scrolling
^^^^^^^^

.. automethod:: makcu.MakcuController.scroll

.. code-block:: python

   # Scroll down (negative values)
   makcu.scroll(-3)  # 3 scroll "notches" down
   
   # Scroll up (positive values)  
   makcu.scroll(5)   # 5 scroll "notches" up

Dragging
^^^^^^^

.. automethod:: makcu.MakcuController.drag

.. code-block:: python

   # Drag from current position
   makcu.drag(0, 0, 300, 200)  # Drag to (300, 200)
   
   # Drag with specific button and timing
   makcu.drag(
       start_x=0, start_y=0,
       end_x=300, end_y=200,
       button=MouseButton.LEFT,
       duration=2.0  # Take 2 seconds
   )

Advanced Mouse Features
----------------------

Human-Like Clicking
^^^^^^^^^^^^^^^^^^

.. automethod:: makcu.MakcuController.click_human_like

.. code-block:: python

   # Basic human-like clicking
   makcu.click_human_like(MouseButton.LEFT, count=3)
   
   # Gaming profile (fastest)
   makcu.click_human_like(
       button=MouseButton.LEFT,
       count=5,
       profile="gaming"  # "fast", "normal", "slow", "variable", "gaming"
   )
   
   # Add random mouse movement between clicks
   makcu.click_human_like(
       button=MouseButton.LEFT,
       count=3,
       profile="normal",
       jitter=5  # Random movement up to 5 pixels
   )

**Available Profiles:**

* ``"gaming"`` - Ultra-fast for competitive gaming (fastest)
* ``"fast"`` - Quick clicks with minimal delay
* ``"normal"`` - Natural human timing (default)
* ``"slow"`` - Deliberate, careful clicking
* ``"variable"`` - Randomized timing patterns

Button State Management
^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: makcu.MakcuController.get_button_states

.. code-block:: python

   # Get all button states at once
   states = makcu.get_button_states()
   print(states)  # {"LEFT": False, "RIGHT": True, "MIDDLE": False, ...}

.. automethod:: makcu.MakcuController.is_pressed

.. code-block:: python

   # Check if specific button is pressed
   if makcu.is_pressed(MouseButton.LEFT):
       print("Left button is currently pressed")

Button and Axis Locking
^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: makcu.MakcuController.lock
.. automethod:: makcu.MakcuController.unlock

.. code-block:: python

   # Lock mouse buttons (they won't register clicks)
   makcu.lock(MouseButton.LEFT)
   makcu.lock(MouseButton.RIGHT)
   
   # Lock mouse axes (prevent movement)
   makcu.lock("X")  # Can't move left/right
   makcu.lock("Y")  # Can't move up/down
   
   # Unlock everything
   makcu.unlock(MouseButton.LEFT)
   makcu.unlock("X")

.. automethod:: makcu.MakcuController.is_locked

.. code-block:: python

   # Check lock status
   if makcu.is_locked(MouseButton.LEFT):
       print("Left button is locked")
   
   if makcu.is_locked("X"):
       print("X-axis movement is locked")

.. automethod:: makcu.MakcuController.get_all_lock_states

.. code-block:: python

   # Get all lock states at once (fast!)
   locks = makcu.get_all_lock_states()
   print(locks)  # {"LEFT": True, "RIGHT": False, "X": True, "Y": False}

Button Event Monitoring
^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: makcu.MakcuController.set_button_callback

.. code-block:: python

   # Monitor button press/release events
   def handle_button_event(button: MouseButton, pressed: bool):
       action = "pressed" if pressed else "released"
       print(f"{button.name} {action}")
   
   makcu.set_button_callback(handle_button_event)

.. automethod:: makcu.MakcuController.enable_button_monitoring

.. code-block:: python

   # Start monitoring
   makcu.enable_button_monitoring(True)
   
   # Stop monitoring
   makcu.enable_button_monitoring(False)

Connection Management
--------------------

.. automethod:: makcu.MakcuController.connect
.. automethod:: makcu.MakcuController.disconnect
.. automethod:: makcu.MakcuController.is_connected

.. code-block:: python

   # Manual connection control
   if not makcu.is_connected():
       makcu.connect()
   
   # Always disconnect when done
   makcu.disconnect()

Connection Status Callbacks
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: makcu.MakcuController.on_connection_change

.. code-block:: python

   @makcu.on_connection_change
   def handle_connection(connected: bool):
       if connected:
           print("Device reconnected!")
       else:
           print("Device disconnected!")

Device Information
^^^^^^^^^^^^^^^^^

.. automethod:: makcu.MakcuController.get_device_info

.. code-block:: python

   info = makcu.get_device_info()
   print(info)  # {"port": "COM3", "vid": "0x1a86", "pid": "0x55d3", ...}

Advanced Features
----------------

Serial Spoofing
^^^^^^^^^^^^^^

.. automethod:: makcu.MakcuController.spoof_serial
.. automethod:: makcu.MakcuController.reset_serial

.. code-block:: python

   # Change device serial number
   makcu.spoof_serial("CUSTOM123456")
   
   # Reset to original
   makcu.reset_serial()

Batch Operations
^^^^^^^^^^^^^^^

.. automethod:: makcu.MakcuController.batch_execute

.. code-block:: python

   # Execute multiple commands efficiently
   makcu.batch_execute([
       lambda: makcu.move(50, 0),
       lambda: makcu.click(MouseButton.LEFT),
       lambda: makcu.move(-50, 0),
       lambda: makcu.click(MouseButton.RIGHT)
   ])

Low-Level Transport Access
^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoattribute:: makcu.MakcuController.transport

.. code-block:: python

   # Direct access to transport layer
   response = makcu.transport.send_command("km.version()")
   print(response)

Context Manager Support
----------------------

The MakcuController supports Python's ``with`` statement for automatic resource management:

.. code-block:: python

   # Automatically connects and disconnects
   with create_controller() as makcu:
       makcu.click(MouseButton.LEFT)
       makcu.move(100, 50)
   # Device is automatically disconnected here

Error Handling
-------------

The controller raises specific exceptions for different error conditions:

.. code-block:: python

   from makcu import MakcuConnectionError, MakcuTimeoutError
   
   try:
       makcu = create_controller()
   except MakcuConnectionError as e:
       print(f"Connection failed: {e}")
   
   try:
       makcu.click(MouseButton.LEFT)
   except MakcuTimeoutError as e:
       print(f"Command timed out: {e}")

Properties and State
-------------------

.. autoattribute:: makcu.MakcuController.debug
   
   Controls debug output:
   
   .. code-block:: python
   
      makcu.debug = True   # Enable debug logging
      makcu.debug = False  # Disable debug logging

.. autoattribute:: makcu.MakcuController.auto_reconnect

   Controls automatic reconnection:
   
   .. code-block:: python
   
      makcu.auto_reconnect = True   # Enable auto-reconnect
      makcu.auto_reconnect = False  # Disable auto-reconnect

Performance Notes
----------------

**Fast Operations (≤1ms):**
- ``click()``, ``press()``, ``release()``
- ``move()`` (single movement)
- ``scroll()``
- ``is_locked()``, ``get_button_states()``

**Medium Operations (1-5ms):**
- ``get_all_lock_states()``
- ``get_device_info()`` (cached after first call)
- ``move_smooth()`` with few segments

**Slower Operations (>5ms):**
- Initial ``connect()`` (~46ms)
- ``move_smooth()`` with many segments
- ``click_human_like()`` (intentionally variable timing)
- ``drag()`` with long duration

**Optimization Tips:**
- Use batch operations for multiple commands
- Cache device info and lock states
- Disable debug mode in production
- Use the gaming profile for fastest human-like clicking

Thread Safety
-------------

The MakcuController is **not** thread-safe. If you need to use it from multiple threads, use proper synchronization (locks, queues, etc.) or consider the async API instead.

For async applications, see :doc:`../async_usage` and :doc:`../api/async_controller`.

Examples
--------

**Complete Example:**

.. code-block:: python

   from makcu import create_controller, MouseButton, MakcuConnectionError
   
   def main():
       try:
           # Create controller with auto-reconnect
           with create_controller(debug=True, auto_reconnect=True) as makcu:
               
               # Basic operations
               makcu.click(MouseButton.LEFT)
               makcu.move(100, 50)
               makcu.scroll(-2)
               
               # Human-like clicking for gaming
               makcu.click_human_like(
                   MouseButton.LEFT, 
                   count=5, 
                   profile="gaming"
               )
               
               # Lock right button temporarily
               makcu.lock(MouseButton.RIGHT)
               
               # Try to right-click (will be blocked)
               makcu.click(MouseButton.RIGHT)  # No effect!
               
               # Unlock and try again
               makcu.unlock(MouseButton.RIGHT)
               makcu.click(MouseButton.RIGHT)  # Works now!
               
               # Smooth movement
               makcu.move_smooth(200, 100, segments=20)
               
       except MakcuConnectionError:
           print("Could not connect to Makcu device!")
   
   if __name__ == "__main__":
       main()

See Also
--------

* :doc:`../getting_started` - Basic usage tutorial
* :doc:`../examples` - More code examples
* :doc:`../async_usage` - Async/await version  
* :doc:`mouse` - Mouse helper class
* :doc:`connection` - Transport layer details