import { render, fireEvent, waitFor } from '@testing-library/svelte';
import axios from 'axios';
import '@testing-library/jest-dom';
import App from './App.svelte'; // Replace with the actual component path
import { getStorageItem, setStorageItem } from './utils/storage';
import {vi} from "vitest";

// Mock axios and local storage functions
vi.mock('axios');
vi.mock('./utils/storage');

describe('App', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    test('should fetch items and update state on mount', async () => {
        const mockItems = [{ id: 1, description: 'Item 1' }, { id: 2, description: 'Item 2' }];
        axios.get.mockResolvedValue({ data: mockItems });

        const { getByText } = render(App);

        await waitFor(() => {
            expect(getByText('Item 1')).toBeInTheDocument();
            expect(getByText('Item 2')).toBeInTheDocument();
        });
    });

    test('should load cart and subtotal from local storage on mount', async () => {
        const mockCart = [{ id: 1, quantity: 2 }];
        const mockSubtotal = '20.00';
        getStorageItem.mockImplementation((key) => {
            if (key === 'cart') return JSON.stringify(mockCart);
            if (key === 'subtotal') return mockSubtotal;
            return null;
        });

        render(App);

        await waitFor(() => {
            expect(getStorageItem).toHaveBeenCalledWith('cart');
            expect(getStorageItem).toHaveBeenCalledWith('subtotal');
        });
    });

    test('should handle API errors gracefully', async () => {
        axios.get.mockRejectedValue(new Error('Network Error'));

        const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

        render(App);

        await waitFor(() => {
            expect(consoleErrorSpy).toHaveBeenCalledWith(expect.any(Error));
        });

        consoleErrorSpy.mockRestore();
    });
});
