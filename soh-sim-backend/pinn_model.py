import numpy as np
import tensorflow as tf
from scipy.integrate import solve_ivp

from database import PinnModelWeights, db


class PINN:
    def __init__(self, layers, learning_rate=0.001):
        self.layers = layers
        self.learning_rate = learning_rate
        self.model = self._build_model()

    def _build_model(self):
        model = tf.keras.Sequential()
        for i in range(len(self.layers) - 2):
            model.add(tf.keras.layers.Dense(self.layers[i + 1], activation="tanh", input_dim=self.layers[i]))
        model.add(tf.keras.layers.Dense(self.layers[-1], input_dim=self.layers[-2]))
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate), loss="mse")
        return model

    def train(self, X, y, epochs=1000):
        self.model.fit(X, y, epochs=epochs, verbose=1)

    def predict(self, X):
        return self.model.predict(X)

    def save_weights(self, model_name):
        weights = self.model.get_weights()
        serialized_weights = tf.io.serialize_tensor(weights)
        pinn_weights = PinnModelWeights(model_name=model_name, weights=serialized_weights.numpy())
        db.session.add(pinn_weights)
        db.session.commit()

    def load_weights(self, model_name):
        pinn_weights = PinnModelWeights.query.filter_by(model_name=model_name).first()
        if pinn_weights:
            serialized_weights = pinn_weights.weights
            weights = tf.io.parse_tensor(serialized_weights, out_type=tf.float32)
            self.model.set_weights(weights)
        else:
            raise ValueError(f"No weights found for model: {model_name}")


# 示例数据
X_train = np.random.rand(1000, 1)
y_train = np.sin(2 * np.pi * X_train)

# 创建 PINN 模型
pinn = PINN(layers=[1, 20, 20, 1])

# 训练模型
pinn.train(X_train, y_train)

# 保存权重
pinn.save_weights("example_model")

# 加载权重
pinn.load_weights("example_model")

# 预测
X_test = np.linspace(0, 1, 100).reshape(-1, 1)
y_pred = pinn.predict(X_test)

print("Predictions:", y_pred)
