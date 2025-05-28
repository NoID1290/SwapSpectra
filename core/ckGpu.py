import GPUtil



#GPU
def get_gpu_info():
    gpus = GPUtil.getGPUs()
    if not gpus:
        return None
    
    nvcV = any("NVIDIA" in gpu.name.upper() for gpu in GPUtil.getGPUs())
    print(f"NVIDIA GPU Hardware status: {nvcV}")

    gpu_info_list = []
    for gpu in gpus:
        gpu_info = {
            'id': gpu.id,
            'name': gpu.name,
            'load': gpu.load,
            'memoryTotal': gpu.memoryTotal,
            'memoryUsed': gpu.memoryUsed,
            'memoryFree': gpu.memoryFree,
            'temperature': gpu.temperature,
            'uuid': gpu.uuid
        }

        gpu_info_list.append(gpu_info)
    
    return gpu_info_list

gpu_info_list = get_gpu_info()

# Extract individual values
if gpu_info_list:
    first_gpu_info = gpu_info_list[0]  # Accessing information for the first GPU
    GPUid_ = first_gpu_info['id']
    GPUname = first_gpu_info['name']
    GPUload = first_gpu_info['load']
    GPUmemory_total = first_gpu_info['memoryTotal']
    GPUmemory_used = first_gpu_info['memoryUsed']
    GPUmemory_free = first_gpu_info['memoryFree']
    GPUtemperature = first_gpu_info['temperature']
    GPUuuid = first_gpu_info['uuid']
else:
    id_ = name = load = memory_total = memory_used = memory_free = temperature = uuid = None



    




