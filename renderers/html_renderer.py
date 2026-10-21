import json
import os
import webbrowser
from jinja2 import Template

def render_html_report(data, output_path="report.html", auto_open=False):
    template_file = os.path.join(os.path.dirname(__file__), "template.html")
    with open(template_file, "r", encoding="utf-8") as f:
        tmpl_content = f.read()

    template = Template(tmpl_content)

    # Calculate stroke-dashoffset for circular health gauge
    score = data["health"]["score"]
    target_offset = 100 - score

    # Generate smooth activity sparks for visual aesthetics
    cpu_load = data["cpu"]["overall_load"]
    ram_pct = data["memory"]["percent"]
    gpu_load = data["gpu"]["load_pct"]

    spark_cpu = [max(5, int(cpu_load * 0.7)), max(10, int(cpu_load * 1.2)), int(cpu_load), max(8, int(cpu_load * 0.9)), int(cpu_load)]
    spark_ram = [ram_pct, ram_pct, ram_pct, ram_pct, ram_pct]
    spark_gpu = [max(2, int(gpu_load * 0.5)), int(gpu_load), max(2, int(gpu_load * 1.3)), int(gpu_load)]

    rendered = template.render(
        system=data["system"],
        cpu=data["cpu"],
        gpu=data["gpu"],
        memory=data["memory"],
        storage=data["storage"],
        network=data["network"],
        health=data["health"],
        safe_mode=data["safe_mode"],
        target_offset=target_offset,
        spark_cpu=json.dumps(spark_cpu),
        spark_ram=json.dumps(spark_ram),
        spark_gpu=json.dumps(spark_gpu)
    )

    abs_path = os.path.abspath(output_path)
    with open(abs_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    if auto_open:
        webbrowser.open(f"file://{abs_path}")

    return abs_path
