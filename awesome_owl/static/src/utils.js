import { useRef, onMounted } from "@odoo/owl";

export function useAutofocus(refName) {
    const myRef = useRef(refName);

    onMounted(() => {
        if (myRef.el) {
            myRef.el.focus();
        }
    });

    return myRef;
}