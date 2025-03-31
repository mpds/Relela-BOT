import os
import subprocess
import pynvml as nvidia_smi


# Module for loading Nvidia SMI
def get_gpu_status():
    try:
        nvidia_smi.nvmlInit()
        deviceCount = nvidia_smi.nvmlDeviceGetCount()
        gpu_info = []
        
        for i in range(deviceCount):
            handle = nvidia_smi.nvmlDeviceGetHandleByIndex(i)
            info = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)
            device_name = nvidia_smi.nvmlDeviceGetName(handle)
            
            gpu_info.append(
                f"Device {i}: {device_name}, "
                f"Memory: ({100 * info.free / info.total:.2f}% free): "
                f"{info.total/(1024**3):.2f} GB (total), "
                f"{info.free/(1024**3):.2f} GB (free), "
                f"{info.used/(1024**3):.2f} GB (used)"
            )
            
        return gpu_info
        
    except Exception as e:
        return [f"Error getting GPU status: {str(e)}"]
    finally:
        try:
            nvidia_smi.nvmlShutdown()
        except:
            pass


# Module for getting running status
def get_running_status():
    cmd = "ps -up `nvidia-smi -q -x | grep pid | sed -e 's/<pid>//g' -e 's/<\/pid>//g' -e 's/^[[:space:]]*//'`"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else None
