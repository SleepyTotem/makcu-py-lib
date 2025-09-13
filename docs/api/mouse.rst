Mouse Helper Class
==================

The ``Mouse`` class is an internal helper that handles the low-level mouse operations for the MakcuController. While you typically won't use this class directly, understanding it can help with advanced usage and troubleshooting.

.. currentmodule:: makcu

Class Overview
--------------

.. autoclass:: makcu.Mouse
   :no-members:

The Mouse class provides:

* **Raw Command Generation**: Creates the actual device commands
* **State Management**: Tracks button states and lock status  
* **Protocol Handling**: Formats commands for the Makcu device
* **Response Parsing**: Interprets device responses

**Note:** You typically don't create Mouse instances directly. The MakcuController creates and manages one for you.

Internal Architecture
--------------------

The Mouse class works as a bridge between your Python code and the Makcu device's protocol:

.. code-block:: text

   Your Code → MakcuController → Mouse → SerialTransport → Device
   
   makcu.click() → mouse.click() → "km.click(1)" → Device

This layered approach provides:
- Clean separation of concerns
- Easy testing and debugging
- Protocol abstraction
- State management

Core Operations
--------------

Click Operations
^^^^^^^^^^^^^^^

.. automethod:: makcu.Mouse.click

The click method generates commands like:

.. code-block:: python

   # Internal command generation:
   mouse.click(MouseButton.LEFT)    # → "km.click(1)"
   mouse.click(MouseButton.RIGHT)   # → "km.click(2)"  
   mouse.click(MouseButton.MIDDLE)  # → "km.click(4)"

.. automethod:: makcu.Mouse.press
.. automethod:: makcu.Mouse.release

.. code-block:: python

   # Press/release generate separate commands:
   mouse.press(MouseButton.LEFT)    # → "km.press(1)"
   mouse.release(MouseButton.LEFT)  # → "km.release(1)"

Movement Operations
^^^^^^^^^^^^^^^^^^

.. automethod:: makcu.Mouse.move

.. code-block:: python

   # Movement commands:
   mouse.move(100, 50)  # → "km.move(100,50)"
   mouse.move(-25, 0)   # → "km.move(-25,0)"

.. automethod:: makcu.Mouse.scroll

.. code-block:: python

   # Scroll commands:
   mouse.scroll(-3)  # → "km.scroll(-3)"
   mouse.scroll(2)   # → "km.scroll(2)"

State Management
---------------

Button State Tracking
^^^^^^^^^^^^^^^^^^^^^

.. automethod:: makcu.Mouse.get_button_states

The Mouse class maintains an internal representation of button states:

.. code-block:: python

   # Internal state format (bitwise):
   # Bit 0 (1): LEFT button
   # Bit 1 (2): RIGHT button  
   # Bit 2 (4): MIDDLE button
   # Bit 3 (8): MOUSE4 button
   # Bit 4 (16): MOUSE5 button
   
   states = mouse.get_button_states()
   # Returns: {"LEFT": False, "RIGHT": True, "MIDDLE": False, ...}

.. automethod:: makcu.Mouse.is_pressed

.. code-block:: python

   # Check individual button state:
   if mouse.is_pressed(MouseButton.LEFT):
       print("Left button is pressed")

Lock State Management
^^^^^^^^^^^^^^^^^^^^

.. automethod:: makcu.Mouse.lock
.. automethod:: makcu.Mouse.unlock

The locking system prevents buttons/axes from functioning:

.. code-block:: python

   # Lock commands:
   mouse.lock(MouseButton.LEFT)  # → "km.lock.button(1)"
   mouse.lock("X")               # → "km.lock.axis(1)"
   mouse.lock("Y")               # → "km.lock.axis(2)"

.. automethod:: makcu.Mouse.is_locked

.. code-block:: python

   # Query lock state:
   mouse.is_locked(MouseButton.LEFT)  # → "km.lock.query(1)"
   mouse.is_locked("X")               # → "km.lock.query.axis(1)"

.. automethod:: makcu.Mouse.get_all_lock_states

.. code-block:: python

   # Batch query for performance:
   locks = mouse.get_all_lock_states()
   # → "km.lock.query.all()" → parsing response

Protocol Details
---------------

Command Format
^^^^^^^^^^^^^

The Mouse class generates commands in the Makcu protocol format:

**Basic Commands:**
.. code-block:: text

   km.click(button)      # Click button (1=LEFT, 2=RIGHT, 4=MIDDLE, etc.)
   km.press(button)      # Press and hold button
   km.release(button)    # Release button
   km.move(x,y)          # Move mouse relatively
   km.scroll(delta)      # Scroll wheel

**State Commands:**
.. code-block:: text

   km.button.state()     # Get button states (returns bitmask)
   km.button.query(btn)  # Check if button is pressed

**Lock Commands:**
.. code-block:: text

   km.lock.button(btn)   # Lock button
   km.unlock.button(btn) # Unlock button
   km.lock.axis(axis)    # Lock movement axis (1=X, 2=Y)
   km.lock.query.all()   # Get all lock states

Response Parsing
^^^^^^^^^^^^^^^

The Mouse class parses device responses:

.. code-block:: python

   # Example response parsing:
   raw_response = ">>> button_state:7"  # Bitmask: 7 = LEFT+RIGHT+MIDDLE
   
   # Parsed into:
   parsed_states = {
       "LEFT": True,    # Bit 0 set
       "RIGHT": True,   # Bit 1 set  
       "MIDDLE": True,  # Bit 2 set
       "MOUSE4": False, # Bit 3 not set
       "MOUSE5": False  # Bit 4 not set
   }

