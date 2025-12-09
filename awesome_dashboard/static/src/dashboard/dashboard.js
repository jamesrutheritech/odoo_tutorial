/** @odoo-module **/
import { Component, useState, onWillStart } from "@odoo/owl";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { DashboardItem } from "./dashboard_item";
import { DashboardConfigDialog } from "./dashboard_config";
import { NumberCard } from "./number_card";
import { PieChartCard } from "./pie_chart_card";

export class AwesomeDashboard extends Component {
    setup() {
        this.action = useService("action");
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.dialog = useService("dialog");
        this.statistics = useState(this.statisticsService.data);

        this.displayOptions = {
            controlPanel: {},
        };

        onWillStart(async () => {
            await this.statisticsService.loadStatistics();
        });

        const itemsRegistry = registry.category("awesome_dashboard_items");
        this.rawItems = itemsRegistry.getAll();
        this.items = useState(this.getItems());
    }

    getItems() {
        const removedItemIds =
            JSON.parse(localStorage.getItem("awesome_dashboard.removed_items")) || [];
        return this.rawItems.filter((item) => !removedItemIds.includes(item.id));
    }

    openConfigDialog() {
        this.dialog.add(DashboardConfigDialog, {
            items: this.rawItems,
            onApply: (removedItemIds) => {
                localStorage.setItem("awesome_dashboard.removed_items", JSON.stringify(removedItemIds));
                Object.assign(this.items, this.getItems());
            },
        });
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: _t("Leads"),
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }

    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, NumberCard, PieChartCard };
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);