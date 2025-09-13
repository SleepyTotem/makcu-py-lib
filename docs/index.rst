.. Makcu Python Library documentation master file

Makcu Python Library Documentation
==================================

.. image:: https://img.shields.io/pypi/v/makcu.svg
   :target: https://pypi.org/project/makcu/
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/makcu.svg
   :target: https://pypi.org/project/makcu/
   :alt: Python Support

.. image:: https://img.shields.io/badge/license-GPL-blue.svg
   :alt: License

**Python library for Makcu device control**

The Makcu Python Library is a high-performance toolkit for controlling Makcu devices with **async/await support**, **zero-delay execution**, and **optimized performance**. Perfect for any application requiring precise mouse control.

What have I done in v2.0?
----------------

⚡ **Blazing Fast Performance**
   Commands execute in 1-3ms - up to **117x faster** than previous versions

🎮 **Gaming Optimized**  
   Built for 240Hz+ gaming with sub-3ms response times

🔄 **Smart Auto-Reconnection**
   Never lose connection - automatically reconnects if device is unplugged/loses connection

🐍 **Modern Python**
   Full async/await support alongside classic synchronous API

🎯 **Human-Like Interactions**
   Realistic clicking patterns and smooth movements, soon to include WindMouse integration

📊 **Parallel Operations**
   Execute multiple commands simultaneously

Quick Preview
------------

**Simple & Clean:**

.. code-block:: python

   from makcu import create_controller, MouseButton

   with create_controller() as makcu:
       makcu.click(MouseButton.LEFT)
       makcu.move(100, 50)
       makcu.scroll(-3)

**Async & Modern:**

.. code-block:: python

   import asyncio
   from makcu import create_async_controller, MouseButton

   async def main():
       async with await create_async_controller() as makcu:
           await asyncio.gather(
               makcu.move(100, 0),
               makcu.click(MouseButton.LEFT),
               makcu.scroll(-1)
           )

   asyncio.run(main())

**Gaming & Performance:**

.. code-block:: python

   # Human-like clicking for gaming
   makcu.click_human_like(
       MouseButton.LEFT, 
       count=5, 
       profile="gaming",
       jitter=3
   )

Table of Contents
----------------

.. toctree::
   :maxdepth: 2
   :caption: 🚀 Getting Started

   getting_started
   installation_guide

.. toctree::
   :maxdepth: 2
   :caption: 📖 User Guide

   basic_usage
   async_usage
   examples
   advanced_features

.. toctree::
   :maxdepth: 2
   :caption: 🛠️ Tools & Testing

   command_line
   debugging

.. toctree::
   :maxdepth: 2
   :caption: 📚 API Reference

   api/controller
   api/mouse
   api/connection
   api/enums

.. toctree::
   :maxdepth: 1
   :caption: 📈 Project Info

   changelog
   performance_benchmarks

Performance Comparison
=====================

**Version 2.0 delivers incredible performance improvements:**

.. list-table:: Test Performance (v1.3 → v2.0)
   :header-rows: 1
   :widths: 30 15 15 15 25

   * - Test Operation
     - v1.3 Time
     - v2.0 Time  
     - Speed Gain
     - Use Case
   * - Single Click
     - ~18ms
     - **1ms**
     - 18x faster
     - Gaming macros
   * - Mouse Movement
     - ~17ms
     - **2ms**
     - 8.5x faster
     - Smooth animations
   * - Batch Commands
     - ~350ms
     - **3ms**
     - 117x faster
     - Complex sequences
   * - Button States
     - ~18ms
     - **1ms**
     - 18x faster
     - Real-time monitoring
   * - Device Connection
     - ~100ms
     - **46ms**
     - 2.2x faster
     - App startup

**Gaming Performance Targets:**

* ✅ **144Hz Gaming** (7ms): Easily exceeded - most operations ≤ 3ms
* ✅ **240Hz Gaming** (4.2ms): Consistently met - operations ≤ 2ms  
* ⚡ **360Hz Gaming** (2.8ms): Achievable for single operations

