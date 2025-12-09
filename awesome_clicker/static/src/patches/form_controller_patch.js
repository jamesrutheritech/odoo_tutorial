import { FormController } from "@web/views/form/form_controller";
import { patch } from "@web/core/utils/patch";
import { getReward } from "../utils/click_rewards";


patch(FormController.prototype, {
    setup() {
        super.setup(...arguments);
        
        const random = Math.random();
        if (random < 0.01) {
            this.triggerReward();
        }
    },

    triggerReward() {
        const clicker = this.env.services.clicker_service;
        const notification = this.env.services.notification;
        const action = this.env.services.action;
        
        const reward = getReward(clicker.level);
        
        if (reward) {
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
                                reward.apply(clicker);
                                
                                notification.add(
                                    `✅ Reward collected: ${reward.description}`,
                                    { type: "success" }
                                );
                                
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