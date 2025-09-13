Performance Benchmarks
=====================

This document provides detailed performance analysis and benchmarking data for the Makcu Python Library across different versions, with a focus on gaming performance and real-time applications.

Overview
--------

The Makcu Python Library has undergone significant performance optimizations, culminating in v2.0's **zero-delay architecture**. This page documents the performance improvements, benchmarking methodology, and provides guidance for performance-critical applications.

Benchmark Summary
-----------------

**Average Performance Improvement: v1.3 → v2.0**

* **17x faster** across all core operations
* **Sub-3ms** command execution for gaming applications
* **Zero artificial delays** - no ``sleep()`` calls
* **240Hz+ gaming ready** - consistently under 4.2ms frame time

Version Comparison
------------------

Detailed Benchmark Results
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table:: **Complete Performance Comparison**
   :header-rows: 1
   :widths: 25 15 15 15 30

   * - Test Operation
     - v1.3 (ms)
     - v1.4 (ms)
     - v2.0 (ms)
     - Improvement Factor
   * - **Connection & Setup**
     - 
     - 
     - 
     - 
   * - connect_to_port
     - ~100
     - ~55
     - **46**
     - 2.2x faster
   * - device_info
     - ~25
     - ~13
     - **6**
     - 4.1x faster
   * - firmware_version
     - ~20
     - ~9
     - **1**
     - 20x faster
   * - port_connection
     - ~20
     - ~9
     - **1**
     - 20x faster
   * - **Mouse Operations**
     - 
     - 
     - 
     - 
   * - press_and_release
     - ~18
     - ~9
     - **1**
     - 18x faster
   * - middle_click
     - ~18
     - ~9
     - **1**
     - 18x faster
   * - button_mask
     - ~17
     - ~8
     - **1**
     - 17x faster
   * - get_button_states
     - ~18
     - ~9
     - **1**
     - 18x faster
   * - rapid_moves
     - ~17
     - ~8
     - **2**
     - 8.5x faster
   * - button_performance
     - ~18
     - ~9
     - **2**
     - 9x faster
   * - **State Management**
     - 
     - 
     - 
     - 
   * - lock_state
     - ~33
     - ~10
     - **1**
     - 33x faster
   * - makcu_behavior
     - ~20
     - ~10
     - **1**
     - 20x faster
   * - mixed_operations
     - ~22
     - ~10
     - **2**
     - 11x faster
   * - **Batch Operations**
     - 
     - 
     - 
     - 
   * - batch_commands
     - ~350
     - ~90
     - **3**
     - 117x faster

Gaming Performance Analysis
---------------------------

Frame Rate Compatibility
^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table:: **Gaming Performance Targets**
   :header-rows: 1
   :widths: 20 20 20 40

   * - Gaming Target
     - Frame Time
     - v2.0 Performance
     - Status
   * - **60Hz Gaming**
     - 16.7ms
     - 1-3ms avg
     - ✅ **Easily exceeded**
   * - **144Hz Gaming**
     - 7.0ms
     - 1-3ms avg
     - ✅ **Easily exceeded**
   * - **240Hz Gaming**
     - 4.2ms
     - ≤2ms most ops
     - ✅ **Consistently met**
   * - **360Hz Gaming**
     - 2.8ms
     - ≤2ms atomic ops
     - ⚡ **Achievable**
   * - **480Hz Gaming**
     - 2.1ms
     - ≤1ms single ops
     - ⚡ **Limited scenarios**

**Gaming Recommendations**

* **Competitive Gaming (144-240Hz)**: Use v2.0 with ``profile="gaming"`` for optimal performance
* **Professional Esports (240Hz+)**: Enable ``debug=False`` and use atomic operations
* **Ultra-High Refresh (360Hz+)**: Combine operations and use async batching

Latency Analysis
^^^^^^^^^^^^^^^^

**Command Execution Pipeline (v2.0)**

.. code-block:: none

   User Call → Command Format → Serial Write → Device Process → Response → Parse
   ↑_________________________________________________________________________↑
                           Total Latency: ~1-3ms typical

**Latency Breakdown**

* **Command Formatting**: <0.1ms (pre-computed templates)
* **Serial Write**: ~0.5ms (optimized timeouts)
* **Device Processing**: ~0.3-1ms (firmware dependent)
* **Response Parse**: <0.1ms (zero-copy parsing)
* **State Update**: <0.1ms (bitwise operations)

**v1.3 vs v2.0 Latency Sources**

.. list-table::
   :header-rows: 1
   :widths: 30 25 25 20

   * - Latency Source
     - v1.3 Impact
     - v2.0 Impact
     - Improvement
   * - Artificial Delays (``sleep()``)
     - 10-15ms
     - **0ms**
     - Eliminated
   * - Command Formatting
     - 1-2ms
     - **<0.1ms**
     - 10-20x faster
   * - Serial Timeouts
     - 5-10ms
     - **1ms**
     - 5-10x faster
   * - Response Parsing
     - 1-2ms
     - **<0.1ms**
     - 10-20x faster
   * - State Management
     - 2-5ms
     - **<0.1ms**
     - 20-50x faster

