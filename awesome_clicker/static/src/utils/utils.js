/**
 * Selects a random element from an array
 * @param {Array} array - The array to choose from
 * @returns {*} A random element from the array
 */
export function choose(array) {
    const index = Math.floor(Math.random() * array.length);
    return array[index];
}