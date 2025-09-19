Enums and Constants
===================

This section documents the enumerations and constants used in the Makcu library, aligned with the current API as shown in the main documentation.

MouseButton
-----------

The ``MouseButton`` enum defines the available mouse buttons that can be controlled by Makcu devices.

.. py:class:: MouseButton

   An enumeration of mouse buttons supported by Makcu devices.

   .. py:attribute:: LEFT
      :type: MouseButton
      :value: 0

      Left mouse button (primary button for most users)

   .. py:attribute:: RIGHT  
      :type: MouseButton
      :value: 1

      Right mouse button (secondary button, typically context menu)

   .. py:attribute:: MIDDLE
      :type: MouseButton
      :value: 2

      Middle mouse button (typically scroll wheel click)

   .. py:attribute:: MOUSE4
      :type: MouseButton
      :value: 3

      Side button 1 (typically "back" button on gaming mice)

   .. py:attribute:: MOUSE5
      :type: MouseButton
      :value: 4

      Side button 2 (typically "forward" button on gaming mice)

**Usage Examples:**

.. code-block:: python

    from makcu import MouseButton

    # Synchronous API
    makcu.click(MouseButton.LEFT)
    makcu.click(MouseButton.RIGHT)
    makcu.click(MouseButton.MIDDLE)

    # Gaming mouse side buttons
    makcu.click(MouseButton.MOUSE4)
    makcu.click(MouseButton.MOUSE5)

    # Asynchronous API
    await makcu.click(MouseButton.LEFT)
    await makcu.click(MouseButton.RIGHT)

    # Get button properties
    button = MouseButton.LEFT
    print(button.name)   # "LEFT"
    print(button.value)  # 0

**Button Values:**

.. list-table:: MouseButton Values and Usage
   :widths: 25 15 60
   :header-rows: 1

   * - Button
     - Value
     - Typical Use
   * - ``LEFT``
     - 0
     - Primary clicking, selection, dragging
   * - ``RIGHT``
     - 1
     - Context menus, secondary actions
   * - ``MIDDLE``
     - 2
     - Scroll wheel click, special functions
   * - ``MOUSE4``
     - 3
     - Back/previous navigation, gaming macros
   * - ``MOUSE5``
     - 4
     - Forward/next navigation, gaming macros

Human-Like Profiles
-------------------

The library supports string-based timing profiles for human-like mouse interactions, used with the ``click_human_like()`` method.

**Available Profiles:**

.. py:data:: GAMING_PROFILE
   :type: str
   :value: "gaming"

   Ultra-fast profile optimized for competitive gaming (1-5ms delays)

.. py:data:: FAST_PROFILE
   :type: str
   :value: "fast"

   Fast clicking profile (10-30ms delays)

.. py:data:: NORMAL_PROFILE
   :type: str
   :value: "normal"

   Natural human-like timing (50-150ms delays, default)

.. py:data:: SLOW_PROFILE
   :type: str
   :value: "slow"

   Slow, deliberate timing (200-500ms delays)

.. py:data:: VARIABLE_PROFILE
   :type: str
   :value: "variable"

   Highly variable timing to avoid detection (50-300ms delays)

**Usage Examples:**

.. code-block:: python

    # Synchronous API
    makcu.click_human_like(MouseButton.LEFT, count=3, profile="gaming")
    makcu.click_human_like(MouseButton.RIGHT, count=5, profile="normal", jitter=5)

    # Asynchronous API
    await makcu.click_human_like(MouseButton.LEFT, count=2, profile="gaming", jitter=3)
    await makcu.click_human_like(MouseButton.RIGHT, count=3, profile="variable")

**Profile Characteristics:**

.. list-table:: Human-Like Profile Timing
   :widths: 20 20 20 40
   :header-rows: 1

   * - Profile
     - Min Delay
     - Max Delay
     - Best For
   * - ``"gaming"``
     - 1ms
     - 5ms
     - Competitive gaming, maximum speed
   * - ``"fast"``
     - 10ms
     - 30ms
     - Productivity automation, quick tasks
   * - ``"normal"``
     - 50ms
     - 150ms
     - General automation, natural feel
   * - ``"slow"``
     - 200ms
     - 500ms
     - Careful automation, older systems
   * - ``"variable"``
     - 50ms
     - 300ms
     - Anti-detection, randomized patterns

Lock Targets
------------

The locking system accepts string identifiers for buttons and axes that can be locked to prevent input.

**Button Lock Targets:**

.. py:data:: LOCK_LEFT
   :type: str
   :value: "LEFT"

   Lock left mouse button

