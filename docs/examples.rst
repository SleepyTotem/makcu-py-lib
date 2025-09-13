Examples
========

This section contains practical examples for common use cases with the Makcu library. Each example includes both synchronous and asynchronous versions where applicable.

.. toctree::
   :maxdepth: 2
   :caption: Basic Usage

   basic_mouse_control
   human_like_interactions
   button_monitoring

.. toctree::
   :maxdepth: 2
   :caption: Advanced Features

   gaming_applications
   automation_scripts
   web_integration

.. toctree::
   :maxdepth: 2
   :caption: Real-World Applications

   discord_bot
   fastapi_web_app
   gui_applications

.. toctree::
   :maxdepth: 2
   :caption: Performance & Optimization

   high_performance_gaming
   batch_operations
   parallel_processing

Quick Start Examples
--------------------

Here are some quick examples to get you started:

Basic Mouse Control
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from makcu import create_controller, MouseButton

    # Simple click and move
    makcu = create_controller()
    makcu.click(MouseButton.LEFT)
    makcu.move(100, 50)
    makcu.disconnect()

Async Version
^^^^^^^^^^^^^

.. code-block:: python

    import asyncio
    from makcu import create_async_controller, MouseButton

    async def main():
        async with await create_async_controller() as makcu:
            await makcu.click(MouseButton.LEFT)
            await makcu.move(100, 50)

    asyncio.run(main())

Gaming Example
^^^^^^^^^^^^^^

.. code-block:: python

    from makcu import create_controller, MouseButton

    makcu = create_controller(debug=False)  # Max performance

    # Ultra-fast gaming clicks
    makcu.click_human_like(MouseButton.LEFT, profile="gaming")
    
    # Precise movement
    makcu.move_smooth(200, 100, segments=30)

Choose Your Use Case
--------------------

🎮 **Gaming Applications**
  High-performance mouse control for competitive gaming, with sub-3ms response times and parallel operations.
  
  → See: :doc:`gaming_applications`, :doc:`high_performance_gaming`

🤖 **Automation Scripts**  
  Automate repetitive tasks with human-like mouse movements and intelligent timing.
  
  → See: :doc:`automation_scripts`, :doc:`human_like_interactions`

🌐 **Web Applications**
  Integrate mouse control into web servers, APIs, and online services.
  
  → See: :doc:`web_integration`, :doc:`fastapi_web_app`

💬 **Discord/Chat Bots**
  Add mouse control commands to Discord bots and chat applications.
  
  → See: :doc:`discord_bot`

🖥️ **GUI Applications**  
  Embed mouse control into desktop applications with proper async integration.
  
  → See: :doc:`gui_applications`

⚡ **High Performance**
  Maximize performance for real-time applications requiring minimal latency.

Performance Comparison
----------------------

Here's how different approaches perform:

.. list-table:: Performance by Use Case
   :widths: 25 25 25 25
   :header-rows: 1

   * - Use Case
     - Sync Performance
     - Async Performance  
     - Best For
   * - Gaming
     - ~2ms per operation
     - ~1ms per operation
     - Real-time gaming
   * - Automation
     - ~5ms per operation
     - ~3ms per operation
     - Scripts & bots
   * - Web Apps
     - Blocking
     - Non-blocking
     - Server applications
   * - Bulk Operations
     - Sequential
     - Parallel
     - Large datasets

Code Standards
--------------

All examples follow these standards:

* ✅ **Error Handling**: Proper exception handling
* ✅ **Resource Cleanup**: Context managers and proper disconnection
* ✅ **Type Hints**: Full type annotations for clarity
* ✅ **Documentation**: Detailed comments and docstrings  
* ✅ **Performance**: Optimized for their specific use case
* ✅ **Modern Python**: Uses Python 3.7+ features and best practices

Running Examples
----------------

Each example can be run directly:

.. code-block:: bash

    # Download example
    curl -O https://raw.githubusercontent.com/SleepyTotem/makcu-py-lib/main/examples/basic_mouse_control.py
    
    # Run example
    python basic_mouse_control.py

Or integrated into your own projects:

.. code-block:: python

    # Import and adapt
    from examples.gaming_applications import gaming_combo
    
    # Use in your code
    await gaming_combo()

Contributing Examples
---------------------

Have a great example to share? We'd love to include it!

**Example Requirements:**

1. **Clear Purpose**: Solves a specific, common use case
2. **Well Documented**: Comments explaining what each part does
3. **Error Handling**: Proper exception handling
4. **Performance**: Optimized for its use case
5. **Both Versions**: Include sync and async versions if applicable

**Submit via:**

* GitHub Pull Request to the examples/ directory
* GitHub Discussions with your code
* GitHub Issues tagged as "example request"

Next Steps
----------

1. 📖 **Browse Examples**: Pick your use case from the list above
2. 💻 **Try the Code**: Copy and run examples locally  
3. 🔧 **Adapt for Your Needs**: Modify examples for your specific requirements
4. 🚀 **Build Something Cool**: Use examples as starting points for your projects
5. 🤝 **Share Back**: Contribute your own examples to help others!