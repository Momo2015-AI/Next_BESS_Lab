"""
SOH/RTE 模型训练与预测工具

功能：
1. 数据导入：从 CSV 导入实际项目数据
2. 参数校准：贝叶斯优化自动调整模型参数
3. 模型预测：输入工况，输出准确的 SOH/RTE
4. 模型管理：保存/加载训练好的模型

使用示例：
    python train_model.py --mode train --data training_data.csv --output calibrated_model.json
    python train_model.py --mode predict --model calibrated_model.json --input工况参数.json
"""

import argparse
import json
import os
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


# ==================== Arrhenius 模型 ====================

class ArrheniusSOHModel:
    """阿伦尼乌斯电池衰减模型"""

    def __init__(self, params: Dict = None):
        """初始化模型参数"""
        self.R = 8.314  # 理想气体常数

        # 默认参数
        self.params = {
            'A_cal': 0.02,
            'Ea_cal': 20000,
            'alpha': 0.8,
            'A_cyc': 0.001,
            'Ea_cyc': 15000,
            'beta': 0.5,
            'gamma': 1.5,
            'delta': 0.2,
            'degradation_rate': 0.1
        }

        if params:
            self.params.update(params)

    def calculate_calendar_aging(self, years: float, temperature: float) -> float:
        """计算日历老化"""
        T = temperature + 273.15  # 转换为开尔文温度
        rate = self.params['A_cal'] * np.exp(-self.params['Ea_cal'] / (self.R * T))
        Q_cal = rate * (years ** self.params['alpha'])
        return Q_cal

    def calculate_cycle_aging(self, years: float, temperature: float,
                             cycles_per_day: float, dod: float, c_rate: float) -> float:
        """计算循环老化"""
        T = temperature + 273.15  # 转换为开尔文温度

        # 计算影响因子
        DOD_factor = dod ** self.params['gamma']
        C_rate_factor = 1 + self.params['delta'] * (c_rate - 0.5)

        rate = self.params['A_cyc'] * np.exp(-self.params['Ea_cyc'] / (self.R * T))
        N = years * cycles_per_day * 365  # 计算总循环次数
        Q_cyc = rate * (N ** self.params['beta']) * DOD_factor * C_rate_factor

        return Q_cyc

    def calculate_soh(self, years: float, temperature: float,
                     cycles_per_day: float, dod: float, c_rate: float) -> float:
        """计算SOH衰减"""
        # 计算日历老化
        Q_cal = self.calculate_calendar_aging(years, temperature)

        # 计算循环老化
        Q_cyc = self.calculate_cycle_aging(years, temperature, cycles_per_day, dod, c_rate)

        # 计算总衰减
        total_loss = Q_cal + Q_cyc
        soh = 1 - total_loss

        return max(soh, 0)  # 确保 SOH 不为负

    def calculate_rte(self, soh: float, rte_initial: float) -> float:
        """计算RTE衰减"""
        soh_loss = 1 - soh
        rte = rte_initial * (1 - self.params['degradation_rate'] * soh_loss)
        return max(rte, 0)

    def predict(self, X: Dict[str, float]) -> Dict[str, float]:
        """
        给定工况，预测 SOH/RTE

        Args:
            X: 工况参数字典，包含：
                - years: 运行年数
                - temperature: 温度 (°C)
                - cycles_per_day: 每日循环次数
                - dod: 放电深度 (0-1)
                - c_rate: 充放电倍率 (C)
                - rte_initial: 初始RTE (%)

        Returns:
            预测结果字典，包含：
                - soh: SOH (%)
                - rte: RTE (%)
        """
        soh = self.calculate_soh(
            years=X.get('years', 1),
            temperature=X.get('temperature', 25),
            cycles_per_day=X.get('cycles_per_day', 1),
            dod=X.get('dod', 0.8),
            c_rate=X.get('c_rate', 0.5)
        )

        rte = self.calculate_rte(soh, X.get('rte_initial', 97.03))

        return {
            'soh': round(soh * 100, 2),
            'rte': round(rte, 2)
        }

    def predict_soh_batch(self, years: np.ndarray, temperature: np.ndarray,
                         cycles_per_day: np.ndarray, dod: np.ndarray,
                         c_rate: np.ndarray) -> np.ndarray:
        """
        向量化批量预测 SOH（用于训练和批量预测，性能比循环调用高 1-2 个数量级）

        Args:
            years/temperature/cycles_per_day/dod/c_rate: 一维 ndarray，长度相同

        Returns:
            SOH 一维 ndarray（0-1 范围）
        """
        T = temperature + 273.15

        # 日历老化（向量化）
        Q_cal = self.params['A_cal'] * np.exp(-self.params['Ea_cal'] / (self.R * T)) \
                * np.power(years, self.params['alpha'])

        # 循环老化（向量化）
        DOD_factor = np.power(dod, self.params['gamma'])
        C_rate_factor = 1 + self.params['delta'] * (c_rate - 0.5)
        N = years * cycles_per_day * 365
        Q_cyc = self.params['A_cyc'] * np.exp(-self.params['Ea_cyc'] / (self.R * T)) \
                * np.power(N, self.params['beta']) * DOD_factor * C_rate_factor

        soh = 1 - (Q_cal + Q_cyc)
        return np.maximum(soh, 0)