.. py:data:: LOCK_RIGHT
   :type: str
   :value: "RIGHT"

   Lock right mouse button

.. py:data:: LOCK_MIDDLE
   :type: str
   :value: "MIDDLE"

   Lock middle mouse button

**Axis Lock Targets:**

.. py:data:: LOCK_X_AXIS
   :type: str
   :value: "X"

   Lock X-axis movement (horizontal)

.. py:data:: LOCK_Y_AXIS
   :type: str
   :value: "Y"

   Lock Y-axis movement (vertical)

**Usage Examples:**

.. code-block:: python

    # Lock buttons (synchronous)
    makcu.lock(MouseButton.LEFT)    # Using enum
    makcu.lock("RIGHT")             # Using string
    makcu.lock("MIDDLE")

    # Lock movement axes
    makcu.lock("X")    # Lock horizontal movement
    makcu.lock("Y")    # Lock vertical movement

    # Asynchronous API
    await makcu.lock(MouseButton.LEFT)
    await makcu.lock("X")
    await makcu.unlock("Y")

    # Check lock status
    is_locked = makcu.is_locked(MouseButton.LEFT)
    all_locks = makcu.get_all_lock_states()
    # Returns: {"LEFT": True, "RIGHT": False, "X": True, "Y": False, ...}

Constants and Default Values
----------------------------

Serial Communication
^^^^^^^^^^^^^^^^^^^^

.. py:data:: DEFAULT_BAUDRATE
   :type: int
   :value: 4000000

   Default serial communication speed (4 Mbps)

.. py:data:: DEFAULT_TIMEOUT
   :type: float
   :value: 0.1

   Default timeout for device operations (100ms, optimized for gaming)

.. py:data:: VID_PID
   :type: tuple
   :value: (0x1a86, 0x55d3)

   USB Vendor ID and Product ID for auto-detection (CH343 chipset)

**Usage Examples:**

.. code-block:: python

    # Custom timeout (synchronous)
    makcu = create_controller(timeout=0.05)  # 50ms timeout

    # Custom timeout (asynchronous)
    makcu = await create_async_controller(timeout=0.05)

Device Limits
^^^^^^^^^^^^^

.. py:data:: MAX_MOVE_DISTANCE
   :type: int
   :value: 32767

   Maximum single movement distance in pixels

.. py:data:: MIN_MOVE_DISTANCE
   :type: int
   :value: -32768

   Minimum single movement distance in pixels

.. py:data:: MAX_SCROLL_STEPS
   :type: int
   :value: 127

   Maximum scroll steps in single operation

**Usage Examples:**

.. code-block:: python

    # Large movements are automatically clamped
    makcu.move(50000, 25000)  # Clamped to MAX_MOVE_DISTANCE

    # Asynchronous version
    await makcu.move(50000, 25000)

    # Maximum scroll
    makcu.scroll(MAX_SCROLL_STEPS)
    await makcu.scroll(-MAX_SCROLL_STEPS)  # Scroll down maximum

Performance Constants
^^^^^^^^^^^^^^^^^^^^

.. py:data:: GAMING_REFRESH_RATES
   :type: dict
   :value: {"60Hz": 16.7, "144Hz": 7.0, "240Hz": 4.2, "360Hz": 2.8}

   Common gaming refresh rates and their frame times in milliseconds

.. py:data:: PERFORMANCE_TARGETS
   :type: dict
   :value: {"excellent": 1, "good": 3, "acceptable": 5}

   Performance targets in milliseconds per operation (v2.0 benchmarks)

**Usage Examples:**

.. code-block:: python

    # Performance-aware gaming code
    import time

    # Benchmark operation timing
    start = time.perf_counter()
    makcu.click(MouseButton.LEFT)
    operation_time = (time.perf_counter() - start) * 1000  # Convert to ms
    
    if operation_time < PERFORMANCE_TARGETS["excellent"]:
        print(f"Excellent performance: {operation_time:.2f}ms (suitable for 360Hz gaming)")
    elif operation_time < GAMING_REFRESH_RATES["144Hz"]:
        print(f"Good for 144Hz gaming: {operation_time:.2f}ms")

Error Handling Constants
------------------------

The library defines specific error types for different failure conditions.

.. py:data:: ERROR_TYPES
   :type: tuple
   :value: (MakcuError, MakcuConnectionError, MakcuTimeoutError)

   Main exception types used by the library

**Usage Examples:**

