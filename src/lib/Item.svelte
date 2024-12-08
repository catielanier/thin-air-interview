<script lang="ts">
    import type { Item } from "../utils/types";

    // Set props
    export let item: Item;
</script>

<div class="item">
    <p class="item-description">{item.description}</p>
    <p class="item-price">{item.price}</p>
</div>