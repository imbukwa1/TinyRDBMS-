TinyRDBMS: A Custom Relational Database System
TinyRDBMS is a lightweight, simplified Relational Database Management System (RDBMS) built from scratch in Python. It features a custom SQL parser, a JSON-based storage engine, and a demonstration web application built with Flask.
Features
Custom SQL Parser: Uses regular expressions to interpret standard SQL commands.

Persistent Storage: Data is serialized to a local .json file, ensuring data persists across sessions.

CRUD Operations: Full support for Creating tables, Reading data, Updating/Inserting, and Deleting.

Primary Key Constraints: Prevents duplicate entries on designated unique columns.

Relational Joins: Implements a Nested Loop Join algorithm to combine data from multiple tables.

Interactive REPL: A built-in shell for real-time database interaction.

Web Integration: A Flask-based interface demonstrating the engine's integration into a full-stack environment.

Architecture
TinyRDBMS is built using a modular 4-layer architecture:

Interface Layer: The REPL (rdbms.py) and the Web API (app.py).

Parser Layer: A regex-driven logic that tokenizes and interprets SQL strings.

Execution Engine: The "brain" of the DB that handles logic for filtering, joining, and constraint checking.

Storage Manager: Handles file I/O operations to save and load the state of the tables.
