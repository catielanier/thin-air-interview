<script lang="ts">
  import { onMount } from "svelte";
  import axios from 'axios';
  import type { Cart, Items } from "./utils/types";
  import {getStorageItem, setStorageItem} from "./utils/storage";
  import Item from "./lib/Item.svelte";
  import CartItem from "./lib/CartItem.svelte";

  // Set initial states
  let items: Items = [];
  // Cart and subtotal can be derived from localStorage to be maintained across browsing sessions, will default to blank if never created
  // Must parse JSON for cart and float for subtotal since all localStorage is stringified
  // Float required since we won't always have whole numbers
  let cart: Cart = JSON.parse(getStorageItem('cart')!) ?? [];
  let subtotal = parseFloat(getStorageItem('subtotal')!) ?? 0;
  let cartIsUpdating: boolean = false;

  // Retrieve sale items from backend when app is mounted
  onMount((): void => {
    axios.get('/api/v1/items').then(({ data }): void => {
      items = data;
    });
  });

  // Standalone function to ensure cart storage is updated
  const updateCartStorage = (): void => {
    setStorageItem('cart', JSON.stringify(cart));
    setStorageItem('subtotal', subtotal.toString());
  }

  const updateCart = (itemId: number, quantity: number): void => {
    cartIsUpdating = true;
    const cartItem = {
      id: itemId,
      quantity
    }
    axios.put('/api/v1/cart/update', ({ cart, cartItem }))
      .then(({ data }): void => {
        cart = data.cart;
        subtotal = data.subtotal;
      })
      .finally(() => {
        updateCartStorage();
        cartIsUpdating = false;
      });
  }
</script>

<main>
  <h1>Holy Shirt!</h1>
  <!-- Wait for products to be retrieved before rendering -->
  {#if items.length}
    <div class="items">
      <!-- Loop through each product and render with child component -->
      {#each items as item}
        <Item {item} {updateCart} {cartIsUpdating} />
      {/each}
    </div>
  {/if}
  <!-- Check to see if items are in the cart before rendering -->
  {#if cart.length}
    <div class="cart">
      <h2>Your Cart:</h2>
      <div class="cart-items">
        <!-- Loop through each cart item and render with child component -->
        {#each cart as cartItem}
          <CartItem item={cartItem} itemName={items.find(item => item.id === cartItem.id)?.description} />
        {/each}
      </div>
      <!--
       Don't need to pass subtotal to child, just render directly here,
       if we were doing Sales Taxes, we would pass to child to handle
       rendering each with less nesting
      -->
      <!-- TODO: Create child component to show subtotal, taxes, and grand total -->
      <p>Subtotal: ${subtotal.toFixed(2)}</p>
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
