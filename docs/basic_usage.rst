Basic Usage
===========

This guide covers the core functionality of the Makcu Python Library using the synchronous API.

Creating a Controller
---------------------

**Basic Connection:**

.. code-block:: python

   from makcu import create_controller
   
   # Simple connection
   makcu = create_controller()
   
   # With debugging enabled
   makcu = create_controller(debug=True)
   
   # With auto-reconnection
   makcu = create_controller(auto_reconnect=True)

**Using Context Managers (Recommended):**

.. code-block:: python

   with create_controller(debug=True) as makcu:
       # Device automatically connects and disconnects
       makcu.click(MouseButton.LEFT)

Mouse Button Control
-------------------

**Available Buttons:**

.. code-block:: python

   from makcu import MouseButton
   
   MouseButton.LEFT    # Left mouse button
   MouseButton.RIGHT   # Right mouse button  
   MouseButton.MIDDLE  # Middle mouse button (scroll wheel)
   MouseButton.MOUSE4  # Side button 1
   MouseButton.MOUSE5  # Side button 2

**Basic Clicking:**

.. code-block:: python

   # Single clicks
   makcu.click(MouseButton.LEFT)
   makcu.click(MouseButton.RIGHT)
   makcu.click(MouseButton.MIDDLE)
   
   # Double clicking
   makcu.double_click(MouseButton.LEFT)

**Press and Release:**

.. code-block:: python

   # Hold down a button
   makcu.press(MouseButton.LEFT)
   
   # Do something while button is held...
   makcu.move(100, 0)
   
   # Release the button
   makcu.release(MouseButton.LEFT)

**Human-like Clicking:**

.. code-block:: python

   # Realistic clicking with timing variations
   makcu.click_human_like(
       button=MouseButton.LEFT,
       count=5,                    # Number of clicks
       profile="normal",           # "fast", "normal", "slow", "variable", "gaming"
       jitter=3                    # Random movement between clicks
   )

Mouse Movement
-------------

**Basic Movement:**

.. code-block:: python

   # Relative movement (pixels)
   makcu.move(100, 50)    # Move right 100px, down 50px
   makcu.move(-50, -25)   # Move left 50px, up 25px

**Smooth Movement:**

.. code-block:: python

   # Linear interpolated movement
   makcu.move_smooth(
       x=200, 
       y=100, 
       segments=20          # More segments = smoother movement
   )

**Bezier Curve Movement:**

.. code-block:: python

   # Natural curved movement
   makcu.move_bezier(
       x=150, 
       y=150, 
       segments=30,
       ctrl_x=75,           # Control point X
       ctrl_y=200           # Control point Y
   )

**Dragging:**

.. code-block:: python

   # Drag from current position to (300, 200) over 1.5 seconds
   makcu.drag(
       start_x=0, start_y=0,      # Relative to current position
       end_x=300, end_y=200,
       button=MouseButton.LEFT,
       duration=1.5
   )

Scrolling
---------

.. code-block:: python

   # Scroll up (positive values)
   makcu.scroll(3)
   
   # Scroll down (negative values)  
   makcu.scroll(-5)
   
   # Single scroll unit
   makcu.scroll(1)     # One notch up
   makcu.scroll(-1)    # One notch down

Button and Axis Locking
----------------------

**Button Locking:**

.. code-block:: python

   # Lock buttons (prevents physical button presses)
   makcu.lock(MouseButton.LEFT)
   makcu.lock(MouseButton.RIGHT)
   
   # Unlock buttons
   makcu.unlock(MouseButton.LEFT)
   makcu.unlock(MouseButton.RIGHT)
   
   # Check lock status
   if makcu.is_locked(MouseButton.LEFT):
       print("Left button is locked")

**Axis Locking:**

.. code-block:: python

   # Lock movement axes
   makcu.lock("X")      # Prevent horizontal movement
   makcu.lock("Y")      # Prevent vertical movement
   
   # Unlock axes
   makcu.unlock("X")
   makcu.unlock("Y")
   
   # Check axis lock status
   if makcu.is_locked("X"):
       print("X-axis movement is locked")

