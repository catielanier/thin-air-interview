<script lang="ts">
  import { onMount } from "svelte";
  import axios from "axios";
  import Item from "./lib/Item.svelte";
  import CartItem from "./lib/CartItem.svelte";
  import type {Cart, CartItemMutation, ProductItems} from "./utils/types";
  import {getStorageItem, setStorageItem} from "./utils/storage";

  let cart: Cart = [];
  let subtotal: number = 0;
  let items: ProductItems = [];
  let cartIsUpdating: boolean = false;

  onMount(() => {
    const cartFromStorage: string | null = getStorageItem("cart");
    const subtotalFromStorage: string | null = getStorageItem("subtotal");
    cart = cartFromStorage ? JSON.parse(cartFromStorage) : [];
    subtotal = subtotalFromStorage ? parseFloat(subtotalFromStorage) : 0;

    axios.get("/api/v1/items")
            .then(({ data }) => {
              items = data;
            })
            .catch(err => console.error(err));
  });

  const updateCartStorage = (): void => {
    setStorageItem('cart', JSON.stringify(cart));
    setStorageItem('subtotal', subtotal.toString());
  }

  const updateCart = (itemId: number, quantity: number): void => {
    // Disable increment buttons
    cartIsUpdating = true;
    // Format the incremented item to a format backend will be able to read
    const cartItem: CartItemMutation = {
      id: itemId,
      quantity
    }
    // Pass original cart and incremented item to backend
    axios
            .put('/api/v1/cart/update', ({ cart, cartItem }))
            .then(({ data }): void => {
      // Update state
      cart = data.cart;
      subtotal = data.subtotal;
    })
  .finally(() => {
      // Update localStorage then re-enable quantity increment buttons, make sure this happens after state is changed to avoid any synchronicity issues
      updateCartStorage();
      cartIsUpdating = false;
    })
            .catch(err => console.error(err));
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
      <!-- TODO: Create child component to show subtotal, taxes, and grand total -->
      <p>Subtotal: ${subtotal.toFixed(2)}</p>
    </div>
  {/if}
</main>

<style>
  /* Root Variables for Theme Colors */
  :root {
    --primary-color: #6c63ff; /* Stylish purple */
    --secondary-color: #ff6b6b; /* Soft coral red */
    --background-color: #f5f7fa; /* Soft off-white */
    --card-bg-color: #ffffff; /* White for cards */
    --text-color: #333333; /* Dark gray for text */
    --muted-text-color: #666666; /* Muted text for secondary info */
    --accent-color: #4caf50; /* Green accent */
    --cart-bg-color: #e8f5e9; /* Light green for cart */
  }

  body {
    background-color: var(--background-color);
    color: var(--text-color);
    font-family: "Arial", sans-serif;
    margin: 0;
    padding: 0;
    line-height: 1.6;
  }

  main {
    padding: 2rem;
  }

  h1 {
    text-align: center;
    color: var(--primary-color);
    font-size: 2.5rem;
    margin-bottom: 2rem;
  }

  .items {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
  }

  .items > * {
    background-color: var(--card-bg-color);
    border: 1px solid var(--primary-color);
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    padding: 1rem;
    transition: transform 0.2s, box-shadow 0.2s;
  }

  .items > *:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
  }

  .cart {
    margin-top: 2rem;
    padding: 1rem;
    background-color: var(--cart-bg-color);
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  .cart h2 {
    color: var(--secondary-color);
    font-size: 1.8rem;
    margin-bottom: 1rem;
  }

  .cart-items {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .cart-items > * {
    padding: 1rem;
    border-radius: 6px;
    transition: background-color 0.3s;
  }

  .cart-items > *:nth-child(odd) {
    background-color: #f1f1f1;
  }

  .cart-items > *:nth-child(even) {
    background-color: #e7e7e7;
  }

  .cart-items > *:hover {
    background-color: var(--accent-color);
    color: white;
  }

  p {
    text-align: right;
    font-weight: bold;
    color: var(--muted-text-color);
    margin-top: 1rem;
  }

  p span {
    color: var(--primary-color);
  }

  /* Button Styles */
  button {
    background-color: var(--primary-color);
    color: white;
    border: none;
    border-radius: 5px;
    padding: 0.5rem 1rem;
    cursor: pointer;
    transition: background-color 0.3s, transform 0.2s;
  }

  button:disabled {
    background-color: #d1d1d1;
    cursor: not-allowed;
  }

  button:hover:not(:disabled) {
    background-color: var(--secondary-color);
    transform: translateY(-2px);
  }

  button:active {
    transform: translateY(1px);
  }
</style>
