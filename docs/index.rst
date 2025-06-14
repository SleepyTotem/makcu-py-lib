.. Makcu Python Library documentation master file

Welcome to Makcu Python Library Documentation
=============================================

.. image:: https://img.shields.io/pypi/v/makcu.svg
   :target: https://pypi.org/project/makcu/
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/makcu.svg
   :target: https://pypi.org/project/makcu/
   :alt: Python Support

.. image:: https://img.shields.io/badge/license-GPL-blue.svg
   :target: LICENSE
   :alt: License

Makcu Py Lib is a high-performance Python library for controlling Makcu devices — now with **async/await support**, **zero-delay command execution**, and **automatic reconnection**!

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   getting_started

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   async_usage
   examples
   advanced_features
   command_line
   testing

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/controller
   api/mouse
   api/connection
   api/errors
   api/enums

.. toctree::
   :maxdepth: 1
   :caption: Project Info

   changelog
   contributing

Key Features
------------

* ⚡ **Async/Await Support**: Full async API for modern Python applications
* 🎯 **Zero-Delay Commands**: No `sleep()` calls with intelligent command tracking
* 🔄 **Auto-Reconnection**: Automatic device reconnection on disconnect
* 📊 **Parallel Operations**: Execute multiple commands simultaneously
* 🔍 **Enhanced Debugging**: Better logging and error tracking
* 🎮 **Improved Performance**: 5–10x faster command execution

Quick Start
-----------

Installation
^^^^^^^^^^^^

.. code-block:: bash

   pip install makcu>=2.0.0

Basic Usage
^^^^^^^^^^^

.. code-block:: python

   from makcu import create_controller, MouseButton

   # Create and connect
   makcu = create_controller(debug=True)

   # Basic operations
   makcu.click(MouseButton.LEFT)
   makcu.move(100, 50)
   makcu.scroll(-1)

   # Clean disconnect
   makcu.disconnect()

Async Usage
^^^^^^^^^^^

.. code-block:: python

   import asyncio
   from makcu import create_async_controller, MouseButton

   async def main():
       async with await create_async_controller() as makcu:
           await makcu.click(MouseButton.LEFT)
           await makcu.move(100, 50)

   asyncio.run(main())

Test Performance Comparison (v1.3 → v2.0)
=========================================

Test Timings (v1.3 vs v1.4 vs v2.0)
----------------------------------

+--------------------------+--------+-------+--------+----------------------------+
| Test Name               | v1.3   | v1.4  | v2.0   | Improvement (v1.3 → v2.0) |
+==========================+========+=======+========+============================+
| connect_to_port         | ~100ms | ~55ms | **46ms** | ~2.2x faster             |
| press_and_release       | ~18ms  | ~9ms  | **1ms**  | ~18x faster              |
| firmware_version        | ~20ms  | ~9ms  | **1ms**  | ~20x faster              |
| middle_click            | ~18ms  | ~9ms  | **1ms**  | ~18x faster              |
| device_info             | ~25ms  | ~13ms | **6ms**  | ~4.1x faster             |
| port_connection         | ~20ms  | ~9ms  | **1ms**  | ~20x faster              |
| button_mask             | ~17ms  | ~8ms  | **1ms**  | ~17x faster              |
| get_button_states       | ~18ms  | ~9ms  | **1ms**  | ~18x faster              |
| lock_state              | ~33ms  | ~10ms | **1ms**  | ~33x faster              |
| makcu_behavior          | ~20ms  | ~10ms | **1ms**  | ~20x faster              |
| batch_commands          | ~350ms | ~90ms | **3ms**  | ~117x faster             |
| rapid_moves             | ~17ms  | ~8ms  | **2ms**  | ~8.5x faster             |
| button_performance      | ~18ms  | ~9ms  | **2ms**  | ~9x faster               |
| mixed_operations        | ~22ms  | ~10ms | **2ms**  | ~11x faster              |
+--------------------------+--------+-------+--------+----------------------------+

Based on the measured test suite, v2.0 is on average **~17x faster** than v1.3 across all core operations.

Support
-------

* **GitHub Issues**: `Report bugs <https://github.com/SleepyTotem/makcu-py-lib/issues>`_
* **Discussions**: `Ask questions <https://github.com/SleepyTotem/makcu-py-lib/discussions>`_
* **PyPI**: `Package page <https://pypi.org/project/makcu/>`_

License
-------

This project is licensed under the GPL License. See the LICENSE file for details.

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`