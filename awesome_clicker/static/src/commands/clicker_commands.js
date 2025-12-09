/** @odoo-module **/

import { registry } from "@web/core/registry";

/**
 * Command Palette Integration for Clicker Game
 * (Exercise 15)
 * 
 * Adds commands to quickly access game features via Ctrl+K
 */

const commandPaletteRegistry = registry.category("command_provider");

/**
 * Command: Open Clicker Game
 */
commandPaletteRegistry.add("awesome_clicker.commands", {
    namespace: "clicker",
    provide: (env, options) => {
        const clicker = env.services.clicker_service;
        const commands = [];

        // Command 1: Open the clicker game
        commands.push({
            name: "Open Clicker Game",
            action: () => {
                env.services.action.doAction({
                    type: "ir.actions.client",
                    tag: "awesome_clicker.client_action",
                    target: "new",
                    name: "Clicker Game",
                });
            },
        });

        // Command 2: Buy ClickBot (only if unlocked and affordable)
        if (clicker.level >= 1) {
            commands.push({
                name: `Buy 1 ClickBot (1,000 clicks) ${clicker.clicks >= 1000 ? "✓" : "✗"}`,
                action: () => {
                    if (clicker.clicks >= 1000) {
                        clicker.buyClickBot();
                        env.services.notification.add("🤖 Purchased 1 ClickBot!", {
                            type: "success",
                        });
                    } else {
                        env.services.notification.add("Not enough clicks!", {
                            type: "warning",
                        });
                    }
                },
            });
        }

        // Command 3: Buy BigBot (only if unlocked and affordable)
        if (clicker.level >= 2) {
            commands.push({
                name: `Buy 1 BigBot (5,000 clicks) ${clicker.clicks >= 5000 ? "✓" : "✗"}`,
                action: () => {
                    if (clicker.clicks >= 5000) {
                        clicker.buyBigBot();
                        env.services.notification.add("🦾 Purchased 1 BigBot!", {
                            type: "success",
                        });
                    } else {
                        env.services.notification.add("Not enough clicks!", {
                            type: "warning",
                        });
                    }
                },
            });
        }

        // Command 4: Buy Power Upgrade (only if unlocked and affordable)
        if (clicker.level >= 3) {
            commands.push({
                name: `Buy Power Upgrade (50,000 clicks) ${clicker.clicks >= 50000 ? "✓" : "✗"}`,
                action: () => {
                    if (clicker.clicks >= 50000) {
                        clicker.buyPower();
                        env.services.notification.add("⚡ Power upgraded!", {
                            type: "success",
                        });
                    } else {
                        env.services.notification.add("Not enough clicks!", {
                            type: "warning",
                        });
                    }
                },
            });
        }

        // Command 5: Plant Pear Tree (only if unlocked and affordable)
        if (clicker.level >= 4) {
            commands.push({
                name: `Plant Pear Tree (1,000,000 clicks) ${clicker.clicks >= 1000000 ? "✓" : "✗"}`,
                action: () => {
                    if (clicker.clicks >= 1000000) {
                        clicker.buyPearTree();
                        env.services.notification.add("🍐 Planted a Pear Tree!", {
                            type: "success",
                        });
                    } else {
                        env.services.notification.add("Not enough clicks!", {
                            type: "warning",
                        });
                    }
                },
            });
        }

        return commands;
    },
});