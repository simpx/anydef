# Contributing

We welcome contributions to the AnyDef project! Here's how you can help:

## Setting Up Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/anydef.git
   cd anydef
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the package in development mode:
   ```bash
   pip install -e .
   ```

4. Install development dependencies:
   ```bash
   pip install pytest black flake8
   ```

## Code Style

We follow PEP 8 guidelines for code style. Before submitting a pull request, please ensure your code adheres to these standards by running:

```bash
black .
flake8
```

## Testing

We use pytest for testing. To run the tests:

```bash
pytest
```

Please ensure all tests pass before submitting a pull request. If you're adding new functionality, please include appropriate tests.

## Submitting Changes

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes
4. Add tests if applicable
5. Ensure all tests pass
6. Commit your changes with a clear, descriptive commit message
7. Push to your fork
8. Submit a pull request

## Reporting Issues

If you find a bug or have a feature request, please open an issue on GitHub with as much detail as possible.