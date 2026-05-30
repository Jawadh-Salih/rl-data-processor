# RL Data Processor

A multiprocessing sensor data simulator and processor. A sensor worker generates a continuous stream of integer readings (0-100) with simulated missing and corrupted data, while a processor worker consumes the data in chunks and computes statistics.

## Prerequisites

- Python 3.6 or higher

No external dependencies are required. The project uses only Python standard library modules:
`datetime`, `multiprocessing`, `random`, `statistics`, `time`

## How to Run

```bash
python sensor_processor.py <mode> [--chunk-size N]
```

- `mode` — `i` for infinite mode, or a number for finite mode
- `--chunk-size` — Number of samples per chunk (default: 10% of samples in finite mode, 5 in infinite mode)

## Examples

Run in infinite mode with default chunk size (100). Runs until stopped with Ctrl+C:
```bash
python sensor_processor.py i
```

Run in infinite mode with a chunk size of 10:
```bash
python sensor_processor.py i --chunk-size 10
```

Run in finite mode with 50 samples (chunk size defaults to 10% = 5):
```bash
python sensor_processor.py 50
```

Run in finite mode with 100 samples and chunk size of 10:
```bash
python sensor_processor.py 100 --chunk-size 10
```

Run in finite mode with 20 samples and chunk size of 20 (1 chunk):
```bash
python sensor_processor.py 20 --chunk-size 20
```

Invalid — will raise a `ValueError` because 10 is not a multiple of 3:
```bash
python sensor_processor.py 10 --chunk-size 3
```

## Note on Execution Time

The sensing interval is set to 1 second per sample. This means each sample takes 1 second to generate. For example, running `python sensor_processor.py 100` will take approximately 100 seconds (~1.5 minutes) to complete. Keep this in mind when choosing large sample counts for testing.

## Validation (Finite Mode)

In finite mode, the number of samples must:
- Be greater than or equal to `chunk-size`
- Be a multiple of `chunk-size`

Otherwise, the program will raise a `ValueError` at startup.

## Output

For each processed chunk, the program prints:
- **Average** of valid readings in the chunk
- **Maximum** and **Minimum** valid readings
- **Standard Deviation** of valid readings
- **Missing data** count (simulated at 5% probability)
- **Corrupted data** count (simulated at 10% probability, values > 100)
