/** @odoo-module **/
import { KanbanRenderer } from "@web/views/kanban/kanban_renderer";
import { CustomerList } from "./customer_list";

export class AwesomeKanbanRenderer extends KanbanRenderer {
    static components = { ...KanbanRenderer.components, CustomerList };
}