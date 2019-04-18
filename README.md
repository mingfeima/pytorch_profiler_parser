# PyTorch Profiler Parser
parser script to process pytorch autograd profiler result, convert json file to excel.

## Performance Profiling on PyTorch
1. Enable profiler in user code
```python
# To enable GPU profiling, provide use_cuda=True for profiler()
withtorch.autograd.profiler.profile() as prof:
    func_()
prof.export_chrome_trace(“result.json")
```
2. Convert the output json record file to a more human friendly excel
```python
python process.py --input result.json --output result.xlsx
```
3. Annotation
PyTorch autograd profiler records each operator executed by autograd engine, the profiler overcounts nested function calls from both engine side and underlying ATen library side, so total summation will exceed actual total runtime.
Columns in the output excel:
- `name`: kernel name from PyTorch ATen library (the native C++ Tensor library)
- `ts`  : time stamp
- `dur` : execution sum time in us
- `tid` : 0 for CPU forward path; for CPU backward path; N+2 for GPU N (tid2 refers to GPU 0)
- `call_num` : iteration count
Sort by `dur` column, then you will get hotspot kernels.
