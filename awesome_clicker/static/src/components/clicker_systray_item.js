/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { useClicker } from "../services/clicker_service";
import { ClickValue } from "./click_value";

/**
 * Clicker Systray Item
 * Shows game stats in systray with dropdown menu for quick actions
 * (Exercise 17)
 */
export class ClickerSystrayItem extends Component {
    static template = "awesome_clicker.ClickerSystrayItem";
    static components = { Dropdown, DropdownItem, ClickValue };

    setup() {
        this.clicker = useClicker();
        this.action = useService("action");
    }

    /**
     * Open the main clicker game client action
     */
    openClientAction() {
        this.action.doAction({
            type: "ir.actions.client",
            tag: "awesome_clicker.client_action",
            target: "new",
            name: "Clicker Game",
        });
    }

    /**
     * Quick action: Buy a ClickBot from systray
     */
    buyClickBot() {
        this.clicker.buyClickBot();
    }

    /**
     * Quick action: Buy a BigBot from systray
     */
    buyBigBot() {
        this.clicker.buyBigBot();
    }

    /**
     * Quick action: Buy power upgrade from systray
     */
    buyPower() {
        this.clicker.buyPower();
    }

    /**
     * Check if user can afford an item
     */
    canAfford(cost) {
        return this.clicker.clicks >= cost;
    }
}

registry.category("systray").add(
    "awesome_clicker.systray",
    {
        Component: ClickerSystrayItem,
    },
    { sequence: 1 }
);