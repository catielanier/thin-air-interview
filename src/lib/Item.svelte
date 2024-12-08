<script lang="ts">
    import type { Item } from "../utils/types";
    import { OPERATORS } from "../utils/constants";

    // Set props
    export let item: Item;
    export let cartIsUpdating: boolean;
    export let updateCart: (itemId: number, quantity: number) => void;

    const incrementItem = (operator: string, itemId: number) => {
        let quantity = 0;
        switch (operator) {
            case OPERATORS.ADD:
                quantity += 1;
                break;
            case OPERATORS.SUB:
                quantity -= 1;
                break;
            default:
                break;
        }
        updateCart(itemId, quantity);
    }
</script>

<div class="item">
    <p class="item-description">{item.description}</p>
    <p class="item-price">${item.price}</p>
    <button disabled={cartIsUpdating} on:click={(e) => {
        e.preventDefault();
        incrementItem(OPERATORS.ADD, item.id);
    }}>+</button>
    <button disabled={cartIsUpdating} on:click={(e) => {
        e.preventDefault();
        incrementItem(OPERATORS.SUB, item.id);
    }}>-</button>
</div>