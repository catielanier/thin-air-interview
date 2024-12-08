<script lang="ts">
  import { onMount } from "svelte";
  import axios from 'axios';
  import type { Cart, Items } from "./utils/types";
  import { getStorageItem } from "./utils/storage";
  import Item from "./lib/Item.svelte";

  // Set initial states
  let items: Items = [];
  // Cart and subtotal can be derived from localStorage to be maintained across browsing sessions, will default to blank if never created
  // Must parse JSON for cart and integer for subtotal since all localStorage is stringified
  let cart: Cart = JSON.parse(getStorageItem('cart')!) ?? [];
  let subtotal = parseInt(getStorageItem('subtotal')!, 10) ?? 0;

  // Retrieve sale items from backend when app is mounted
  onMount((): void => {
    axios.get('/api/v1/items').then(({ data }): void => {
      items = data;
    });
  });
</script>

<main>
  <h1>Holy Shirt!</h1>
  {#if items.length}
    <div class="items">
      {#each items as item}
        <Item {item} />
      {/each}
    </div>
  {/if}
</main>

<style>
  .logo {
    height: 6em;
    padding: 1.5em;
    will-change: filter;
    transition: filter 300ms;
  }
  .logo:hover {
    filter: drop-shadow(0 0 2em #646cffaa);
  }
  .logo.svelte:hover {
    filter: drop-shadow(0 0 2em #ff3e00aa);
  }
  .read-the-docs {
    color: #888;
  }
</style>
