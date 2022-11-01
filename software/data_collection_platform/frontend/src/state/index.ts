import { configureStore } from "@reduxjs/toolkit";

// Import reducers and default export the store.
import videos from "./videos";
import bci from "./bci";

const store = configureStore({
  reducer: {
    videos,
    bci,
  },
  devTools: true,
});
export default store;

// Export actions.
export * as videos from "./videos";
export * as bci from "./bci";