# ==================== 参数校准器 ====================

try:
    import optuna
    OPTUNA_AVAILABLE = True
except ImportError:
    OPTUNA_AVAILABLE = False
    print("警告: Optuna 未安装，参数校准功能将不可用。安装命令: pip install optuna")


class ModelCalibrator:
    """模型参数校准器"""

    def __init__(self, model: ArrheniusSOHModel, data: pd.DataFrame):
        """
        初始化校准器

        Args:
            model: ArrheniusSOHModel 实例
            data: 训练数据 DataFrame
        """
        self.model = model
        self.data = data
        self.best_params = None
        self.best_rmse = float('inf')

    def prepare_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        准备训练数据（向量化提取，无循环）

        Returns:
            (X, y): 特征矩阵 (N, 5) 和标签 (N,)
        """
        # 直接列切片，避免 iterrows 性能损耗
        years = (self.data['operating_days'] / 365).to_numpy(dtype=float)
        temperature = self.data['temperature'].to_numpy(dtype=float)
        cycles_per_day = self.data['cycles_per_day'].to_numpy(dtype=float)
        dod = self.data['dod'].to_numpy(dtype=float)
        c_rate = self.data['c_rate'].to_numpy(dtype=float)
        labels = (self.data['measured_soh'] / 100).to_numpy(dtype=float)

        X = np.column_stack([years, temperature, cycles_per_day, dod, c_rate])
        return X, labels

    def calculate_rmse(self, params: Dict) -> float:
        """
        计算给定参数的 RMSE（向量化批量预测，无循环）

        Args:
            params: 模型参数

        Returns:
            RMSE 值
        """
        temp_model = ArrheniusSOHModel(params)
        X, labels = self.prepare_data()

        # 向量化批量预测
        predictions = temp_model.predict_soh_batch(
            years=X[:, 0], temperature=X[:, 1],
            cycles_per_day=X[:, 2], dod=X[:, 3], c_rate=X[:, 4]
        )

        return float(np.sqrt(np.mean((predictions - labels) ** 2)))

    def calibrate(self, n_trials: int = 500, verbose: bool = True) -> Dict:
        """
        使用贝叶斯优化校准参数

        Args:
            n_trials: 优化尝试次数
            verbose: 是否输出详细信息

        Returns:
            最优参数字典
        """
        if not OPTUNA_AVAILABLE:
            print("错误: Optuna 未安装，无法进行参数校准")
            return self.model.params

        features, labels = self.prepare_data()
        print(f"训练数据准备完成: {len(features)} 个数据点")

        def objective(trial):
            """目标函数"""
            params = {
                'A_cal': trial.suggest_float('A_cal', 0.001, 0.1),
                'Ea_cal': trial.suggest_float('Ea_cal', 10000, 50000),
                'alpha': trial.suggest_float('alpha', 0.5, 1.2),
                'A_cyc': trial.suggest_float('A_cyc', 0.0001, 0.01),
                'Ea_cyc': trial.suggest_float('Ea_cyc', 10000, 30000),
                'beta': trial.suggest_float('beta', 0.3, 0.8),
                'gamma': trial.suggest_float('gamma', 1.0, 2.0),
                'delta': trial.suggest_float('delta', 0.1, 0.5),
            }
            return self.calculate_rmse(params)

        print(f"\n开始贝叶斯优化 ({n_trials} 次尝试)...")
        study = optuna.create_study(direction='minimize')
        study.optimize(objective, n_trials=n_trials, show_progress_bar=verbose)

        self.best_params = study.best_params
        self.best_rmse = study.best_value

        print(f"\n✓ 参数校准完成!")
        print(f"  最优 RMSE: {self.best_rmse * 100:.3f}%")
        print(f"  最优参数:")
        for key, value in self.best_params.items():
            print(f"    {key}: {value:.6f}")

        return self.best_params


# ==================== 模型管理 ====================

class ModelManager:
    """模型管理器"""

    @staticmethod
    def save_model(model: ArrheniusSOHModel, filepath: str, metadata: Dict = None):
        """
        保存模型到文件

        Args:
            model: ArrheniusSOHModel 实例
            filepath: 保存路径
            metadata: 额外元数据（如训练数据信息、RMSE 等）
        """
        data = {
            'model_params': model.params,
            'metadata': metadata or {},
            'saved_at': datetime.now().isoformat()
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"✓ 模型已保存到: {filepath}")

    @staticmethod
    def load_model(filepath: str) -> ArrheniusSOHModel:
        """
        从文件加载模型

        Args:
            filepath: 模型文件路径

        Returns:
            ArrheniusSOHModel 实例
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        model = ArrheniusSOHModel(data['model_params'])

        if 'metadata' in data:
            print(f"模型元数据:")
            for key, value in data['metadata'].items():
                print(f"  {key}: {value}")
        print(f"保存时间: {data.get('saved_at', '未知')}")

        return model


