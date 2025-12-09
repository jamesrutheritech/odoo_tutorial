/** @odoo-module **/
import { registry } from "@web/core/registry";
import { NumberCard } from "./number_card";
import { PieChartCard } from "./pie_chart_card";

const dashboardItemsRegistry = registry.category("awesome_dashboard_items");

dashboardItemsRegistry.add("new_orders", {
    id: "new_orders",
    label: "New Orders",
    Component: NumberCard,
    props: (statistics) => ({
        title: "New Orders This Month",
        value: statistics.nb_new_orders,
    }),
});

dashboardItemsRegistry.add("total_amount", {
    id: "total_amount",
    label: "Total Amount",
    Component: NumberCard,
    props: (statistics) => ({
        title: "Total Amount This Month",
        value: statistics.total_amount,
    }),
});

dashboardItemsRegistry.add("average_quantity", {
    id: "average_quantity",
    label: "Average Quantity",
    Component: NumberCard,
    props: (statistics) => ({
        title: "Average Quantity",
        value: statistics.average_quantity,
    }),
});

dashboardItemsRegistry.add("cancelled_orders", {
    id: "cancelled_orders",
    label: "Cancelled Orders",
    Component: NumberCard,
    props: (statistics) => ({
        title: "Cancelled Orders",
        value: statistics.nb_cancelled_orders,
    }),
});

dashboardItemsRegistry.add("average_time", {
    id: "average_time",
    label: "Average Time",
    Component: NumberCard,
    props: (statistics) => ({
        title: "Average Time (days)",
        value: statistics.average_time,
    }),
});

dashboardItemsRegistry.add("orders_pie", {
    id: "orders_pie",
    label: "Orders by Size",
    Component: PieChartCard,
    props: (statistics) => ({
        chartData: Object.entries(statistics.orders_by_size || {}).map(
            ([label, value]) => ({ label: label.toUpperCase(), value })
        ),
    }),
    size: 2,
});