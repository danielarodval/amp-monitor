import os, asyncio, httpx
from dotenv import load_dotenv
import reflex as rx
from datetime import datetime

load_dotenv()
API_BASE = os.getenv("API_BASE", "http://localhost:8000")

class Metric(rx.Base):
    id: int
    ApplicationName: str
    InstanceName: str
    UserCount: int
    MaxUsers: int
    Time: datetime
    Uptime: int
    RAMUsage: float
    CPUUsage: float

class State(rx.State):
    metrics: list[Metric] = []
    servers: list[dict] = []
    loading: bool = False
    error: str = ""

    async def load(self):
        self.loading = True
        self.error = ""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                m = await client.get(f"{API_BASE}/metrics")
                s = await client.get(f"{API_BASE}/server-info")
            self.metrics = [Metric(**x) for x in m.json()]
            self.servers = s.json()
        except Exception as e:
            self.error = str(e)
        finally:
            self.loading = False

def server_table():
    return rx.card(
        rx.heading("Servers", size="5"),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Application"),
                    rx.table.column_header_cell("Instance"),
                    rx.table.column_header_cell("Max Users"),
                    rx.table.column_header_cell("Created"),
                )
            ),
            rx.table.body(
                rx.foreach(State.servers, lambda s:
                    rx.table.row(
                        rx.table.cell(s["ApplicationName"]),
                        rx.table.cell(s["InstanceName"]),
                        rx.table.cell(s["MaxUsers"]),
                        rx.table.cell(str(s["CreatedAt"])),
                    )
                )
            ),
        ),
        width="100%",
    )

def metrics_table():
    return rx.card(
        rx.heading("Recent Metrics", size="5"),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Time"),
                    rx.table.column_header_cell("App"),
                    rx.table.column_header_cell("Instance"),
                    rx.table.column_header_cell("Users"),
                    rx.table.column_header_cell("Max"),
                    rx.table.column_header_cell("Uptime(s)"),
                    rx.table.column_header_cell("RAM"),
                    rx.table.column_header_cell("CPU"),
                )
            ),
            rx.table.body(
                rx.foreach(State.metrics, lambda m:
                    rx.table.row(
                        rx.table.cell(str(m.Time)),
                        rx.table.cell(m.ApplicationName),
                        rx.table.cell(m.InstanceName),
                        rx.table.cell(m.UserCount),
                        rx.table.cell(m.MaxUsers),
                        rx.table.cell(m.Uptime),
                        rx.table.cell(m.RAMUsage),
                        rx.table.cell(m.CPUUsage),
                    )
                )
            ),
        ),
        width="100%",
    )

def index() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.hstack(
                rx.heading("AMP Stats Dashboard", size="7"),
                rx.spacer(),
                rx.button("Refresh", on_click=State.load),
            ),
            rx.cond(State.error != "", rx.text(State.error, color="red")),
            rx.cond(State.loading, rx.text("Loading...")),
            server_table(),
            metrics_table(),
            spacing="4",
            width="100%",
        ),
        size="4",
        padding="2rem",
        width="100%",
    )

app = rx.App()
app.add_page(index, on_load=State.load, route="/")
