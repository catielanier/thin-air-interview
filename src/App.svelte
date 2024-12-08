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
  // Must parse JSON for cart and integer for subtotal since all localStorage is stringified
  let cart: Cart = JSON.parse(getStorageItem('cart')!) ?? [];
  let subtotal = parseFloat(getStorageItem('subtotal')!) ?? 0;
  let cartIsUpdating: boolean = false;

  // Retrieve sale items from backend when app is mounted
  onMount((): void => {
    axios.get('/api/v1/items').then(({ data }): void => {
      items = data;
    });
  });

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
  {#if items.length}
    <div class="items">
      {#each items as item}
        <Item {item} {updateCart} {cartIsUpdating} />
      {/each}
    </div>
  {/if}
  {#if cart.length}
    <div class="cart">
      <h2>Your Cart:</h2>
      <div class="cart-items">
        {#each cart as cartItem}
          <CartItem item={cartItem} itemName={items.find(item => item.id === cartItem.id)?.description} />
        {/each}
      </div>
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