Benchmarking Methodology
------------------------

Test Environment
^^^^^^^^^^^^^^^^

**Hardware Configuration**

* **CPU**: Intel i7-12700K / AMD Ryzen 7 5800X3D class
* **RAM**: 32GB DDR4-3200 / DDR5-5600
* **USB**: Native USB 3.0+ ports (no hubs)
* **Device**: Makcu hardware with CH343 USB serial
* **OS**: Windows 10/11 with high-performance power plan

**Software Configuration**

.. code-block:: python

   # Test configuration
   ITERATIONS = 1000
   WARMUP_ITERATIONS = 100
   TIMEOUT = 0.1  # 100ms max per operation
   DEBUG = False  # Production settings

Benchmark Test Suite
^^^^^^^^^^^^^^^^^^^^

The complete benchmark suite (``test_suite.py``) includes:

**Connection Tests**

.. code-block:: python

   def test_connect_to_port():
       """Test device connection time"""
       start = time.perf_counter()
       makcu = create_controller()
       end = time.perf_counter()
       assert (end - start) < 0.1  # <100ms for v2.0

**Mouse Operation Tests**

.. code-block:: python

   def test_rapid_moves():
       """Test rapid mouse movement performance"""
       start = time.perf_counter()
       for i in range(100):
           makcu.move(1, 1)
       end = time.perf_counter()
       avg_time = (end - start) / 100
       assert avg_time < 0.005  # <5ms average

**Batch Operation Tests**

.. code-block:: python

   def test_batch_commands():
       """Test batch command execution"""
       commands = [
           lambda: makcu.move(10, 0),
           lambda: makcu.click(MouseButton.LEFT),
           lambda: makcu.move(-10, 0)
       ] * 50  # 150 total commands
       
       start = time.perf_counter()
       makcu.batch_execute(commands)
       end = time.perf_counter()
       assert (end - start) < 0.01  # <10ms for 150 commands

Running Benchmarks
^^^^^^^^^^^^^^^^^^^

**Automated Benchmark Suite**

.. code-block:: bash

   # Run complete test suite with timing
   python -m makcu --runtest
   
   # Generates: latest_pytest.html with detailed timings

**Manual Performance Testing**

.. code-block:: python

   import time
   from makcu import create_controller, MouseButton

   def benchmark_clicks(iterations=1000):
       makcu = create_controller(debug=False)
       
       # Warmup
       for _ in range(100):
           makcu.click(MouseButton.LEFT)
       
       # Benchmark
       start = time.perf_counter()
       for _ in range(iterations):
           makcu.click(MouseButton.LEFT)
       end = time.perf_counter()
       
       avg_time = (end - start) / iterations * 1000  # Convert to ms
       print(f"Average click time: {avg_time:.3f}ms")
       
       makcu.disconnect()

   benchmark_clicks()  # Typical result: ~1ms in v2.0

**Custom Benchmark Script**

.. code-block:: python

   import asyncio
   import time
   from makcu import create_async_controller, MouseButton

   async def async_benchmark():
       async with await create_async_controller() as makcu:
           # Test parallel operations
           start = time.perf_counter()
           await asyncio.gather(*[
               makcu.move(10, 0),
               makcu.click(MouseButton.LEFT),
               makcu.move(-10, 0),
               makcu.scroll(-1)
           ])
           end = time.perf_counter()
           
           print(f"Parallel ops time: {(end-start)*1000:.1f}ms")

   asyncio.run(async_benchmark())  # Typical: ~2-3ms

Performance Optimization Guide
------------------------------

Code-Level Optimizations
^^^^^^^^^^^^^^^^^^^^^^^^^

**1. Disable Debug Mode in Production**

.. code-block:: python

   # Development
   makcu = create_controller(debug=True)
   
   # Production
   makcu = create_controller(debug=False)  # ~10% faster

**2. Use Context Managers**

.. code-block:: python

   # Optimal - automatic cleanup
   with create_controller() as makcu:
       makcu.click(MouseButton.LEFT)  # Connection cached

**3. Batch Similar Operations**

.. code-block:: python

   # Slow - individual calls
   for _ in range(100):
       makcu.move(1, 0)
   
   # Fast - batched execution
   makcu.batch_execute([lambda: makcu.move(1, 0)] * 100)

**4. Use Gaming Profiles**

.. code-block:: python

   # Optimized for speed
   makcu.click_human_like(
       MouseButton.LEFT, 
       profile="gaming",  # Fastest timing profile
       count=5
   )

**5. Leverage Async for Parallelism**

.. code-block:: python

   # Sequential (slower)
   makcu.move(100, 0)
   makcu.click(MouseButton.LEFT)
   makcu.scroll(-1)
   
   # Parallel (faster)
   await asyncio.gather(
       makcu.move(100, 0),
       makcu.click(MouseButton.LEFT),
       makcu.scroll(-1)
   )

System-Level Optimizations
^^^^^^^^^^^^^^^^^^^^^^^^^^

**1. USB Configuration**