# ==================== 主程序 ====================

def validate_data(df: pd.DataFrame) -> bool:
    """
    验证数据格式

    Args:
        df: 数据 DataFrame

    Returns:
        是否有效
    """
    required_columns = [
        'temperature', 'cycles_per_day', 'dod', 'c_rate',
        'operating_days', 'measured_soh'
    ]

    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        print(f"错误: 缺少必要的列: {', '.join(missing_cols)}")
        return False

    # 检查数据范围
    if df['measured_soh'].max() > 100 or df['measured_soh'].min() < 0:
        print("警告: SOH 值应在 0-100 范围内")

    return True


def train_mode(args):
    """训练模式"""
    print("=" * 60)
    print("SOH/RTE 模型训练模式")
    print("=" * 60)

    # 检查数据文件
    if not os.path.exists(args.data):
        print(f"错误: 数据文件不存在: {args.data}")
        return

    # 导入数据
    print(f"\n导入数据: {args.data}")
    try:
        data = pd.read_csv(args.data)
        print(f"✓ 数据导入成功: {len(data)} 行, {len(data.columns)} 列")
    except Exception as e:
        print(f"错误: 数据导入失败: {e}")
        return

    # 验证数据
    print("\n验证数据格式...")
    if not validate_data(data):
        return
    print("✓ 数据格式验证通过")

    # 显示数据统计
    print("\n数据统计:")
    print(data.describe())

    # 创建模型
    print("\n初始化模型...")
    model = ArrheniusSOHModel()
    print(f"初始参数:")
    for key, value in model.params.items():
        print(f"  {key}: {value}")

    # 初始 RMSE
    calibrator = ModelCalibrator(model, data)
    initial_rmse = calibrator.calculate_rmse(model.params)
    print(f"\n初始 RMSE: {initial_rmse * 100:.3f}%")

    # 参数校准
    print("\n开始参数校准...")
    calibrated_params = calibrator.calibrate(n_trials=args.trials, verbose=True)

    # 更新模型
    model = ArrheniusSOHModel(calibrated_params)

    # 评估最终效果
    print("\n评估最终效果...")
    features, labels = calibrator.prepare_data()
    predictions = model.predict_soh_batch(
        years=features[:, 0], temperature=features[:, 1],
        cycles_per_day=features[:, 2], dod=features[:, 3], c_rate=features[:, 4]
    ) * 100

    final_rmse = float(np.sqrt(np.mean((predictions - labels * 100) ** 2)))
    max_error = float(np.max(np.abs(predictions - labels * 100)))
    print(f"最终 RMSE: {final_rmse:.3f}%")
    print(f"最大误差: {max_error:.3f}%")

    # 保存模型
    output_path = args.output or 'calibrated_model.json'
    metadata = {
        'training_data': args.data,
        'data_points': len(data),
        'initial_rmse': round(initial_rmse * 100, 3),
        'final_rmse': round(final_rmse, 3),
        'max_error': round(max_error, 3),
        'trials': args.trials
    }
    ModelManager.save_model(model, output_path, metadata)

    print("\n" + "=" * 60)
    print("训练完成!")
    print("=" * 60)


def predict_mode(args):
    """预测模式"""
    print("=" * 60)
    print("SOH/RTE 模型预测模式")
    print("=" * 60)

    # 检查模型文件
    if not os.path.exists(args.model):
        print(f"错误: 模型文件不存在: {args.model}")
        return

    # 加载模型
    print(f"\n加载模型: {args.model}")
    model = ModelManager.load_model(args.model)
    print("✓ 模型加载成功")

    # 获取输入工况
    if args.input and os.path.exists(args.input):
        # 从文件读取
        with open(args.input, 'r', encoding='utf-8') as f:
            input_data = json.load(f)
    else:
        # 使用命令行参数
        input_data = {
            'years': args.years,
            'temperature': args.temperature,
            'cycles_per_day': args.cycles_per_day,
            'dod': args.dod,
            'c_rate': args.c_rate,
            'rte_initial': args.rte_initial
        }

    print("\n输入工况:")
    for key, value in input_data.items():
        print(f"  {key}: {value}")

    # 预测
    print("\n预测结果:")
    result = model.predict(input_data)
    for key, value in result.items():
        print(f"  {key}: {value}%")

    print("\n" + "=" * 60)


