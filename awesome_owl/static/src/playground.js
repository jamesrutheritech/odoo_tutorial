import { Component, useState, markup } from "@odoo/owl"; 
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list"; 

export class Playground extends Component {
    static template = "awesome_owl.Playground"; 
    
    static components = { Counter, Card, TodoList }; 
    
    static props = {}; 

    setup() {
        this.state = useState({
            sum: 0, 

            safeHtml: markup(`
                <ul>
                    <li>This is <strong>SAFE</strong> HTML</li>
                    <li>The <code>markup</code> function allows t-out to render this list.</li>
                </ul>
            `),
            unsafeHtml: `
                <p style="color: red;">This is <strong>UNSAFE</strong> HTML</p>
                <p>Because it's not wrapped in markup(), it will be displayed as raw text.</p>
            `,
        });
    }

    incrementSum = () => {
        this.state.sum++;
    }
}