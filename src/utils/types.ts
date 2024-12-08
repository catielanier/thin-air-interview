export interface CartItem {
    id: number;
    quantity: number;
}

export interface Item {
    id: number;
    description: string;
    price: number;
}

export type Items = Item[];

export type Cart = CartItem[];

export interface CartResponse {
    cart: Cart;
    subtotal: number;
}

export interface CartItemMutation {
    id: number;
    quantity: number;
}