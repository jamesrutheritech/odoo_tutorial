/** @odoo-module **/

import { FormController } from "@web/views/form/form_controller";
import { patch } from "@web/core/utils/patch";
import { getReward } from "../utils/click_rewards";

/**
 * Patch FormController to randomly give rewards when opening forms
 * (Exercise 14)
 * 
 * 1% chance when opening any form view to receive a random reward
 */
patch(FormController.prototype, {
    setup() {
        super.setup(...arguments);
        
        // 1% chance to trigger a reward
        const random = Math.random();
        if (random < 0.01) {
            this.triggerReward();
        }
    },

    /**
     * Trigger a reward notification with "Collect" button
     */
    triggerReward() {
        const clicker = this.env.services.clicker_service;
        const notification = this.env.services.notification;
        const action = this.env.services.action;
        
        // Get a reward appropriate for current level
        const reward = getReward(clicker.level);
        
        if (reward) {
            // Show sticky notification with "Collect" button
            notification.add(
                `🎁 Bonus found! ${reward.description}`,
                {
                    type: "info",
                    sticky: true,
                    buttons: [
                        {
                            name: "Collect",
                            primary: true,
                            onClick: () => {
                                // Apply the reward
                                reward.apply(clicker);
                                
                                // Show success message
                                notification.add(
                                    `✅ Reward collected: ${reward.description}`,
                                    { type: "success" }
                                );
                                
                                // Open the clicker game
                                action.doAction({
                                    type: "ir.actions.client",
                                    tag: "awesome_clicker.client_action",
                                    target: "new",
                                    name: "Clicker Game",
                                });
                            },
                        },
                    ],
                }
            );
        }
    },
});