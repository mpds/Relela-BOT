import os

import nvidia_smi


# Module for loading Nvidia SMI
def get_gpu_status():
    nvidia_smi.nvmlInit()
    deviceCount = nvidia_smi.nvmlDeviceGetCount()
    gpu_info = []

    for i in range(deviceCount):
        handle = nvidia_smi.nvmlDeviceGetHandleByIndex(i)
        info = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)
        gpu_info.append(
            f"Device {i}: {nvidia_smi.nvmlDeviceGetName(handle).decode('utf-8')}, "
            f"Memory: ({100 * info.free / info.total:.2f}% free): "
            f"{round(info.total / (1024**3), 3)} GB (total), "
            f"{round(info.free / (1024**3), 3)} GB (free), "
            f"{round(info.used / (1024**3), 3)} GB (used)"
        )

    nvidia_smi.nvmlShutdown()
    return gpu_info


# Module for getting running status
def get_running_status():
    run_info = os.popen(
        "ps -up `nvidia-smi -q -x | grep pid | sed -e 's/<pid>//g' -e 's/<\/pid>//g' -e 's/^[[:space:]]*//'`"
    ).read()
    return run_info