.. code-block:: python

    from makcu import MakcuError, MakcuConnectionError, MakcuTimeoutError

    # Synchronous error handling
    try:
        makcu = create_controller()
        makcu.click(MouseButton.LEFT)
    except MakcuConnectionError as e:
        print(f"Connection failed: {e}")
    except MakcuTimeoutError as e:
        print(f"Operation timed out: {e}")
    except MakcuError as e:
        print(f"General error: {e}")

    # Asynchronous error handling
    try:
        makcu = await create_async_controller()
        await makcu.click(MouseButton.LEFT)
    except MakcuConnectionError as e:
        print(f"Connection failed: {e}")

Version Information
-------------------

.. py:data:: LIBRARY_VERSION
   :type: str
   :value: "2.2.1"

   Current library version

.. py:data:: API_VERSION
   :type: str
   :value: "2.0"

   API version (both sync and async APIs supported)

**Usage Examples:**

.. code-block:: python

    # Check library version
    import makcu
    print(f"Makcu library version: {makcu.__version__}")

    # Version-specific feature usage
    if makcu.__version__ >= "2.0":
        # Use new async features
        makcu = await create_async_controller()
    else:
        # Fall back to sync only
        makcu = create_controller()

Type Hints and Validation
-------------------------

The library provides flexible input types while maintaining type safety.

**Acceptable Button Types:**

- ``MouseButton`` enum values (recommended)
- Integer values (0-4, mapped to buttons)
- String names ("LEFT", "RIGHT", etc., case-insensitive)

**Acceptable Profile Types:**

- String literals ("gaming", "fast", "normal", "slow", "variable")

**Acceptable Lock Target Types:**

- ``MouseButton`` enum values for button locks
- String identifiers ("X", "Y" for axes; "LEFT", "RIGHT", etc. for buttons)

**Usage Examples:**

.. code-block:: python

    # All of these work (flexible input types):
    
    # Using enums (recommended for type safety)
    makcu.click(MouseButton.LEFT)
    
    # Using integers
    makcu.click(0)  # Same as MouseButton.LEFT
    
    # Using strings (case-insensitive)
    makcu.click("left")
    makcu.click("LEFT")
    makcu.click("Left")

    # Profile flexibility
    makcu.click_human_like(MouseButton.LEFT, profile="gaming")
    makcu.click_human_like(MouseButton.LEFT, profile="GAMING")
    
    # Lock target flexibility
    makcu.lock(MouseButton.LEFT)  # Enum
    makcu.lock("LEFT")            # String
    makcu.lock("x")               # Axis (case-insensitive)

Best Practices
--------------

1. **Use MouseButton Enum for Type Safety**:

   .. code-block:: python

      # Recommended: Clear and type-safe
      await makcu.click(MouseButton.LEFT)
      
      # Avoid: Magic numbers
      await makcu.click(0)

2. **Consistent Profile Usage**:

   .. code-block:: python

      # Consistent profile strings
      GAMING_PROFILE = "gaming"
      await makcu.click_human_like(MouseButton.LEFT, profile=GAMING_PROFILE)

3. **Error Handling**:

   .. code-block:: python

      # Always handle connection errors
      try:
          async with await create_async_controller() as makcu:
              await makcu.click(MouseButton.LEFT)
      except MakcuConnectionError:
          print("Could not connect to Makcu device")

4. **Performance-Aware Code**:

   .. code-block:: python

      # Check performance for gaming applications
      if operation_time < GAMING_REFRESH_RATES["240Hz"]:
          print("Suitable for 240Hz gaming!")

5. **Use Context Managers**:

   .. code-block:: python

      # Automatic connection management
      async with await create_async_controller() as makcu:
          await makcu.click(MouseButton.LEFT)
      # Automatically disconnects

Integration with Main API
------------------------

These enums and constants integrate seamlessly with both synchronous and asynchronous APIs:

.. code-block:: python

    from makcu import create_controller, create_async_controller, MouseButton
    import asyncio

    # Synchronous usage
    def sync_example():
        with create_controller() as makcu:
            makcu.click(MouseButton.LEFT)
            makcu.move(100, 50)
            makcu.click_human_like(MouseButton.RIGHT, count=3, profile="gaming")

    # Asynchronous usage  
    async def async_example():
        async with await create_async_controller() as makcu:
            await makcu.click(MouseButton.LEFT)
            await makcu.move(100, 50)
            await makcu.click_human_like(MouseButton.RIGHT, count=3, profile="gaming")

    # Run async version
    asyncio.run(async_example())

See Also
--------

* :doc:`controller` - Main synchronous controller API
* :doc:`async_controller` - Asynchronous controller API  
* :doc:`../getting_started` - Basic usage tutorial
* :doc:`../examples` - More code examples with enums
* :doc:`../async_usage` - Async/await patterns