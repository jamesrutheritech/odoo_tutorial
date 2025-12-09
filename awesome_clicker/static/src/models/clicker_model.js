import { Reactive } from "@web/core/utils/reactive";
import { browser } from "@web/core/browser/browser";
import { EventBus } from "@odoo/owl";

const STORAGE_KEY = "awesome_clicker_state";
const CURRENT_VERSION = 2;

const migrations = [
    {
        fromVersion: 1,
        toVersion: 2,
        apply(state) {
            if (!state.peachTrees) {
                state.peachTrees = 0;
                state.peachFruits = 0;
            }
            console.log("🔄 Migrated state from v1 to v2");
        }
    }
];

export class ClickerModel extends Reactive {
    constructor() {
        super();
        console.log("🎮 ClickerModel: Constructor called");
        this.bus = new EventBus();
        this.loadState();
        this.setupAutoIncrement();
        this.setupAutoSave();
        this.setupTreeProduction();
        console.log("🎮 ClickerModel: Initialized successfully", this);
    }

    loadState() {
        console.log("📂 Loading state from localStorage...");
        try {
            const saved = browser.localStorage.getItem(STORAGE_KEY);
            if (saved) {
                const state = JSON.parse(saved);
                console.log("📂 Found saved state:", state);
                this.applyMigrations(state);
                this.restoreState(state);
                console.log("✅ State loaded successfully");
            } else {
                console.log("📂 No saved state found, initializing new game");
                this.initializeDefaultState();
            }
        } catch (err) {
            console.error("❌ Error loading state:", err);
            this.initializeDefaultState();
        }
    }

    applyMigrations(state) {
        const stateVersion = state.version || 1;
        
        if (stateVersion < CURRENT_VERSION) {
            console.log(`🔄 Migrating state from v${stateVersion} to v${CURRENT_VERSION}`);
            
            migrations.forEach(migration => {
                if (stateVersion >= migration.fromVersion && stateVersion < migration.toVersion) {
                    migration.apply(state);
                }
            });
            
            state.version = CURRENT_VERSION;
        }
    }

    restoreState(state) {
        this.version = state.version || CURRENT_VERSION;
        this.clicks = state.clicks || 0;
        this.level = state.level || 0;
        this.clickBots = state.clickBots || 0;
        this.bigBots = state.bigBots || 0;
        this.power = state.power || 1;
        this.pearTrees = state.pearTrees || 0;
        this.pearFruits = state.pearFruits || 0;
        this.cherryTrees = state.cherryTrees || 0;
        this.cherryFruits = state.cherryFruits || 0;
        this.peachTrees = state.peachTrees || 0;
        this.peachFruits = state.peachFruits || 0;
        this.milestones = state.milestones || {};
    }

    initializeDefaultState() {
        console.log("🆕 Initializing default state");
        this.version = CURRENT_VERSION;
        this.clicks = 0;
        this.level = 0;
        this.clickBots = 0;
        this.bigBots = 0;
        this.power = 1;
        this.pearTrees = 0;
        this.pearFruits = 0;
        this.cherryTrees = 0;
        this.cherryFruits = 0;
        this.peachTrees = 0;
        this.peachFruits = 0;
        this.milestones = {};
        console.log("✅ Default state initialized");
    }

    saveState() {
        const state = {
            version: this.version,
            clicks: this.clicks,
            level: this.level,
            clickBots: this.clickBots,
            bigBots: this.bigBots,
            power: this.power,
            pearTrees: this.pearTrees,
            pearFruits: this.pearFruits,
            cherryTrees: this.cherryTrees,
            cherryFruits: this.cherryFruits,
            peachTrees: this.peachTrees,
            peachFruits: this.peachFruits,
            milestones: this.milestones,
        };
        browser.localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
        console.log("💾 State saved:", state);
    }

    setupAutoSave() {
        console.log("⏰ Setting up auto-save (every 10s)");
        setInterval(() => this.saveState(), 10000);
    }

    checkMilestones() {
        if (this.clicks >= 1000 && !this.milestones.level1) {
            console.log("🎉 MILESTONE: Level 1 reached (1,000 clicks)!");
            this.level = 1;
            this.milestones.level1 = true;
            this.bus.trigger("MILESTONE_1K");
        }
        
        if (this.clicks >= 5000 && !this.milestones.level2) {
            console.log("🎉 MILESTONE: Level 2 reached (5,000 clicks)!");
            this.level = 2;
            this.milestones.level2 = true;
            this.bus.trigger("MILESTONE_5K");
        }
        
        if (this.clicks >= 100000 && !this.milestones.level3) {
            console.log("🎉 MILESTONE: Level 3 reached (100,000 clicks)!");
            this.level = 3;
            this.milestones.level3 = true;
            this.bus.trigger("MILESTONE_100K");
        }
        
        if (this.clicks >= 1000000 && !this.milestones.level4) {
            console.log("🎉 MILESTONE: Level 4 reached (1,000,000 clicks)!");
            this.level = 4;
            this.milestones.level4 = true;
            this.bus.trigger("MILESTONE_1M");
        }
    }

