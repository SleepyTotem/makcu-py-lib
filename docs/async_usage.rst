Async Usage
===========

The Makcu library provides full async/await support for modern Python applications. The async API offers the same functionality as the synchronous version with added benefits for concurrent operations.

Why Use Async?
--------------

**Benefits:**
* Execute multiple mouse operations in parallel
* Non-blocking integration with async applications
* Better resource utilization in I/O-bound applications
* Modern Python patterns with async/await

**When to Use Async:**
* Building GUI applications with async frameworks
* Creating bots or automation tools
* Integrating with async web applications
* Need parallel mouse operations

Creating an Async Controller
----------------------------

**Basic Async Connection:**

.. code-block:: python

   import asyncio
   from makcu import create_async_controller

   async def main():
       # Create async controller
       makcu = await create_async_controller(debug=True)
       
       # Use the controller
       await makcu.click(MouseButton.LEFT)
       
       # Don't forget to disconnect
       await makcu.disconnect()

   asyncio.run(main())

**Using Async Context Managers (Recommended):**

.. code-block:: python

   import asyncio
   from makcu import create_async_controller, MouseButton

   async def main():
       # Automatic connection and cleanup
       async with await create_async_controller(debug=True) as makcu:
           await makcu.click(MouseButton.LEFT)
           await makcu.move(100, 50)
       # Automatically disconnected

   asyncio.run(main())

Async Mouse Operations
---------------------

All mouse operations support async/await:

**Button Control:**

.. code-block:: python

   async def button_demo(makcu):
       # Basic clicking
       await makcu.click(MouseButton.LEFT)
       await makcu.double_click(MouseButton.RIGHT)
       
       # Press and release
       await makcu.press(MouseButton.MIDDLE)
       await asyncio.sleep(1.0)  # Hold for 1 second
       await makcu.release(MouseButton.MIDDLE)

**Movement:**

.. code-block:: python

   async def movement_demo(makcu):
       # Basic movement
       await makcu.move(100, 50)
       
       # Smooth movement
       await makcu.move_smooth(200, 100, segments=30)
       
       # Bezier curves
       await makcu.move_bezier(150, 150, segments=25, ctrl_x=75, ctrl_y=200)

**Scrolling:**

.. code-block:: python

   async def scroll_demo(makcu):
       await makcu.scroll(5)     # Scroll up
       await makcu.scroll(-3)    # Scroll down

Parallel Operations
------------------

**Execute Multiple Commands Simultaneously:**

.. code-block:: python

   import asyncio
   from makcu import create_async_controller, MouseButton

   async def parallel_demo():
       async with await create_async_controller() as makcu:
           # Execute multiple operations at once
           await asyncio.gather(
               makcu.move(100, 0),
               makcu.click(MouseButton.LEFT),
               makcu.scroll(-1)
           )

   asyncio.run(parallel_demo())

**Sequential vs Parallel Timing:**

.. code-block:: python

   async def timing_comparison():
       async with await create_async_controller() as makcu:
           # Sequential (slower)
           start = time.time()
           await makcu.move(50, 0)
           await makcu.click(MouseButton.LEFT)
           await makcu.move(-50, 0)
           sequential_time = time.time() - start
           
           # Parallel (faster)
           start = time.time()
           await asyncio.gather(
               makcu.move(50, 0),
               makcu.click(MouseButton.LEFT),
               makcu.move(-50, 0)
           )
           parallel_time = time.time() - start
           
           print(f"Sequential: {sequential_time:.3f}s")
           print(f"Parallel: {parallel_time:.3f}s")

Async Button Monitoring
----------------------

**Real-time Button Events:**

.. code-block:: python

   async def button_monitoring():
       async def on_button_event(button: MouseButton, pressed: bool):
           action = "pressed" if pressed else "released"
           print(f"[ASYNC] {button.name} {action}")
       
       async with await create_async_controller() as makcu:
           # Set async callback
           makcu.set_button_callback(on_button_event)
           await makcu.enable_button_monitoring(True)
           
           # Monitor for 10 seconds
           await asyncio.sleep(10)
           
           await makcu.enable_button_monitoring(False)

**Async Button State Checks:**

.. code-block:: python

   async def check_button_states(makcu):
       # Get current states
       states = await makcu.get_button_states()
       
       # Check specific button
       if await makcu.is_pressed(MouseButton.LEFT):
           print("Left button is pressed")

Async Locking Operations
-----------------------

.. code-block:: python

   async def locking_demo():
       async with await create_async_controller() as makcu:
           # Lock buttons and axes
           await makcu.lock(MouseButton.LEFT)
           await makcu.lock("X")  # Lock X-axis
           
           # Check lock states
           left_locked = await makcu.is_locked(MouseButton.LEFT)
           x_locked = await makcu.is_locked("X")
           
           print(f"Left button locked: {left_locked}")
           print(f"X-axis locked: {x_locked}")
           
           # Unlock
           await makcu.unlock(MouseButton.LEFT)
           await makcu.unlock("X")

Connection Management
--------------------

**Connection Status:**

.. code-block:: python

   async def connection_demo():
       makcu = await create_async_controller()
       
       if await makcu.is_connected():
           print("Device connected")
       else:
           print("Device not connected")
           await makcu.connect()  # Manual connection

