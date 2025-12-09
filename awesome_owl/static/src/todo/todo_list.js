// awesome_owl/static/src/todo/todo_list.js

import { Component, useState } from "@odoo/owl"; 
import { TodoItem } from "./todo_item"; 
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem }; 
    static props = {}; 
    
    nextId = 2; 

    setup() {
        this.todos = useState([
             { id: 0, description: "Test the toggle feature", isCompleted: false },
             { id: 1, description: "Delete this task when done", isCompleted: true },
        ]);
        
        this.inputRef = useAutofocus('input');
    }

    toggleTodo(id) {
        const todo = this.todos.find(t => t.id === id);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(id) {
        const index = this.todos.findIndex(t => t.id === id);
        
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }

    addTodo(ev) {
        if (ev.keyCode === 13) {
            const description = ev.target.value.trim();
            if (description === "") {
                return;
            }

            this.todos.push({
                id: this.nextId++,
                description: description,
                isCompleted: false,
            });

            ev.target.value = "";
        }
    }
}