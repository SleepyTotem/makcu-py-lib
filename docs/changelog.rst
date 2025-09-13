Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_, and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.


v2.2.0 (Current)
----------------

**Added**

* Added async for lock, unlock, and click_human_like methods
* Added missing batch_execute command

**Fixed**

* Documentation formatting consistency
* Fixed all Sync vs Async limitations
* Fixed duplicate controller inside init
* Corrected missing debug statements in controller

**Changed**

* Enhanced documentation with complete API reference

v2.1.3
----------------

**Fixed**

* Async controller bug
* Documentation formatting consistency

v2.1.2
----------------

**Added**

* Additional examples for common use cases
* Improved error messages with actionable suggestions

**Fixed**

* Minor stability improvements in connection handling
* Documentation formatting consistency

**Changed**

* Updated dependencies for better compatibility

v2.1.0
------

**Added**

* Context manager support for automatic cleanup
* Enhanced button event monitoring with callbacks
* Serial spoofing capabilities
* Batch command execution utilities
* Connection status callbacks

**Changed**

* Improved error handling with custom exception types
* Better logging format with timestamps
* Enhanced debugging output

**Fixed**

* Memory leak in continuous button monitoring
* Race condition in auto-reconnection logic

v2.0.0 (Major Release)
----------------------

**🚀 Huge Performance Update**

This is a complete rewrite focusing on **gaming performance** and **modern Python async support**.

**Added**

* **Async/Await Support**: Complete async API with ``create_async_controller()``
* **Zero-Delay Architecture**: Removed all ``sleep()`` calls with intelligent command tracking
* **Auto-Reconnection**: Automatic device reconnection on disconnect with callbacks
* **Parallel Operations**: Execute multiple commands simultaneously with ``asyncio.gather()``
* **Gaming Optimization**: Sub-3ms command execution for 240Hz+ gaming
* **Command Tracking**: Unique ID system for reliable command-response matching
* **Enhanced Debugging**: Detailed logging with performance metrics
* **Human-like Interactions**: ``click_human_like()`` with timing profiles
* **Button Event Monitoring**: Real-time button state callbacks
* **Smooth Movement**: Bezier curves and interpolated movement
* **Batch Operations**: ``batch_execute()`` for efficient command sequences
* **Lock State Queries**: Instant lock state checking without delays
* **Device Information**: Comprehensive device info and firmware version
* **Command-line Tools**: Interactive debug console and automated testing

**Performance Improvements**

* **17x faster** average performance compared to v1.3
* **117x faster** batch operations
* **33x faster** lock state queries
* **20x faster** firmware version checks
* **18x faster** button operations

**Technical Enhancements**

* Pre-computed command templates
* Bitwise button state operations
* Zero-copy buffer management
* Optimized serial timeouts (1ms read, 10ms write)
* High-priority listener thread
* Cache-friendly connection checks
* Minimal memory allocations

**Breaking Changes**

* Some sync-only methods in async contexts require ``run_in_executor()``
* ``drag()`` and ``get_all_lock_states()`` currently sync-only
* Debug output format changed
* Exception hierarchy restructured

**Migration Notes**

* Most v1.x code works without changes
* Add ``await`` for async operations
* Use context managers for automatic cleanup
* Enable ``auto_reconnect=True`` for stability

v1.4.0
------

**Added**

* Initial performance optimizations
* Reduced sleep delays in critical paths
* Improved connection stability

**Changed**

* Faster command execution (~2x improvement over v1.3)
* Better error handling

**Fixed**

* Connection timeout issues
* Memory usage improvements

v1.3.0
------

**Added**

* Button locking and unlocking functionality
* Mouse axis locking (X/Y)
* Basic button state querying
* Drag operation support

**Changed**

* Improved command parsing
* Better error messages

**Fixed**

* Serial communication stability
* Button mask handling

v1.2.0
------

**Added**

* Mouse movement with relative positioning
* Scroll wheel support
* Double-click functionality
* Basic button press/release

**Changed**

* Refactored core communication layer
* Improved device discovery

v1.1.0
------

**Added**

* Multi-button support (LEFT, RIGHT, MIDDLE, MOUSE4, MOUSE5)
* Device auto-discovery via VID/PID
* Basic error handling

**Fixed**

* Serial port detection on Windows
* Command response parsing

v1.0.0 (Initial Release)
------------------------

**Added**

* Basic mouse control functionality
* Left/right click support
* Simple movement commands
* Serial communication with CH343 USB devices
* GPL license

**Known Limitations**

* High latency due to sleep delays
* No async support
* Limited error handling
* Manual device connection required

Gaming Performance Targets
---------------------------

**v2.0 Gaming Benchmarks**

* **144Hz Gaming** (7ms frame time): ✅ **Easily met** (avg 1-3ms per operation)
* **240Hz Gaming** (4.2ms frame time): ✅ **Consistently met** (most ops ≤2ms) 
* **360Hz Gaming** (2.8ms frame time): ⚡ **Achievable** (for atomic/single operations)

**Performance Evolution**

.. list-table::
   :header-rows: 1
   :widths: 30 20 20 20 30

   * - Operation
     - v1.3
     - v1.4  
     - v2.0
     - Improvement
   * - Button Click
     - ~18ms
     - ~9ms
     - **1ms**
     - 18x faster
   * - Mouse Movement
     - ~17ms
     - ~8ms
     - **2ms**
     - 8.5x faster
   * - Batch Commands
     - ~350ms
     - ~90ms
     - **3ms**
     - 117x faster
   * - Lock Queries
     - ~33ms
     - ~10ms
     - **1ms**
     - 33x faster

Migration Guide
---------------

**From v1.x to v2.0**

Most existing code continues to work. Key migration paths:

**Synchronous (No Changes Required)**

.. code-block:: python

   # v1.x and v2.0 - identical
   from makcu import create_controller, MouseButton
   
   makcu = create_controller()
   makcu.click(MouseButton.LEFT)
   makcu.move(100, 50)
   makcu.disconnect()

**Asynchronous (New in v2.0)**

.. code-block:: python

   # v2.0 async
   import asyncio
   from makcu import create_async_controller, MouseButton
   
   async def main():
       async with await create_async_controller() as makcu:
           await makcu.click(MouseButton.LEFT)
           await makcu.move(100, 50)
   
   asyncio.run(main())

**Mixed Operations (v2.0)**

.. code-block:: python

   # Use executor for sync-only methods in async context
   loop = asyncio.get_running_loop()
   await loop.run_in_executor(None, makcu.lock, MouseButton.LEFT)

**Auto-Reconnection (v2.0)**

.. code-block:: python

   # Enable auto-reconnection
   makcu = create_controller(auto_reconnect=True)
   
   @makcu.on_connection_change
   def handle_connection(connected: bool):
       if connected:
           print("Device reconnected!")

Deprecation Notices
-------------------

**Currently Deprecated**

* None - v2.0 maintains full v1.x compatibility

**Future Deprecations (v3.0)**

* Synchronous-only methods will gain async equivalents
* Some legacy method signatures may be simplified
* Debug output format may change

**Removal Schedule**

* No removals planned - library maintains backwards compatibility