.. code-block:: bash

   # Windows: Disable USB selective suspend
   # Power Options → Advanced → USB selective suspend → Disabled

**2. Process Priority**

.. code-block:: python

   import psutil
   import os
   
   # Set high priority for gaming applications
   p = psutil.Process(os.getpid())
   p.nice(psutil.HIGH_PRIORITY_CLASS)  # Windows
   # p.nice(-10)  # Linux

**3. Thread Affinity**

.. code-block:: python

   # Pin to specific CPU cores for consistent timing
   import psutil
   psutil.Process().cpu_affinity([0, 1])  # Use cores 0 and 1

Performance Monitoring
----------------------

Real-Time Performance Tracking
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   import time
   from collections import deque
   from makcu import create_controller, MouseButton

   class PerformanceMonitor:
       def __init__(self, window_size=100):
           self.timings = deque(maxlen=window_size)
           
       def time_operation(self, operation):
           start = time.perf_counter()
           result = operation()
           end = time.perf_counter()
           
           timing = (end - start) * 1000  # Convert to ms
           self.timings.append(timing)
           return result
           
       @property
       def average_ms(self):
           return sum(self.timings) / len(self.timings) if self.timings else 0
           
       @property
       def max_ms(self):
           return max(self.timings) if self.timings else 0

   # Usage
   monitor = PerformanceMonitor()
   makcu = create_controller()

   # Monitor click performance
   for _ in range(1000):
       monitor.time_operation(
           lambda: makcu.click(MouseButton.LEFT)
       )
       
       if len(monitor.timings) % 100 == 0:
           print(f"Avg: {monitor.average_ms:.1f}ms, "
                 f"Max: {monitor.max_ms:.1f}ms")

Performance Troubleshooting
---------------------------

Common Performance Issues
^^^^^^^^^^^^^^^^^^^^^^^^^

**1. High Latency (>5ms per operation)**

*Possible Causes:*
- Debug mode enabled in production
- USB hub or extension cable
- System power management
- Background processes

*Solutions:*
- Set ``debug=False``
- Use direct USB connection
- Disable USB power management
- Close unnecessary applications

**2. Inconsistent Performance**

*Possible Causes:*
- Windows timer resolution
- CPU throttling
- Memory pressure
- USB port sharing

*Solutions:*

.. code-block:: python

   # Force high timer resolution (Windows)
   import ctypes
   ctypes.windll.winmm.timeBeginPeriod(1)

**3. Connection Timeouts**

*Possible Causes:*
- Incorrect COM port
- Driver issues
- Hardware failure
- Power supply insufficient

*Solutions:*
- Use device auto-discovery
- Update CH343 drivers
- Check device LED status
- Use powered USB hub if needed

Performance Regression Testing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Automated Performance Tests**

.. code-block:: python

   import pytest
   import time
   from makcu import create_controller, MouseButton

   class TestPerformance:
       def setup_method(self):
           self.makcu = create_controller(debug=False)
           
       def teardown_method(self):
           self.makcu.disconnect()
           
       def test_click_performance(self):
           """Ensure click operations stay under 3ms"""
           timings = []
           for _ in range(100):
               start = time.perf_counter()
               self.makcu.click(MouseButton.LEFT)
               end = time.perf_counter()
               timings.append((end - start) * 1000)
           
           avg_time = sum(timings) / len(timings)
           max_time = max(timings)
           
           assert avg_time < 3.0, f"Average time {avg_time:.1f}ms too slow"
           assert max_time < 10.0, f"Max time {max_time:.1f}ms too slow"

Future Performance Improvements
-------------------------------

**Roadmap for v2.2+**

* **Hardware Acceleration**: Direct USB bulk transfers
* **Predictive Caching**: Pre-compute command sequences
* **NUMA Awareness**: Optimize for multi-socket systems
* **Real-Time Scheduling**: Integration with RT kernels
* **GPU Offloading**: Parallel command processing

**Research Areas**

* **Sub-millisecond Operations**: Target <1ms for all operations
* **Jitter Reduction**: More consistent timing
* **Power Efficiency**: Lower CPU usage
* **Memory Optimization**: Reduced allocation overhead

Historical Performance Data
---------------------------

**Performance Evolution Timeline**

.. code-block:: none

   v1.0 (2023-01): Basic functionality, ~50ms operations
   ├─ v1.1 (2023-03): Multi-button support, ~30ms operations  
   ├─ v1.2 (2023-06): Movement optimization, ~25ms operations
   ├─ v1.3 (2023-09): State management, ~20ms operations
   ├─ v1.4 (2023-12): Initial optimizations, ~10ms operations
   └─ v2.0 (2024-03): Zero-delay rewrite, ~1-3ms operations

**Key Performance Milestones**

* **v1.3**: Baseline performance measurement system
* **v1.4**: First optimization pass, 2x improvement
* **v2.0**: Complete architectural rewrite, 17x improvement
* **v2.1.3**: Async fix

This comprehensive performance analysis demonstrates the Makcu Python Library's evolution into a high-performance, gaming-ready solution suitable for the most demanding real-time applications.