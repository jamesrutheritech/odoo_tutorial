/** @odoo-module **/
import { KanbanController } from "@web/views/kanban/kanban_controller";
import { CustomerList } from "./customer_list";

export class AwesomeKanbanController extends KanbanController {
    static template = "awesome_kanban.KanbanViewWithSidebar";
    static components = { 
        ...KanbanController.components, 
        CustomerList 
    };

    get rendererProps() {
        const props = super.rendererProps;
        return props;
    }

    selectCustomer(partner) {
        const searchModel = this.env.searchModel;
        const oldFilters = searchModel.getSearchItems(item => item.isFromAwesomeKanban);
        for (const filter of oldFilters) {
            if (filter.isActive) {
                searchModel.toggleSearchItem(filter.id);
            }
        }
        searchModel.createNewFilters([{
            description: partner.display_name,
            domain: `[("partner_id", "=", ${partner.id})]`,
            isFromAwesomeKanban: true,
        }]);
    }
}