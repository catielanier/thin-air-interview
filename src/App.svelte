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