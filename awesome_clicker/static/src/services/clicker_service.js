/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { ClickerModel } from "../models/clicker_model";
import { browser } from "@web/core/browser/browser";

const clickerModel = new ClickerModel();

export const clickerService = {
    dependencies: ["effect", "notification"],
    
    start(env, { effect, notification }) {
        // Global click tracking
        document.body.addEventListener(
            "click",
            () => clickerModel.increment(1),
            true
        );

        // Milestone celebrations
        clickerModel.bus.addEventListener("MILESTONE_1K", () => {
            effect.add({
                type: "rainbow_man",
                message: "🎉 You reached 1,000 clicks! ClickBots are now available!",
            });
        });

        clickerModel.bus.addEventListener("MILESTONE_5K", () => {
            effect.add({
                type: "rainbow_man",
                message: "🚀 You reached 5,000 clicks! BigBots are now unlocked!",
            });
        });

        clickerModel.bus.addEventListener("MILESTONE_100K", () => {
            effect.add({
                type: "rainbow_man",
                message: "⚡ You reached 100,000 clicks! Power upgrades available!",
            });
        });

        clickerModel.bus.addEventListener("MILESTONE_1M", () => {
            effect.add({
                type: "rainbow_man",
                message: "🌳 You reached 1,000,000 clicks! Plant fruit trees!",
            });
        });

        // Add reset function
        clickerModel.reset = () => {
            notification.add("Are you sure? This will delete all progress!", {
                type: "warning",
                sticky: true,
                buttons: [
                    {
                        name: "Yes, Reset Game",
                        primary: true,
                        onClick: () => {
                            browser.localStorage.removeItem('awesome_clicker_state');
                            clickerModel.initializeDefaultState();
                            notification.add("🔄 Game reset successfully!", { type: "success" });
                        }
                    },
                    {
                        name: "Cancel",
                        onClick: () => {}
                    }
                ]
            });
        };

        return clickerModel;
    },
};

registry.category("services").add("clicker_service", clickerService);

export function useClicker() {
    return useService("clicker_service");
}