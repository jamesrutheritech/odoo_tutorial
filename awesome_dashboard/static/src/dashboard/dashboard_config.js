/** @odoo-module **/
import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";

export class DashboardConfigDialog extends Component {
    static template = "awesome_dashboard.DashboardConfigDialog";
    static components = { Dialog, CheckBox };
    static props = {
        items: Array,
        close: Function,
        onApply: Function,
    };

    setup() {
        const removedItemIds = JSON.parse(
            localStorage.getItem("awesome_dashboard.removed_items") || "[]"
        );

        this.state = useState({
            itemStates: this.props.items.map((item) => ({
                id: item.id,
                label: item.label,
                checked: !removedItemIds.includes(item.id),
            })),
        });
    }

    onCheckboxChange(itemId, checked) {
        const item = this.state.itemStates.find((i) => i.id === itemId);
        if (item) {
            item.checked = checked;
        }
    }

    onApply() {
        const removedItemIds = this.state.itemStates
            .filter((item) => !item.checked)
            .map((item) => item.id);

        this.props.onApply(removedItemIds);
        this.props.close();
    }
}