Button Mapping
-------------

The Mouse class uses internal button mapping:

.. code-block:: python

   # MouseButton enum to device values:
   BUTTON_MAPPING = {
       MouseButton.LEFT: 1,    # Binary: 00001
       MouseButton.RIGHT: 2,   # Binary: 00010
       MouseButton.MIDDLE: 4,  # Binary: 00100
       MouseButton.MOUSE4: 8,  # Binary: 01000
       MouseButton.MOUSE5: 16  # Binary: 10000
   }
   
   # Multiple buttons can be combined:
   # LEFT + RIGHT = 3 (binary: 00011)

Advanced Features
----------------

Batch Operations
^^^^^^^^^^^^^^^

.. automethod:: makcu.Mouse.batch_execute

.. code-block:: python

   # Execute multiple operations efficiently:
   mouse.batch_execute([
       lambda: mouse.move(50, 0),
       lambda: mouse.click(MouseButton.LEFT),
       lambda: mouse.scroll(-1)
   ])

Human-Like Timing
^^^^^^^^^^^^^^^^

.. automethod:: makcu.Mouse.click_human_like

The Mouse class includes timing profiles for realistic behavior:

.. code-block:: python

   # Timing profiles (internal delays):
   PROFILES = {
       "gaming": (0.001, 0.003),    # 1-3ms between clicks
       "fast": (0.02, 0.08),        # 20-80ms  
       "normal": (0.1, 0.3),        # 100-300ms
       "slow": (0.3, 0.8),          # 300-800ms
       "variable": (0.05, 0.5)      # 50-500ms (random)
   }

Error Handling
-------------

The Mouse class handles various error conditions:

.. code-block:: python

   # Common error scenarios:
   try:
       mouse.click(MouseButton.LEFT)
   except Exception as e:
       # Device communication errors
       # Invalid button parameters  
       # Timeout errors
       # Connection lost errors
       pass

Internal State Properties
------------------------

The Mouse class maintains several internal properties:

.. code-block:: python

   # Button states (cached for performance)
   mouse._button_states = 0  # Bitmask of pressed buttons
   
   # Lock states (cached)
   mouse._lock_states = {
       "LEFT": False, "RIGHT": False, "MIDDLE": False,
       "MOUSE4": False, "MOUSE5": False,
       "X": False, "Y": False
   }
   
   # Transport reference
   mouse.transport = serial_transport_instance

Performance Optimizations
-------------------------

The Mouse class includes several performance optimizations:

**Pre-computed Commands:**
.. code-block:: python

   # Commands are pre-formatted for speed:
   CLICK_COMMANDS = {
       MouseButton.LEFT: "km.click(1)",
       MouseButton.RIGHT: "km.click(2)", 
       # ... etc
   }

**State Caching:**
.. code-block:: python

   # Button states cached to avoid repeated queries:
   if not self._state_cache_expired():
       return self._cached_button_states

**Bitwise Operations:**
.. code-block:: python

   # Fast button state checking:
   def is_pressed(self, button):
       mask = BUTTON_MAPPING[button]
       return bool(self._button_states & mask)

Usage Examples
-------------

**Direct Usage (Advanced):**

.. code-block:: python

   # You typically don't do this - use MakcuController instead
   from makcu.mouse import Mouse
   from makcu.connection import SerialTransport
   
   transport = SerialTransport("COM3")
   mouse = Mouse(transport)
   
   # Direct mouse operations:
   mouse.click(MouseButton.LEFT)
   mouse.move(100, 50)

**Accessing via MakcuController:**

.. code-block:: python

   from makcu import create_controller, MouseButton
   
   makcu = create_controller()
   
   # Access the internal mouse instance:
   internal_mouse = makcu.mouse
   
   # Now you can call mouse methods directly if needed:
   internal_mouse.click(MouseButton.LEFT)

Debugging
--------

The Mouse class supports debug output:

.. code-block:: python

   # Debug output shows command generation:
   mouse.debug = True
   mouse.click(MouseButton.LEFT)
   
   # Output:
   # [DEBUG] Generated command: km.click(1)
   # [DEBUG] Sending to transport...
   # [DEBUG] Response received: >>> clicked

Thread Safety
-------------

The Mouse class is **not thread-safe**. It maintains internal state that can be corrupted by concurrent access. Always use proper synchronization if accessing from multiple threads.

Integration with Transport Layer
-------------------------------

The Mouse class works closely with the SerialTransport:

.. code-block:: python

   # Command flow:
   mouse.click(MouseButton.LEFT)
   ↓
   command = "km.click(1)"  # Generated by Mouse
   ↓  
   transport.send_command(command)  # Sent via SerialTransport
   ↓
   response = ">>> clicked"  # Received from device
   ↓
   mouse.parse_response(response)  # Processed by Mouse

Limitations
----------

**Synchronous Only:**
The Mouse class is designed for synchronous operations. For async usage, see the AsyncMouse class.

**Single Device:**
Each Mouse instance works with one device connection.

**State Timing:**
Button state queries may have slight delays (~1ms) due to device communication.

See Also
--------

* :doc:`controller` - Main controller that uses this class
* :doc:`connection` - Transport layer details
* :doc:`../async_usage` - Async version of mouse operations
* :doc:`../examples` - Practical usage examples
* :doc:`enums` - MouseButton enumeration details