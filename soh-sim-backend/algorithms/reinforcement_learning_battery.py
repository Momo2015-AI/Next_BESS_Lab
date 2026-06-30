"""
强化学习算法 - 用于优化储能系统充放电策略
"""
import numpy as np
import random
from collections import deque
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import json
import os

class DQNAgent:
    """
    深度Q网络代理，用于储能系统充放电策略优化
    """
    def __init__(self, state_size, action_size, learning_rate=0.001):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.epsilon = 1.0  # 探索率
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.learning_rate = learning_rate
        self.model = self._build_model()
        self.target_model = self._build_model()
        self.update_target_model()
        
    def _build_model(self):
        """
        构建神经网络模型
        """
        model = keras.Sequential([
            layers.Dense(24, input_dim=self.state_size, activation='relu'),
            layers.Dense(24, activation='relu'),
            layers.Dense(self.action_size, activation='linear')
        ])
        model.compile(loss='mse', optimizer=keras.optimizers.Adam(lr=self.learning_rate))
        return model
    
    def update_target_model(self):
        """
        更新目标模型
        """
        self.target_model.set_weights(self.model.get_weights())
    
    def remember(self, state, action, reward, next_state, done):
        """
        存储经验
        """
        self.memory.append((state, action, reward, next_state, done))
    
    def act(self, state):
        """
        根据当前状态选择动作
        """
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])
    
    def replay(self, batch_size=32):
        """
        经验回放
        """
        if len(self.memory) < batch_size:
            return
        
        batch = random.sample(self.memory, batch_size)
        states = np.array([e[0] for e in batch])
        states = states.reshape((batch_size, self.state_size))
        
        targets = self.model.predict(states)
        
        for i, (state, action, reward, next_state, done) in enumerate(batch):
            target = reward
            if not done:
                target = reward + 0.95 * np.amax(self.target_model.predict(next_state)[0])
            targets[i][action] = target
            
        self.model.fit(states, targets, epochs=1, verbose=0)
        
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


class BatteryOptimizationEnvironment:
    """
    储能系统优化环境
    """
    def __init__(self, initial_soc=0.5, capacity_kwh=100, max_charge_kw=50, max_discharge_kw=50):
        self.initial_soc = initial_soc
        self.capacity_kwh = capacity_kwh
        self.max_charge_kw = max_charge_kw
        self.max_discharge_kw = max_discharge_kw
        self.reset()
        
    def reset(self):
        """
        重置环境
        """
        self.soc = self.initial_soc  # State of Charge
        self.current_step = 0
        self.total_reward = 0
        return self._get_state()
    
    def _get_state(self):
        """
        获取当前状态
        """
        # 状态包括：当前SOC、当前电价、时间信息等
        return np.array([[self.soc, random.uniform(0.1, 1.0), self.current_step % 24 / 24]])
    
    def step(self, action):
        """
        执行动
        """
        # 动作空间：0-充电，1-放电，2-保持
        power_actions = [-self.max_charge_kw, self.max_discharge_kw, 0]  # kW
        power = power_actions[action]
        
        # 计算SOC变化
        energy_change = power * (1/60)  # 偏设1分钟的时间步长
        new_soc = self.soc + energy_change / self.capacity_kwh
        
        # 确保SOC在合理范围内
        new_soc = np.clip(new_soc, 0.0, 1.0)
        
        # 计算奖励 - 基于电价差异和SOC管理
        current_price = random.uniform(0.1, 1.0)  # 当前电价
        reward = 0
        
        if action == 0:  # 充电
            if current_price < 0.5:  # 低电价时充电
                reward = 1
            else:
                reward = -1
        elif action == 1:  # 放电
            if current_price > 0.7:  # 高电价时放电
                reward = 2
            else:
                reward = -1
        else:  # 保持
            if 0.3 <= self.soc <= 0.7:  # SOC在合理范围内
                reward = 0.5
            else:
                reward = -0.5
        
        # 更新状态
        self.soc = new_soc
        self.current_step += 1
        done = self.current_step >= 1440  # 24小时内的分钟数
        
        return self._get_state(), reward, done, {}


def train_battery_optimization_agent(episodes=1000):
    """
    训练储能系统优化代理
    """
    env = BatteryOptimizationEnvironment()
    state_size = env.reset().shape[1]
    action_size = 3  # 充电、放电、保持
    
    agent = DQNAgent(state_size, action_size)
    batch_size = 32
    
    scores = []
    
    for e in range(episodes):
        state = env.reset()
        state = np.reshape(state, [1, state_size])
        total_reward = 0
        
        for time in range(500):  # 每个episode最多500步
            action = agent.act(state)
            next_state, reward, done, _ = env.step(action)
            next_state = np.reshape(next_state, [1, state_size])
            
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            total_reward += reward
            
            if done:
                agent.update_target_model()
                print(f"Episode: {e}/{episodes}, score: {time}, e: {agent.epsilon:.2}")
                scores.append(total_reward)
                break
                
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)
    
    return agent, scores


def save_agent(agent, filepath):
    """
    保存代理模型
    """
    agent.model.save(filepath)


def load_agent(filepath, state_size, action_size):
    """
    加载代理模型
    """
    agent = DQNAgent(state_size, action_size)
    agent.model = keras.models.load_model(filepath)
    return agent


if __name__ == "__main__":
    print("Training battery optimization agent...")
    trained_agent, scores = train_battery_optimization_agent(episodes=100)
    
    # 保存模型
    save_agent(trained_agent, "battery_optimization_model.h5")
    print("Model saved!")
    
    # 测试模型
    env = BatteryOptimizationEnvironment()
    state = env.reset()
    state_size = state.shape[1]
    
    test_agent = load_agent("battery_optimization_model.h5", state_size, 3)
    test_agent.epsilon = 0  # 不再探索，只利用
    
    state = np.reshape(state, [1, state_size])
    total_reward = 0
    
    for _ in range(100):
        action = test_agent.act(state)
        next_state, reward, done, _ = env.step(action)
        state = np.reshape(next_state, [1, state_size])
        total_reward += reward
        
        if done:
            break
    
    print(f"Test episode total reward: {total_reward}")