Key Features Overview
====================

🖱️ **Complete Mouse Control**
   * All button types (left, right, middle, side buttons)
   * Precise movement with multiple interpolation methods
   * Smooth scrolling with variable speed
   * Press/release for sustained actions

🎭 **Human-Like Behavior**
   * Realistic timing variations
   * Natural mouse movements with jitter
   * Multiple behavior profiles (gaming, normal, variable)
   * Anti-detection features

🔒 **Advanced Locking System**
   * Lock individual mouse buttons
   * Lock X or Y axis movement
   * Query lock states instantly
   * Persistent across reconnections

📡 **Real-Time Monitoring**
   * Button press/release events
   * Connection status callbacks
   * Live device state tracking
   * Custom event handlers

🎯 **Gaming Features**
   * Sub-3ms command execution
   * Zero-delay architecture
   * Batch command processing
   * High-frequency operation support

Installation
===========

**Quick Install:**

.. code-block:: bash

   pip install makcu

**Requirements:**
* Python 3.8+ (3.10+ recommended)
* USB port for Makcu device
* Windows, macOS, or Linux

**Verify Installation:**

.. code-block:: bash

   python -m makcu --debug

Getting Help
===========

**Documentation:**
* 📖 **Start Here**: :doc:`getting_started` - Installation and first program
* 🔧 **Examples**: :doc:`examples` - Copy-paste code for common tasks  
* ⚡ **Async Guide**: :doc:`async_usage` - Modern async/await patterns
* 🎮 **Gaming**: :doc:`gaming_features` - Performance optimization tips

**Support Channels:**
* 🐛 `GitHub Issues <https://github.com/SleepyTotem/makcu-py-lib/issues>`_ - Bug reports
* 💬 `Discussions <https://github.com/SleepyTotem/makcu-py-lib/discussions>`_ - Questions & community
* 📦 `PyPI Package <https://pypi.org/project/makcu/>`_ - Official releases
* 📋 `Test Reports <https://github.com/SleepyTotem/makcu-py-lib>`_ - Latest test results

Common Use Cases
===============

**🎮 Gaming & Esports**
   * Macro creation and execution
   * Rapid-fire clicking
   * Precise aim assistance
   * Custom key bindings

**🤖 Automation & Testing**  
   * UI testing automation
   * Repetitive task automation
   * Screen interaction scripts
   * Quality assurance workflows

**♿ Accessibility Tools**
   * Alternative input methods
   * Assistive technology integration  
   * Custom interaction patterns
   * Adaptive interfaces

**🔬 Research & Development**
   * Human-computer interaction studies
   * Input device testing
   * Performance benchmarking
   * Prototype development

What Makes v2.0 Special?
========================

**Zero-Delay Architecture:** Eliminated all `sleep()` calls using intelligent command tracking and pre-computed operations.

**Gaming-First Design:** Built from the ground up for high-frequency gaming applications with frame-perfect timing.

**Modern Python:** Full async/await support alongside the classic synchronous API - use what works best for your project.

**Bulletproof Reliability:** Automatic reconnection, comprehensive error handling, and extensive test coverage.

**Developer Experience:** Rich debugging tools, clear error messages, and comprehensive documentation.

License & Contributing
=====================

**License:** GPL License © SleepyTotem

**Contributing:** We welcome contributions! See :doc:`contributing` for guidelines.

**Project Links:**
* `GitHub Repository <https://github.com/SleepyTotem/makcu-py-lib>`_
* `PyPI Package <https://pypi.org/project/makcu/>`_
* `Issue Tracker <https://github.com/SleepyTotem/makcu-py-lib/issues>`_

Quick Navigation
===============

**New Users:**
   👉 Start with :doc:`getting_started`

**Async Developers:**  
   👉 Jump to :doc:`async_usage`

**Gaming Applications:**
   👉 Check out :doc:`gaming_features`

**API Reference:**
   👉 Browse :doc:`api/controller`

**Having Issues?**
   👉 Visit :doc:`debugging` and :doc:`faq`

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`