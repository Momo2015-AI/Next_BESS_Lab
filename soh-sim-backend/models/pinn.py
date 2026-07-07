from . import db, _utcnow
class PinnModelWeights(db.Model):
    """PINN 神经网络权重存储模型"""

    __tablename__ = "pinn_model_weights"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_name = db.Column(db.String(255), nullable=False)
    weights = db.Column(db.LargeBinary, nullable=False)
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    def __repr__(self):
        return f"<PinnModelWeights {self.model_name}>"


