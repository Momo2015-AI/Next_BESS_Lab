# 储能电池健康状态（SOH）仿真系统

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Vue](https://img.shields.io/badge/Vue-3.0+-green.svg)](https://vuejs.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-red.svg)](https://flask.palletsprojects.com/)

## 项目概述

储能电池健康状态（SOH）仿真系统是一个基于阿伦尼乌斯衰减模型的专业储能系统寿命评估平台。该系统帮助工程师评估电池在不同工况下的寿命表现，支持参数配置、计算、可视化、多场景对比和结果导出。

### 核心功能

- **SOH衰减计算**：基于阿伦尼乌斯模型计算25年生命周期内的容量衰减
- **多场景对比**：支持同时计算多个场景，便于对比分析
- **可视化展示**：提供SOH曲线、RTE曲线、净可用能量趋势等多种图表
- **财务分析**：计算NPV、IRR、LCOE、ROI、DSCR等财务指标
- **工程计算**：计算场地面积、BOM清单、备品备件等
- **参数配置**：灵活的参数配置和产品库管理
- **结果导出**：支持CSV、PNG等格式导出

### 技术栈

#### 前端
- **框架**：Vue 3 + Vite
- **UI组件**：Element Plus
- **图表库**：ECharts
- **状态管理**：Pinia
- **路由**：Vue Router 4

#### 后端
- **框架**：Flask
- **数据处理**：NumPy
- **跨域支持**：Flask-CORS
- **API文档**：OpenAPI 3.0

---

## 快速开始

### 环境要求

- **Node.js**：≥ 18.0.0
- **npm**：≥ 9.0.0
- **Python**：≥ 3.10
- **pip**：最新版本

### 安装步骤

#### 1. 克隆项目

```bash
git clone https://github.com/your-org/soh-simulation.git
cd soh-simulation
```

#### 2. 安装前端依赖

```bash
cd soh-sim-frontend
npm install
```

#### 3. 安装后端依赖

```bash
cd ../soh-sim-backend
pip install -r requirements.txt
```

### 启动项目

#### 启动前端

```bash
cd soh-sim-frontend
npm run dev
```

前端将运行在 `http://localhost:5173`

#### 启动后端

```bash
cd soh-sim-backend
python app.py
```

后端将运行在 `http://localhost:5001`

---

## 项目结构

```
soh-simulation/
├── .monkeycode/                  # 项目规范
│   └── specs/
│       └── soh-simulation/
│           └── requirements.md   # 原始需求文档
├── docs/                         # 文档目录
│   ├── SRS.md                    # 软件需求规格说明书
│   ├── API-Specification.yaml    # API接口规范文档
│   ├── Algorithm-Design.md       # 算法设计文档
│   └── README.md                 # 项目文档（本文件）
├── soh-sim-frontend/             # 前端项目
│   ├── public/                   # 静态资源
│   ├── src/
│   │   ├── components/           # Vue组件
│   │   │   ├── DataInjection.vue         # 数据注入组件
│   │   │   ├── FinancialDashboard.vue    # 财务仪表盘组件
│   │   │   ├── FormulaLab.vue            # 公式实验室组件
│   │   │   ├── MatrixTable.vue           # 矩阵表格组件
│   │   │   ├── ParameterPanel.vue        # 参数配置面板组件
│   │   │   ├── ProductConfig.vue         # 产品配置组件
│   │   │   ├── RunningConditions.vue     # 运行条件配置组件
│   │   │   └── SohChart.vue              # SOH图表组件
│   │   ├── data/                 # 数据文件
│   │   │   └── products.json     # 产品数据
│   │   ├── App.vue               # 根组件
│   │   ├── main.js               # 入口文件
│   │   └── style.css             # 全局样式
│   ├── .gitignore
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── soh-sim-backend/              # 后端项目
    ├── app.py                    # Flask应用主文件
    └── requirements.txt          # Python依赖
```

---

## 使用指南

### 基本使用流程

1. **配置参数**
   - 在左侧参数配置面板中设置系统参数（能量、集装箱数量、PCS容量等）
   - 配置运行条件（温度、循环次数、DOD、倍率等）
   - 从产品库中选择电芯、集装箱、PCS等组件

2. **计算SOH**
   - 点击"计算"按钮，系统将基于阿伦尼乌斯模型计算25年SOH衰减曲线
   - 支持单场景计算和多场景对比

3. **查看结果**
   - 在中间图表区域查看SOH曲线、RTE曲线、净可用能量趋势
   - 在右侧数据表格中查看详细的25年数据矩阵
   - 支持手动编辑数据

4. **财务分析**
   - 在财务仪表盘中查看NPV、IRR、LCOE等财务指标
   - 查看现金流预测表
   - 进行敏感性分析

5. **导出结果**
   - 支持导出CSV格式数据
   - 支持导出PNG格式图表

### 高级功能

#### 数据注入
- 支持从CSV文件导入SOH、RTE、DOD等参数序列
- 支持手动编辑25年参数矩阵
- 适用于高级用户自定义衰减曲线

#### 公式实验室
- 查看阿伦尼乌斯模型的详细公式
- 动态调整算法参数
- 实时查看参数变化对结果的影响

#### 多场景对比
- 创建多个对比场景
- 在同一图表中对比不同工况下的SOH衰减
- 快速识别最优运行策略

---

## API文档

完整的API文档请参考：[API-Specification.yaml](./API-Specification.yaml)

### 主要接口

#### SOH计算接口
```
POST /api/soh/calculate
Content-Type: application/json

Request Body:
{
  "energy": 1000,
  "containers": 10,
  "pcs": 50,
  "duration": 2,
  "acEfficiency": 97.03,
  "dcEfficiency": 97.5,
  "selfDischarge": 0.05,
  "selfConsumption": 0.5,
  "standbyConsumption": 0.1,
  "temperature": 25,
  "cyclesPerDay": 1,
  "dod": 0.8,
  "cRate": 0.5
}

Response:
{
  "years": [0, 1, 2, ..., 25],
  "soh": [100, 98.5, 97.0, ..., 80.0],
  "rte": [97.03, 96.8, 96.5, ..., 94.0],
  "capacity": [1000, 985, 970, ..., 800],
  "netAvailable": [950, 935, 920, ..., 760]
}
```

#### 多场景计算接口
```
POST /api/soh/calculate-multi
Content-Type: application/json

Request Body:
[
  { /* 场景1参数 */ },
  { /* 场景2参数 */ }
]

Response:
[
  { /* 场景1结果 */ },
  { /* 场景2结果 */ }
]
```

#### 文件上传解析接口
```
POST /api/upload/extract
Content-Type: multipart/form-data

Request:
file: <文件>

Response:
{
  "params": { /* 提取的参数 */ },
  "source": "CSV",
  "confidence": 0.95
}
```

---

## 算法说明

系统基于阿伦尼乌斯衰减模型计算电池容量衰减：

### 日历老化
```
Q_cal(t) = A_cal × exp(-Ea_cal / (R × T)) × t^alpha
```

### 循环老化
```
Q_cyc(N) = A_cyc × exp(-Ea_cyc / (R × T)) × N^beta × DOD_factor × C_rate_factor
```

### 总衰减
```
SOH(t) = 1 - (Q_cal(t) + Q_cyc(N(t)))
```

详细的算法设计文档请参考：[Algorithm-Design.md](./Algorithm-Design.md)

---

## 开发指南

### 前端开发

#### 添加新组件
```bash
cd soh-sim-frontend/src/components
# 创建新组件文件
```

#### 添加新路由
```javascript
// src/router/index.js
import NewComponent from '@/components/NewComponent.vue'

const routes = [
  {
    path: '/new-component',
    name: 'NewComponent',
    component: NewComponent
  }
]
```

#### 状态管理
```javascript
// src/store/index.js
import { defineStore } from 'pinia'

export const useNewStore = defineStore('new', {
  state: () => ({
    data: null
  }),
  actions: {
    fetchData() {
      // 获取数据逻辑
    }
  }
})
```

### 后端开发

#### 添加新接口
```python
# app.py
@app.route('/api/new-endpoint', methods=['POST'])
def new_endpoint():
    data = request.get_json()
    # 处理逻辑
    return jsonify(result)
```

#### 添加新算法
```python
# algorithms/new_algorithm.py
class NewAlgorithm:
    def calculate(self, params):
        # 算法实现
        pass
```

---

## 测试

### 前端测试
```bash
cd soh-sim-frontend
npm run test
```

### 后端测试
```bash
cd soh-sim-backend
pytest
```

---

## 部署

### 前端部署
```bash
cd soh-sim-frontend
npm run build
# 将dist目录部署到Web服务器
```

### 后端部署
```bash
cd soh-sim-backend
# 使用gunicorn部署
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

### Docker部署
```bash
# 构建前端镜像
docker build -t soh-sim-frontend -f soh-sim-frontend/Dockerfile .

# 构建后端镜像
docker build -t soh-sim-backend -f soh-sim-backend/Dockerfile .

# 启动服务
docker-compose up -d
```

---

## 配置说明

### 前端配置
```javascript
// vite.config.js
export default {
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:5001',
        changeOrigin: true
      }
    }
  }
}
```

### 后端配置
```python
# app.py
UPLOAD_DIR = os.path.join(tempfile.gettempdir(), 'soh_uploads')
CORS_ORIGINS = ['http://localhost:5173']
```

---

## 常见问题

### Q1: 前端无法连接后端
**A**: 检查后端是否启动，端口是否正确，CORS配置是否正确。

### Q2: 计算结果不准确
**A**: 检查参数是否在合理范围内，算法参数是否正确配置。

### Q3: 图表不显示
**A**: 检查ECharts是否正确加载，数据格式是否正确。

### Q4: 导出功能不工作
**A**: 检查浏览器是否支持下载功能，文件权限是否正确。

---

## 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

### 代码规范
- 前端：遵循ESLint配置
- 后端：遵循PEP 8规范
- 提交信息：遵循Conventional Commits规范

---

## 许可证

本项目采用MIT许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 联系方式

- **项目主页**：https://github.com/your-org/soh-simulation
- **问题反馈**：https://github.com/your-org/soh-simulation/issues
- **邮箱**：dev@example.com

---

## 致谢

感谢所有为本项目做出贡献的开发者！

特别感谢以下开源项目：
- [Vue.js](https://vuejs.org/)
- [Flask](https://flask.palletsprojects.com/)
- [ECharts](https://echarts.apache.org/)
- [NumPy](https://numpy.org/)

---

## 更新日志

### v1.0.0 (2026-06-20)
- 初始版本发布
- 实现SOH衰减计算功能
- 实现多场景对比功能
- 实现财务分析功能
- 实现工程计算功能
- 实现可视化图表展示
- 实现结果导出功能

---

**文档结束**