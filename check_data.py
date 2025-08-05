import h5py
import os

def check_hdf5_file(file_path):
    """
    检查单个HDF5文件的数据结构
    """
    try:
        with h5py.File(file_path, 'r') as f:
            # 1. 读取根属性
            attrs = dict(f.attrs)  # 修复点：将属性保存到新变量而不是file_path
            print(f"\file: {os.path.basename(file_path)} attribution:")
            def print_structure(name, obj):
                if isinstance(obj, h5py.Dataset):
                    print(f"dataset: {name}, shape: {obj.shape}, type: {obj.dtype}")
                elif isinstance(obj, h5py.Group):
                    print(f"group: {name}")
            f.visititems(print_structure)  # 打印完整结构
            
    except Exception as e:
        print(f"process {file_path} wrong: {str(e)}")
        raise  # 重新抛出异常以便调试

def process_directory(directory_path):
    """
    遍历目录下的所有HDF5文件
    """
    if not os.path.isdir(directory_path):
        print(f"wrong: {directory_path} is not a valid directory")
        return
    
    file_count = 0
    
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(('.hdf5', '.h5')):
                file_path = os.path.join(root, file)
                print(f"\check file path: {file_path}")
                check_hdf5_file(file_path)
                file_count += 1
                
    print(f"\ncheck finished, totally found {file_count} HDF5 files")

if __name__ == "__main__":
    path = "/home/tars/FastUMI_Data/dataset/test_tcp_with_gripper"
    
    if os.path.isfile(path) and path.lower().endswith(('.hdf5', '.h5')):
        print("found single HDF5 file")
        check_hdf5_file(path)
    elif os.path.isdir(path):
        print("found multiple HDF5 files")
        process_directory(path)
    else:
        print(f"wrong!: {path} is not a valid file or directory")