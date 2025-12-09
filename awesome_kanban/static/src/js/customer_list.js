/** @odoo-module **/
import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Pager } from "@web/core/pager/pager";

export class CustomerList extends Component {
    static template = "awesome_kanban.CustomerList";
    static components = { Pager };
    
    setup() {
        this.orm = useService("orm");
        this.state = useState({
            searchString: "",
            onlyActive: true,
            customers: [],
            offset: 0,
            limit: 20,
            total: 0,
        });
        onWillStart(() => this.loadCustomers());
    }

    async loadCustomers() {
        let domain = [["is_company", "=", true]];  // Changed from customer_rank
        if (this.state.onlyActive) {
            domain.push(["active", "=", true]);
        }
        if (this.state.searchString) {
            domain.push(["display_name", "ilike", this.state.searchString]);
        }
        const result = await this.orm.searchRead(
            "res.partner",
            domain,
            ["display_name"],
            {
                offset: this.state.offset,
                limit: this.state.limit,
            }
        );
        const count = await this.orm.searchCount("res.partner", domain);
        this.state.customers = result;
        this.state.total = count;
    }

    onSearch(ev) {
        this.state.searchString = ev.target.value;
        this.state.offset = 0;
        this.loadCustomers();
    }

    onToggleActive() {
        this.state.onlyActive = !this.state.onlyActive;
        this.state.offset = 0;
        this.loadCustomers();
    }

    onPagerChange(newState) {
        this.state.offset = newState.offset;
        this.state.limit = newState.limit;
        this.loadCustomers();
    }

    selectCustomer(customer) {
        if (this.props.onCustomerSelected) {
            this.props.onCustomerSelected(customer);
        }
    }
}

registry.category("components").add("CustomerList", CustomerList);