from sqlalchemy.orm import Session
from models.metric import Metric
from models.metric_association import MetricAssociation

def save_metrics_docs(
    db: Session, 
    document_id: int, 
    execution_times: dict, 
    cpu_usage: dict, 
    memory_usage: dict
):
    print("\n\n +  ++  ++  ++  ++ + ++ +  [save_metrics]+ + + + + + ++ +  ++  +")
    # print(f"\db: {db}")
    # print(f"\ndocument_id: {document_id}")
    # print(f"\nexecution_times: {execution_times}")
    # print(f"\ncpu_usage: {cpu_usage}")
    # print(f"\nmemory_usage: {memory_usage}")
    # Crear el objeto de métricas
    metrics = Metric(
        total_time=execution_times.get('total_time', 0),
        save_time=execution_times.get('save_time', 0),
        process_time=execution_times.get('process_time', 0),
        cpu_initial=cpu_usage.get('initial', 0),
        cpu_save=cpu_usage.get('save', 0),
        cpu_process=cpu_usage.get('process', 0),
        cpu_final=cpu_usage.get('final', 0),
        memory_initial=memory_usage.get('initial', 0),
        memory_save=memory_usage.get('save', 0),
        memory_process=memory_usage.get('process', 0),
        memory_final=memory_usage.get('final', 0)
    )

    # Guardar las métricas en la base de datos
    db.add(metrics)
    db.commit()
    db.refresh(metrics)
    
    # Crear la asociación entre la métrica y el documento
    metric_association = MetricAssociation(
        metric_id=metrics.id,
        document_id=document_id
    )

    # Guardar la asociación en la base de datos
    db.add(metric_association)
    db.commit()

    # Opcionalmente, actualizar las métricas con las asociaciones
    db.refresh(metrics)
    db.refresh(metric_association)
    
    print(f"Metricas guardadas: {metric_association}")
    
    return metrics
