Getting Started
===============

This guide will help you get up and running with the Makcu Python Library.

Installation
------------

Requirements
^^^^^^^^^^^^

* Python 3.8 or higher
* Windows, macOS, or Linux
* Makcu device connected via USB

Install from PyPI
^^^^^^^^^^^^^^^^^

The easiest way to install is via pip:

.. code-block:: bash

   pip install makcu>=2.0.0

Install from Source
^^^^^^^^^^^^^^^^^^^

For development or to get the latest features:

.. code-block:: bash

   git clone https://github.com/SleepyTotem/makcu-py-lib
   cd makcu-py-lib
   pip install -e .

First Steps
-----------

Basic Connection
^^^^^^^^^^^^^^^^

.. code-block:: python

   from makcu import create_controller, MouseButton

   # Auto-detect and connect to device
   makcu = create_controller()
   
   # Or specify a port
   makcu = create_controller(fallback_com_port="COM3")
   
   # Enable debug output
   makcu = create_controller(debug=True)

Simple Operations
^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Mouse clicks
   makcu.click(MouseButton.LEFT)
   makcu.double_click(MouseButton.RIGHT)
   
   # Mouse movement
   makcu.move(100, 50)  # Move 100 pixels right, 50 down
   
   # Scrolling
   makcu.scroll(-3)  # Scroll down
   makcu.scroll(5)   # Scroll up
   
   # Clean up
   makcu.disconnect()

Using Context Managers
^^^^^^^^^^^^^^^^^^^^^^

The recommended way to use the library is with context managers:

.. code-block:: python

   from makcu import create_controller, MouseButton

   # Synchronous
   with create_controller() as makcu:
       makcu.click(MouseButton.LEFT)
       makcu.move(200, 100)
   # Automatically disconnects

   # Asynchronous
   import asyncio
   from makcu import create_async_controller

   async def main():
       async with await create_async_controller() as makcu:
           await makcu.click(MouseButton.LEFT)
           await makcu.move(200, 100)
   
   asyncio.run(main())

Command-Line Interface
----------------------

The library includes a CLI for testing and debugging:

.. code-block:: bash

   # Interactive debug console
   python -m makcu --debug
   
   # Test a specific port
   python -m makcu --testPort COM3
   
   # Run test suite
   python -m makcu --runtest

Error Handling
--------------

Always handle potential connection errors:

.. code-block:: python

   from makcu import create_controller, MakcuConnectionError, MakcuTimeoutError

   try:
       makcu = create_controller()
   except MakcuConnectionError as e:
       print(f"Failed to connect: {e}")
       # Handle connection failure
   
   try:
       makcu.click(MouseButton.LEFT)
   except MakcuTimeoutError as e:
       print(f"Command timed out: {e}")
       # Handle timeout

Configuration Options
---------------------

The controller supports several configuration options:

.. code-block:: python

   makcu = create_controller(
       fallback_com_port="COM3",  # Specific port
       debug=True,                # Enable debug logging
       send_init=True,            # Send initialization command
       auto_reconnect=True,        # Auto-reconnect on disconnect
       override_port=True,         # Force connecion to specified port
   )

Mouse Button Enumeration
------------------------

The library uses an enumeration for mouse buttons:

.. code-block:: python

   from makcu import MouseButton

   MouseButton.LEFT    # Left mouse button
   MouseButton.RIGHT   # Right mouse button  
   MouseButton.MIDDLE  # Middle mouse button
   MouseButton.MOUSE4  # Side button 1
   MouseButton.MOUSE5  # Side button 2

Next Steps
----------

* :doc:`api_reference` - Complete API documentation
* :doc:`async_usage` - Using the async API
* :doc:`examples` - Code examples for common tasks
* :doc:`advanced_features` - Advanced features and techniques