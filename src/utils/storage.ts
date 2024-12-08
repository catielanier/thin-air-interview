export const getStorageItem = (key: string): string | null => {
    return localStorage.getItem(key);
}

export const setStorageItem = (key: string, value: string | number): void => {
    if (typeof value === "number") {
        value = value.toString();
    }
    localStorage.setItem(key, value);
}