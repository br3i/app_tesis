import json
from sqlalchemy.orm import Session
from models.metric import Metric
from models.metric_association import MetricAssociation

# {

#     "load_duration": 2079163600,
#     "prompt_eval_count": 1833,
#     "prompt_eval_duration": 81458000000,
#     "eval_count": 242,
#     "eval_duration": 20594000000,
#     "execution_time": 105.93487906455994,
#     "cpu_usage": {
#         "initial": 29.8,
#         "final": 38.8
#     },
#     "memory_usage": {
#         "initial": 67.4,
#         "final": 82.8
#     },
# }


def save_metrics_response(db: Session, metrics_data):
    print(f"[save_metrics_response] db {db}")
    print(f"[save_metrics_response] metrics_data {json.dumps(metrics_data, indent=4)}")

    # memory_initial = metrics_data["memory_usage"]["initial"]
    # memory_final = metrics_data["memory_usage"]["final"]

    # metrics = Metric(
    #     total_time=execution_times.get(
    #         "total_time", 0
    #     ),  #     "total_duration": 104325859600,
    #     save_time=execution_times.get("save_time", 0),
    #     process_time=execution_times.get("process_time", 0),
    #     cpu_initial=cpu_usage.get("initial", 0),
    #     cpu_save=cpu_usage.get("save", 0),
    #     cpu_process=cpu_usage.get("process", 0),
    #     cpu_final=cpu_usage.get("final", 0),
    #     memory_initial=memory_usage.get("initial", 0),
    #     memory_save=memory_usage.get("save", 0),
    #     memory_process=memory_usage.get("process", 0),
    #     memory_final=memory_usage.get("final", 0),
    # )
