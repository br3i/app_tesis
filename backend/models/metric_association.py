from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# Tabla intermedia para relaciones entre Metric y otros modelos
class MetricAssociation(Base):
    __tablename__ = "metric_associations"  # Nombre de la tabla de asociación

    id = Column(Integer, primary_key=True)
    metric_id = Column(Integer, ForeignKey('metrics.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    document_id = Column(Integer, ForeignKey('documents.id'), nullable=True)
    notification_id = Column(Integer, ForeignKey('notifications.id'), nullable=True)
    code_id = Column(Integer, ForeignKey('codes.id'), nullable=True)
    feedback_id = Column(Integer, ForeignKey('feedbacks.id'), nullable=True)

    # Relaciones
    metric = relationship("Metric", back_populates="associations")
    user = relationship("User", back_populates="metric_associations")
    document = relationship("Document", back_populates="metric_associations")
    notification = relationship("Notification", back_populates="metric_associations")
    code = relationship("Code", back_populates="metric_associations")
    feedback = relationship("Feedback", back_populates="metric_associations")

    def __repr__(self):
        return f"<MetricAssociation(id={self.id}, metric_id={self.metric_id}, user_id={self.user_id}, document_id={self.document_id}, notification_id={self.notification_id}, code_id={self.code_id}, feedback_id={self.feedback_id})>"