**Auto-Reconnection with Callbacks:**

.. code-block:: python

   async def auto_reconnect_demo():
       async def on_connection_change(connected: bool):
           if connected:
               print("Device reconnected!")
           else:
               print("Device disconnected!")
       
       makcu = await create_async_controller(auto_reconnect=True)
       
       # Set connection callback
       @makcu.on_connection_change
       async def handle_connection(connected):
           await on_connection_change(connected)
       
       # Your application continues...
       # Reconnection happens automatically

Error Handling in Async
-----------------------

.. code-block:: python

   from makcu import MakcuError, MakcuConnectionError, MakcuTimeoutError

   async def error_handling_demo():
       try:
           async with await create_async_controller() as makcu:
               await makcu.click(MouseButton.LEFT)
               
       except MakcuConnectionError as e:
           print(f"Async connection failed: {e}")
           
       except MakcuTimeoutError as e:
           print(f"Async command timed out: {e}")
           
       except MakcuError as e:
           print(f"General async error: {e}")

Complete Async Example
---------------------

Here's a comprehensive async example:

.. code-block:: python

   import asyncio
   from makcu import create_async_controller, MouseButton

   async def advanced_async_demo():
       """Demonstrates advanced async Makcu usage."""
       
       async def button_monitor_task(makcu):
           """Background task to monitor button presses."""
           async def on_button(button, pressed):
               if pressed:
                   print(f"Detected: {button.name} pressed")
           
           makcu.set_button_callback(on_button)
           await makcu.enable_button_monitoring(True)
           
           # Monitor for 30 seconds
           await asyncio.sleep(30)
           await makcu.enable_button_monitoring(False)
       
       async def mouse_actions_task(makcu):
           """Main mouse control task."""
           # Warm-up clicks
           await asyncio.gather(*[
               makcu.click(MouseButton.LEFT) for _ in range(5)
           ])
           
           # Smooth movement sequence
           movements = [
               (100, 0), (0, 100), (-100, 0), (0, -100)
           ]
           
           for x, y in movements:
               await makcu.move_smooth(x, y, segments=20)
               await asyncio.sleep(0.5)
           
           # Parallel operations
           await asyncio.gather(
               makcu.click(MouseButton.RIGHT),
               makcu.scroll(-2),
               makcu.move(50, 25)
           )

       # Main async execution
       async with await create_async_controller(debug=True) as makcu:
           print("Starting advanced async demo...")
           
           # Run tasks concurrently
           await asyncio.gather(
               button_monitor_task(makcu),
               mouse_actions_task(makcu)
           )
           
           print("Async demo completed!")

   # Run the demo
   asyncio.run(advanced_async_demo())

Integration Examples
-------------------

**With FastAPI:**

.. code-block:: python

   from fastapi import FastAPI
   from makcu import create_async_controller, MouseButton

   app = FastAPI()
   makcu_controller = None

   @app.on_event("startup")
   async def startup():
       global makcu_controller
       makcu_controller = await create_async_controller()

   @app.post("/click/{button}")
   async def click_button(button: str):
       button_enum = getattr(MouseButton, button.upper())
       await makcu_controller.click(button_enum)
       return {"status": "clicked", "button": button}

   @app.post("/move")
   async def move_mouse(x: int, y: int):
       await makcu_controller.move(x, y)
       return {"status": "moved", "x": x, "y": y}

**With AsyncIO Event Loop:**

.. code-block:: python

   import asyncio
   from makcu import create_async_controller, MouseButton

   class MakcuBot:
       def __init__(self):
           self.makcu = None
           self.running = False
       
       async def start(self):
           self.makcu = await create_async_controller(auto_reconnect=True)
           self.running = True
           
           # Start background tasks
           await asyncio.gather(
               self.monitor_buttons(),
               self.periodic_actions()
           )
       
       async def monitor_buttons(self):
           await self.makcu.enable_button_monitoring(True)
           while self.running:
               await asyncio.sleep(0.1)
       
       async def periodic_actions(self):
           while self.running:
               await self.makcu.move(1, 0)  # Tiny movement
               await asyncio.sleep(10)      # Every 10 seconds

   # Usage
   async def main():
       bot = MakcuBot()
       await bot.start()

   asyncio.run(main())

Performance Considerations
-------------------------

**Async Performance Tips:**

.. code-block:: python

   # Good: Use gather for parallel operations
   await asyncio.gather(
       makcu.click(MouseButton.LEFT),
       makcu.move(50, 0),
       makcu.scroll(-1)
   )
   
   # Avoid: Sequential awaits when parallel is possible
   await makcu.click(MouseButton.LEFT)
   await makcu.move(50, 0)
   await makcu.scroll(-1)

**Concurrent Limits:**

.. code-block:: python

   # Limit concurrent operations to avoid overwhelming device
   semaphore = asyncio.Semaphore(5)
   
   async def limited_click():
       async with semaphore:
           await makcu.click(MouseButton.LEFT)
   
   # Execute many clicks with concurrency limit
   tasks = [limited_click() for _ in range(100)]
   await asyncio.gather(*tasks)

Next Steps
----------

* :doc:`advanced_features` - Advanced async patterns and customization  
* :doc:`examples` - More async examples and real-world applications