<script lang="ts">
    import type { CartItem } from "../utils/types";

    // Define props
    export let item: CartItem;
    export let itemName: string | undefined;
</script>

<div class="cart-item">
    <div class="item-name">{itemName}</div>
    <div class="item-quantity">x {item.quantity}</div>
</div>