    increment(amount) {
        console.log(`➕ Increment: +${amount} clicks (${this.clicks} → ${this.clicks + amount})`);
        this.clicks += amount;
        this.checkMilestones();
    }

    buyClickBot() {
        console.log(`🤖 Attempting to buy ClickBot (Cost: 1000, Current: ${this.clicks})`);
        if (this.clicks >= 1000) {
            this.clicks -= 1000;
            this.clickBots += 1;
            console.log(`✅ ClickBot purchased! Total: ${this.clickBots}`);
        } else {
            console.log(`❌ Not enough clicks to buy ClickBot`);
        }
    }

    buyBigBot() {
        console.log(`🦾 Attempting to buy BigBot (Cost: 5000, Current: ${this.clicks})`);
        if (this.clicks >= 5000) {
            this.clicks -= 5000;
            this.bigBots += 1;
            console.log(`✅ BigBot purchased! Total: ${this.bigBots}`);
        } else {
            console.log(`❌ Not enough clicks to buy BigBot`);
        }
    }

    buyPower() {
        console.log(`⚡ Attempting to buy Power (Cost: 50000, Current: ${this.clicks})`);
        if (this.clicks >= 50000) {
            this.clicks -= 50000;
            this.power += 1;
            console.log(`✅ Power upgraded! New power: ${this.power}`);
        } else {
            console.log(`❌ Not enough clicks to buy Power`);
        }
    }

    buyPearTree() {
        console.log(`🍐 Attempting to buy Pear Tree (Cost: 1000000, Current: ${this.clicks})`);
        if (this.clicks >= 1000000) {
            this.clicks -= 1000000;
            this.pearTrees += 1;
            console.log(`✅ Pear Tree planted! Total: ${this.pearTrees}`);
        } else {
            console.log(`❌ Not enough clicks to buy Pear Tree`);
        }
    }

    buyCherryTree() {
        console.log(`🍒 Attempting to buy Cherry Tree (Cost: 1000000, Current: ${this.clicks})`);
        if (this.clicks >= 1000000) {
            this.clicks -= 1000000;
            this.cherryTrees += 1;
            console.log(`✅ Cherry Tree planted! Total: ${this.cherryTrees}`);
        } else {
            console.log(`❌ Not enough clicks to buy Cherry Tree`);
        }
    }

    buyPeachTree() {
        console.log(`🍑 Attempting to buy Peach Tree (Cost: 1000000, Current: ${this.clicks})`);
        if (this.clicks >= 1000000) {
            this.clicks -= 1000000;
            this.peachTrees += 1;
            console.log(`✅ Peach Tree planted! Total: ${this.peachTrees}`);
        } else {
            console.log(`❌ Not enough clicks to buy Peach Tree`);
        }
    }

    getTotalTrees() {
        return this.pearTrees + this.cherryTrees + this.peachTrees;
    }

    getTotalFruits() {
        return this.pearFruits + this.cherryFruits + this.peachFruits;
    }

    setupAutoIncrement() {
        console.log("⏰ Setting up auto-increment (bots produce every 10s)");
        setInterval(() => {
            let produced = 0;
            
            produced += this.clickBots * 10 * this.power;
            produced += this.bigBots * 100 * this.power;
            
            if (produced > 0) {
                console.log(`🤖 Bots produced: +${produced} clicks`);
                this.increment(produced);
            }
            
            this.saveState();
        }, 10000);
    }

    setupTreeProduction() {
        console.log("⏰ Setting up tree production (fruits every 30s)");
        setInterval(() => {
            if (this.pearTrees > 0 || this.cherryTrees > 0 || this.peachTrees > 0) {
                this.pearFruits += this.pearTrees;
                this.cherryFruits += this.cherryTrees;
                this.peachFruits += this.peachTrees;
                console.log(`🌳 Trees produced fruits: Pears +${this.pearTrees}, Cherries +${this.cherryTrees}, Peaches +${this.peachTrees}`);
            }
        }, 30000);
    }

    getClickPower() {
        return 10;
    }
}