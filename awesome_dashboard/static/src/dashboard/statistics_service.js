/** @odoo-module **/
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

export const StatisticsService = {
    start(env) {
        const data = reactive({
            nb_new_orders: 0,
            total_amount: 0,
            average_quantity: 0,
            nb_cancelled_orders: 0,
            average_time: 0,
            orders_by_size: {},
            total_leads: 0,
            leads_by_stage: [],
        });

        async function loadStatistics() {
            try {
                const result = await rpc("/awesome_dashboard/statistics", {});
                if (result) {
                    Object.assign(data, result);
                }
            } catch (error) {
                console.error("Failed to load statistics:", error);
            }
        }

        loadStatistics();

        // Auto-refresh every 10 minutes (600000ms)
        // For testing, use 10000ms (10 seconds)
        setInterval(() => {
            loadStatistics();
        }, 600000);

        return {
            data,
            loadStatistics,
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", StatisticsService);