/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { useClicker } from "../services/clicker_service";
import { ClickValue } from "./click_value";
import { Notebook } from "@web/core/notebook/notebook";
import { browser } from "@web/core/browser/browser";

/**
 * Clicker Client Action
 * Main game interface with tabs for different resource types
 */
export class ClickerClientAction extends Component {
    static template = "awesome_clicker.ClientAction";
    static components = { ClickValue, Notebook };

    setup() {
        this.clicker = useClicker();
        this.notification = useService("notification");
    }

    /**
     * Manual click action (+10 clicks)
     */
    click() {
        this.clicker.increment(10);
    }

    /**
     * Buy a ClickBot
     */
    buyClickBot() {
        this.clicker.buyClickBot();
    }

    /**
     * Buy a BigBot
     */
    buyBigBot() {
        this.clicker.buyBigBot();
    }

    /**
     * Buy a power upgrade
     */
    buyPower() {
        this.clicker.buyPower();
    }

    /**
     * Buy a pear tree
     */
    buyPearTree() {
        this.clicker.buyPearTree();
    }

    /**
     * Buy a cherry tree
     */
    buyCherryTree() {
        this.clicker.buyCherryTree();
    }

    /**
     * Buy a peach tree
     */
    buyPeachTree() {
        this.clicker.buyPeachTree();
    }

    /**
     * Check if user can afford an item
     */
    canAfford(cost) {
        return this.clicker.clicks >= cost;
    }

    /**
     * Reset the game with confirmation
     */
    resetGame() {
        this.notification.add("⚠️ Are you sure you want to reset? All progress will be lost!", {
            type: "warning",
            sticky: true,
            buttons: [
                {
                    name: "Yes, Reset Everything",
                    primary: true,
                    onClick: () => {
                        // Clear localStorage
                        browser.localStorage.removeItem('awesome_clicker_state');
                        
                        // Reset the model
                        this.clicker.initializeDefaultState();
                        
                        // Show success message
                        this.notification.add("🔄 Game reset successfully! Starting fresh.", {
                            type: "success"
                        });
                    }
                },
                {
                    name: "Cancel",
                    onClick: () => {
                        this.notification.add("Reset cancelled.", { type: "info" });
                    }
                }
            ]
        });
    }
}

registry.category("actions").add("awesome_clicker.client_action", ClickerClientAction);