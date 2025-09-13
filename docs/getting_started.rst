Getting Started with Makcu Python Library
==========================================

Welcome to the Makcu Python Library! This guide will help you install and start using the library in just a few minutes.

What is Makcu?
--------------

The Makcu Python Library lets you control Makcu devices from your Python code. Think of it as a way to programmatically control mouse movements, clicks, and scrolling - perfect for automation, gaming macros, or accessibility applications.

**Key Benefits:**

* **⚡ Super Fast**: Commands execute in 1-3ms (up to 117x faster than older versions)
* **🎯 Gaming Ready**: Optimized for 240Hz+ gaming with sub-3ms execution
* **🔄 Auto-Reconnect**: Automatically reconnects if the device gets unplugged
* **🚀 Modern Python**: Full async/await support for modern applications

Installation
------------

System Requirements
^^^^^^^^^^^^^^^^^^

Before installing, make sure you have:

* **Python 3.8 or higher** (Python 3.10+ recommended)
* **USB port** for your Makcu device
* **Operating System**: Windows, macOS, or Linux

Quick Install (Recommended)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open your terminal or command prompt and run:

.. code-block:: bash

   pip install makcu

That's it! The library will automatically detect your Makcu device when you connect it.

Install from Source (Advanced)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want the latest features or plan to contribute:

.. code-block:: bash

   git clone https://github.com/SleepyTotem/makcu-py-lib
   cd makcu-py-lib
   pip install -e .

Your First Makcu Program
------------------------

Let's start with a simple "Hello World" example:

.. code-block:: python

   from makcu import create_controller, MouseButton

   # Connect to your Makcu device
   makcu = create_controller()
   
   # Click the left mouse button
   makcu.click(MouseButton.LEFT)
   
   # Move the mouse 100 pixels right, 50 pixels down
   makcu.move(100, 50)
   
   # Scroll down a bit
   makcu.scroll(-2)
   
   # Always disconnect when done
   makcu.disconnect()

**What this code does:**
1. Imports the necessary parts of the library
2. Automatically finds and connects to your Makcu device
3. Performs some basic mouse actions
4. Properly disconnects from the device

Better Way: Using Context Managers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The recommended way is to use ``with`` statements - they automatically handle connection and disconnection:

.. code-block:: python

   from makcu import create_controller, MouseButton

   # This automatically connects AND disconnects
   with create_controller() as makcu:
       makcu.click(MouseButton.LEFT)
       makcu.move(100, 50)
       makcu.scroll(-2)
   # Device automatically disconnected here!

Understanding Mouse Buttons
---------------------------

The library uses clear names for mouse buttons:

.. code-block:: python

   from makcu import MouseButton

   # All available buttons:
   MouseButton.LEFT     # Left click
   MouseButton.RIGHT    # Right click  
   MouseButton.MIDDLE   # Middle click (scroll wheel)
   MouseButton.MOUSE4   # Side button 1
   MouseButton.MOUSE5   # Side button 2

Common Operations
----------------

Here are the most common things you'll do:

**Clicking:**

.. code-block:: python

   makcu.click(MouseButton.LEFT)           # Single click
   makcu.double_click(MouseButton.LEFT)    # Double click
   makcu.press(MouseButton.RIGHT)          # Hold down
   makcu.release(MouseButton.RIGHT)        # Let go

**Moving the Mouse:**

.. code-block:: python

   makcu.move(100, 0)      # Move right 100 pixels
   makcu.move(-50, 25)     # Move left 50, down 25
   makcu.move(0, -30)      # Move up 30 pixels

**Scrolling:**

.. code-block:: python

   makcu.scroll(3)         # Scroll up 3 "notches"
   makcu.scroll(-5)        # Scroll down 5 "notches"

**Smooth Movement:**

.. code-block:: python

   # Move in a smooth line instead of instantly jumping
   makcu.move_smooth(200, 100, segments=20)
   
   # Move in a curved path (like a human would)
   makcu.move_bezier(150, 150, segments=30, ctrl_x=75, ctrl_y=200)

Testing Your Setup
------------------

The library includes built-in tools to test everything is working:

**Quick Test:**

.. code-block:: bash

   python -m makcu --debug

This opens an interactive console where you can type commands and see what happens.

**Test Specific Port:**

.. code-block:: bash

   python -m makcu --testPort COM3

Replace ``COM3`` with your device's port if you know it.

**Run Full Test Suite:**

.. code-block:: bash

   python -m makcu --runtest

This runs all tests and creates a detailed HTML report.

Handling Problems
----------------

**Device Not Found:**

.. code-block:: python

   from makcu import create_controller, MakcuConnectionError

   try:
       makcu = create_controller()
   except MakcuConnectionError:
       print("Could not find Makcu device!")
       print("Make sure it's plugged in and drivers are installed.")

**Commands Timing Out:**

.. code-block:: python

   from makcu import MakcuTimeoutError

   try:
       makcu.click(MouseButton.LEFT)
   except MakcuTimeoutError:
       print("Command took too long - device might be busy")

**Specifying a Specific Port:**

If auto-detection doesn't work, you can specify the exact port:

.. code-block:: python

   # Windows
   makcu = create_controller(fallback_com_port="COM3")
   
   # Linux/Mac  
   makcu = create_controller(fallback_com_port="/dev/ttyUSB0")

Configuration Options
--------------------

You can customize how the controller behaves:

.. code-block:: python

   makcu = create_controller(
       debug=True,                # Show detailed logs
       auto_reconnect=True,       # Reconnect if device unplugged
       fallback_com_port="COM3",  # Use this port if auto-detect fails
       send_init=True             # Send setup commands on connect
   )

Debug Mode
^^^^^^^^^

When ``debug=True``, you'll see detailed information:

.. code-block:: python

   makcu = create_controller(debug=True)
   makcu.click(MouseButton.LEFT)
   
   # Output:
   # [123.456] [INFO] Sent command #42: km.click(1)
   # [123.458] [DEBUG] Command #42 completed in 0.002s

This is super helpful when things aren't working as expected.

What's Next?
-----------

Now that you have the basics down, you can:

* Learn about **async/await** for modern applications: :doc:`async_usage`
* See **real-world examples**: :doc:`examples` 
* Explore **advanced features** like human-like clicking: :doc:`advanced_features`
* Check the **complete API reference**: :doc:`api_reference`

**Quick tip:** Start with the synchronous API (what we showed here) - it's simpler and perfect for most use cases. You can always upgrade to async later if needed!