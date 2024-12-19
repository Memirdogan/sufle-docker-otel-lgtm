from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from prometheus_client import start_http_server, Counter
import logging

# Tracing Ayarları
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
span_exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)
span_processor = BatchSpanProcessor(span_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Logging Ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("otel-example")
logger.info("LGTM Stack'e log gönderiliyor...")

# Metrics Ayarları
start_http_server(8000)  # Prometheus için HTTP sunucusu
example_counter = Counter("example_counter", "An example metric counter")
example_counter.inc()  # Sayaç değerini artır

# Trace Gönderimi
with tracer.start_as_current_span("example-span") as span:
    logger.info("Span aktif...")
    span.set_attribute("example-attribute", "LGTM Test")
