import { render, fireEvent } from '@testing-library/svelte';
import Item from './Item.svelte';
import {vi} from 'vitest';

describe('Item', () => {
    let mockUpdateCart: jest.Mock;

    beforeEach(() => {
        mockUpdateCart = vi.fn();
    });

    const item = {
        id: 1,
        description: 'Sample Item',
        price: 10,
    };

    it('should render item description and price', () => {
        const { getByText } = render(Item, {
            props: { item, cartIsUpdating: false, updateCart: mockUpdateCart },
        });

        expect(getByText('Sample Item')).toBeInTheDocument();
        expect(getByText('$10')).toBeInTheDocument();
    });

    it('should disable buttons when cart is updating', () => {
        const { getByText } = render(Item, {
            props: { item, cartIsUpdating: true, updateCart: mockUpdateCart },
        });

        const addButton = getByText('+');
        const subButton = getByText('-');

        expect(addButton).toBeDisabled();
        expect(subButton).toBeDisabled();
    });

    it('should call updateCart with correct arguments when increment button is clicked', async () => {
        const { getByText } = render(Item, {
            props: { item, cartIsUpdating: false, updateCart: mockUpdateCart },
        });

        const addButton = getByText('+');
        await fireEvent.click(addButton);

        expect(mockUpdateCart).toHaveBeenCalledWith(item.id, 1);
    });

    it('should call updateCart with correct arguments when decrement button is clicked', async () => {
        const { getByText } = render(Item, {
            props: { item, cartIsUpdating: false, updateCart: mockUpdateCart },
        });

        const subButton = getByText('-');
        await fireEvent.click(subButton);

        expect(mockUpdateCart).toHaveBeenCalledWith(item.id, -1);
    });
});