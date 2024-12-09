import { render } from '@testing-library/svelte';
import CartItem from './CartItem.svelte';
import { vi, describe, it, expect } from 'vitest';

describe('CartItem Component', () => {
    it('renders the item name and quantity', () => {
        const { getByText } = render(CartItem, {
            props: {
                item: { quantity: 3 },
                itemName: 'Sample Item'
            }
        });

        expect(getByText('Sample Item')).toBeInTheDocument();
        expect(getByText('x 3')).toBeInTheDocument();
    });

    it('handles undefined itemName gracefully', () => {
        const { getByText, container } = render(CartItem, {
            props: {
                item: { quantity: 5 },
                itemName: undefined
            }
        });

        // Assuming there's a default display or conditional rendering in the component
        expect(container.querySelector('.item-name')?.textContent).toBeFalsy();
        expect(getByText('x 5')).toBeInTheDocument();
    });
});