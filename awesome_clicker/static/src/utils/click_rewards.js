import { choose } from "./utils";

/**
 * List of available rewards in the game
 * Each reward has:
 * - description: User-friendly text shown in notifications
 * - apply: Function that modifies the clicker state
 * - minLevel: (optional) Minimum unlock level required
 * - maxLevel: (optional) Maximum level where this reward is available
 */
export const rewards = [
    {
        description: "Get 1 ClickBot",
        apply(clicker) {
            clicker.clickBots += 1;
        },
        maxLevel: 2,
    },
    {
        description: "Get 100 bonus clicks",
        apply(clicker) {
            clicker.increment(100);
        },
        maxLevel: 1,
    },
    {
        description: "Get 500 bonus clicks",
        apply(clicker) {
            clicker.increment(500);
        },
        minLevel: 1,
        maxLevel: 2,
    },
    {
        description: "Get 1 BigBot",
        apply(clicker) {
            clicker.bigBots += 1;
        },
        minLevel: 2,
        maxLevel: 3,
    },
    {
        description: "Get 5000 bonus clicks!",
        apply(clicker) {
            clicker.increment(5000);
        },
        minLevel: 2,
    },
    {
        description: "Increase bot power by 1!",
        apply(clicker) {
            clicker.power += 1;
        },
        minLevel: 3,
    },
    {
        description: "Double your ClickBots!",
        apply(clicker) {
            clicker.clickBots *= 2;
        },
        minLevel: 2,
    },
    {
        description: "Get 10% of your current clicks as bonus!",
        apply(clicker) {
            clicker.increment(Math.floor(clicker.clicks * 0.1));
        },
        minLevel: 1,
    },
];

/**
 * Gets a random reward appropriate for the current level
 * @param {number} level - Current unlock level
 * @returns {Object|null} A random reward object or null if none available
 */
export function getReward(level) {
    const availableRewards = rewards.filter(reward => {
        const minOk = !reward.minLevel || level >= reward.minLevel;
        const maxOk = !reward.maxLevel || level <= reward.maxLevel;
        return minOk && maxOk;
    });
    
    if (availableRewards.length > 0) {
        return choose(availableRewards);
    }
    
    return null;
}