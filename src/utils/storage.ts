export const getStorageItem = (key: string): string | null => {
    return localStorage.getItem(key);
}

export const setStorageItem = (key: string, value: string): void => {
    localStorage.setItem(key, value);
}