**Getting All Lock States:**

.. code-block:: python

   # Get complete lock status
   states = makcu.get_all_lock_states()
   print(states)
   # Output: {"LEFT": True, "RIGHT": False, "X": False, "Y": True, ...}

Button State Monitoring
-----------------------

**Check Current Button States:**

.. code-block:: python

   # Get all button states
   states = makcu.get_button_states()
   print(states)  # {"LEFT": False, "RIGHT": True, "MIDDLE": False, ...}
   
   # Check specific button
   if makcu.is_pressed(MouseButton.RIGHT):
       print("Right button is currently pressed")

**Real-time Event Monitoring:**

.. code-block:: python

   def on_button_event(button: MouseButton, pressed: bool):
       action = "pressed" if pressed else "released"
       print(f"{button.name} {action}")
   
   # Set the callback function
   makcu.set_button_callback(on_button_event)
   
   # Enable monitoring
   makcu.enable_button_monitoring(True)
   
   # Your program continues...
   # Button events will trigger the callback
   
   # Disable monitoring when done
   makcu.enable_button_monitoring(False)

Device Information
-----------------

**Get Device Details:**

.. code-block:: python

   # Device information
   info = makcu.get_device_info()
   print(info)
   # Output: {'port': 'COM3', 'vid': '0x1a86', 'pid': '0x55d3', ...}

**Connection Status:**

.. code-block:: python

   if makcu.is_connected():
       print("Device is connected")
   else:
       print("Device is disconnected")

Error Handling
--------------

**Common Exceptions:**

.. code-block:: python

   from makcu import MakcuError, MakcuConnectionError, MakcuTimeoutError

   try:
       makcu = create_controller()
       makcu.click(MouseButton.LEFT)
       
   except MakcuConnectionError as e:
       print(f"Connection failed: {e}")
       
   except MakcuTimeoutError as e:
       print(f"Command timed out: {e}")
       
   except MakcuError as e:
       print(f"General Makcu error: {e}")

**Connection Recovery:**

.. code-block:: python

   try:
       makcu.move(100, 50)
   except MakcuConnectionError:
       print("Connection lost, attempting reconnection...")
       makcu.connect()  # Manual reconnection
       makcu.move(100, 50)  # Retry the command

Complete Example
---------------

Here's a comprehensive example showing various features:

.. code-block:: python

   from makcu import create_controller, MouseButton
   import time

   def main():
       with create_controller(debug=True, auto_reconnect=True) as makcu:
           print(f"Connected to device: {makcu.get_device_info()['port']}")
           
           # Basic mouse control
           makcu.click(MouseButton.LEFT)
           makcu.move(100, 50)
           makcu.scroll(-2)
           
           # Human-like interaction
           makcu.click_human_like(MouseButton.RIGHT, count=2, profile="gaming")
           
           # Smooth movement
           makcu.move_smooth(150, 100, segments=25)
           
           # Button locking demonstration
           makcu.lock(MouseButton.LEFT)
           print("Try clicking left button - it should be blocked")
           time.sleep(2)
           makcu.unlock(MouseButton.LEFT)
           print("Left button unlocked")
           
           # Check button states
           states = makcu.get_button_states()
           if any(states.values()):
               print("Some buttons are currently pressed")
           
           print("Demo complete!")

   if __name__ == "__main__":
       main()

Performance Tips
---------------

**For Maximum Speed:**

.. code-block:: python

   # Disable debug mode in production
   makcu = create_controller(debug=False)
   
   # Use context manager to avoid repeated connection checks
   with makcu:
       for i in range(100):
           makcu.click(MouseButton.LEFT)  # Fast execution

**Batch Operations:**

.. code-block:: python

   # Execute multiple commands efficiently
   with makcu:
       makcu.move(50, 0)
       makcu.click(MouseButton.LEFT)
       makcu.move(-50, 0)
       makcu.click(MouseButton.RIGHT)

Next Steps
----------

* :doc:`async_usage` - Learn the async/await API
* :doc:`advanced_features` - Advanced functionality and customization
* :doc:`examples` - More practical examples and use cases