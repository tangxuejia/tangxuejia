const KEY = 'renometric-unit-system';

export const getUnitSystem = () => localStorage.getItem(KEY) || 'metric';

export const setUnitSystem = (value) => {
  localStorage.setItem(KEY, value);
};
