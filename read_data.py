import h5py
import numpy as np

def read_trajectory_data(hdf5_path):
    """
    专用于读取UMI采集的轨迹数据（qpos和action）
    参数:
        hdf5_path: HDF5文件路径
    返回:
        dict: 包含轨迹数据和元信息的字典
    """
    try:
        with h5py.File(hdf5_path, 'r') as f:
            # 1. 验证文件结构
            required_datasets = ['/observations/qpos', '/action']
            for ds in required_datasets:
                if ds not in f:
                    raise ValueError(f"缺失必要数据集: {ds}")

            # 2. 提取轨迹数据
            trajectory_data = {
                'qpos': np.array(f['/observations/qpos']),  # 关节位置
                'action': np.array(f['/action']),          # 动作数据
                'timesteps': len(f['/observations/qpos']), # 时间步数
                'sim': f.attrs.get('sim', False)           # 是否仿真数据
            }

            # 3. 数据一致性检查
            if trajectory_data['qpos'].shape != trajectory_data['action'].shape:
                print(f"警告: qpos和action形状不匹配 {trajectory_data['qpos'].shape} vs {trajectory_data['action'].shape}")

            return trajectory_data

    except Exception as e:
        print(f"读取轨迹数据失败: {str(e)}")
        return None

def print_trajectory_info(data):
    """打印轨迹数据摘要"""
    if not data:
        return
    
    print("\n=== 轨迹数据摘要 ===")
    print(f"时间步数: {data['timesteps']}")
    print(f"数据类型: {'仿真' if data['sim'] else '真实'}")
    
    print("\nqpos (关节位置) 示例:")
    print(f"首条: {data['qpos'][0]}")
    print(f"中间: {data['qpos'][len(data['qpos'])//2]}")
    print(f"末尾: {data['qpos'][-1]}")
    
    print("\naction (动作) 示例:")
    print(f"首条: {data['action'][0]}")
    print(f"中间: {data['action'][len(data['action'])//2]}")
    print(f"末尾: {data['action'][-1]}")

def main(path):
    try:
        with h5py.File(path, 'r') as f:
            f['/observations/qpos']
    except Exception as e:
        print(f"read data failed: {str(e)}")
        return None

if __name__ == "__main__":
    # 示例文件路径（替换为实际路径）
    file_path = "/home/tars/FastUMI_Data/dataset/task1/episode_1.hdf5"
    
    # 读取数据
    traj_data = read_trajectory_data(file_path)
    
    # 打印信息
    if traj_data:
        print_trajectory_info(traj_data)
        
        # 获取完整数据示例
        qpos = traj_data['qpos']  # 形状: (timesteps, 7)
        actions = traj_data['action']  # 形状: (timesteps, 7)
        
        print(f"\n可用数据:")
        print(f"- qpos.shape: {qpos.shape} (X/Y/Z + 四元数)")
        print(f"- action.shape: {actions.shape}")