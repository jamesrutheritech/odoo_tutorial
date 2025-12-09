/** @odoo-module **/
import { Component, onMounted, onWillStart, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChartCard extends Component {
    setup() {
        this.canvasRef = useRef("canvas");
        
        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });
        
        onMounted(() => {
            this.renderChart();
        });
    }

    renderChart() {
        const { chartData } = this.props;
        if (!chartData || !chartData.length) {
            return;
        }
        
        const canvas = this.canvasRef.el;
        if (!canvas || typeof Chart === "undefined") {
            return;
        }
        
        new Chart(canvas, {
            type: "pie",
            data: {
                labels: chartData.map((d) => d.label),
                datasets: [
                    {
                        data: chartData.map((d) => d.value),
                        backgroundColor: [
                            "#665C7B",
                            "#5C7B66",
                            "#7B665C",
                            "#667B7B",
                            "#7B667B",
                        ],
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: "top" } },
            },
        });
    }

    static template = "awesome_dashboard.PieChartCard";
    static props = { chartData: { type: Array } };
}