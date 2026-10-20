def calculate_health(cpu_info, memory_info, gpu_info, storage_info, system_info):
    score = 100
    attention_items = []

    # CPU load check
    if cpu_info["overall_load"] > 80:
        score -= 10
        attention_items.append(f"Processor load is high ({cpu_info['overall_load']}%), check background tasks.")

    # Memory check
    if memory_info["percent"] > 85:
        score -= 15
        attention_items.append(f"Memory is {memory_info['percent']}% full. Consider closing unused tabs or applications.")
    elif memory_info["percent"] > 70:
        score -= 5
        attention_items.append(f"Memory usage is moderate ({memory_info['percent']}%).")

    # Storage check
    if storage_info["percent"] > 85:
        score -= 15
        attention_items.append(f"Primary drive {storage_info['root_mount']} is {storage_info['percent']}% full. Low free space affects performance.")
    elif storage_info["percent"] > 70:
        score -= 8
        attention_items.append(f"Primary drive {storage_info['root_mount']} is {storage_info['percent']}% full.")

    # Temp files check
    if storage_info["temp_cleanable_gb"] > 2.0:
        score -= 3
        attention_items.append(f"Around {storage_info['temp_cleanable_gb']} GB of temporary files can safely be cleared.")

    # Startup apps check
    if system_info["slow_startup_count"] >= 3:
        score -= 4
        attention_items.append(f"{system_info['startup_count']} startup apps detected ({system_info['slow_startup_count']} slow apps may delay boot).")

    # GPU check
    if gpu_info.get("is_discrete") and gpu_info.get("secondary"):
        attention_items.append("Hybrid GPU setup active. Ensure high-performance games utilize the dedicated GPU.")

    # Clamp score between 20 and 100
    score = max(min(score, 100), 20)

    # Health status label
    if score >= 80:
        label = "Health score, good"
    elif score >= 60:
        label = "Health score, fair"
    else:
        label = "Health score, needs attention"

    return {
        "score": score,
        "label": label,
        "attention_items": attention_items
    }
