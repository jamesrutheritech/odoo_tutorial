/** @odoo-module **/

import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    // Props must match what dashboard.xml passes in
    static props = {
        item: { type: Object },
        statistics: { type: Object },
    };

    static template = "awesome_dashboard.DashboardItem";
}