def batch_predict_mode(args):
    """批量预测模式"""
    print("=" * 60)
    print("SOH/RTE 模型批量预测模式")
    print("=" * 60)

    # 检查模型文件
    if not os.path.exists(args.model):
        print(f"错误: 模型文件不存在: {args.model}")
        return

    # 加载模型
    print(f"\n加载模型: {args.model}")
    model = ModelManager.load_model(args.model)
    print("✓ 模型加载成功")

    # 检查输入文件
    if not os.path.exists(args.input):
        print(f"错误: 输入文件不存在: {args.input}")
        return

    # 导入输入数据
    print(f"\n导入输入数据: {args.input}")
    try:
        input_data = pd.read_csv(args.input)
        print(f"✓ 数据导入成功: {len(input_data)} 行")
    except Exception as e:
        print(f"错误: 数据导入失败: {e}")
        return

    # 批量预测（向量化，无 iterrows）
    print("\n开始批量预测...")
    rte_initial = input_data['rte_initial'] if 'rte_initial' in input_data.columns else 97.03
    soh_arr = model.predict_soh_batch(
        years=(input_data['operating_days'] / 365).to_numpy(dtype=float),
        temperature=input_data['temperature'].to_numpy(dtype=float),
        cycles_per_day=input_data['cycles_per_day'].to_numpy(dtype=float),
        dod=input_data['dod'].to_numpy(dtype=float),
        c_rate=input_data['c_rate'].to_numpy(dtype=float),
    )
    rte_arr = rte_initial * (1 - model.params['degradation_rate'] * (1 - soh_arr))
    rte_arr = np.maximum(rte_arr, 0)

    input_data = input_data.copy()
    input_data['predicted_soh'] = np.round(soh_arr * 100, 2)
    input_data['predicted_rte'] = np.round(rte_arr, 2)

    # 保存结果
    output_path = args.output or 'prediction_results.csv'
    input_data.to_csv(output_path, index=False, encoding='utf-8')
    print(f"✓ 预测结果已保存到: {output_path}")

    print("\n预测统计:")
    print(f"  平均预测 SOH: {input_data['predicted_soh'].mean():.2f}%")
    print(f"  平均预测 RTE: {input_data['predicted_rte'].mean():.2f}%")

    print("\n" + "=" * 60)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='SOH/RTE 模型训练与预测工具')
    subparsers = parser.add_subparsers(dest='mode', help='运行模式')

    # 训练模式
    train_parser = subparsers.add_parser('train', help='训练模型')
    train_parser.add_argument('--data', required=True, help='训练数据 CSV 文件路径')
    train_parser.add_argument('--output', '-o', help='输出模型文件路径 (默认: calibrated_model.json)')
    train_parser.add_argument('--trials', '-t', type=int, default=500, help='优化尝试次数 (默认: 500)')

    # 预测模式
    predict_parser = subparsers.add_parser('predict', help='预测 SOH/RTE')
    predict_parser.add_argument('--model', required=True, help='模型文件路径')
    predict_parser.add_argument('--input', '-i', help='输入工况 JSON 文件路径')
    predict_parser.add_argument('--years', type=float, default=1, help='运行年数 (默认: 1)')
    predict_parser.add_argument('--temperature', type=float, default=25, help='温度 °C (默认: 25)')
    predict_parser.add_argument('--cycles_per_day', type=float, default=1, help='每日循环次数 (默认: 1)')
    predict_parser.add_argument('--dod', type=float, default=0.8, help='放电深度 (默认: 0.8)')
    predict_parser.add_argument('--c_rate', type=float, default=0.5, help='充放电倍率 C (默认: 0.5)')
    predict_parser.add_argument('--rte_initial', type=float, default=97.03, help='初始 RTE % (默认: 97.03)')

    # 批量预测模式
    batch_parser = subparsers.add_parser('batch_predict', help='批量预测 SOH/RTE')
    batch_parser.add_argument('--model', required=True, help='模型文件路径')
    batch_parser.add_argument('--input', '-i', required=True, help='输入数据 CSV 文件路径')
    batch_parser.add_argument('--output', '-o', help='输出结果文件路径 (默认: prediction_results.csv)')

    args = parser.parse_args()

    if args.mode == 'train':
        train_mode(args)
    elif args.mode == 'predict':
        predict_mode(args)
    elif args.mode == 'batch_predict':
        batch_predict_mode(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()